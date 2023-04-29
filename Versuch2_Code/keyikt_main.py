#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1                                #
#######################################################################

import pygame
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

width = 400
height = 200

freq = 50  # Sets the frequency of input procession
delta = 1.0 / freq # time per step
acc_max = 2.6  # Max acceleration of the car (per sec.)
dec = 4.5  # Max deceleration of the car (per sec.)
frict_max = -1.0  # max friction
angle_acc = 300  # max change of angle (per sec.)
vmax = 11.0
angle_cur = 0.0
angle_max = 45.0

speed_cur = 0

# Arrays for animation plot
t = [0]
a = [0]
f = [0]
v = [0]

# Start initilization
acc = 0
frict = 0

# start main pygame event processing loop here
pygame.display.init()

# set up the pygame screen enviroment
screen = pygame.display.set_mode((width, height))

# get a clock to generate frequent behaviour
clock = pygame.time.Clock()


# States of the keys
keystates = {'quit': False, 'up': False, 'down': False, 'right': False, 'left': False, 'reset': False}

def calculateAcceleration(velocity, vmax, acc_max):
    µ = vmax/2.0
    sigma = 2.5
    acceleration = acc_max*(1-1.0/2.0*(1+math.erf((abs(velocity)-µ)/(math.sqrt(2*sigma**2)))))
    return acceleration

def calculateFriction(velocity, vmax, frict_max):
    µ = vmax/2.0
    sigma = 4.0
    friction = frict_max/2.0*(1+math.erf((abs(velocity)-µ)/(math.sqrt(2*sigma**2))))
    return friction

def update(frame):
    # Update plots
    t.append(t[-1]+delta)
    a.append(acc)
    f.append(frict)
    v.append(speed_cur)

    plt.clf()
    # Plot the updated data
    plt.plot(a, label='Acceleration')
    plt.plot(f, label='Friction')
    plt.plot(v, label='Velocity')
    plt.legend()

# Animation plot configuration
#fig, ax = plt.subplots()
#ani = FuncAnimation(plt.gcf(), update, interval=100)
#plt.ion()
#plt.show()

running = True
try:
    while running:
        # set clock frequency
        clock.tick(freq);
        
        # save the last speed 4 analysis
        last = speed_cur
     
        # process input events
        for event in pygame.event.get():
        
            # exit on quit
            if event.type == pygame.QUIT:
                running = False

            # check for key down events (press)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keystates['quit'] = True
                elif event.key == pygame.K_UP:
                    keystates['up'] = True
                elif event.key == pygame.K_DOWN:
                    keystates['down'] = True
                elif event.key == pygame.K_RIGHT:
                    keystates['right'] = True
                elif event.key == pygame.K_LEFT:
                    keystates['left'] = True
                elif event.key == pygame.K_r:
                    keystates['reset'] = True

            # check for key up events (release)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    keystates['quit'] = False
                elif event.key == pygame.K_UP:
                    keystates['up'] = False
                elif event.key == pygame.K_DOWN:
                    keystates['down'] = False
                elif event.key == pygame.K_RIGHT:
                    keystates['right'] = False
                elif event.key == pygame.K_LEFT:
                    keystates['left'] = False
                elif event.key == pygame.K_r:
                    keystates['reset'] = False

        # Check what to do depending on key press
        if keystates['quit']:
            running = False
    
        if keystates['reset']:
            speed_cur = 0
            angle_cur = 0

        
        # Calculate acceleration and friction depending on velocity
        acc = calculateAcceleration(speed_cur, vmax, acc_max)
        frict = calculateFriction(speed_cur, vmax, frict_max)

        # Handle Acceleration, breaking depending on key (up, down)
        if keystates['up'] and not keystates['down']:
            if speed_cur < vmax and speed_cur >= 0:     # Accel forward for arrow_up
                speed_cur += acc * delta
            elif speed_cur < 0:                         # Break from backwards travel with arrow_up
                speed_cur += dec * delta
        elif keystates['down'] and not keystates['up']:
            if speed_cur > 0:                           # Break from forward travel with arrow down
                speed_cur -= dec * delta
            elif speed_cur <= 0 and speed_cur > -vmax:  # Accel backwards for arrow down 
                speed_cur -= acc *delta
        else:                                           # Break with friction in either direction
            if speed_cur > 0:
                speed_cur += frict * delta
            elif speed_cur < 0:
                speed_cur -= frict * delta

        # Handle steering angle
        if keystates['right'] and not keystates['left']:
            if angle_cur < angle_max:
                angle_cur += angle_acc * delta
        elif keystates['left'] and not keystates['right']:
            if angle_cur > -angle_max:
                angle_cur -= angle_acc * delta
        else:
            if angle_cur > 0:
                angle_cur -= angle_acc * delta
            elif angle_cur < 0:
                angle_cur += angle_acc * delta


        # Update animation
        #plt.draw()
        #plt.pause(0.001)

        print("({},{} --> {})".format(speed_cur, angle_cur, (speed_cur - last) / delta))
    
except KeyboardInterrupt:
    print ("Exiting through keyboard event (CTRL + C)")
    
# gracefully exit pygame here
pygame.quit()
