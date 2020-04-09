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

COVID_DIR = os.environ.get("COVID_DIR") or "../COVID-19/csse_covid_19_data/csse_covid_19_time_series"

TRACK = {
    'Middlesex, Massachusetts',
    'Suffolk, Massachusetts',
    'New York, New York',
    'District of Columbia, District of Columbia',
    'Denton, Texas',
    'San Francisco, California',
    'Santa Clara, California',
    'San Mateo, California',
    'Spain',
    'Italy',
    'United Kingdom'
}

class Collection:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = re.sub(r'[^A-Za-z0-9]', '_', self.name).lower()
        self.data = {}
        self.population = None
        self.valid_dates = {}

    def load(self, datatype: str, row) -> None:
        # Given a row of data, run the window analysis on it and save the results.
        if not self.population and ('Population' in row):
            self.population = int(row['Population'])

        # Extract the dates and counts from the row.
        counts = []

        for k in row.keys():
            if k[0].isdigit():
                counts.append((k, int(row[k])))

        # We shouldn't already have an entry for this data type...
        if datatype in self.data:
            raise Exception(f"{self.name}: duplicate {datatype} data?")

        self.data[datatype] = {}

        logging.debug(f"{self.name}: loading {datatype}")

        self.data[datatype][7] = self.windows(counts, 7)
        self.data[datatype][14] = self.windows(counts, 14)
        self.data[datatype][21] = self.windows(counts, 21)
        
        # XXX: This shouldn't involve a separate loop, but I don't want to
        # refactor everything right now.

        for window_size in [ 7, 14, 21 ]:
            info = self.data[datatype][window_size]

            if info:
                for d, _, _, _ in info:
                    m = re.match(r'^(\d+)/(\d+)/(\d+)$', d)

                    if not m:
                        raise Exception(f"ill-formatted date {d} in {place_key}")
                    
                    date_key = "20%02d%02d%02d" % (int(m.group(3)), int(m.group(1)), int(m.group(2)))

                    self.valid_dates[date_key] = d

    def windows(self, counts, window_size):
        while len(counts) and (counts[0][1] == 0):
            counts.pop(0)

        # How does Washington DC go from 1 to 0 to 2?
        for i in range(1, len(counts)):
            if counts[i][1] == 0:
                counts[i] = (counts[i][0], counts[i-1][1])

        if len(counts) < window_size:
            logging.debug(f"{self.name}: too little data for {window_size}-day windows")
            return None

        window_offset = window_size - 1
        idx = window_offset

        results = []

        logging.debug(f"  {window_size}-day windows:")

        while idx < len(counts):
            window_end = counts[idx][0]
            week = [x[1] for x in counts[idx-window_offset:idx+1]]

            assert(len(week) == window_size)

            mult = (week[-1] / week[0]) ** (1 / (window_size - 1))

            try:
                dbl_days = math.log(2) / math.log(mult)
                logging.debug("    %8s: %5.2f days (mult %.4f, [%s])" % 
                              (window_end, dbl_days, mult, ", ".join(map(str, week))))
                results.append((window_end, dbl_days, mult, week[-1]))
            except ZeroDivisionError:
                logging.debug("    %8s: steady" % window_end)
                results.append((window_end, math.nan, math.nan, week[-1]))

            idx += 1

        return results

Collections = {}

