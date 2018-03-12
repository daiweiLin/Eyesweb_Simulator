#
# Copyright 2017 by InfoMus Lab - DIST - University of Genova, http://www.infomus.org
#


import csv
from sensor_info import *

def read_csv( filename ):
	topology = {}
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, skipinitialspace=True)
		for row in reader:
			# parse the row
			if len(row) == 5:
				label = row[0]
				type = row[1]
				if( label.startswith( '#')  ):
					continue
				
				if( (type == 'infrared') or (type == 'sma-infrared') or (type == 'light') ):
					sensors = []
					if type in topology:
						sensors = topology[type]
					else:
						topology[type] = sensors
						
					x = float(row[2])
					y = float(row[3])
					z = float(row[4])
					name = label
					s = sensor_info(name,type,x,y,z)
					sensors.append( s )
				else:
					print 'Unexpected type: ' + type + ' at line ' + str( reader.line_num )
					
	return topology


