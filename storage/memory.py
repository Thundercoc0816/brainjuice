"""In-memory implementation of the :mod:`storage.interface` API."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Dict

from .interface import Storage, SupportsBytes


class InMemoryStorage(Storage):
    """Simple storage backend that keeps values in a process-local dict."""

    def __init__(self) -> None:
        self._data: Dict[str, bytes] = {}

    def write(self, key: str, data: SupportsBytes | bytes | bytearray) -> None:
        if not isinstance(key, str) or not key:
            raise ValueError("key must be a non-empty string")

        if isinstance(data, (bytes, bytearray)):
            payload = bytes(data)
        else:
            payload = bytes(data)

        self._data[key] = payload

    def read(self, key: str) -> bytes:
        try:
            return self._data[key]
        except KeyError as exc:  # pragma: no cover - thin wrapper
            raise KeyError(f"Key '{key}' was not found") from exc

    def delete(self, key: str) -> None:
        try:
            del self._data[key]
        except KeyError as exc:  # pragma: no cover - thin wrapper
            raise KeyError(f"Key '{key}' was not found") from exc

    def exists(self, key: str) -> bool:
        return key in self._data

    def iter_keys(self, prefix: str | None = None) -> Iterable[str]:
        if prefix is None:
            return tuple(self._data.keys())

        return tuple(k for k in self._data if k.startswith(prefix))
