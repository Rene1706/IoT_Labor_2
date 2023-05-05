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

def setLeds(wiimote, cur_speed, speed_max):
	limits = speed_max/4.0
	led1 = False
	led2 = False
	led3 = False
	led4 = False
	if cur_speed == 0:
		pass
	elif cur_speed > 0:
		led1 = True
	if cur_speed > limits:
		led2 = True
	if cur_speed > limits*2:
		led3 = True
	if cur_speed > limits*3:
		led4 = True
	print("{},{},{},{}".format(led1,led2,led3,led4))
	wiimote.SetLEDs(led1, led2, led3, led4)

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
			if cur_speed < speed_max:
				cur_speed += speed_max/dividor
		if (wiistate.ButtonState.Left):
			if cur_speed > 0:
				cur_speed -= speed_max/dividor

		# Drive forward/backwards depending on key 1/2
		real_speed = 0	# +- current speed dependent on direction
		if (wiistate.ButtonState.Two):
			real_speed = cur_speed
		if (wiistate.ButtonState.One):
			real_speed = -cur_speed
		
		setLeds(wiimote, cur_speed, speed_max)

		print("{},{}".format(real_speed, cur_angle))
		sleep(0.1)

except KeyboardInterrupt:
	print("Exiting through keyboard event (CTRL + C)")
	exit(wiimote)
