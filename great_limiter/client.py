from datetime import timedelta, datetime
from typing import Dict, Optional


class GreatLimiterClient:
    def __init__(self, rate_limit: int, duration: timedelta) -> None:
        self.rate = 0
        self.rate_limit = rate_limit
        self.duration = duration
        self.timestamp = datetime.now()

    def ok(self) -> bool:
        ts = datetime.now()
        if ts > self.timestamp + self.duration:
            self.timestamp = ts
            self.rate = 0

        self.rate += 1
        if self.rate >= self.rate_limit:
            return False
        return True

    def wait(self) -> None:
        while True:
            if self.ok():
                return


class GreatLimiterCluster:
    def __init__(self, clients: Optional[Dict[str, GreatLimiterClient]] = None) -> None:
        if clients is None:
            self.clients = dict()
        self.clients = clients

    def ok(self, key: str) -> (bool, bool):
        if key not in self.clients.keys():
            return None, True
        return self.clients[key].ok(), False

    def wait(self, key: str) -> bool:
        if key not in self.clients.keys():
            return True
        self.clients[key].wait()
        return False

    def rate(self, key: str) -> (int, bool):
        if key not in self.clients.keys():
            return None, True
        return self.clients[key].rate, False

    def new(self, key: str, rate_limit: int, duration: int) -> str:
        if key in self.clients.keys():
            return "limiter already exists"
        self.clients[key] = GreatLimiterClient(rate_limit, timedelta(seconds=duration))