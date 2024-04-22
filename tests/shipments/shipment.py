import unittest
from datetime import datetime
from constants import Size
from lib.providers.provider import Provider
from lib.shipments.shipment import Shipment


class TestShipment(unittest.TestCase):
    def test_valid_shipment(self):
        valid_date = '2023-04-10'
        size = Size.SMALL.value
        provider = Provider(name='Test Provider', prices={size: 10.0})

        shipment = Shipment(date=valid_date, size=size, provider=provider)
        self.assertEqual(shipment.is_shipment_valid(), True)

    def test_invalid_date_shipment(self):
        invalid_date = '2024-13-32'
        size = Size.SMALL.value
        provider = Provider(name='Test Provider', prices={size: 10.0})

        shipment = Shipment(date=invalid_date, size=size, provider=provider)
        self.assertEqual(shipment.is_shipment_valid(), False)

    def test_invalid_size_shipment(self):
        valid_date = '2024-04-10'
        invalid_size = 'XL'
        provider = Provider(name='Test Provider', prices={invalid_size: 10.0})

        shipment = Shipment(date=valid_date, size=invalid_size, provider=provider)
        self.assertEqual(shipment.is_shipment_valid(), False)


if __name__ == '__main__':
    unittest.main()
