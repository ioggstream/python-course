from connexion import problem
from random import randint
import pytz
from datetime import datetime
from throttling_quota import ThrottlingQuota, throttle_user
from flask import after_this_request


def get_status():
    """Implement the get_status operation
    :return: a problem+json with status 200, title "OK" and a successful
             message in detail
    """
    p = randint(1, 5)
    if p == 5:
        return problem(
            status=503,
            title="Service Temporarily Unavailable",
            detail="Retry after the number of seconds specified in the the Retry-After header.",
            headers={"Retry-After": p, "Cache-Control": "no-store"},
        )
    return problem(status=200, title="OK", detail="So far so good.", headers={"Cache-Control": "no-store"})


def get_echo(tz="Zulu", user=None, token_info=None):
    if not user:
        raise RuntimeError("This should not happen on secured endpoints")

    quota_headers = throttle_user(user)
    if quota_headers["X-RateLimit-Remaining"] == 0:
        return problem(
            status=429,
            title="Too many requests",
            detail=f"User {user} over quota of {quota_headers['X-RateLimit-Limit']}. Retry in {quota_headers['X-RateLimit-Reset']} seconds",
            headers={
                "Retry-After": quota_headers["X-RateLimit-Reset"],
                "X-RateLimit-Limit": quota_headers["X-RateLimit-Limit"],
            },
        )

    if tz not in pytz.all_timezones:
        return problem(
            status=400,
            title="Bad Timezone",
            detail="The specified timezone is not valid",
            ext={"valid_timezones": pytz.all_timezones},
        )
    d = datetime.now(tz=pytz.timezone(tz))
    r = {"timestamp": d.isoformat().replace("+00:00", "Z")}

    r["user"] = user
    r["ti"] = token_info

    return (r, 200, quota_headers)
