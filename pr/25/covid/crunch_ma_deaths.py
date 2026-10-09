import sys

import csv
import json
import math
import os
import re

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s covid %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

new_deaths = {}
total = 0

with open(sys.argv[1], "r", newline="") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row['County'] not in new_deaths:
            new_deaths[row['County']] = 0

        new_deaths[row['County']] += 1
        total += 1

for county in sorted(new_deaths.keys()):
    print(f"{county}: {new_deaths[county]}")

print(f"Total: {total}")
