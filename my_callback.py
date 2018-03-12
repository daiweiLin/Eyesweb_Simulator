#
# Copyright 2017 by InfoMus Lab - DIST - University of Genova, http://www.infomus.org
#

"""My callback"""

import eyesweb_mobile
from event_info import event_info
import threading

callback_events = []
callback_events_lock = threading.Lock()

class my_callback(eyesweb_mobile.patch_callback):
	block_name = 'x'
	sensor_type = 'y'
	def block_output_value_changed( self, block_label, output_id, output_value, datatype_info ):
		e = event_info(self.block_name, self.sensor_type, output_value.value)
		if block_label == 'IRSensor':
		#	print self.block_name + ': block_output_value_changed(' + block_label + ', ' + output_id + ', ' + str( output_value.value ) + ')'


			with callback_events_lock:
				callback_events.append( e )

	def block_parameter_value_changed( self, block_label, parameter_id, parameter_value ):
		print self.block_name + ': block_parameter_value_changed(' + block_label + ', ' + parameter_id + ', ' + str( parameter_value.value ) + ')'
