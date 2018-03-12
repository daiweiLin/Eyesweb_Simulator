#
# Copyright 2017 by InfoMus Lab - DIST - University of Genova, http://www.infomus.org
#

# execfile( 'csv_test.py' )
import csv
from sensor_info import *
from csv_reader import read_csv

t = read_csv('sculpture.csv')
print str(t)


print 'Loading infrared sensors info from "file"'
print 'End of script'

