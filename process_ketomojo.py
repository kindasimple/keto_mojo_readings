#!/usr/bin

import csv
from datetime import datetime
from collections import defaultdict
import pytz
from pathlib import Path
import argparse


LOCAL_TIMEZONE = 'America/Los_Angeles'
MAX_READING_TIME_DIFF = 60 * 10  # 10 minutes

FIELDNAMES = ['type', 'value', 'unit', 'date', 'time']
VALUE_TYPES = ['Glucose', 'Ketone', 'Hematocrit', 'Hemoglobin', 'Create Date', 'Update Date']

INPUT_FILEPATH = './KetoMojo.csv'
OUTPUT_FILEPATH = './keto_mojo_readings.csv'

def reading_dict_to_date(reading):
    naive_datetime = datetime.strptime(
        '{}{}'.format(reading['date'], reading['time']).strip()
        , '%m/%d/%y %I:%M %p'
    )
    pst = pytz.timezone(LOCAL_TIMEZONE)
    return pst.localize(naive_datetime)
 

def gather_input(input_file_path):
    """
    iterate over readings in the input file and aggregate data points
    captured within a 15 minute window, averaging readings of the same 
    type.
    """
    readings = []
    last_reading_date = None
    with open(input_file_path) as infile:
        next(infile)
        data = csv.DictReader(infile, fieldnames=FIELDNAMES)
        reading_data = defaultdict(list)
        reading_update_date = None
        for datum in data:
            # get the date from the reading dictionary
            datum_date = reading_dict_to_date(datum)
            if not reading_update_date:
                reading_create_date = reading_update_date = datum_date
            readings_diff_seconds= (datum_date - reading_update_date).total_seconds()
            if abs(readings_diff_seconds) > MAX_READING_TIME_DIFF:
                # if the readings are far apart add the reading
                reading = calculate_reading(reading_data, reading_create_date, reading_update_date)
                readings.append(reading)
                # reset the reading create a new reading
                reading_data = defaultdict(list)
                reading_create_date = datum_date
            reading_data[datum['type']].append(datum['value'])
            reading_update_date = datum_date
        reading = calculate_reading(reading_data, reading_create_date, reading_update_date)
        readings.append(reading)
    return readings


def write_output(output_file_path, readings):
    """Write readings to an output csv file"""
    with open(output_file_path, 'w') as outfile:
        writer = csv.DictWriter(outfile, VALUE_TYPES)
        writer.writeheader()
        writer.writerows(readings)


def calculate_reading(data_type_to_values, create_date, update_date):
    """
    Average readings for each type
    """
    data = {
        reading_type: sum([float(v) for v in values])/len(values) or None
        for reading_type, values in data_type_to_values.items()
    }
    data['Create Date'] = create_date.strftime('%m-%d-%Y %H:%m')
    data['Update Date'] = update_date.strftime('%m-%d-%Y %H:%m')
    return data


def main(input_filepath, output_filepath):
    readings = gather_input(input_filepath)
    write_output(output_file, readings)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--output-file', 
        help="The file to write results to ",
        default=OUTPUT_FILEPATH)
    args = parser.parse_args()

    input_file = Path(INPUT_FILEPATH).absolute()
    output_file = Path(args.output_file).absolute()
    main(input_file, output_file)
