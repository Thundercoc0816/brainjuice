"""In-memory implementation of the :mod:`storage.interface` API."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Dict, Final

from .interface import Storage, SupportsBytes


class InMemoryStorage(Storage):
    """Simple storage backend that keeps values in a process-local dict."""

    _MISSING_KEY_MESSAGE: Final[str] = "key must be a non-empty string"

    def __init__(self) -> None:
        self._data: Dict[str, bytes] = {}

    def write(self, key: str, data: SupportsBytes | bytes | bytearray) -> None:
        self._validate_key(key)

        payload = self._coerce_to_bytes(data)
        self._data[key] = payload

    def read(self, key: str) -> bytes:
        self._validate_key(key)
        try:
            return self._data[key]
        except KeyError as exc:  # pragma: no cover - thin wrapper
            raise KeyError(f"Key '{key}' was not found") from exc

    def delete(self, key: str) -> None:
        self._validate_key(key)
        try:
            del self._data[key]
        except KeyError as exc:  # pragma: no cover - thin wrapper
            raise KeyError(f"Key '{key}' was not found") from exc

    def exists(self, key: str) -> bool:
        self._validate_key(key)
        return key in self._data

    def iter_keys(self, prefix: str | None = None) -> Iterable[str]:
        if prefix is None:
            return self._iter_all_keys()

        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string or None")

        return self._iter_prefixed_keys(prefix)

    def _iter_all_keys(self) -> Iterator[str]:
        for key in self._data.keys():
            yield key

    def _iter_prefixed_keys(self, prefix: str) -> Iterator[str]:
        for key in self._data.keys():
            if key.startswith(prefix):
                yield key

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if not key:
            raise ValueError(self._MISSING_KEY_MESSAGE)

    def _coerce_to_bytes(self, data: SupportsBytes | bytes | bytearray) -> bytes:
        try:
            return bytes(data)
        except TypeError as exc:  # pragma: no cover - thin wrapper
            raise TypeError("data must provide a bytes representation") from exc
