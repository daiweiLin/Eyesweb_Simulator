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
import Tkinter

from csv_reader import read_csv
from my_callback import my_callback
from my_callback import callback_events, callback_events_lock
from patches_manager import *

	
"""
Main
"""

ip_address = '127.0.0.1'
ip_port = 7834
kernel = eyesweb_mobile.kernel( ip_address, ip_port )

sculpture = read_csv('sculpture.csv')
(patches, callbacks) = init_patches_from_structure( kernel, sculpture )
user_simulation_patch = init_users_simulation_patch( kernel, False )
patches['user_simulation_patch'] = [ user_simulation_patch ]

start_all_patches(patches)

		
root = Tkinter.Tk()


# get screen size
screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (screen_w / 2, screen_h / 2))

root.update()
window_w, window_h = root.winfo_width(), root.winfo_height()

def motion(event):
	x, y = event.x, event.y
	rel_x, rel_y = float(x) / float(window_w-1), float(y) / float(window_h-1)
	user_simulation_patch.set_block_parameter( 'UserPosition', 'x_parameter', eyesweb_mobile.double_parameter(rel_x) )
	user_simulation_patch.set_block_parameter( 'UserPosition', 'y_parameter', eyesweb_mobile.double_parameter(rel_y) )
	#time.sleep(200)
	#print 'mouse: ' + str(rel_x) + ', ' + str(rel_y)

root.bind('<Motion>', motion)

canvas = Tkinter.Canvas(root, width=window_w, height=window_h, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()

def _create_circle(self, x, y, rx, ry, **kwargs):
    return self.create_oval(x-rx, y-ry, x+rx, y+ry, **kwargs)
Tkinter.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
Tkinter.Canvas.create_circle_arc = _create_circle_arc

colors = {
    'infrared': 'gray',
    'sma-infrared': 'green',
    'light': 'pink',
}
highlighted_colors = {
    'infrared': 'blue',
    'sma-infrared': 'yellow',
    'light': 'red',
}

for sensor_type in sculpture:
	sensors = sculpture[ sensor_type ]
	color = colors[ sensor_type ]
	for sensor in sensors:
		x = sensor.x * window_w
		y = sensor.y * window_h
		rx = 0.2 * window_w
		ry = 0.2 * window_h
		canvas.create_circle(x, y, rx, ry, fill=color, outline="#DDD", width=4)

	
"""
canvas.create_circle(0, 0, 50, fill="blue", outline="#DDD", width=4)
canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=45, end=140)
canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305)
canvas.create_circle_arc(100, 120, 45, style="arc", outline="white", width=6, start=270-25, end=270+25)
canvas.create_circle(150, 40, 20, fill="#BBB", outline="")
"""
def refresh_ui():
	global callback_events, callback_events_lock
	with callback_events_lock:
		local_events = list(callback_events)
		del callback_events[:]
	
	for e in local_events:
		name = e.name
		type = e.type
		value = e.value
		if value > 0:
			color = highlighted_colors[ type ]
		else:
			color = colors[ type ]
		sensors = sculpture[ type ]
		for sensor in sensors:
			if sensor.name == name:
				x = sensor.x * window_w
				y = sensor.y * window_h
				rx = 0.2 * window_w
				ry = 0.2 * window_h
				canvas.create_circle(x, y, rx, ry, fill=color, outline="#DDD", width=4)
				
	root.after(100, refresh_ui)
	
root.focus_set() # <-- move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())
root.after(1000,refresh_ui)

root.wm_title("EyesWeb InfoMus-LASG Simulator")
root.mainloop()	

stop_all_patches(patches)

patches.clear()
kernel = None

print 'End of script'

