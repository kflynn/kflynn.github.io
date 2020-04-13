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
    'Los Angeles, California',
    'British Columbia, Canada',
    'Spain',
    'Italy',
    'United Kingdom',
    'US'
}

AGGREGATE = {
    'Canada',
    'Massachusetts',
    'New York',
    'California',
    'Texas'
}

class Collection:
    def __init__(self, name: str, aggregator=False) -> None:
        self.name = name
        self.id = re.sub(r'[^A-Za-z0-9]', '_', self.name).lower()
        self.raw_data = {}      # Raw counts
        self.data = {}          # Windowed data
        self.valid_dates = {}

        self.population = 0
        self.is_aggregator = aggregator

    def load(self, datatype: str, row) -> None:
        if not self.is_aggregator:
            # We shouldn't already have an entry for this data type...
            if datatype in self.data:
                raise Exception(f"{self.name}: duplicate {datatype} data?")

        logging.debug(f"{self.name}: loading {datatype}: {row}")

        # OK, good to go. If there's a population here, roll it in.
        if 'Population' in row:
            self.population += int(row['Population'])

        # Figure out where we're saving stuff.
        if datatype not in self.raw_data:
            self.raw_data[datatype] = {}

        raw_data = self.raw_data[datatype]

        # Extract the dates and counts from the row.
        for k in row.keys():
            if k[0].isdigit():
                m = re.match(r'^(\d+)/(\d+)/(\d+)$', k)

                if not m:
                    raise Exception(f"ill-formatted date {k} in {self.name}")

                date_key = "20%02d%02d%02d" % (int(m.group(3)), int(m.group(1)), int(m.group(2)))

                if date_key not in raw_data:
                    raw_data[date_key] = [k, 0]

                raw_data[date_key][1] += int(row[k])
                self.valid_dates[date_key] = k

    def analyze(self):
        for datatype in self.raw_data.keys():
            self.data[datatype] = {}

            self.data[datatype][7] = self.windows(self.raw_data[datatype], 7)
            self.data[datatype][14] = self.windows(self.raw_data[datatype], 14)
            self.data[datatype][21] = self.windows(self.raw_data[datatype], 21)

    def windows(self, raw_data, window_size):
        raw_keys = list(sorted(raw_data.keys()))
        counts = [ raw_data[k] for k in raw_keys ]

        logging.debug(f"Analyzing {self.name}, raw_data {raw_data}, counts {counts}")

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

for key in AGGREGATE:
    Collections[key] = Collection(key, aggregator=True)

