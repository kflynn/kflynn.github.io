import sys

from openpyxl import load_workbook

wb = load_workbook(sys.argv[1])
sheet = wb['Hospital COVID census']

for cell_id, wanted in [
    ( "A1", "Hospital Name" ),
    ( "B1", "Hospital County and Zip Code" ),
    ( "C1", "Hospitalized Total COVID patients - suspected and confirmed (including ICU)" ),
    ( "D1", "Hospitalized COVID patients in ICU - suspected and confirmed" )
]:
    if sheet[cell_id].value != wanted:
        raise Exception(f"Cell {cell_id} should be {wanted} but is {sheet[cell_id].value}")

counties = {}
massachusetts = 0
ma_other = 0

for row in sheet[2:sheet.max_row]:
    name = row[0].value
    c_and_z = row[1].value
    confirmed = row[2].value
    icu = row[3].value

    # print(f"{name} ({c_and_z}): {confirmed}, {icu} ICU")

    county, zip = c_and_z.split('-')
    county = county.strip()
    zip = zip.strip()

    if county not in counties:
        counties[county] = 0
    
    counties[county] += confirmed
    massachusetts += confirmed

    if (county != "Middlesex") and (county != "Suffolk"):
        ma_other += confirmed

print("---- counties")

for county in sorted(counties.keys()):
    print("%s: %d" % (county, counties[county]))

print("---- total %d" % massachusetts)

print("Massachusetts without Middlesex and Suffolk: %d" % ma_other)
