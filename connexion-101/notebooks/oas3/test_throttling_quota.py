"""Tests for throttling_quota middleware."""

import throttling_quota as mod
from throttling_quota import RateLimitMiddleware, ThrottlingQuota, make_connexion_app


def test_throttlingquota_basic():
    tq = ThrottlingQuota(60, 3)
    r = tq.consume("u")
    assert not r["over_quota"] and r["remaining"] == 2
    r = tq.consume("u")
    assert not r["over_quota"] and r["remaining"] == 1
    r = tq.consume("u")
    assert not r["over_quota"] and r["remaining"] == 0
    # 4th request - over quota
    r = tq.consume("u")
    assert r["over_quota"] and r["remaining"] == 0


def test_throttlingquota_window_reset(monkeypatch):
    t = [0.0]
    monkeypatch.setattr(mod, "time", lambda: t[0])

    tq = ThrottlingQuota(10, 2)
    tq.consume("u")
    tq.consume("u")
    assert tq.consume("u")["over_quota"]

    t[0] = 20.0  # advance past the TTL
    r = tq.consume("u")
    assert not r["over_quota"]


def test_middleware_headers():
    from starlette.applications import Starlette
    from starlette.responses import PlainTextResponse
    from starlette.routing import Route
    from starlette.testclient import TestClient

    def homepage(request):
        return PlainTextResponse("ok")

    app = Starlette(routes=[Route("/", homepage)])
    app.add_middleware(RateLimitMiddleware, quota=ThrottlingQuota(ttl=60, limit=5))
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert "RateLimit" in resp.headers
    assert "RateLimit-Policy" in resp.headers
    assert "r=4" in resp.headers["RateLimit"]
    assert "q=5" in resp.headers["RateLimit-Policy"]
    assert "w=60" in resp.headers["RateLimit-Policy"]


def test_middleware_throttles():
    from starlette.applications import Starlette
    from starlette.responses import PlainTextResponse
    from starlette.routing import Route
    from starlette.testclient import TestClient

    def homepage(request):
        return PlainTextResponse("ok")

    app = Starlette(routes=[Route("/", homepage)])
    app.add_middleware(RateLimitMiddleware, quota=ThrottlingQuota(ttl=60, limit=2))
    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/").status_code == 200

    r = client.get("/")
    assert r.status_code == 429
    assert "Retry-After" in r.headers
    assert "application/problem+json" in r.headers["content-type"]
    body = r.json()
    assert body["status"] == 429
    assert "default" in body["violated-policies"]


def test_connexion_app_with_middleware():
    from starlette.testclient import TestClient

    app = make_connexion_app(ttl=60, limit=2)
    client = TestClient(app)

    r = client.get("/hello")
    assert r.status_code == 200, r.text
    assert "RateLimit" in r.headers

    r = client.get("/hello")
    assert r.status_code == 200

    r = client.get("/hello")
    assert r.status_code == 429
    assert "application/problem+json" in r.headers["content-type"]
