#!/usr/bin/python

import RPi.GPIO as GPIO
import datetime
import time

def waterPlant():

	if GPIO.getmode() != GPIO.BOARD:
		GPIO.setmode(GPIO.BOARD)
	
	GPIO.setup(37, GPIO.OUT)
	
	time.sleep(2)
	for i in range(4):
	    GPIO.output(37, True)
	    print('switching pump: ON')
	    time.sleep(10)
	    GPIO.output(37, False)
	    print('pump: OFF')
	    time.sleep(5)

	GPIO.cleanup()
	print('DONE')
