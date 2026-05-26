"""
Starlette rate-limiting middleware for connexion applications.

Implements the ``RateLimit`` and ``RateLimit-Policy`` response header fields as
defined in draft-ietf-httpapi-ratelimit-headers-11::

    RateLimit: "default";r=<remaining>;t=<window_seconds>
    RateLimit-Policy: "default";q=<limit>;w=<ttl_seconds>

On quota exhaustion the middleware returns HTTP 429 with ``Retry-After`` and an
``application/problem+json`` body (RFC 9457 / ``quota-exceeded`` problem type).

Configuration examples
----------------------
Add **before** authentication to throttle every caller by IP address::

    import connexion
    from throttling_quota import RateLimitMiddleware, ThrottlingQuota

    app = connexion.AsyncApp(__name__, specification_dir="specs/")
    app.add_api("openapi.yaml")
    app.add_middleware(
        RateLimitMiddleware,
        quota=ThrottlingQuota(ttl=60, limit=100),
    )

Add **after** authentication to throttle by authenticated user
(assumes the auth middleware stores the identity in ``request.state.user``)::

    app.add_middleware(
        RateLimitMiddleware,
        quota=ThrottlingQuota(ttl=60, limit=100),
        key_func=lambda req: getattr(req.state, "user", req.client.host),
    )

Use a custom policy name for multi-policy setups::

    app.add_middleware(
        RateLimitMiddleware,
        quota=ThrottlingQuota(ttl=3600, limit=1000),
        policy_name="hourly",
    )
"""

import functools
import sys
from pathlib import Path
from time import time

import connexion
from http_sf import ser
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# ---------------------------------------------------------------------------
# Quota store
# ---------------------------------------------------------------------------


