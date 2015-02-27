"""QWLA join similarity tool.

Usage:
    analyse2 [-d DATABASE]
    analyse2  (-h | --help)
    analyse2  --version

Options:
    -d [DATABASE]  The database to read from or write into
    -h --help      Show this screen.
    --version      Show version.

"For a moment, nothing happened. Then, after a second or so,
nothing continued to happen."
"""

from docopt import docopt
import matplotlib.pyplot as plt
import math
import numpy as np
import dataset
import sqlalchemy as sa
from datetime import datetime
from collections import Counter

def analyse2(database):
	db = dataset.connect(database);

	tables = list(db.query('SELECT distinct("table") FROM sqlshare_tables'))

	#tables = tables[-1200:] # smaller subset for testing.
	lifetime = {}
	ecount = 0;
	for i,t in enumerate(tables):
		try:
			timestamps = list(db.query(
				'select to_timestamp(time_start, \'MM/DD/YYYY HH12:MI:SS am\') as start from sqlshare_logs where id in (select query_id from sqlshare_tables where "table" = $$'+t['table']+'$$) order by start desc'
				))
			if len(timestamps) <= 1:
				lifetime[i] = 0
			else:
				start = datetime.strptime(timestamps[-1]['time_start'],"%m/%d/%Y %I:%M:%S %p")
				end = datetime.strptime(timestamps[0]['time_start'],"%m/%d/%Y %I:%M:%S %p")
				lifetime[i] = (end - start).days
		except:
			ecount += 1
			pass
	print 'done with ' + str(ecount) + ' errors'

	def write_to_csv(dict_obj, col1, col2, filename, to_reverse=True):
		f = open(filename, 'w')
		f.write("%s,%s\n"%(col1,col2))
		for key in sorted(dict_obj, reverse=to_reverse):
			f.write("%d,%d\n"%(key, dict_obj[key]))
		f.close()

	write_to_csv(lifetime, 'query_id', 'lifetime', '../results/sqlshare/query_lifetime.csv')

def main():
	arguments = docopt(__doc__, version='SDSS Tools 0.0.1')

	db = (('-d' in arguments and arguments['-d']) or 'sqlite:///test.sqlite')
	analyse2(db)

if __name__ == '__main__':
	main()