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

from csv_reader import read_csv
from my_callback import my_callback
from patches_manager import *
from movement import *

from patchflag import *

"""
Main
"""

ip_address = '127.0.0.1'
ip_port = 7834
kernel = eyesweb_mobile.kernel(ip_address, ip_port)

sculpture = read_csv('sculpture.csv')
(patches, callbacks) = init_patches_from_structure(kernel, sculpture)
# user_simulation_patch = init_users_simulation_patch( kernel, False )
visitor_patch = init_my_visitor(kernel)
patches['visitor'] = visitor_patch

start_all_patches(patches)

target_index = 0
position = 1
t = 0
traj = [0, 0.5, 1, 0.5]
prev_position = 0

print 'Waiting for CTRL+C to be pressed'
# check patches exists before using them
if 'sma-infrared' in patches:
	sma_patches = patches['sma-infrared']
	num_sma_patches = len(sma_patches)
	print 'sma patches : ' + str(num_sma_patches)
	patch_flags = {}
	for patch_id in sma_patches:
		patch_flags[patch_id] = patchflag('sma-infrared')
if 'visitor' in patches:
	visitor = patches['visitor']

try:
	while True:
		time.sleep(0.1)
		t = t + 1

		if num_sma_patches > 0:
			# sma_index = random.randint(0, num_sma_patches - 1 )
			sma_patch_index = 0
			p = sma_patches['sma-ir1']
			prev_position = movement(t, traj, p, prev_position)
			time.sleep(0.1)
			for sma in sma_patches:
				ir_out = sma_patches[sma].get_block_output('IRSensor_1', 'ir')
				print str(sma) + ':' + str(ir_out.value)
			print '*************'
			sma_index = 1
			target = random.uniform(-3.14, 3.14)
			p.set_block_parameter('sma_control_' + str(sma_index), 'value', eyesweb_mobile.double_parameter(target))

		# target = random.uniform(-3.14, 3.14 )
		# position = 1-position

		# print 'Setting target for sma ' + str(sma_index) + ' to ' + str( target )
		# p.set_block_parameter( 'sma_control', 'value', eyesweb_mobile.double_parameter(target) )
except KeyboardInterrupt:
	pass

stop_all_patches(patches)

patches.clear()
kernel = None

print 'End of script'
