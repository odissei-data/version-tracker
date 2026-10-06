import asyncio
import os

os.environ.setdefault("MONGO_URI", "mongodb://localhost:1")

from main import app, health  # noqa: E402
from version import get_version  # noqa: E402


def test_health():
    assert "/health" in {route.path for route in app.routes}
    assert asyncio.run(health()) == {"status": "ok", "version": get_version()}
