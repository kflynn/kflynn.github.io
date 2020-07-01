#!python

import sys

import csv
import datetime
import os
import zipfile

import requests

from io import BytesIO
from crunch_ma_hosp_xls import crunch_xls
from hosp import Hospitalizations

def date_key(then: datetime.datetime.date) -> str:
    return then.strftime("%Y%m%d")

def prev_day(then: datetime.datetime.date) -> datetime.datetime.date:
    return then + datetime.timedelta(days=-1)

def next_day(then: datetime.datetime.date) -> datetime.datetime.date:
    return then + datetime.timedelta(days=1)

def dash_path(then: datetime.datetime.date) -> str:
    return os.path.join("ma.gov", "%s-raw" % date_key(then))

def dash_url(then: datetime.datetime.date) -> str:
    return f"https://www.mass.gov/doc/covid-19-raw-data-{then:%B}-{then.day}-{then.year}/download".lower()

def pdf_path(then: datetime.datetime.date) -> str:
    return os.path.join("ma.gov", "covid-19-dashboard-%d-%d-%d.pdf" % (then.month, then.day, then.year))

def pdf_url(then: datetime.datetime.date) -> str:
    return f"https://www.mass.gov/doc/covid-19-dashboard-{then:%B}-{then.day}-{then.year}/download".lower()

hosp = Hospitalizations("hospitalizations.csv")

now = datetime.datetime.date(datetime.datetime.now())
# cur = now

# while True:
#     # print(f"check {dash_path(cur)}:", end="")

#     if os.path.exists(dash_path(cur)):
#         cur = next_day(cur)
#         # print(f" exists, start with {date_key(cur)}")

#         break

#     # print(" does not exist")
#     cur = prev_day(cur)

# Start loading data for the day after the last day we have hospitalizations for.
cur = next(hosp)
print(f"Starting with {date_key(cur)}")

curdir = os.getcwd()

# Basically, walk from the start date up until the present. Try to pull data for 
# each date.

while cur <= now:
    sys.stdout.write(f"{date_key(cur)}: pulling PDF... ")
    sys.stdout.flush()

    got_dash = False
    got_xls = False

    resp = requests.get(pdf_url(cur))

    if resp.status_code == 200:
        got_dash = True
        sys.stdout.write(f" OK")
        sys.stdout.flush()

        with open(pdf_path(cur), "wb") as raw_out:
            raw_out.write(resp.content)
    else:
        sys.stdout.write(f" failed {resp.status_code} -- {pdf_url(cur)}")
        sys.stdout.flush()

    if os.path.exists(dash_path(cur)):
        got_xls = True
        sys.stdout.write("; have dash")
        sys.stdout.flush()        
    else:
        sys.stdout.write("; pulling dash... ")
        sys.stdout.flush()

        resp = requests.get(dash_url(cur))

        if resp.status_code == 200:
            got_xls = True
            sys.stdout.write(f"OK")
            sys.stdout.flush()

            with open(f"{dash_path(cur)}.zip", "wb") as raw_out:
                raw_out.write(resp.content)

            z = zipfile.ZipFile(BytesIO(resp.content))

            os.mkdir(dash_path(cur))
            os.chdir(dash_path(cur))

            z.extractall()

            os.chdir(curdir)
        else:
            sys.stdout.write(f" failed {resp.status_code}")
            sys.stdout.flush()

    if not got_dash and not got_xls:
        sys.stdout.write("; no data, bailing\n")
        sys.stdout.flush()
        break

    sys.stdout.write("; crunching dash:\n")
    sys.stdout.flush()

    counties = crunch_xls(dash_path(cur))

    if counties is None:
        raise Exception(f"no XLS found for {date_key(cur)}")

    # OK, if we were able to crunch county data, update hospitalizations 
    # with that... but remember! Hospitalizations lag by a day.
    hosp.update(cur + datetime.timedelta(days=-1), counties)

    cur = next_day(cur)

hosp.save()