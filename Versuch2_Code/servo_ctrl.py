#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1.3                              #
#######################################################################

import gpio_class
import time

def write(servo, pulse):
    gpio_class.write(servo, pulse)

class Motor(object):
    PWM_PIN = 1     # GPIO pin 11
    min_pulse = 100 # *10us
    max_pulse = 200
    max_speed = 11.0
    speed_servo = None # TODO Check for speed servo
    def __init__(self, servo=PWM_PIN):
        self.speed_servo = servo
        #assert() # TODO Check that servo != None
        write(servo, 150)

    def set_speed(self, speed):
        if speed > self.max_speed or speed < - self.max_speed:
            print("Speed out of bounds")
            return
            #raise() #TODO Raise value out of bound error

        pulse = int(50.0/self.max_speed * speed + 150)
        print("Setting speed to {} m/s with pulse {} * 10us".format(speed, pulse))
        write(self.speed_servo, pulse)

    def stop(self):
        write(self.speed_servo, 150)

class Steering(object):
    PWM_PIN = 2     # GPIO pin 12
    min_pulse = 100
    max_pulse = 200
    max_angle = 45.0
    steering_servo = None # TODO Check for steering servo
    def __init__(self, servo=None):
        print("Initilizing Servo: {}".format(servo))
        self.steering_servo = servo
        #assert() # TODO Check that servo != None

    def set_angle(self, angle):
        if angle > self.max_angle or angle < -self.max_angle:
            print("Angle out of bounds")
            return
            #raise() #TODO Raise value out of bound error

        pulse = int(40.0/self.max_angle * angle + 155)
        print("Setting angle to {} with pulse {} * 10us".format(angle, pulse))
        write(self.steering_servo, pulse)

    def stop(self):
        write(self.steering_servo, 155)

if __name__ == "__main__":
    steering = Steering(servo=1)
    motor = Motor(servo=2)

    # Check Motor PWM
    motor.set_speed(0)
    time.sleep(1)
    motor.set_speed(11)
    time.sleep(1)
    motor.set_speed(-11)
    time.sleep(1)
    motor.set_speed(15)
    time.sleep(1)
    motor.stop()

    # Check steering PWM
    steering.set_angle(0)
    time.sleep(1)
    steering.set_angle(45)
    time.sleep(1)
    steering.set_angle(-45)
    time.sleep(1)
    steering.set_angle(200)
    time.sleep(1)
    steering.stop()