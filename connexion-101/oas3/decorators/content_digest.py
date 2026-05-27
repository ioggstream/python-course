import functools
import hashlib
import json

import connexion
from http_sf import parse, ser

_SUPPORTED = {
    "sha-256": hashlib.sha256,
    "sha-512": hashlib.sha512,
}


def content_digest(func):
    """Add Content-Digest to the response when the client sends Want-Content-Digest.

    Parses the Want-Content-Digest structured-field dictionary (RFC 9530 §4) and
    computes a digest for each algorithm the client requests with weight > 0.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Pop from kwargs first: connexion injects header params by name.
        # The wrapped handler may not declare this param in its signature.
        want_raw = kwargs.pop("want_content_digest", None)
        if want_raw is None:
            want_raw = connexion.request.headers.get("Want-Content-Digest")

        result = await func(*args, **kwargs)

        if not want_raw:
            return result

        try:
            prefs = parse(
                want_raw.encode() if isinstance(want_raw, str) else want_raw,
                tltype="dictionary",
            )
        except Exception:
            return result  # malformed header – pass through unchanged

        # Normalize to (body, status, headers).
        match result:
            case (body, int(status), dict(headers)):
                pass
            case (body, int(status)):
                headers = {}
            case body:
                status, headers = 200, {}

        # Serialize body the same way connexion will put it on the wire.
        body_bytes = json.dumps(body, separators=(",", ":")).encode()

        algos = {
            alg: (fn(body_bytes).digest(), {})
            for alg, fn in _SUPPORTED.items()
            if prefs.get(alg, (0,))[0] > 0
        }

        if not algos:
            return body, status, headers

        return body, status, {**headers, "Content-Digest": ser(algos)}

    return wrapper
