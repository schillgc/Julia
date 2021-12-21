import csv
import json
from .models import File
from io import StringIO


# CSV
def csv_file():
    with open(File.path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    with open(File.path + '.json', 'w') as f:
        json.dump(rows, f)


# JSON
def json_file():
    json_data = open(File.path)
    data = json.load(json_data)
    json.dump(data, json_data)


# Plain Text (txt)
def txt_file():
    with open(File.path, "r") as infile:
        for line in infile:
            val = line.split()