class ThrottlingQuota:
    """In-memory fixed-window quota store.

    BEWARE: tutorial quality only - not thread-safe, not process-safe,
    not persistent.  Replace with Redis or similar in production.

    Args:
        ttl:   window size in seconds.
        limit: maximum requests allowed per window per key.
    """

    def __init__(self, ttl: int, limit: int):
        self._store: dict = {}
        self.ttl = ttl
        self.limit = limit

    def consume(self, key) -> dict:
        """Consume one quota unit for *key* and return the current state.

        Returns:
            dict with keys:

            - ``remaining``  - quota units left in the current window (>= 0).
            - ``reset``      - seconds until the window resets.
            - ``over_quota`` - ``True`` when the key has exceeded its limit.
        """
        now = time()
        if key in self._store:
            q = self._store[key]
            if q["reset"] < now:
                # Window expired - start a new one.
                q["remaining"] = self.limit - 1
                q["reset"] = (1 + now // self.ttl) * self.ttl
            else:
                q["remaining"] -= 1
        else:
            q = self._store[key] = {
                "remaining": self.limit - 1,
                "reset": (1 + now // self.ttl) * self.ttl,
            }
        return {
            "remaining": max(0, q["remaining"]),
            "reset": max(0, int(q["reset"] - time())),
            "over_quota": q["remaining"] < 0,
        }


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Starlette ASGI middleware that enforces a per-key request quota.

    Attaches ``RateLimit`` and ``RateLimit-Policy`` headers to every response,
    and returns HTTP 429 when the quota is exceeded.

    Args:
        app:         the ASGI application to wrap.
        quota:       a :class:`ThrottlingQuota` instance shared across
                     requests.
        key_func:    ``(Request) -> str`` - produces the throttle key.
                     Defaults to ``request.client.host`` (throttle by IP).
        policy_name: label used in the ``RateLimit``/``RateLimit-Policy``
                     header fields. Default: ``"default"``.

    Examples::

        # Throttle by IP (place before auth middleware):
        app.add_middleware(
            RateLimitMiddleware,
            quota=ThrottlingQuota(ttl=60, limit=100),
        )

        # Throttle by authenticated user (place after auth middleware):
        app.add_middleware(
            RateLimitMiddleware,
            quota=ThrottlingQuota(ttl=60, limit=100),
            key_func=lambda req: getattr(req.state, "user", req.client.host),
        )
    """

    def __init__(self, app, quota: ThrottlingQuota, key_func=None, policy_name="default"):
        super().__init__(app)
        self.quota = quota
        self.key_func = key_func or (lambda req: req.client.host if req.client else "unknown")
        self.policy_name = policy_name

    async def dispatch(self, request: Request, call_next):
        key = self.key_func(request)
        result = self.quota.consume(key)

        # Serialize per draft-ietf-httpapi-ratelimit-headers-11 using RFC 9651
        # Structured Fields. Policy name is an SF String (quoted).
        rl = ser([(self.policy_name, {"r": result["remaining"], "t": result["reset"]})])
        rl_policy = ser([(self.policy_name, {"q": self.quota.limit, "w": self.quota.ttl})])

        if result["over_quota"]:
            return JSONResponse(
                status_code=429,
                content={
                    "type": "https://iana.org/assignments/http-problem-types#quota-exceeded",
                    "title": "Too Many Requests",
                    "status": 429,
                    "violated-policies": [self.policy_name],
                },
                headers={
                    "Retry-After": str(result["reset"]),
                    "RateLimit": rl,
                    "RateLimit-Policy": rl_policy,
                },
                media_type="application/problem+json",
            )

        response = await call_next(request)
        response.headers["RateLimit"] = rl
        response.headers["RateLimit-Policy"] = rl_policy
        return response


# ---------------------------------------------------------------------------
# Handler decorator
# ---------------------------------------------------------------------------


def ratelimit(quota: ThrottlingQuota, key_func=None, policy_name="default"):
    """Decorate a connexion handler to enforce a per-key request quota.

    Mirrors :class:`RateLimitMiddleware` at the handler level: attaches
    ``RateLimit`` and ``RateLimit-Policy`` headers on every response and
    short-circuits with 429 when the quota is exceeded.

    Args:
        quota:       a :class:`ThrottlingQuota` instance shared across requests.
        key_func:    ``() -> str`` throttle key. Defaults to client IP.
        policy_name: label for the RateLimit headers.

    Example::

        quota = ThrottlingQuota(ttl=60, limit=10)

        @ratelimit(quota)
        async def get_echo(tz="Zulu"):
            ...
    """
    _key = key_func or (lambda: connexion.request.client.host)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = quota.consume(_key())

            rl = ser([(policy_name, {"r": result["remaining"], "t": result["reset"]})])
            rl_policy = ser([(policy_name, {"q": quota.limit, "w": quota.ttl})])
            rate_headers = {"RateLimit": rl, "RateLimit-Policy": rl_policy}

            if result["over_quota"]:
                return connexion.problem(
                    status=429,
                    title="Too Many Requests",
                    detail="Quota exceeded.",
                    headers={"Retry-After": str(result["reset"]), **rate_headers},
                )

            response = await func(*args, **kwargs)

            match response:
                case (body, int(status), dict(existing)):
                    return body, status, {**existing, **rate_headers}
                case (body, int(status)):
                    return body, status, rate_headers
                case body:
                    return body, 200, rate_headers

        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Connexion test app
# ---------------------------------------------------------------------------

# Make this module importable as 'throttling_quota' so connexion can resolve
# operationIds (e.g. "throttling_quota.hello_handler") regardless of how
# pytest discovers the file.
_here = Path(__file__).parent.resolve()
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))


def hello_handler():
    """Handler used by the connexion test app."""
    return {"hello": "world"}, 200


def make_connexion_app(ttl: int = 60, limit: int = 3, key_func=None):
    """Create a minimal connexion AsyncApp with :class:`RateLimitMiddleware`.

    Exposes a single ``GET /hello`` endpoint that returns
    ``{"hello": "world"}``, suitable for integration tests.

    Args:
        ttl:      quota window in seconds.
        limit:    requests allowed per window.
        key_func: optional throttle-key function (see :class:`RateLimitMiddleware`).

    Example::

        from starlette.testclient import TestClient

        app = make_connexion_app(ttl=60, limit=10)
        client = TestClient(app)
        resp = client.get("/hello")
        assert resp.headers["RateLimit"]
    """
    import connexion

    spec = {
        "openapi": "3.0.0",
        "info": {"title": "throttle-test", "version": "0.1"},
        "paths": {
            "/hello": {
                "get": {
                    "operationId": "throttling_quota.hello_handler",
                    "responses": {"200": {"description": "OK"}},
                }
            }
        },
    }

    app = connexion.AsyncApp(__name__)
    app.add_api(spec)
    app.add_middleware(
        RateLimitMiddleware,
        quota=ThrottlingQuota(ttl=ttl, limit=limit),
        **({"key_func": key_func} if key_func else {}),
    )
    return app
