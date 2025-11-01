import pytest

from storage.memory import InMemoryStorage


@pytest.fixture()
def storage() -> InMemoryStorage:
    return InMemoryStorage()


def test_write_and_read_roundtrip(storage: InMemoryStorage) -> None:
    storage.write("hello", b"world")
    assert storage.read("hello") == b"world"


def test_write_accepts_objects_that_support_bytes(storage: InMemoryStorage) -> None:
    class Dummy:
        def __bytes__(self) -> bytes:
            return b"payload"

    storage.write("dummy", Dummy())
    assert storage.read("dummy") == b"payload"


def test_delete_removes_key(storage: InMemoryStorage) -> None:
    storage.write("item", b"value")
    storage.delete("item")
    assert not storage.exists("item")


def test_delete_missing_key_raises(storage: InMemoryStorage) -> None:
    with pytest.raises(KeyError):
        storage.delete("missing")


def test_iter_keys_supports_prefix(storage: InMemoryStorage) -> None:
    storage.write("foo/a", b"1")
    storage.write("foo/b", b"2")
    storage.write("bar/c", b"3")

    assert set(storage.iter_keys()) == {"foo/a", "foo/b", "bar/c"}
    assert set(storage.iter_keys(prefix="foo/")) == {"foo/a", "foo/b"}
