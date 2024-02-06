from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class Entity:
    value: int

    def sum(self, value: int) -> int:
        return self.value + value


class DataNamedTuple(NamedTuple):
    a: int
    b: int
