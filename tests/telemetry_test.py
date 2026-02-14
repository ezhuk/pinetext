import pinetext.telemetry as telemetry


def test_op():
    @telemetry.op()
    def f(x: int) -> int:
        return x + 1

    assert f(1) == 2


def test_init(monkeypatch):
    calls = {"login": 0, "init": 0}

    class DummyWandB:
        def login(self, key: str):
            calls["login"] += 1
            assert key == "secret"

    class DummyWeave:
        def init(self, project: str):
            calls["init"] += 1
            assert project == "pinetext-proj"

    monkeypatch.setattr(telemetry, "wandb", DummyWandB())
    monkeypatch.setattr(telemetry, "weave", DummyWeave())

    telemetry.init("pinetext-proj", api_key="secret")
    assert calls["login"] == 1
    assert calls["init"] == 1
