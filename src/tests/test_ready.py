import asyncio
import json
import os

os.environ.setdefault("MONGO_URI", "mongodb://localhost:1")

import main  # noqa: E402


class Client:
    def __init__(self, reachable):
        self.topology_description = self
        self.reachable = reachable

    def has_writable_server(self):
        return self.reachable


def ready(monkeypatch, reachable):
    monkeypatch.setattr(main, "client", Client(reachable))
    response = asyncio.run(main.ready())
    return response.status_code, json.loads(response.body)


def test_ready_when_mongodb_is_reachable(monkeypatch):
    assert ready(monkeypatch, True) == (200, {"status": "ok", "mongodb": "ok"})


def test_not_ready_without_mongodb(monkeypatch):
    assert ready(monkeypatch, False) == (
        503, {"status": "not ready", "mongodb": "unreachable"})
