import pytest

from pathlib import Path

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
    class DummyAssistant:
        def __init__(self):
            self.files = []

        def create_assistant(self, assistant_name: str, instructions: str = None):
            return self

        def describe_assistant(self, assistant_name: str):
            return self

        def list_files(self):
            return self.files

        def upload_file(self, file_path: str, metadata=None, timeout=None):
            self.files.append(Path(file_path).name)

        def chat(self, messages, model=None):
            class Message:
                def __init__(self, content):
                    self.content = content

            class Response:
                def __init__(self, content):
                    self.message = Message(content)

            return Response("Test")

    class DummyPinecone:
        def __init__(self, assistant: DummyAssistant):
            self.assistant = assistant

    client = PineText()
    client.assistant = DummyAssistant()
    client.pinecone = DummyPinecone(client.assistant)
    return client
