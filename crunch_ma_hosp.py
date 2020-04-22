#!/usr/bin/env python3

import sys

Hospitals = {}
Current_Batch = []
Current_Index = 0

state="need hospital name header"

for line in sys.stdin:
	line = line.strip()

	if not line:
		break

	# print("%-30s %s" % (state, line))

	if state == "need hospital name header":
		if line == "Hospital Name":
			state = "read hospital names"
			Current_Batch = []
		else:
			raise Exception(f"Need hospital name header, got {line}")

	elif state == "read hospital names":
		if line == "Hospital county":
			state = "need and zip code"
		elif line in Hospitals:
			raise Exception(f"Duplicate hospital {line}")
		else:
			Hospitals[line] = {}
			Current_Batch.append(line)

	elif state == "need and zip code":
		if line == "and zip code":
			state = "read county and zip"
			Current_Index = 0
		else:
			raise Exception(f"Need 'and zip code', got {line}")

	elif state == "read county and zip":
		if line == "Hospitalized Total COVID":
			state = "need patients"
		else:
			(county, zipcode) = line.split('-')

			hospital = Current_Batch[Current_Index]
			Hospitals[hospital]["county"] = county.strip()
			Current_Index += 1

	elif state == "need patients":
		if line == "patients - suspected and":
			state = "need confirmed"
		else:
			raise Exception(f"Need 'patients - suspected and', got {line}")

	elif state == "need confirmed":
		if line == "confirmed (including ICU)":
			state = "read confirmed"
			Current_Index = 0
		else:
			raise Exception(f"Need 'confirmed (including ICU)', got {line}")

	elif state == "read confirmed":
		if line == "Hospitalized COVID Patients in":
			state = "need ICU"
		else:
			hospital = Current_Batch[Current_Index]
			Hospitals[hospital]["confirmed"] = int(line)
			Current_Index += 1

	elif state == "need ICU":
		if line == "ICU - suspected and confirmed":
			state = "read ICU"
			Current_Index = 0
		else:
			raise Exception(f"Need 'ICU - suspected and confirmed', got {line}")

	elif state == "read ICU":
		if line.startswith("Massachusetts Department of Public Health"):
			state = "skip page break"
		else:
			hospital = Current_Batch[Current_Index]
			Hospitals[hospital]["ICU"] = int(line)
			Current_Index += 1

	elif state == "skip page break":
		if line.startswith("COVID Patient Census by Hospital"):
			state = "skip page break count"
		else:
			raise Exception(f"Need 'COVID Patient Census by Hospital...', got {line}")


	elif state == "skip page break count":
		state = "need hospital name header"

counts_by_county = {}
total = 0

print("---- hospitals")
for hospital in sorted(Hospitals.keys()):
	county = Hospitals[hospital]["county"]
	confirmed = Hospitals[hospital]["confirmed"]

	if county not in counts_by_county:
		counts_by_county[county] = 0

	counts_by_county[county] += confirmed
	total += confirmed

	print(f"{hospital} ({county}): {confirmed}")

print("---- counties")
for county in sorted(counts_by_county.keys()):
	print(f"{county}: {counts_by_county[county]}")

middlesex = counts_by_county['Middlesex']
suffolk = counts_by_county['Suffolk']

print(f"---- total {total}")
print(f"Massachusetts without Middlesex and Suffolk: {total - (middlesex + suffolk)}")

