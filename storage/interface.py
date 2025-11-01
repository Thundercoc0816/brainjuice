"""Core storage interface definitions for brainjuice."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Protocol


class SupportsBytes(Protocol):
    """Protocol for values that can be converted to bytes."""

    def __bytes__(self) -> bytes:  # pragma: no cover - structural typing hook
        ...


class Storage(ABC):
    """Abstract interface describing a byte-addressable storage backend.

    The interface is intentionally minimal so that it can be implemented
    by in-memory dictionaries, local file systems, cloud object storage,
    or any other key-value store that can handle binary payloads.
    """

    @abstractmethod
    def write(self, key: str, data: SupportsBytes | bytes | bytearray) -> None:
        """Persist *data* at *key*, overwriting any previous value."""

    @abstractmethod
    def read(self, key: str) -> bytes:
        """Retrieve the bytes stored at *key*.

        Implementations should raise :class:`KeyError` when the key does
        not exist or cannot be retrieved.
        """

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove *key* and its data from the backend.

        Deleting a non-existent key should raise :class:`KeyError` to help
        surface mismatches between callers and the state of the storage.
        """

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Return ``True`` if *key* is present in the backend."""

    @abstractmethod
    def iter_keys(self, prefix: str | None = None) -> Iterable[str]:
        """Yield all keys, optionally restricting the set by *prefix*."""
