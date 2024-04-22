from constants import Size, Providers
from helpers import configure_logging
from lib.discounts.discount_calculator import DiscountCalculator
from lib.processors.shipment_processor import ShipmentProcessor
from lib.providers.provider import Provider

logger = configure_logging()

if __name__ == "__main__":
    input_file = 'data/input.txt'
    output_file = 'data/output.txt'

    calculator = DiscountCalculator(max_discount_per_month=10)

    lp_provider = Provider(Providers.LP.name, {Size.SMALL.value: 1.50, Size.MEDIUM.value: 4.90, Size.LARGE.value: 6.90})
    mr_provider = Provider(Providers.MR.name, {Size.SMALL.value: 2.00, Size.MEDIUM.value: 3.00, Size.LARGE.value: 4.00})
    provider_list = [lp_provider, mr_provider]

    for provider in provider_list:
        calculator.add_provider(provider)

    processor = ShipmentProcessor(calculator)
    processor.process_transactions(input_filename=input_file, output_filename=output_file)
