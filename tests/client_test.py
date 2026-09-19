import builtins

from pinetext.client import PineText


def test_get_or_create_assistant(pinetext):
    assistant = pinetext.get_or_create_assistant("foo")

    assert assistant is pinetext.pinecone.assistants


def test_upload_files(pinetext, tmp_path):
    data = tmp_path / "data"
    data.mkdir()

    (data / "test.txt").write_text("TEST")

    pinetext.upload_files(data)

    files = pinetext.pinecone.assistants.files.values()

    assert any(file.name == "test.txt" for file in files)


def test_upload_files_skips_unchanged(pinetext, tmp_path):
    data = tmp_path / "data"
    data.mkdir()

    file = data / "test.txt"
    file.write_text("TEST")

    pinetext.upload_files(data)

    first_files = dict(pinetext.pinecone.assistants.files)

    pinetext.upload_files(data)

    assert pinetext.pinecone.assistants.files == first_files


def test_upload_files_updates_changed_file(pinetext, tmp_path):
    data = tmp_path / "data"
    data.mkdir()

    file = data / "test.txt"
    file.write_text("ONE")

    pinetext.upload_files(data)

    uploaded = next(iter(pinetext.pinecone.assistants.files.values()))

    first_hash = uploaded.metadata["sha256"]

    file.write_text("TWO")

    pinetext.upload_files(data)

    uploaded = next(iter(pinetext.pinecone.assistants.files.values()))

    second_hash = uploaded.metadata["sha256"]

    assert first_hash != second_hash

    assert len(pinetext.pinecone.assistants.files) == 1


def test_chat(pinetext):
    resp = pinetext.chat("This is a test")

    assert resp.message.content == "Test"


def test_chat_preserves_context(pinetext):
    pinetext.chat("First question")

    pinetext.chat("Follow-up question")

    call = pinetext.pinecone.assistants.chat_calls[-1]

    assert call["messages"] == [
        {
            "role": "user",
            "content": "First question",
        },
        {
            "role": "assistant",
            "content": "Test",
        },
        {
            "role": "user",
            "content": "Follow-up question",
        },
    ]


def test_run(pinetext, monkeypatch):
    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": "exit",
    )

    monkeypatch.setattr(
        pinetext,
        "get_or_create_assistant",
        lambda name: pinetext.pinecone.assistants,
    )

    res = pinetext.run()

    assert res is None
