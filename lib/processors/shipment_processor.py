import logging
import pandas as pd

from constants import Providers
from lib.shipments.shipment import Shipment


class ShipmentProcessor:
    def __init__(self, discount_calculator):
        self.discount_calculator = discount_calculator
        self.logger = logging.getLogger()

    def process_transactions(self, input_filename, output_filename):
        try:
            df = pd.read_csv(input_filename, sep=' ', header=None, names=['date', 'size', 'provider'])
            output_df = df.copy()

            # Vectorized operation to apply discount
            output_df['price'], output_df['discount'] = zip(*output_df.apply(self.apply_discount, axis=1))

            output_df.to_csv(output_filename, sep=' ', header=False, index=False, float_format='%.2f')
            self.logger.debug(f"Output written to {output_filename}")
            self.logger.info(output_df)

        except FileNotFoundError as e:
            self.logger.error(f"File not found. {e}")
            raise SystemExit(1)

    def apply_discount(self, row):
        provider = self.discount_calculator.providers.get(row['provider'])

        shipment = Shipment(row['date'], row['size'], provider)
        shipment.price, shipment.discount = self.discount_calculator.apply_discount(shipment)
        formatted_discount = round(shipment.discount, 2) if shipment.discount else '-'
        formatted_price = round(shipment.price, 2) if shipment.price or isinstance(formatted_discount, float) else Providers.UNKNOWN.value

        return formatted_price, formatted_discount

