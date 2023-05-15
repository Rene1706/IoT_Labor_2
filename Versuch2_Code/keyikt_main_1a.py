#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1                                #
#######################################################################

import pygame
import math
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation

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
engine_active = False
speed_cur = 0

# Start initilization
acc = 0
frict = 0

# start main pygame event processing loop here
pygame.display.init()

# set up the pygame screen enviroment
screen = pygame.display.set_mode((width, height))

# get the center position of the pygame window
center_pos = (width / 2, height / 2)

# get a clock to generate frequent behaviour
clock = pygame.time.Clock()


# States of the keys
keystates = {'quit': False, 'up': False, 'down': False, 'reset': False}

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
                elif event.key == pygame.K_r:
                    keystates['reset'] = False

        # Check what to do depending on key press
        if keystates['quit']:
            running = False
    
        if keystates['reset']:
            speed_cur = 0
            angle_cur = 0
            mouse_modus = False

        # Handle Acceleration, breaking depending on key (up, down)
        if keystates['up'] and not keystates['down']:
            if speed_cur < vmax:     # Accel forward for arrow_up
                speed_cur += vmax/11
        elif keystates['down'] and not keystates['up']:
            if speed_cur > -vmax:
                speed_cur -= vmax/11                          # Break from forward travel with arrow down


        print("({},{} --> {})".format(speed_cur, 0, 0))
    
except KeyboardInterrupt:
    print ("Exiting through keyboard event (CTRL + C)")
    
# gracefully exit pygame here
pygame.quit()
