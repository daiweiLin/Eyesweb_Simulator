"""
Read sensor from csv
"""

class sensor_info(object):
	def __init__(self,name,type,x,y,z):
		self.name = name
		self.type = type
		self.x = x
		self.y = y
		self.z = z