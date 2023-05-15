#!/usr/bin/env python

#######################################################################
#                            Aufgabe 2	                              #
#######################################################################

from linuxWiimoteLib import *

# initialize wiimote
wiimote = Wiimote()

# Get wiimote adress via hcitool scan
#Insert address and name of device here
#device = ('00:1F:C5:49:AE:86', 'Nintendo RVL-CNT-01')
#device = ('00:1F:C5:45:E0:A5', 'Nintendo RVL-CNT-01')
#device = ('B8:AE:6E:30:0F:0F', 'Nintendo RVL-CNT-01-TR')
device = ('B8:AE:6E:2F:FF:4D', 'Nintendo RVL-CNT-01-TR')


connected = False
speed_max = 11.0
angle_max = 45.0
cur_speed = 0
cur_angle = 0
dividor = 10.0

wiimote_roll = 0
wiimote_pitch = 0

def calculateSpeed(wiimote_roll, speed_max):
    max_roll = 90.0
    if wiimote_roll >= max_roll:
	    speed = speed_max
    elif wiimote_roll <= -max_roll:
	    speed = -speed_max
    else:
        speed = (wiimote_roll / max_roll) * speed_max

    return speed

def calculateWiimoteRoll(wimoteAccelStates):
	x,y,z = wimoteAccelStates
	if x >= 0:
		roll = -z
	elif x < 0:
		roll = z
	print(x,y,z)
	return roll

def setLeds(cur_speed, speed_max):
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
	#print("{},{},{},{}".format(led1,led2,led3,led4))
	wiimote.SetLEDs(led1, led2, led3, led4)

class SteeringHandler(threading.Thread):
	def __init__(self, wiimote):
		threading.Thread.__init__(self)
		self.wiimote = wiimote
		self.wiimote_pitch = 0
		self.last_pitch = 0
		self.start()

	def calculateWiimotePitch(self, wimoteAccelStates):
		x,y,z = wimoteAccelStates
		print(x,y,z)
		return y
	
	def movingAverage(self, pitch_value, w=0.5):
		filtered_value = w * pitch_value + (1 - w) * self.last_pitch
		self.last_pitch = pitch_value
		return filtered_value
	
	def exponentialSmoothing(pitch_value, alpha=1.2, n=2):
		return alpha * pitch_value**n + (1-alpha)*pitch_value

	def run(self):
		while True:
			self.wiimote_pitch = self.calculateWiimotePitch(self.wiimote.getAccelState())
			filtered_val = self.movingAverage(self.wiimote_pitch)
			print("Steering Thread is running {} {}...".format(self.wiimote_pitch, filtered_val))
			time.sleep(0.1)
	
	def stop(self):
		pass

try:
	print("Press any key on wiimote to connect")
	while (not connected):
		connected = wiimote.Connect(device)

	print("succesfully connected")

	wiimote.SetAccelerometerMode()

	wiistate = wiimote.WiimoteState

	steeringHandler = SteeringHandler(wiimote)
	while True:
		# re-calibrate accelerometer
		if (wiistate.ButtonState.Home):
			print('re-calibrating')
			wiimote.calibrateAccelerometer()
			steeringHandler.last_pitch = 0

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
		
		# Reset Button
		if (wiistate.ButtonState.A):
			cur_angle = 0
			cur_speed = 0

		# Motor Active Button
		if (wiistate.ButtonState.B):
			wiimote_roll = calculateWiimoteRoll(wiimote.getAccelState())
			print(wiimote_roll)

			speed = calculateSpeed(wiimote_roll, speed_max)
			print(speed)
			#TODO write to function set_speed

		setLeds(cur_speed, speed_max)
		#print(wiimote.getAccelState())
		#print("{},{}".format(real_speed, cur_angle))
		sleep(0.1)

except KeyboardInterrupt:
	print("Exiting through keyboard event (CTRL + C)")
	exit(wiimote)
	steeringHandler.stop()
