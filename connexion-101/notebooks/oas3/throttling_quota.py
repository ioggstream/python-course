from datetime import datetime
from functools import wraps
from time import time

from connexion import problem
from connexion.lifecycle import ConnexionResponse
from flask import request


class ThrottlingQuota:
    """ A simple class to implement quota.

        BEWARE: It's a tutorial function, don't use in production!
                this is not thread-safe nor process-aware and
                stores everything in a dict().
    """

    def __init__(self, ttl, limit):
        self._dict = dict()
        self.ttl = ttl
        self.limit = limit

    def consume(self, user):
        if user in self._dict:
            q = self._dict[user]
            if q["reset"] < time():
                q["remaining"] = self.limit
                q["reset"] = (1 + time() // self.ttl) * self.ttl
            else:
                q["remaining"] -= 1
                if q["remaining"] < 0:
                    return dict(
                        limit=self.limit,
                        remaining=0,
                        reset=int(q["reset"] - time()),
                        user=user,
                        comment=datetime.fromtimestamp(q["reset"]).isoformat(),
                    )
        else:
            q = self._dict[user] = {
                "remaining": self.limit - 1,
                "reset": (1 + time() // self.ttl) * self.ttl,
            }
        return dict(
            limit=self.limit,
            remaining=q["remaining"],
            reset=int(q["reset"] - time()),
            user=user,
            comment=datetime.fromtimestamp(q["reset"]).isoformat(),
        )


quota_store = ThrottlingQuota(20, 10)


def throttle_user(user):
    quota = quota_store.consume(user)
    return {
        "X-RateLimit-Limit": quota["limit"],
        "X-RateLimit-Remaining": quota["remaining"],
        "X-RateLimit-Reset": quota["reset"],
    }


def throttle(wrapped):
    """A decorator to apply throttling policies.

        BEWARE: It's a tutorial function, don't use in production.
    """

    @wraps(wrapped)
    def tmp(*args, **kwargs):
        # Unauthenticated endpoints can throttle by IP.
        throttle_key = kwargs.get("user") or request.remote_addr
        quota_headers = throttle_user(throttle_key)
        print(quota_headers)
        if quota_headers["X-RateLimit-Remaining"] == 0:
            return problem(
                status=429,
                title="Too many requests",
                detail=f"User {throttle_key} over quota of {quota_headers['X-RateLimit-Limit']}. Retry in {quota_headers['X-RateLimit-Reset']} seconds. Count: {quota_headers['X-RateLimit-Remaining']}",
                headers={
                    "Retry-After": quota_headers["X-RateLimit-Reset"],
                    "X-RateLimit-Limit": quota_headers["X-RateLimit-Limit"],
                },
            )
        response = wrapped(*args, **kwargs)

        print(response)

        if isinstance(response, ConnexionResponse):
            response.headers.update(quota_headers)
            return response

        if not isinstance(response, tuple):
            return response, 200, quota_headers

        if len(response) == 3:
            response[2].update(quota_headers)
            return response

        if len(response) == 2:
            return response + (quota_headers,)

        raise NotImplementedError(response)

    return tmp


def test_throttlingquota():
    tq = ThrottlingQuota(20, 100)
    for i in range(90):
        tq.consume(1)
    assert tq.consume(1)["remaining"]
    for i in range(90):
        tq.consume(1)
    assert tq.consume(1)["remaining"] == 0
