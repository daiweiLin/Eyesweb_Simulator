"""
Read sensor from csv
"""

class event_info(object):
	def __init__(self,name,type,value):
		self.name = name
		self.type = type
		self.value = value