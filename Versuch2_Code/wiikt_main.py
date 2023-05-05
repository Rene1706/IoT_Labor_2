#!/usr/bin/env python

#######################################################################
#                            Aufgabe 2	                              #
#######################################################################

from linuxWiimoteLib import *

# initialize wiimote
wiimote = Wiimote()

#Insert address and name of device here
#device = ('00:1F:C5:49:AE:86', 'Nintendo RVL-CNT-01')
device = ('00:1F:C5:45:E0:A5', 'Nintendo RVL-CNT-01')

connected = False
speed_max = 11.0
angle_max = 45.0
cur_speed = 0
cur_angle = 0
dividor = 10.0

try:
	print("Press any key on wiimote to connect")
	while (not connected):
		connected = wiimote.Connect(device)

	print("succesfully connected")

	wiimote.SetAccelerometerMode()

	wiistate = wiimote.WiimoteState
	while True:
		# re-calibrate accelerometer
		if (wiistate.ButtonState.Home):
			print('re-calibrating')
			wiimote.calibrateAccelerometer()


		# Handle Speed angle with keys
		if (wiistate.ButtonState.Up):
			if cur_angle > -angle_max:
				cur_angle -= angle_max/dividor
		if (wiistate.ButtonState.Down):
			if cur_angle < angle_max:
				cur_angle += angle_max/dividor
		if (wiistate.ButtonState.Right):
			if cur_speed <= speed_max:
				cur_speed += speed_max/dividor
		if (wiistate.ButtonState.Left):
			if cur_speed >= -speed_max:
				cur_speed -= speed_max/dividor

		print("{},{}".format(cur_speed, cur_angle))
		sleep(0.1)

except KeyboardInterrupt:
	print("Exiting through keyboard event (CTRL + C)")
	exit(wiimote)
