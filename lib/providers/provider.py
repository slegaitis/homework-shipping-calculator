from dataclasses import dataclass
from typing import Dict

from constants import Size


@dataclass
class Provider:
    name: str
    prices: Dict[Size, float]

    def get_price(self, size: Size) -> float:
        return self.prices.get(size, 0.0)
