import datetime
from typing import Dict, Any

from constants import Size
from lib.providers.provider import Provider


class Shipment:
    def __init__(self, date: str, size: Size, provider: Provider):
        self.is_valid = True
        self.date = date
        self.size = size
        self.provider = provider

    def is_shipment_valid(self) -> bool:
        self._validate_date(self.date)
        self._validate_size()

        return self.is_valid

    def _validate_date(self, date) -> None:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            self.is_valid = False

    def _validate_size(self) -> None:
        if self.size not in [s.value for s in Size]:
            self.is_valid = False

    def to_dict(self) -> Dict[str, Any]:
        size = self.size.value if isinstance(self.size, Size) else self.size

        return {
            'date': self.date,
            'size': size,
            'provider': self.provider
        }
