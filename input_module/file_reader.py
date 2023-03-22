from typing import Dict, List
import csv

def read_csv(filename: str) -> csv.DictReader:
    with open(filename) as file:
        return csv.DictReader(file)