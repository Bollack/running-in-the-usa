import csv
import json
import os

files = os.listdir('../output')

fieldnames = ["Blank", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Total"]
state = "State"
city = "City"
county = "County"
race_event = "Race Event"

for file in files:
    csvfile = open('../output/csv/' + file, 'r')
    jsonfile = open('../output/json/' + file.replace('.csv', '.json'), 'w')

    if file.startswith('All_'):
        del fieldnames[0]
        fieldnames.insert(0, state)
    elif file.startswith('City_'):
        del fieldnames[0]
        fieldnames.insert(0, city)
    elif file.startswith('County_'):
        del fieldnames[0]
        fieldnames.insert(0, county)
    elif file.startswith('RaceEvent_'):
        del fieldnames[0]
        fieldnames.insert(0, race_event)

    reader = csv.DictReader(csvfile, fieldnames)
    out = json.dumps([row for row in reader])
    jsonfile.write(out)
