# brainjuice

A lightweight playground project. This commit introduces a storage interface with an accompanying in-memory implementation and tests.

## Storage interface

The `storage` package defines an abstract :class:`Storage` interface that exposes the minimal API required for a byte-addressable key/value backend:

- `write(key: str, data: SupportsBytes | bytes | bytearray) -> None`
- `read(key: str) -> bytes`
- `delete(key: str) -> None`
- `exists(key: str) -> bool`
- `iter_keys(prefix: str | None = None) -> Iterable[str]`

An `InMemoryStorage` implementation is provided for quick experimentation or testing.

## Running the tests

Install the development dependencies and execute the test suite with `pytest`:

```bash
pip install -r requirements-dev.txt  # if you have one
pytest
```
