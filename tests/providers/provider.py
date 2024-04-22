import unittest
from lib.providers.provider import Provider
from constants import Size


class TestProvider(unittest.TestCase):
    def test_get_price(self):
        prices = {Size.SMALL.value: 10.0, Size.LARGE.value: 20.0}
        provider = Provider(name='Test Provider', prices=prices)

        self.assertEqual(provider.get_price(Size.SMALL.value), 10.0)
        self.assertEqual(provider.get_price(Size.LARGE.value), 20.0)
        self.assertEqual(provider.get_price('XL'), 0.0)  # Non-existing size


if __name__ == '__main__':
    unittest.main()
