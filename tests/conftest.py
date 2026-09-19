import pytest

from pathlib import Path
from types import SimpleNamespace

import pinetext.client as client_mod
from pinetext.client import PineText


@pytest.fixture
def cli(monkeypatch):
    def dummy_run(self):
        return

    monkeypatch.setattr(
        "pinetext.client.PineText.run",
        dummy_run,
    )


@pytest.fixture
def pinetext(monkeypatch):
    class DummyAssistants:
        def __init__(self):
            self.files = {}
            self.chat_calls = []

        def describe(self, name: str):
            return self

        def create(self, name: str):
            return self

        def list_files(self, assistant_name: str):
            return list(self.files.values())

        def upload_file(
            self,
            assistant_name: str,
            file_path: str,
            file_id: str,
            metadata=None,
        ):
            file = SimpleNamespace(
                id=file_id,
                name=Path(file_path).name,
                metadata=metadata or {},
            )

            self.files[file_id] = file

            return file

        def chat(
            self,
            assistant_name: str,
            messages,
            model: str,
        ):
            self.chat_calls.append(
                {
                    "assistant_name": assistant_name,
                    "messages": [message.copy() for message in messages],
                    "model": model,
                }
            )

            return SimpleNamespace(
                message=SimpleNamespace(
                    content="Test",
                )
            )

    class DummyPinecone:
        def __init__(self, api_key):
            self.assistants = DummyAssistants()

    monkeypatch.setattr(client_mod, "Pinecone", DummyPinecone)

    client = PineText()
    client.pinecone = DummyPinecone(None)
    return client
