from datetime import timedelta
from great_limiter.client import GreatLimiterClient


def test_great_limiter_client():
    client = GreatLimiterClient(5, timedelta(seconds=5))
    ok = client.ok()
    assert ok
    ok = client.ok()
    assert ok
    ok = client.ok()
    assert ok
    ok = client.ok()
    assert ok
    ok = client.ok()
    assert not ok