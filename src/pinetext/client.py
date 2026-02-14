from pathlib import Path

from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

from pinetext.settings import Settings
from pinetext import telemetry


class PineText:
    def __init__(self, *, data_dir: str | None = None):
        self.settings = Settings()
        if data_dir is not None:
            self.settings.pinecone.data_dir = data_dir

    def get_or_create_assistant(self, name: str):
        try:
            return self.pinecone.assistant.describe_assistant(assistant_name=name)
        except Exception:
            return self.pinecone.assistant.create_assistant(assistant_name=name)

    def upload_files(self, path: str):
        folder = Path(path)
        if folder.is_dir():
            uploaded = [x.name for x in self.assistant.list_files()]
            for x in sorted(folder.iterdir()):
                if x.name not in uploaded:
                    self.assistant.upload_file(
                        file_path=str(x.resolve()),
                        metadata={
                            "filename": x.name,
                            "extension": x.suffix.lower().lstrip("."),
                        },
                        timeout=None,
                    )

    @telemetry.op()
    def chat(self, text: str, model: str):
        msg = Message(role="user", content=text)
        resp = self.assistant.chat(messages=[msg], model=model)
        return resp.message.content

    def run(self):
        telemetry.init(self.settings.wandb.project, self.settings.wandb.api_key)
        self.pinecone = Pinecone(api_key=self.settings.pinecone.api_key)
        self.assistant = self.get_or_create_assistant(self.settings.pinecone.assistant)
        self.upload_files(self.settings.pinecone.data_dir)

        while True:
            text = input("> ").strip()
            if text.lower() in ("exit", "quit"):
                break
            res = self.chat(text, self.settings.pinecone.model)
            print(res)
