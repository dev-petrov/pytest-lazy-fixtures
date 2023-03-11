from dataclasses import dataclass


@dataclass
class Entity:
    value: int

    def sum(self, value: int) -> int:
        return self.value + value
