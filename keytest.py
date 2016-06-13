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

from pad4pi import rpi_gpio
import time

import subprocess
import os
import signal

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
#def pialarmbox():

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
	global finished
	finished = False
	#global FNULL
	#FNULL = open(os.devnull, 'w')
	
	global popen_list
	popen_list = list()
	global popen_counter
	popen_counter = 0
	
	#os.environ["finished"] = "0"
	
	def key_pressed(key):
		global currsetalarm
		global finishedstamp
		global modeset
		global timestamp
		global finished
		
		global popen_list
		global popen_counter
		
		if(finished == True):
			print("hold on")
			espeakline = 'espeak "Additional Alarm Requested" ' + "2>/dev/null"
			subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
			#print(1/0)
			currsetalarm = False
			finishedstamp =""
			modeset = False
			finishedstamp = False
			finished = False
		elif (key == "*" and currsetalarm == False):
			print("adding new alarm?")
			espeakline = 'espeak "Setting new alarm" ' + "2>/dev/null"
			subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
			currsetalarm = True
			#time.sleep(1)
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
				print("now setting the alarm then, no coffee tho")
				print(timestamp)
				alarmline = 'sudo python pi-alarm.py' + timestamp
				#subprocess.call(alarmline, shell=True)
				command_split = timestamp.split('-')
				command_split = command_split[1:]
				counter = 0
				while(counter < len(command_split)):
					command_split[counter] = "-" + str(command_split[counter])
					counter = counter + 1
				#subprocess.call(["sudo", "python", "pi-alarm.py", command_split[0]], shell=False, stdout=FNULL, stderr=FNULL)
				
				finished = True
				#subprocess.call(["sudo", "python", "pi-alarm.py", command_split[0]], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
				#popen_list[popen_counter] = subprocess.Popen(["sudo", "python", "pi-alarm.py", command_split[0]], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
				popen_list.append(subprocess.Popen(["sudo", "python", "pi-alarm.py", command_split[0]], shell=False, stdout=subprocess.PIPE, preexec_fn=os.setsid, close_fds = True))
				popen_counter = popen_counter + 1 ##Next process.
				print("now going to loop")
				#pialarmbox()
				#return()
				#finished = True
				currsetalarm = False
				finishedstamp =""
				modeset = False
				finishedstamp = False
				#os.environ["finished"] = "1"
				#print(make_error) ##Oh no! Error!
				#test = 1/0 ##Really big?
			else:
				#espeakline = 'espeak "May liquid ambrosia descend from the very pinnacle of Mount Olympus and bless thine lips" ' + "2>/dev/null"
				espeakline = 'espeak "May liquid ambrosia descend from the very pinnacle of Mount Olympus" ' + "2>/dev/null"
				subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
				timestamp = timestamp + " -c True"
				print("now setting the alarm then")
				print(timestamp)
				alarmline = 'sudo python pi-alarm.py' + timestamp
				#subprocess.call(alarmline, shell=True)
				command_split = timestamp.split('-')
				command_split = command_split[1:] ##Skips first space.
				counter = 0 
				print(command_split)
				while(counter < len(command_split)):
					command_split[counter] = "-" + str(command_split[counter])
					counter = counter + 1
				print(command_split)
				#subprocess.call(["sudo", "python", "pi-alarm.py", command_split[0], command_split[1]], shell=False, stdout=FNULL, stderr=FNULL)
				finished = True
				#subprocess.call(["sudo", "python", "pi-alarm.py", command_split[0], command_split[1]], shell=False, stdin=None, stdout=None, close_fds=True)
				#popen_list[popen_counter] = subprocess.Popen(["sudo", "python", "pi-alarm.py", command_split[0], command_split[1]], shell=False, stdin=None, stdout=None, close_fds=True)
				popen_list.append(subprocess.Popen(["sudo", "python", "pi-alarm.py", command_split[0], command_split[1]], shell=False, stdout=subprocess.PIPE, preexec_fn=os.setsid, close_fds=True))
				popen_counter = popen_counter + 1 ##Next process.
				print("now going to loop")
				#print(make_error) ##Oh noes! Error!
				#pialarmbox()
				#return()
				#finished = True
				currsetalarm = False
				finishedstamp =""
				modeset = False
				finishedstamp = False
				finished = False
				#os.environ["finished"] = "1"
				
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
				if((len(timestamp)-4+1) > 5):
					print("error thing")
				else:
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

	
	# printKey will be called each time a keypad button is pressed
	keypad.registerKeyPressHandler(key_pressed)
	while True:
		time.sleep(1)
		#if(os.environ["finished"] == "1"):
		#	print("looping")
			#espeakline = 'espeak "Additional Alarm Requested" ' + "2>/dev/null"
			#subprocess.call(espeakline, shell=True) ##Though I don't think I'm supposed to be using shell=True for security reasons.
			#return
		#keypress = waitforkeypress()
except KeyboardInterrupt:
	print("Closing all alarms")
	for process in popen_list:
		print("killing this thread")
		print(process.pid)
	#	process.terminate() ##Hopefully kills all the alarms.
		os.killpg(os.getpgid(process.pid), signal.SIGTERM)
		##That doesn't work.
		kill_line = "kill -9 " + str(process.pid)
		subprocess.call(kill_line, shell=True)
		print("should have been killed?")
finally:
	keypad.cleanup()
