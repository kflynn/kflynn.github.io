#!python

import sys

import datetime
import glob
import os
import zipfile

import requests

from io import BytesIO
from crunch_ma_hosp_xls import crunch_path

def date_key(then: datetime.datetime.date) -> str:
    return then.strftime("%Y%m%d")

def prev_day(then: datetime.datetime.date) -> datetime.datetime.date:
    return then + datetime.timedelta(days=-1)

def next_day(then: datetime.datetime.date) -> datetime.datetime.date:
    return then + datetime.timedelta(days=1)

def dash_path(then: datetime.datetime.date) -> str:
    return os.path.join("ma.gov", "%s-raw" % date_key(then))

def dash_url(then: datetime.datetime.date) -> str:
    return then.strftime("https://www.mass.gov/doc/covid-19-raw-data-%b-%d-%Y/download").lower()

def pdf_path(then: datetime.datetime.date) -> str:
    return os.path.join("ma.gov", "covid-19-dashboard-%d-%d-%d.pdf" % (then.month, then.day, then.year))

def pdf_url(then: datetime.datetime.date) -> str:
    return then.strftime("https://www.mass.gov/doc/covid-19-dashboard-%b-%d-%Y/download").lower()

now = datetime.datetime.date(datetime.datetime.now())
cur = now

while True:
    # print(f"check {dash_path(cur)}:", end="")

    if os.path.exists(dash_path(cur)):
        cur = next_day(cur)
        # print(f" exists, start with {date_key(cur)}")

        break

    # print(" does not exist")
    cur = prev_day(cur)

print(f"Starting with {date_key(cur)}")

curdir = os.getcwd()

while cur <= now:
    sys.stdout.write(f"{date_key(cur)}: pulling PDF... ")
    sys.stdout.flush()

    resp = requests.get(pdf_url(cur))

    if resp.status_code == 200:
        sys.stdout.write(f" OK")
        sys.stdout.flush()

        with open(pdf_path(cur), "wb") as raw_out:
            raw_out.write(resp.content)
    else:
        sys.stdout.write(f" failed {r.status_code}")
        sys.stdout.flush()

    sys.stdout.write("; pulling dash... ")
    sys.stdout.flush()

    resp = requests.get(dash_url(cur))

    if resp.status_code == 200:
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
        sys.stdout.write(f" failed {r.status_code}")
        sys.stdout.flush()

    sys.stdout.write("; crunching dash:\n")
    sys.stdout.flush()

    spreadsheet_glob = os.path.join(dash_path(cur), "External dashboard *.xlsx")

    pathnames = glob.glob(spreadsheet_glob)

    if len(pathnames) != 1:
        raise Exception("no such file: %s" % spreadsheet_glob)

    crunch_path(pathnames[0])

    cur = next_day(cur)

