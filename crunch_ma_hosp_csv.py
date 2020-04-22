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

total_hosp = {}
icu_hosp = {}

with open(sys.argv[1], "r", newline="") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        print([ "'%s'" % x for x in row ])
        raw_date, hospital, county, zip, total, icu = list(row)

        m = re.match(r'^(\d+)/(\d+)/(\d+)$', raw_date)

        if not m:
            raise Exception(f"ill-formatted date {raw_date} in {sys.argv[1]}")

        formatted = "%d/%d/%02d" % (int(m.group(1)), int(m.group(2)), int(m.group(3)) % 100)

        th = total_hosp.setdefault(formatted, {})
        ti = icu_hosp.setdefault(formatted, {})

        if county not in th:
            th[county] = 0
        
        th[county] += int(total)

        if county not in ti:
            ti[county] = 0
        
        ti[county] += int(icu)

        if "MA" not in th:
            th["MA"] = 0
        
        th["MA"] += int(total)

        if "MA" not in ti:
            ti["MA"] = 0
        
        ti["MA"] += int(icu)

print("==== total")
print(total_hosp)

print("==== ICU")
print(icu_hosp)
