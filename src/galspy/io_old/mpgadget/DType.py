from typing import Any

class _DTYPE:
    def __init__(self, typestring: str) -> None:
        self.raw_string         = typestring
        self.endianness         = self.raw_string[0]
        self.character          = self.raw_string[1]
        self.byte_width         = int(self.raw_string[2])

    def __str__(self) -> str:
        return self.raw_string

    def __repr__(self) -> str:
        return self.raw_string

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.raw_string