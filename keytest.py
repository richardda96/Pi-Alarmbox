from pad4pi import rpi_gpio
import time

import subprocess

##
##Alarm box based on Raspberry Pi
##
##Keypad script
##
##Daniel Richard 2016
##
##Usage: Runs on start-up, activated by GPIO interrupt,
##collecting data on when to set the alarm (and, importantly,
##whether or not to make coffee), then passes this off to
##'pi-alarm.py', which actually does the timestamp parsing,
##sound making, coffee-generation, etc.
##
##

KEYPAD = [
        [1,2,3],
        [4,5,6],
        [7,8,9],
        ["*",0,"#"]
]

#ROW_PINS = [4,25,8,7] # BCM numbering

##These took an embarrasingly long amount of time to figure out.
ROW_PINS = [7,8,25,24] # BCM numbering
COL_PINS = [10,9,11] # BCM numbering.

#espeakline = 'espeak " ' + str(24 - (invokehours - hours)) + ' hours ' + str(abs(minutes - invokeminutes)) + ' minutes' + ' " ' + "2>/dev/null"


try:
	factory = rpi_gpio.KeypadFactory()
	
	# Try factory.create_4_by_3_keypad
	# and factory.create_4_by_4_keypad for reasonable defaults
	keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
	
	global keypress
	
	#def printKey(key):
	#        print(key)
	#        #return(key)
	#        keypress = key
	#        return(keypress)
	
	global currsetalarm
	currsetalarm = False
	global finishedstamp
	finishedstamp = False
	global modeset
	modeset = False
	global timestamp
	
	def key_pressed(key):
		global currsetalarm
		global finishedstamp
		global modeset
		global timestamp
		
		if (key == "*" and currsetalarm == False):
			print("adding new alarm?")
			espeakline = 'espeak "Setting new alarm" ' + "2>/dev/null"
			subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
			currsetalarm = True
			time.sleep(1)
			espeakline = 'espeak "1 for period mode, 3 for timestamp mode" ' + "2>/dev/null"
			subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
			currsetalarm = True
		elif(key == "*" and currsetalarm == True):
			espeakline = 'espeak "Cancelling new alarm" ' + "2>/dev/null"
			subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
			del timestamp
		elif(key != "*" and finishedstamp == True):
			if (key == "#"):
				espeakline = 'espeak "Not generating liquid ambrosia" ' + "2>/dev/null"
				subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
			else:
				espeakline = 'espeak "May liquid ambrosia descend from the very pinnacle of Mount Olympus and bless thine lips" ' + "2>/dev/null"
				subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
				timestamp = timestamp + " -c True"
				print("now setting the alarm then")
				print(timestamp)
		elif(key != "*" and currsetalarm == True):
			if (modeset == False):
				if(str(key) == '1'):
					modeset = True
					timestamp = " -p "
					espeakline = 'espeak "Period mode set" ' + "2>/dev/null"
					subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
					
				elif(str(key) == '3'):
					modeset = True
					timestamp = " -t "
					espeakline = 'espeak "Timestamp mode set" ' + "2>/dev/null"
					subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
					
				else:
					espeakline = 'espeak "1 for period mode, 3 for timestamp mode" ' + "2>/dev/null"
					subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
			else:
				espeakline = 'espeak " ' + str(key) + ' " 2>/dev/null'
				subprocess.call(espeakline, shell=True)
				timestamp = timestamp + str(key)
				#if(len(timestamp) == 2):
				##
				##Need to add in the mode strings.
				##So we add 4 to everything.
				if((len(timestamp)-4) == 2):
					print("going to do minutes now")
					##I don't think I need to have the system tell me that I'm setting minutes
					##as it might be interrupted by me actually setting the minutes.
					
					#espeakline = 'espeak "Set minutes" ' + "2>/dev/null"
					#subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
					timestamp = timestamp + ":" ##Timestamp format for 'pi-alarm.py'
				elif((len(timestamp)-4) == 5):
					print("finished timestamp")
					espeakline = 'espeak "Should I make coffee?" ' + "2>/dev/null"
					subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
					finishedstamp = True
	def waitforkeypress():
		global keypress
		while True:
			time.sleep(1)
			if(keypress != 0):
				print("got keypress")
				return(keypress)

# printKey will be called each time a keypad button is pressed
	keypad.registerKeyPressHandler(key_pressed)
	while True:
		time.sleep(1)
		keypress = 0
		#keypress = waitforkeypress()
		if (keypress == "*"): ##So the user will have to press '*' to set the alarm.
				keypress = 0
				#while True:
				#	time.sleep(1)
				#	if(keypress != 0):
				#		print("got another keypress!")
				
				firsthour = waitforkeypress()
				secondhour = waitforkeypress()
				print("got first set")
				espeakline = 'espeak " ' + str(firsthour) + str(secondhour)+ ' hours ' + ' " ' + "2>/dev/null"
				
				
except KeyboardInterrupt:
	print("Goodbye")
finally:
	keypad.cleanup()
