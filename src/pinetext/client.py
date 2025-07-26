from pathlib import Path

from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

from pinetext.settings import Settings


settings = Settings()


class PineText:
    def __init__(self):
        pass

    def run(self):
        self.pinecone = Pinecone(api_key=settings.pinecone.api_key)
        self.assistant = self.pinecone.assistant.create_assistant(
            assistant_name=settings.pinecone.assistant,
            instructions="You are a helpful assistant. Answer in polite, short sentences. Use American English spelling and vocabulary.",
            timeout=15,
        )
        self.data_dir = Path(settings.pinecone.data_dir)

        for f in sorted(self.data_dir.iterdir()):
            print(f"Uploading {f.name}...")
            self.assistant.upload_file(
                file_path=str(f.resolve()), metadata={"filename": f.name}, timeout=None
            )

        while True:
            q = input("> ").strip()
            if q.lower() in ("exit", "quit"):
                break
            msg = Message(role="user", content=q)
            res = self.assistant.chat(messages=[msg])
            print(res.message.content)
