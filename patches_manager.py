#
# Copyright 2017 by InfoMus Lab - DIST - University of Genova, http://www.infomus.org
#

"""patches manager"""

import eyesweb_mobile
import sensor_info
import time
from my_callback import my_callback


def init_my_visitor(kernel):
	patch_filename = 'myVisitor.eywx'
	patch = kernel.load_patch(patch_filename)

	return patch


def init_users_simulation_patch(kernel, local_control):
	patch_filename = 'visitors.eywx'
	patch_ids = kernel.get_open_patches()
	patch = None
	for id in patch_ids:
		filename = kernel.get_patch_filename(id)
		if filename.endswith(patch_filename):
			patch = kernel.open_patch(id)
			break

	if patch is None:
		patch = kernel.load_patch(patch_filename)

	patch.set_block_parameter('LocalControl', 'value', eyesweb_mobile.bool_parameter(local_control))
	return patch


def init_infrared_patch(kernel, sensor):
	p = kernel.load_patch('simulator_ir_sensor.eywx')

	p.set_block_parameter('SensorPosition', 'x_parameter', eyesweb_mobile.double_parameter(sensor.x))
	p.set_block_parameter('SensorPosition', 'y_parameter', eyesweb_mobile.double_parameter(sensor.y))
	p.set_block_parameter('SensorPosition', 'z_parameter', eyesweb_mobile.double_parameter(sensor.z))

	cbk = my_callback()
	cbk.block_name = sensor.name
	cbk.sensor_type = 'infrared'
	p.set_callback(cbk)
	p.add_block_output_listener('IRSensor', 'Output')
	return (p, cbk)


def init_patches(kernel, sensor_type, sensors):
	patches = {}
	callbacks = []

	# if sensor_type == 'infrared':
	# 	for sensor in sensors:
	# 		(p, cbk) = init_infrared_patch( kernel, sensor )
	# 		patches.append( p )
	# 		callbacks.append( cbk )

	if sensor_type == 'sma-infrared':
		for sma in sensors:
			p = kernel.load_patch('simulator_sma_ir_sensor.eywx')
			patches[sma.name] = p

			p.set_block_parameter('SensorPosition', 'x_parameter', eyesweb_mobile.double_parameter(sma.x))
			p.set_block_parameter('SensorPosition', 'y_parameter', eyesweb_mobile.double_parameter(sma.y))
			p.set_block_parameter('SensorPosition', 'z_parameter', eyesweb_mobile.double_parameter(sma.z))

			cbk = my_callback()
			callbacks.append(cbk)
			cbk.block_name = sma.name
			cbk.sensor_type = sensor_type
			p.set_callback(cbk)
			p.add_block_output_listener('IRSensor', 'Output')
			p.add_block_output_listener('Accelerometer_X', 'Output')
			p.add_block_output_listener('Accelerometer_Y', 'Output')
			p.add_block_output_listener('Accelerometer_Z', 'Output')

	# elif sensor_type == 'light':
	# 	for sma in sensors:
	# 		p = kernel.load_patch( 'simulator_light_sensor.eywx' )
	# 		patches.append( p )
	#
	# 		p.set_block_parameter( 'SensorPosition', 'x_parameter', eyesweb_mobile.double_parameter(sma.x) )
	# 		p.set_block_parameter( 'SensorPosition', 'y_parameter', eyesweb_mobile.double_parameter(sma.y) )
	# 		p.set_block_parameter( 'SensorPosition', 'z_parameter', eyesweb_mobile.double_parameter(sma.z) )
	#
	# 		cbk=my_callback()
	# 		callbacks.append(cbk)
	# 		cbk.block_name = sma.name
	# 		cbk.sensor_type = sensor_type
	# 		p.set_callback( cbk )
	# 		p.add_block_output_listener( 'LightSensor', 'Output' )

	return (patches, callbacks)


def init_patches_from_structure(kernel, structure):
	callbacks = {}
	patches = {}
	for sensor_type in structure:
		print 'Loading sensors of type ' + sensor_type
		sensors = structure[sensor_type]
		(type_patches, type_callbacks) = init_patches(kernel, sensor_type, sensors)
		patches[sensor_type] = type_patches
		callbacks[sensor_type] = type_callbacks

	return (patches, callbacks)


def start_all_patches(patches):
	for sensor_type in patches:
		print 'Starting ' + sensor_type + ' patches'
		if sensor_type == 'visitor':
			patches[sensor_type].start()
		else:
			type_patches = patches[sensor_type]
			for patch_id in type_patches:
				type_patches[patch_id].start()


def stop_all_patches(patches):
	for sensor_type in patches:
		print 'Stopping ' + sensor_type + ' patches'
		type_patches = patches[sensor_type]
		for patch_id in type_patches:
			type_patches[patch_id].stop()
			type_patches[patch_id].set_callback(None)
	time.sleep(3)
