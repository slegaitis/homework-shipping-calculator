import logging
from collections import defaultdict
from datetime import datetime
from typing import Tuple, Union

from constants import Size, Providers
from lib.providers.provider import Provider
from lib.shipments.shipment import Shipment


class DiscountCalculator:
    def __init__(self, max_discount_per_month: float):
        self.max_discount_per_month = max_discount_per_month
        self.providers = defaultdict()
        self.discount_accumulated = 0
        self.shipments_count_by_month = defaultdict(lambda: defaultdict(int))
        self.nth_free_large_package_lp = 3
        self.logger = logging.getLogger()

    def apply_discount(self, shipment: Shipment) -> Tuple[float, Union[float, str]]:
        if shipment.provider is None:
            self.logger.debug(f'Unknown provider: {shipment.to_dict()}')
            return 0.0, 0.0

        if not shipment.is_shipment_valid():
            self.logger.debug(f'Shipment date or size is invalid: {shipment.to_dict()}')
            return 0.0, 0.0

        price = shipment.provider.get_price(shipment.size)
        discount = 0.0

        if shipment.size == Size.SMALL.value:
            # Discount for size 'S' shipments should match the lowest 'S' package price among all providers
            min_price_s = min(provider.prices[Size.SMALL.value] for provider in self.providers.values())
            discount = price - min_price_s
            self.logger.debug(f'Handling small size package. {shipment.to_dict()} price: {min_price_s} discount: {discount}')
        elif shipment.size == Size.LARGE.value and shipment.provider.name == Providers.LP.value:
            # Note: Readme states that: The third L shipment via LP should be free, but only once a calendar month. but also states that
            # Accumulated discounts cannot exceed 10 € in a calendar month. If there are not enough funds to fully cover a discount this calendar month, it should be covered partially.
            # Wasn't 100% sure if to cover the third shipment and accumulate discounts. For e.g if third shipment cost is 6 euro and maximum discount in a month is 10 euro should it cover next shipment 4 euro discount?
            # Code below covers case where ONLY The third L shipment via LP should be free and then no further discounts are applied to L shipments for LP provider also note if max_discount_per_month is lower then the shipment
            # price it will only deduct partial
            month = datetime.strptime(shipment.date, '%Y-%m-%d').month
            self.shipments_count_by_month[Providers.LP.value][month] += 1

            if self.shipments_count_by_month[Providers.LP.value][month] == self.nth_free_large_package_lp:
                # This is the third shipment, apply discount
                discount = price

            self.logger.debug(
                f'Handling shipment LP large package. {shipment.to_dict()} price: {price} discount: {discount}')
        else:
            self.logger.debug(
                f'Handling standard shipment. {shipment.to_dict()} price: {price} discount: {discount}')
            return price, discount

        remaining_discount = self.max_discount_per_month - self.discount_accumulated
        if discount > remaining_discount:
            # Ensure the discount does not exceed the remaining discount for the month
            discount = remaining_discount

        self.discount_accumulated += discount

        discounted_price = price - discount
        return discounted_price, discount

    def add_provider(self, provider: Provider) -> None:
        self.providers[provider.name] = provider