for datatype, path in [
    ( 'confirmed', os.path.join(COVID_DIR, 'time_series_covid19_confirmed_US.csv') ),
    ( 'confirmed', os.path.join(COVID_DIR, 'time_series_covid19_confirmed_global.csv') ),
    ( 'deaths', os.path.join(COVID_DIR, 'time_series_covid19_deaths_US.csv') ),
    ( 'deaths', os.path.join(COVID_DIR, 'time_series_covid19_deaths_global.csv') ),
    ( 'hospitalizations', 'hospitalizations.csv' )
]:    
    with open(path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            key_elements = []
            state = None
            country = None

            if 'Admin2' in row:
                key_elements.append(row['Admin2'])
            
            if 'Province_State' in row:
                key_elements.append(row['Province_State'])
                state = row['Province_State']
            elif 'Province/State' in row:
                key_elements.append(row['Province/State'])
                state = row['Province/State']

            if 'Country/Region' in row:
                country = row['Country/Region']

                if country:
                    key_elements.append(country)

            place_key = ", ".join([x for x in key_elements if x])

            if place_key in TRACK:
                if not place_key in Collections:
                    Collections[place_key] = Collection(place_key)

                collection = Collections[place_key]
                collection.load(datatype, row)

            if state and (state in AGGREGATE):
                collection = Collections[state]
                collection.load(datatype, row)

            if country and (country in AGGREGATE):
                collection = Collections[country]
                collection.load(datatype, row)

all_valid_dates = {}

for place_key in sorted(Collections.keys()):
    collection = Collections[place_key]

    collection.analyze()

    for dk, d in collection.valid_dates.items():
        if dk >= "20200301":
            all_valid_dates[dk] = d

stringified_dates = ", ".join([f'"{all_valid_dates[x]}"' for x in sorted(all_valid_dates.keys())])

print('''
<!doctype html>
<html>

<head>
	<title>Doubling Times</title>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js"></script>
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
    Lower values are better. Once the number starts actually decreasing over time, the graph
    will show halving times (and, again, lower is better).
  </p>
  <p>
    A final caution: I'm not an epidimiologist, I just think we're not good at intuiting
    about exponential growth rates. Use with caution. If you have questions or other 
    feedback, you can reach me via email at <a href="mailto:covid@kodachi.com">&lt;covid@kodachi.com&gt;</a>.
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
        var ticks = [ 
            -2.000,
            -1.414,
            -1.000,
            -0.707,
            -0.577,
            -0.447,
            -0.378,
            -0.266,
            -0.190,
             0.000,
             0.190,
             0.266,
             0.378,
             0.447,
             0.577,
             0.707,
             1.000,
             1.414,
             2.000
        ];
        var labels = [
            "halve in 6 hours",
            "halve in 12 hours",
            "halve in 1 day",
            "halve in 2 days",
            "halve in 3 days",
            "halve in 5 days",
            "halve in 7 days",
            "halve in 14 days",
            "halve in 28 days",
            "flat",
            "double in 28 days",
            "double in 14 days",
            "double in 7 days",
            "double in 5 days",
            "double in 3 days",
            "double in 2 days",
            "double in 1 day",
            "double in 12 hours",
            "double in 6 hours"
        ];
''')

for place_key in places:
    collection = Collections[place_key]
    place_id = collection.id

    raw_series = {}
    dbl_series = {}
    mult_series = {}

    for datatype in collection.data.keys():
        info = collection.data[datatype][7]
        idict = { x[0]: x for x in info }

        r_series = []
        d_series = []
        m_series = []

        for d in sorted(all_valid_dates.keys()):
            raw_date = all_valid_dates[d]

            if raw_date in idict:
                _, dbl_days, mult, count = idict[raw_date]

                r_series.append(count)
                d_series.append(dbl_days)

                l2mult = math.log(mult) / math.log(2)
                l2sign = -1 if (l2mult < 0) else 1

                y = l2mult * l2sign

                # Square root to even the Y-axis out better.
                y = y ** 0.5

                y *= l2sign

                m_series.append(y)
            else:
                r_series.append(math.nan)
                d_series.append(math.nan)
                m_series.append(math.nan)

        raw_series[datatype] = r_series
        dbl_series[datatype] = d_series
        mult_series[datatype] = m_series

    print("""
        var %s_ticks = [];
        var %s_labels = [];
		var %s_config = {
			type: 'line',
			data: {
                labels: [ %s ],
				datasets: [
    """ % (place_id, place_id, place_id, stringified_dates))

    first = True

    if "deaths" in mult_series:
        if not first:
            print("""
                    ,
            """)

        first = False

        print("""
                    {
                        label: 'Doubling time (deaths)',
                        data: %s,
                        rawData: %s,
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        fill: false,
                        spanGaps: false,
                        yAxisID: "doubling-axis"
                    }
        """ % (json.dumps(mult_series["deaths"]), json.dumps(dbl_series["deaths"])))
        
    if "hospitalizations" in mult_series:
        if not first:
            print("""
                    ,
            """)

        first = False

        print("""
                    {
                        label: 'Doubling time (hospitalizations)',
                        data: %s,
                        rawData: %s,
                        backgroundColor: 'rgb(255, 159, 64)',
                        borderColor: 'rgb(255, 159, 64)',
                        fill: false,
                        spanGaps: false,
                        yAxisID: "doubling-axis"
                    }
        """ % (json.dumps(mult_series["hospitalizations"]), json.dumps(dbl_series["hospitalizations"])))
        
    if "confirmed" in mult_series:
        if not first:
            print("""
                    ,
            """)

        first = False

        print("""
                    {
                        label: 'Doubling time (cases)',
                        data: %s,
                        rawData: %s,
                        backgroundColor: 'rgb(54, 162, 235)',
                        borderColor: 'rgb(54, 162, 235)',
                        fill: false,
                        spanGaps: false,
                        yAxisID: "doubling-axis"
                    }
        """ % (json.dumps(mult_series["confirmed"]), json.dumps(dbl_series["confirmed"])))

    # Come back to deaths for the count.
    if "deaths" in mult_series:
        if not first:
            print("""
                    ,
            """)

        first = False

        print("""
                    {
                        label: 'Total deaths',
                        data: %s,
                        rawData: %s,
                        backgroundColor: 'rgb(240, 240, 240)',
                        borderColor: 'rgb(240, 240, 240)',
                        fill: true,
                        spanGaps: false,
                        yAxisID: "count-axis"
                    }
        """ % (json.dumps(raw_series["deaths"]), json.dumps(raw_series["deaths"])))

				# tooltips: {
				# 	mode: 'index',
				# 	intersect: false,
				# },
				# hover: {
				# 	mode: 'nearest',
				# 	intersect: true
				# },

    print("""
                ]
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: '%s'
				},
                tooltips: {
                    callbacks: {
                        label: function(tooltipItem, data) {
                            var datasetIndex = tooltipItem.datasetIndex;
                            var itemIndex = tooltipItem.index;
                            var dataset = data.datasets[datasetIndex];
                            var dblTime = dataset.rawData[itemIndex];
                            
                            var label = dataset.label || '';

                            if (label == 'Total deaths') {
                                label += ": " + dblTime;
                            }
                            else {
                                if (label) {
                                    label += ': ';
                                }

                                label += Math.round(dblTime * 100) / 100;
                                label += " days";
                            }

                            return label;
                        }
                    }
                },
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Day'
						}
					}],
					yAxes: [
                        {
                            id: "doubling-axis",
                            display: true,
                            position: "left",
                            scaleLabel: {
                                display: false,
                                labelString: 'Value'
                            },
                            ticks: {
                                callback: function(value, index, values) {
                                    return %s_labels[index];
                                }										
                            },
                            afterBuildTicks: function(scale) {
                                %s_ticks = [];
                                %s_labels = [];

                                if (scale.min > 0) {
                                    scale.min = 0;
                                }

                                if (scale.max < 1) {
                                    scale.max = 1;
                                }
                                
                                for (var i = 0; i < ticks.length; i++) {
                                    if ((ticks[i] >= scale.min) && (ticks[i] <= scale.max)) {
                                        %s_ticks.push(ticks[i]);
                                        %s_labels.push(labels[i]);
                                    }
                                }

                                scale.ticks = %s_ticks;
                                return;
                            },
                            beforeUpdate: function(oScale) {
                                return;
                            }
                        },
                        {
                            id: "count-axis",
                            display: true,
                            position: "right",
                            scaleLabel: {
                                display: true,
                                labelString: 'Total'
                            }
                        }
                    ]
				}
			}
		};
    """ % (place_key, place_id, place_id, place_id, place_id, place_id, place_id))

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
