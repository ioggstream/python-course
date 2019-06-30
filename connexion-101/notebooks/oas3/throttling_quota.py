from time import time
from datetime import datetime


class ThrottlingQuota:
    def __init__(self, ttl, limit):
        self._dict = {}
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
                "remaining": self.limit,
                "reset": (1 + time() // self.ttl) * self.ttl,
            }
        return dict(
            limit=self.limit,
            remaining=q["remaining"],
            reset=int(q["reset"] - time()),
            user=user,
            comment=datetime.fromtimestamp(q["reset"]).isoformat(),
        )


tq = ThrottlingQuota(20, 100)
for i in range(90):
    tq.consume(1)
print(tq.consume(1))
for i in range(90):
    tq.consume(1)
print(tq.consume(1))
