import hashlib

from pathlib import Path

from pinecone import Pinecone

from pinetext.settings import Settings
from pinetext import telemetry


SUPPORTED_FILES = {
    ".docx",
    ".json",
    ".md",
    ".pdf",
    ".txt",
}


class PineText:
    def __init__(
        self,
        name: str | None = None,
        model: str | None = None,
    ):
        self.settings = Settings()
        if name is not None:
            self.settings.pinecone.assistant = name
        if model is not None:
            self.settings.pinecone.model = model
        self.messages: list[dict[str, str]] = []

    def get_or_create_assistant(self, name: str):
        try:
            return self.pinecone.assistants.describe(name=name)
        except Exception:
            return self.pinecone.assistants.create(name=name)

    def upload_files(self, path: Path):
        uploaded = {
            file.id: file
            for file in self.pinecone.assistants.list_files(
                assistant_name=self.settings.pinecone.assistant,
            )
        }
        for file in sorted(path.rglob("*")):
            if file.is_file() and file.suffix.lower() in SUPPORTED_FILES:
                id = hashlib.sha256(str(file.relative_to(path)).encode()).hexdigest()
                with open(file, "rb") as f:
                    hash = hashlib.file_digest(f, "sha256").hexdigest()
                remote = uploaded.get(id)
                if remote is None or (remote.metadata or {}).get("sha256") != hash:
                    self.pinecone.assistants.upload_file(
                        assistant_name=self.settings.pinecone.assistant,
                        file_path=str(file),
                        file_id=id,
                        metadata={
                            "sha256": hash,
                        },
                    )

    @telemetry.op()
    def chat(self, text: str):
        self.messages.append({"role": "user", "content": text})
        res = self.pinecone.assistants.chat(
            assistant_name=self.settings.pinecone.assistant,
            messages=self.messages,
            model=self.settings.pinecone.model,
        )
        self.messages.append({"role": "assistant", "content": res.message.content})
        return res

    def run(self, path: Path | None = None, text: str | None = None):
        telemetry.init(self.settings.wandb.project, self.settings.wandb.api_key)
        self.pinecone = Pinecone(api_key=self.settings.pinecone.api_key)
        self.assistant = self.get_or_create_assistant(self.settings.pinecone.assistant)
        self.upload_files(path or Path(self.settings.pinecone.data_dir))

        if text:
            res = self.chat(text)
            print(res.message.content)
        else:
            while True:
                text = input("> ").strip()
                if text.lower() in ("exit", "quit"):
                    break
                res = self.chat(text)
                print(res.message.content)