for datatype, filename in [
    ( 'confirmed', 'time_series_covid19_confirmed_US.csv' ),
    ( 'confirmed', 'time_series_covid19_confirmed_global.csv' ),
    ( 'deaths', 'time_series_covid19_deaths_US.csv' ),
    ( 'deaths', 'time_series_covid19_deaths_global.csv' ),
]:
    path = os.path.join(COVID_DIR, filename)
    
    with open(path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        first = True

        for row in reader:
            key_elements = []

            if 'Admin2' in row:
                key_elements.append(row['Admin2'])
            
            if 'Province_State' in row:
                key_elements.append(row['Province_State'])
            elif 'Province/State' in row:
                key_elements.append(row['Province/State'])

            if 'Country/Region' in row:
                country = row['Country/Region']

                if country != 'US':
                    key_elements.append(country)

            place_key = ", ".join([x for x in key_elements if x])

            if place_key in TRACK:
                
                if not first:
                    logging.debug("")

                if not place_key in Collections:
                    Collections[place_key] = Collection(place_key)

                collection = Collections[place_key]
                collection.load(datatype, row)

                first = False

all_valid_dates = {}

for place_key in sorted(Collections.keys()):
    collection = Collections[place_key]

    for dk, d in collection.valid_dates.items():
        all_valid_dates[dk] = d

stringified_dates = ", ".join([f'"{all_valid_dates[x]}"' for x in sorted(all_valid_dates.keys())])

print('''
<!doctype html>
<html>

<head>
	<title>Doubling Times</title>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js"></script>
	<!-- <script src="../../utils.js"></script> -->
	<style>
	canvas{
		-moz-user-select: none;
		-webkit-user-select: none;
		-ms-user-select: none;
	}
	</style>
</head>

<body>
  <H1>COVID-19 Doubling Times</H1>
  <p>
    These graphs are generated from the 
    <a href="https://github.com/CSSEGISandData/COVID-19">Johns Hopkins CSSE data</a>, 
    which is updated daily.
  </p>
  <p>
    The graph shows the doubling time of COVID-19 deaths (red) or confirmed cases (blue),
    expressed in days, looking at the seven-day window that ended on the date being plotted. 
    No data are graphed for times during which a given location reported no deaths or cases.
    Likewise, no point will be plotted if the number was constant over the whole seven-day
    window.
  </p>
  <p>
    These graphs do <em>not</em> show the number of cases: they show only the doubling times.
    As such, <em>higher values are "better"</em>... except that the graph will show 
    negative values when the number of cases actually start decreasing.
  </p>
  <p>
    A final caution: I'm not an epidimiologist, I just think we're not good at intuiting
    about exponential growth rates. Use with caution.
  </p>
''')

places = list(sorted(Collections.keys()))

# Plot the 7-day graphs for now, and make the X-axis always the same.
dates = {}

for place_key in places:
    collection = Collections[place_key]

    print(f'''
	<div style="width:100%;">
		<canvas id="{collection.id}-canvas"></canvas>
	</div>
    ''')

print('''
	<br>
	<br>
	<script>
''')

for place_key in places:
    collection = Collections[place_key]
    place_id = collection.id

    dbl_series = {}
    mult_series = {}

    for datatype in collection.data.keys():
        info = collection.data[datatype][7]
        idict = { x[0]: x for x in info }

        d_series = []
        m_series = []

        for d in sorted(all_valid_dates.keys()):
            raw_date = all_valid_dates[d]

            if raw_date in idict:
                _, dbl_days, mult, count = idict[raw_date]

                d_series.append(dbl_days)
                m_series.append(mult)
            else:
                d_series.append(math.nan)
                m_series.append(math.nan)

        dbl_series[datatype] = d_series
        mult_series[datatype] = m_series

    print("""
		var %s_config = {
			type: 'line',
			data: {
                labels: [ %s ],
				datasets: [
    """ % (place_id, stringified_dates))

    if "deaths" in  dbl_series:
        print("""
                    {
                        label: 'Doubling Times (deaths)',
                        data: %s,
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        fill: false,
                    }
        """ % json.dumps(dbl_series["deaths"]))

        if "confirmed" in dbl_series:
            print("""
                    ,
            """)
        
    if "confirmed" in dbl_series:
        print("""
                    {
                        label: 'Doubling Times (cases)',
                        data: %s,
                        fill: false,
                        backgroundColor: 'rgb(54, 162, 235)',
                        borderColor: 'rgb(54, 162, 235)',
                        spanGaps: false
                    }
                ]
        """ % json.dumps(dbl_series["confirmed"]))

    print("""
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: '%s'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Day'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Value'
						},
                        ticks: {
                            max: 20
                        }
					}]
				}
			}
		};
    """ % place_key)

print('''
		window.onload = function() {
''')

for place_key in places:
    collection = Collections[place_key]
    place_id = collection.id

    print(f"""
			var {place_id}_ctx = document.getElementById('{place_id}-canvas').getContext('2d');
			var {place_id}_chart = new Chart({place_id}_ctx, {place_id}_config);
    """)

print('''
		};

	</script>
</body>

</html>
''')
