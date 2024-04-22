import unittest

from constants import Size, Providers
from lib.discounts.discount_calculator import DiscountCalculator
from lib.providers.provider import Provider
from lib.shipments.shipment import Shipment


class TestDiscountCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = DiscountCalculator(max_discount_per_month=10.0)
        self.provider_mr = Provider(Providers.MR.name, {
                Size.SMALL.value: 2.00,
                Size.MEDIUM.value: 3.00,
                Size.LARGE.value: 4.00
            })
        self.provider_lp = Provider(Providers.LP.name, {
                Size.SMALL.value: 2.50,
                Size.MEDIUM.value: 3.50,
                Size.LARGE.value: 4.50
            })
        self.provider_unknown = Provider(Providers.UNKNOWN.name, {
                Size.SMALL.value: 3.50,
                Size.MEDIUM.value: 4.50,
                Size.LARGE.value: 5.50
            })

        self.calculator.add_provider(self.provider_mr)
        self.calculator.add_provider(self.provider_lp)
        self.calculator.add_provider(self.provider_unknown)

    def test_apply_discount_small_shipment_mr_no_discount_applied(self):
        shipment = Shipment(date='2024-04-10', size=Size.SMALL.value, provider=self.provider_mr)
        price, discount = self.calculator.apply_discount(shipment)

        self.assertEqual(2.00, price)
        self.assertEqual(0.0, discount)

    def test_apply_no_discount_to_regular_shipment(self):
        shipment = Shipment(date='2024-04-10', size=Size.MEDIUM.value, provider=self.provider_mr)
        price, discount = self.calculator.apply_discount(shipment)

        self.assertEqual(3.00, price)
        self.assertEqual(0.0, discount)

    def test_apply_discount_small_shipment_mr_discount_applied(self):
        calculator = DiscountCalculator(max_discount_per_month=10.0)
        provider_lp = Provider(Providers.LP.name, {
            Size.SMALL.value: 1.50,
            Size.MEDIUM.value: 2.50,
            Size.LARGE.value: 3.50
        })
        calculator.add_provider(self.provider_mr)
        calculator.add_provider(provider_lp)
        shipment = Shipment(date='2024-04-10', size=Size.SMALL.value, provider=self.provider_mr)
        price, discount = calculator.apply_discount(shipment)

        self.assertEqual(1.50, price)
        self.assertEqual(0.50, discount)

    def test_apply_discount_small_shipment_mr_discount_applied_only_until_max_discount_per_month_is_reached(self):
        calculator = DiscountCalculator(max_discount_per_month=3.0)
        provider_lp = Provider(Providers.LP.name, {
            Size.SMALL.value: 1.00,
            Size.MEDIUM.value: 2.50,
            Size.LARGE.value: 3.50
        })
        calculator.add_provider(self.provider_mr)
        calculator.add_provider(provider_lp)
        shipment_one = Shipment(date='2024-04-10', size=Size.SMALL.value, provider=self.provider_mr)
        shipment_two = Shipment(date='2024-04-11', size=Size.SMALL.value, provider=self.provider_mr)
        shipment_three = Shipment(date='2024-04-11', size=Size.SMALL.value, provider=self.provider_mr)
        shipment_four = Shipment(date='2024-04-11', size=Size.SMALL.value, provider=self.provider_mr)

        price_one, discount_one = calculator.apply_discount(shipment_one)
        price_two, discount_two = calculator.apply_discount(shipment_two)
        price_three, discount_three = calculator.apply_discount(shipment_three)
        price_four, discount_four = calculator.apply_discount(shipment_four)

        self.assertEqual(1.00, price_one)
        self.assertEqual(1.00, discount_one)

        self.assertEqual(1.00, price_two)
        self.assertEqual(1.00, discount_two)

        self.assertEqual(1.00, price_three)
        self.assertEqual(1.00, discount_three)

        self.assertEqual(2.00, price_four)
        self.assertEqual(0.00, discount_four)

    def test_apply_discount_large_shipment_mr(self):
        shipment = Shipment(date='2024-04-10', size=Size.LARGE.value, provider=self.provider_mr)
        price, discount = self.calculator.apply_discount(shipment)

        self.assertEqual(4.00, price)
        self.assertEqual(0.0, discount)

    def test_apply_discount_only_one_large_shipment_should_be_free(self):
        shipment_one = Shipment(date='2024-04-11', size=Size.LARGE.value, provider=self.provider_lp)
        shipment_two = Shipment(date='2024-04-12', size=Size.LARGE.value, provider=self.provider_lp)
        shipment_three = Shipment(date='2024-04-13', size=Size.LARGE.value, provider=self.provider_lp)
        shipment_four = Shipment(date='2024-04-13', size=Size.LARGE.value, provider=self.provider_lp)

        price_one, discount_one = self.calculator.apply_discount(shipment_one)
        price_two, discount_two = self.calculator.apply_discount(shipment_two)
        price_three, discount_three = self.calculator.apply_discount(shipment_three)
        price_four, discount_four = self.calculator.apply_discount(shipment_four)

        self.assertEqual(4.50, price_one)
        self.assertEqual(0, discount_one)

        self.assertEqual(4.50, price_two)
        self.assertEqual(0, discount_two)

        self.assertEqual(0, price_three)
        self.assertEqual(4.50, discount_three)

        self.assertEqual(4.50, price_four)
        self.assertEqual(0, discount_four)

    def test_apply_discount_only_one_large_shipment_should_be_free_next_month_should_reset(self):
        shipment_one = Shipment(date='2024-04-11', size=Size.LARGE.value, provider=self.provider_lp)
        shipment_two = Shipment(date='2024-04-12', size=Size.LARGE.value, provider=self.provider_lp)
        shipment_three = Shipment(date='2024-04-13', size=Size.LARGE.value, provider=self.provider_lp)
        shipment_four = Shipment(date='2024-05-13', size=Size.LARGE.value, provider=self.provider_lp)
        shipment_five = Shipment(date='2024-05-13', size=Size.LARGE.value, provider=self.provider_lp)
        shipment_six = Shipment(date='2024-05-13', size=Size.LARGE.value, provider=self.provider_lp)

        price_one, discount_one = self.calculator.apply_discount(shipment_one)
        price_two, discount_two = self.calculator.apply_discount(shipment_two)
        price_three, discount_three = self.calculator.apply_discount(shipment_three)
        price_four, discount_four = self.calculator.apply_discount(shipment_four)
        price_five, discount_five = self.calculator.apply_discount(shipment_five)
        price_six, discount_six = self.calculator.apply_discount(shipment_six)

        self.assertEqual(4.50, price_one)
        self.assertEqual(0, discount_one)

        self.assertEqual(4.50, price_two)
        self.assertEqual(0, discount_two)

        self.assertEqual(0, price_three)
        self.assertEqual(4.50, discount_three)

        self.assertEqual(4.50, price_four)
        self.assertEqual(0, discount_four)

        self.assertEqual(4.50, price_five)
        self.assertEqual(0, discount_five)

        self.assertEqual(0.00, price_six)
        self.assertEqual(4.50, discount_six)

    def test_apply_discount_only_partially_to_large_lp_shipment_when_max_discount_per_month_is_lower_then_shipment_price(self):
        calculator = DiscountCalculator(max_discount_per_month=3.0)
        provider_lp = Provider(Providers.LP.name, {
            Size.SMALL.value: 1.50,
            Size.MEDIUM.value: 2.50,
            Size.LARGE.value: 5.00
        })
        calculator.add_provider(provider_lp)
        shipment_one = Shipment(date='2024-04-11', size=Size.LARGE.value, provider=provider_lp)
        shipment_two = Shipment(date='2024-04-12', size=Size.LARGE.value, provider=provider_lp)
        shipment_three = Shipment(date='2024-04-13', size=Size.LARGE.value, provider=provider_lp)
        shipment_four = Shipment(date='2024-04-13', size=Size.LARGE.value, provider=provider_lp)

        price_one, discount_one = calculator.apply_discount(shipment_one)
        price_two, discount_two = calculator.apply_discount(shipment_two)
        price_three, discount_three = calculator.apply_discount(shipment_three)
        price_four, discount_four = calculator.apply_discount(shipment_four)

        self.assertEqual(5.00, price_one)
        self.assertEqual(0, discount_one)

        self.assertEqual(5.00, price_two)
        self.assertEqual(0, discount_two)

        self.assertEqual(2.00, price_three)
        self.assertEqual(3.00, discount_three)

        self.assertEqual(5.00, price_four)
        self.assertEqual(0, discount_four)


if __name__ == '__main__':
    unittest.main()