import pytest


@pytest.fixture
def cli(monkeypatch):
    def dummy_run(self):
        return

    monkeypatch.setattr(
        "pinetext.client.PineText.run",
        dummy_run,
    )
