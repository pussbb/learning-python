"""

"""
import csv
import json
from collections import namedtuple

transformed_csv = open('sx_requests_pprint.csv', 'w')
fieldnames = ['requested_at', 'customer_email', 'customer_data',
              'scalix_version']

CsvRow = namedtuple('CsvRow', fieldnames)

writer = csv.DictWriter(transformed_csv, fieldnames=fieldnames)
writer.writeheader()


def json_string_to_palin(string):
    result = []
    for key, value in json.loads(string)[0].items():
        result.append(key + ' : ' + value)
    return "\n".join(result)

with open('sx_requests.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
    for row in reader:
        if 'requested_at' in row:
            # skip first line its a header
            continue
        csvRow = CsvRow(*row)
        csvRow = csvRow._replace(
            customer_data=json_string_to_palin(csvRow.customer_data)
        )
        writer.writerow(csvRow._asdict())

