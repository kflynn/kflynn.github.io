import sys

import csv
import datetime

class Hospitalizations:
    def __init__(self, path) -> None:
        self.path = path

        with open("hospitalizations.csv", "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            self.fieldnames = reader.fieldnames

            month, day, year = map(int, self.fieldnames[-1].split('/'))

            if year < 1900:
                year += 2000

            self.rows = list(reader)

            self.cur = datetime.date(day=day, month=month, year=year)

    def __next__(self) -> str:
        self.cur += datetime.timedelta(days=1)

        return self.cur

    def update(self, then, counties):
        key = f"{then.month}/{then.day}/{then.year - 2000}"

        if key not in self.fieldnames:
            self.fieldnames.append(key)

        for r in self.rows:
            county = r['Admin2']

            if county in counties:
                count = counties[county]

                print(f"{key}: {county} = {count}")
                r[key] = str(count)
            else:
                print(f"{key}: {county} = ??")
                r[key] = "0"

    def save(self):
        with open("h2.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)

            writer.writeheader()

            for r in self.rows:
                writer.writerow(r)


