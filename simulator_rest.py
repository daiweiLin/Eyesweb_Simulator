#
# Copyright 2017 by InfoMus Lab - DIST - University of Genova, http://www.infomus.org
#

"""Simulator sketch"""

# execfile( 'simulator.py' )

import eyesweb_mobile
import time
import random
import csv
import sensor_info
from flask import Flask
from flask import jsonify
from flask import request
from flask.json import JSONEncoder
from flask_cors import CORS, cross_origin
from threading import Timer

from csv_reader import read_csv
from my_callback import my_callback
from my_callback import callback_events, callback_events_lock
from patches_manager import *

"""
Main
"""
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

ip_address = '127.0.0.1'
ip_port = 7834
kernel = eyesweb_mobile.kernel( ip_address, ip_port )

sculpture = read_csv('sculpture.csv')
(patches, callbacks) = init_patches_from_structure( kernel, sculpture )
user_simulation_patch = init_users_simulation_patch( kernel, False )
patches['user_simulation_patch'] = [ user_simulation_patch ]

start_all_patches(patches)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, sensor_info.sensor_info):
            return {
			   'name'     : obj.name,
			   'type' : obj.type,
			   'x'     : obj.x,
			   'y'     : obj.y,
			   'z'     : obj.z
            }
        return super(CustomJSONEncoder, self).default(obj)
app.json_encoder = CustomJSONEncoder

sensors_status = {}

@app.route("/version")
def version():
	resp = jsonify( { 'version': '0.1.REST'})
	resp.status_code = 200
	return resp
	
@app.route("/sensors")
def sensors():
	resp = jsonify( sculpture )
	resp.status_code = 200
	return resp
	
@app.route("/status")
def status():
	resp = jsonify( sensors_status )
	resp.status_code = 200
	return resp

@app.route("/visitor_position", methods = ['POST'])
def visitor_position():
	#print request.json
	x = request.json.get( 'x' )
	y = request.json.get( 'y' )
	
	user_simulation_patch.set_block_parameter( 'UserPosition', 'x_parameter', eyesweb_mobile.double_parameter(x) )
	user_simulation_patch.set_block_parameter( 'UserPosition', 'y_parameter', eyesweb_mobile.double_parameter(y) )
	
	return "OK", 200

class Scheduler(object):
	def __init__(self, sleep_time, function):
		self.sleep_time = sleep_time
		self.function = function
		self._t = None

	def start(self):
		if self._t is None:
			self._t = Timer(self.sleep_time, self._run)
			self._t.start()
		else:
			raise Exception("this timer is already running")

	def _run(self):
		self.function()
		self._t = Timer(self.sleep_time, self._run)
		self._t.start()

	def stop(self):
		if self._t is not None:
			self._t.cancel()
			self._t = None
	


def refresh_sensors_status():
	global callback_events, callback_events_lock
	with callback_events_lock:
		local_events = list(callback_events)
		del callback_events[:]
	
	for e in local_events:
		name = e.name
		type = e.type
		value = e.value
		sensors = None
		if type in sensors_status:
			sensors = sensors_status[ type ]
		else:
			sensors = { }
			sensors_status[ type ] = sensors
		sensors[ name ] = value

scheduler = Scheduler(0.05, refresh_sensors_status)
scheduler.start()
app.run()
scheduler.stop()

"""
target_index = 0
print 'Waiting for CTRL+C to be pressed'
try:
	while True:
		time.sleep( 30 )
		
		if 'sma-infrared' in patches:
			sma_patches = patches[ 'sma-infrared' ]
		
			num_sma_patches = len(sma_patches)
			if num_sma_patches > 0:
				sma_index = random.randint(0, num_sma_patches - 1 )
				p = sma_patches[sma_index]
				
				target = random.uniform(-3.14, 3.14 )
				
				print 'Setting target for sma ' + str(sma_index) + ' to ' + str( target )
				p.set_block_parameter( 'sma_control', 'value', eyesweb_mobile.double_parameter(target) )

except KeyboardInterrupt:
	pass
"""	
stop_all_patches(patches)

patches.clear()
kernel = None

print 'End of script'

