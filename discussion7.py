import unittest
import os
import csv

###############################################################################
##### TASK 1: CSV READER
###############################################################################
def load_listings(f):
    """
    Read the Airbnb listings CSV and return a list of records.
    Returns a list of dictionaries with ALL VALUES AS STRINGS.
    """

    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    listings = []

    with open(full_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            listings.append(row)  # keep values as strings

    return listings


###############################################################################
##### TASK 2: CALCULATION FUNCTION (single calculation)
###############################################################################
def calculate_avg_price_by_neighbourhood_group_and_room(listings):
    """
    Calculate the average nightly price for each (neighbourhood_group, room_type).
    Returns dict mapping (neighbourhood_group, room_type) -> average_price (float)
    """

    totals = {}
    counts = {}

    for listing in listings:
        key = (listing['neighbourhood_group'], listing['room_type'])
        price = float(listing['price'])

        if key not in totals:
            totals[key] = 0
            counts[key] = 0

        totals[key] += price
        counts[key] += 1

    averages = {}

    for key in totals:
        averages[key] = totals[key] / counts[key]

    return averages


###############################################################################
##### TASK 3: CSV WRITER
###############################################################################
def write_summary_csv(out_filename, avg_prices):
    """
    Write summary CSV with header:
    neighbourhood_group, room_type, average_price
    """

    with open(out_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['neighbourhood_group', 'room_type', 'average_price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for (group, room), avg_price in avg_prices.items():
            writer.writerow({
                'neighbourhood_group': group,
                'room_type': room,
                'average_price': avg_price
            })


###############################################################################
##### UNIT TESTS (Do not modify the code below!)
###############################################################################
class TestAirbnbListings(unittest.TestCase):

    def setUp(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        full_path = os.path.join(base_path, 'new_york_listings_2024.csv')
        self.listings = load_listings(full_path)

    def test_load_listings(self):
        self.assertIsInstance(self.listings, list)
        self.assertGreater(len(self.listings), 0)
        self.assertIsInstance(self.listings[0], dict)

        expected_keys = ['neighbourhood_group', 'room_type', 'price']
        for key in expected_keys:
            self.assertIn(key, self.listings[0])

    def test_calculate_avg_price_by_neighbourhood_group_and_room(self):
        averages = calculate_avg_price_by_neighbourhood_group_and_room(self.listings)

        self.assertAlmostEqual(
            averages[('Manhattan', 'Entire home/apt')],
            253.74735249621784,
            places=2
        )

        self.assertAlmostEqual(
            averages[('Brooklyn', 'Private room')],
            161.65877598152426,
            places=2
        )

        self.assertAlmostEqual(
            averages[('Queens', 'Entire home/apt')],
            179.92875157629257,
            places=2
        )

        self.assertAlmostEqual(
            averages[('Bronx', 'Private room')],
            97.30147058823529,
            places=2
        )

        self.assertAlmostEqual(
            averages[('Staten Island', 'Entire home/apt')],
            139.85256410256412,
            places=2
        )

    def test_write_and_read_summary(self):
        averages = calculate_avg_price_by_neighbourhood_group_and_room(self.listings)
        test_output = 'test_summary_output.csv'

        write_summary_csv(test_output, averages)

        with open(test_output, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            self.assertEqual(len(rows), 18)
            self.assertEqual(
                reader.fieldnames,
                ['neighbourhood_group', 'room_type', 'average_price']
            )


def main():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()