
##
##Pi Alarmbox Code
##
##Daniel Richard - 2016
##
##Accessed by the 'keytest.py' script,
##or can be manually accessed via ssh (especially useful
##for making coffee remotely...not sure about that use case actually).
##
##usage:
##sudo python pi-alarm.py -t 00:01 -c True
##sudo python pi-alarm.py -p 00:01 -c True
##
##Note that coffee if the '-c' flag is passed anything,
##so even if you used '-c False' makes cofffee.

#import subprocess

#subprocess.call("

from datetime import datetime

import argparse

import time

import pygame

pygame.init()

pygame.display.set_mode((640, 320))

from pygame import mixer

import subprocess

import random ##for picking songs

##Update June 8th 2016
##
##Adding Coffee Maker support.

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

coffeepin = 7

GPIO.setup(coffeepin, GPIO.OUT)

##The way I've written the program now
##it leaves the coffee maker on, under the assumption
##that the user will terminate the program prior to the music
##ending.
GPIO.output(coffeepin, False) 

#import random.randint
from random import randint
def main():
	print("test?")
	p = argparse.ArgumentParser(description='Sets alarm',
							prog='pi-alarm',
							version='pialarm-0.0.6',
							usage='pi-alarm.py xx:xx')
							
	
	##Defining flags for SeqR.
	
	#bowtie2_options = optparse.OptionGroup(p, "Bowtie2 Options",
	#"Options that affect the calls to bowtie2 within the pipeline.") ##Should I actually spell out all the bowtie2 options, or should I just make
	##a call to 'bowtie2 -help' and output that instead? I think that'd be easier for me.
	#p.add_option("-d", "--debug", action="store_true",
	#			 help="Print debug information")
	'''
	p.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
	p.add_argument('-t', '--time', type=str, help="Provide a wakeup time", action='store_true', required=True)
	p.add_argument('-p', "--period", help="number of hours to sleep",  action='store_true')
	args = p.parse_args()
	print("almost there")
	if 'args.time' in locals():
		print(args.time)
	elif 'args.hours' in locals():
		print(args.hours)
		'''
	
	#p.add_argument("-l", "--list", required=True, help="Provide a .txt file containing list of .sra or .fastq files to use with SeqR", action="store_true")
	p.add_argument("-t", "--time", help="Provide a .txt file containing list of .sra or .fastq files to use with SeqR")
	p.add_argument("-p", "--period", help="Provide a .txt file containing list of .sra or .fastq files to use with SeqR")
	
	##Update June 8th 2016
	##Adding Coffee Maker support.
	
	p.add_argument("-c", "--coffee", help="Derive liquid ambrosia from the heavens")
	
	passedflags = p.parse_args()
	#print("what?")
	
	
	if(passedflags.time):
		print(passedflags.time)
		mode = "time"
	elif (passedflags.period):
		print(passedflags.period)
		mode = "period"
	else:
		print("ERROR, nothing selected")
		exit
	#print(passedflags.time)
	
	currtime = datetime.now().time()
	
	make_coffee = False ##Sad coffee.
	
	if(passedflags.coffee):
		make_coffee = True ##Happy coffee.
	
	print(currtime)
	
	timestring = datetime.strftime(datetime.now(), '%H:%M:%S')
	
	print(timestring)
	
	hours = timestring.split(":")[0]
	hours = int(hours)
	minutes = timestring.split(":")[1]
	minutes = int(minutes)
	seconds = timestring.split(":")[2]
	
	print(hours)
	print(minutes)
	print(seconds)
	
	invokehours = int(hours)
	invokeminutes = int(minutes)
	
	invoketime = timestring ##We keep track of this when doing math. It's in 24 hour time, which is nice.
	
	if (mode == "period"):
		hoursgrab=passedflags.period.split(":")[0]
		mingrab=passedflags.period.split(":")[1]
		hoursgrab = int(hoursgrab)
		mingrab = int(mingrab)
		#print("hourgrab")
		#print(hoursgrab)
		#print("minutesgrab")
		#print(mingrab)
		#print((mingrab + invokeminutes >= 60))
		if ((invokehours + hoursgrab) >= 24 or ((mingrab + invokeminutes >= 60) and ((invokehours + hoursgrab + 1) >= 24))): ##Then we'd be heading into tomorrow.
			print("heading into tomorrow")
			tomorrow = 1
		else:
			tomorrow = 0
	elif (mode == "time"):
		hoursgrab=passedflags.time.split(":")[0]
		mingrab=passedflags.time.split(":")[1]
		hoursgrab = int(hoursgrab)
		mingrab = int(mingrab)
		
		if (invokehours > hoursgrab): ##This means that we're headed into tomorrow.
			print("headed into tomorrow")
			tomorrow = 1
		else:
			tomorrow = 0 ##We're not heading into tomorrow.
	
	##Alright, now the rest.
	
	if (mode == "time"): ##We're going by a wake-up time.
		hoursgrab=passedflags.time.split(":")[0]
		mingrab=passedflags.time.split(":")[1]
		hoursgrab = int(hoursgrab)
		mingrab = int(mingrab)
		while True:
			timestring = datetime.strftime(datetime.now(), '%H:%M:%S')
		
			#print(timestring)
			
			hours = timestring.split(":")[0]
			hours = int(hours)
			minutes = timestring.split(":")[1]
			minutes = int(minutes)
			seconds = timestring.split(":")[2]
			'''
			if (abs(hours - hoursgrab) > 1): ##Wait an hour.
				time.sleep(3600)
			if (abs(minutes - mingrab) > 30):
				time.sleep(1800)
			if (abs(minutes - mingrab) > 10):
				time.sleep(600)
			'''
			#if (hours == hoursgrab and minutes == mingrab):
			#if (hours == hoursgrab and minutes == mingrab or (hours > hoursgrab) or (hours == hoursgrab and minutes > mingrab)):
			##Ran into error where it was 23:00, and I set the alarm for 02:00, so obviously we thought we'd gone over time.
			if (hours == hoursgrab and minutes == mingrab or (tomorrow != 1 and  hours > hoursgrab) or (hours == hoursgrab and minutes > mingrab)):
				##If hours > hoursgrab and we're not headed into tomorrow then we're in trouble.
				
			#if (hours == hoursgrab and minutes == mingrab or (hours > hoursgrab and ((hours - hoursgrab) < 12)) or (hours == hoursgrab and minutes > mingrab)):
			#if (hours == hoursgrab and minutes == mingrab or (hours > hoursgrab and ((hours + hoursgrab) < 24)) or (hours > hoursgrab and  or (hours == hoursgrab and minutes > mingrab)):
			##If 23 > 01:00, and 23-1 !< 12, then we don't set the alarm off. 
			##Ah. If we say 'current hours + hour set > 24' then we'll know we went off to another day.
			##So, even if it was 16:00, and the alarm was set at 18:00, total is 34 hours, so the second conditional isn't met.
			##But what if it was 19:00 and the alarm was set for 18:00? 
				##In the unlikely (?) event that we somehow miss the deadline.
				print("FINISH")
				pygame.init()
				mixer.init()
				print(mixer.get_init())
				#morn1 = mixer.music.load('good-morn-1.wav')
				mixer.music.load('good-morn-1.wav')
				#print(morn1.get_length())
				mixer.music.play(0)
				clock = pygame.time.Clock()
				clock.tick(10)
				while mixer.music.get_busy():
				    pygame.event.poll()
				    clock.tick(7)
				#mixer.music.load('good-morn-1.mp3') ##Should play from local directory, right?
				#mixer.music.play()
				#espeakline = '"sudo espeak ' + str(abs(hours - hoursgrab)) + ' hours ' + str(abs(minutes - mingrab)) + ' minutes' + ' " ' + "2>/dev/null"
				#espeakline = 'espeak " ' + str(abs(hours - hoursgrab)) + ' hours ' + str(abs(minutes - mingrab)) + ' minutes' + ' " '
				#espeakline = 'espeak " ' + str(abs(hours - invokehours)) + ' hours ' + str(abs(minutes - invokeminutes)) + ' minutes' + ' " '
				if (tomorrow == 1):
					##We're heading into tomorrow, however, normally if we set an alarm at 23:00 and it went off at 01:00, it'd say we were asleep for 22 hours.
					espeakline = 'espeak " ' + str(24 - (invokehours - hours)) + ' hours ' + str(abs(minutes - invokeminutes)) + ' minutes' + ' " ' + "2>/dev/null"
				else:
					espeakline = 'espeak " ' + str(abs(hours - invokehours)) + ' hours ' + str(abs(minutes - invokeminutes)) + ' minutes' + ' " ' + "2>/dev/null"
				clock.tick(5)
				print(espeakline)
				subprocess.call(espeakline, shell=True) ##Should say the hours and minutes
				#mixer.music.load('good-morn-1.mp3') ##Should play from local directory, right?
				#mixer.music.play()
				mixer.music.load('good-morn-2.wav')
				#print(morn1.get_length())
				mixer.music.play(0)
				clock = pygame.time.Clock()
				clock.tick(10)
				##Awesome beats.
				while mixer.music.get_busy():
				    pygame.event.poll()
				    clock.tick(10)
				x = 0
				'''while (x < 100): ##So much Nozaki-kun.
					#mixer.music.load('gekkan.wav')
					#mixer.music.load('benkyo.wav')
					mixer.music.load('WING.wav')
					mixer.music.play(0)
					clock = pygame.time.Clock()
					clock.tick(10)
					while mixer.music.get_busy():
					    pygame.event.poll()
					    clock.tick(10)
					x = x + 1
				'''
				#while (x < 10):
				picknum = randint(1, 2)
				
				##Update June 8th 2016
				##Coffee Maker
				if (make_coffee == True):
					GPIO.output(coffeepin, True)
					##If I leave it on and exit the program it stays on.
					##So it'll be shut off when next I start the program.

				if (picknum == 1):
					mixer.music.load('WING.wav')
					mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                     	while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
				if (picknum == 2):
                                        mixer.music.load('typeZERO.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)

				picknum = randint(1, 2)
				
                                if (picknum == 1):
                                        mixer.music.load('WING.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
				if (picknum == 2):
                                        mixer.music.load('typeZERO.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
 				picknum = randint(1, 2)

                                if (picknum == 1):
                                        mixer.music.load('WING.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
                                if (picknum == 2):
                                	mixer.music.load('typeZERO.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
				break

			time.sleep(10) ##10 second waiting. I just wanted it to be less than a lot a lot of looping, which seemed to me to be irresponsible.
	
	elif (mode == "period"): ##Going to go out on a limb here and say that we won't allow alarms over 24 hours away. I know, I know.
		hoursgrab=passedflags.period.split(":")[0]
		mingrab=passedflags.period.split(":")[1]
		hoursgrab = int(hoursgrab)
		mingrab = int(mingrab)
		
		timestring = datetime.strftime(datetime.now(), '%H:%M:%S')
		
		#print(timestring)
		
		hours = timestring.split(":")[0]
		hours = int(hours)
		minutes = timestring.split(":")[1]
		minutes = int(minutes)
		seconds = timestring.split(":")[2]
		
		finalhour = hoursgrab + hours
		finalminutes = mingrab + minutes
		if (finalminutes >= 60):
			finalminutes = finalminutes - 60
			finalhour = finalhour + 1
		if (finalhour >= 24):
			finalhour = finalhour - 24 ##This should solve it, right? 24 hour time really is awesome.
		
		##And just to save me some time.
		
		hoursgrab = finalhour
		mingrab = finalminutes
		
		while True:
			timestring = datetime.strftime(datetime.now(), '%H:%M:%S')
		
			#print(timestring)
			
			hours = timestring.split(":")[0]
			hours = int(hours)
			minutes = timestring.split(":")[1]
			minutes = int(minutes)
			seconds = timestring.split(":")[2]
			'''
			if (abs(hours - hoursgrab) > 1): ##Wait an hour.
				time.sleep(3600)
			if (abs(minutes - mingrab) > 30):
				time.sleep(1800)
			if (abs(minutes - mingrab) > 10):
				time.sleep(600)
			'''
			#if (hours == hoursgrab and minutes == mingrab or (hours > hoursgrab) or (hours == hoursgrab and minutes > mingrab)):
			#if (hours == hoursgrab and minutes == mingrab or (hours > hoursgrab and ((hours - hoursgrab) < 12)) or (hours == hoursgrab and minutes > mingrab)):
			if (hours == hoursgrab and minutes == mingrab or (tomorrow != 1 and  hours > hoursgrab) or (hours == hoursgrab and minutes > mingrab)):
				##In the unlikely (?) event that we somehow miss the deadline.
				print("FINISH")
				pygame.init()
				mixer.init()
				print(mixer.get_init())
				#morn1 = mixer.music.load('good-morn-1.wav')
				mixer.music.load('good-morn-1.wav')
				#print(morn1.get_length())
				mixer.music.play(0)
				clock = pygame.time.Clock()
				clock.tick(10)
				while mixer.music.get_busy():
				    pygame.event.poll()
				    clock.tick(10)
				#mixer.music.load('good-morn-1.mp3') ##Should play from local directory, right?
				#mixer.music.play()
				#espeakline = '"sudo espeak ' + str(abs(hours - hoursgrab)) + ' hours ' + str(abs(minutes - mingrab)) + ' minutes' + ' " ' + "2>/dev/null"
				#espeakline = 'espeak " ' + str(abs(hours - hoursgrab)) + ' hours ' + str(abs(minutes - mingrab)) + ' minutes' + ' " '
				#espeakline = 'espeak " ' + str(abs(hours - invokehours)) + ' hours ' + str(abs(minutes - invokeminutes)) + ' minutes' + ' " '
				#espeakline = 'espeak " ' + str(abs(hours - invokehours)) + ' hours ' + str(abs(minutes - invokeminutes)) + ' minutes' + ' " ' + "2>/dev/null"
				if (tomorrow == 1):
					##We're heading into tomorrow, however, normally if we set an alarm at 23:00 and it went off at 01:00, it'd say we were asleep for 22 hours.
					espeakline = 'espeak " ' + str(24 - (invokehours - hours)) + ' hours ' + str(abs(minutes - invokeminutes)) + ' minutes' + ' " ' + "2>/dev/null"
				else:
					espeakline = 'espeak " ' + str(abs(hours - invokehours)) + ' hours ' + str(abs(minutes - invokeminutes)) + ' minutes' + ' " ' + "2>/dev/null"
				clock.tick(5)
				print(espeakline)
				subprocess.call(espeakline, shell=True) ##Should say the hours and minutes
				#mixer.music.load('good-morn-1.mp3') ##Should play from local directory, right?
				#mixer.music.play()
				mixer.music.load('good-morn-2.wav')
				#print(morn1.get_length())
				mixer.music.play(0)
				clock = pygame.time.Clock()
				clock.tick(10)
				while mixer.music.get_busy():
				    pygame.event.poll()
				    clock.tick(10)
				x = 100
				
				while (x < 100): ##So much Nozaki-kun.
					#mixer.music.load('gekkan.wav')
					#mixer.music.load('benkyo.wav')
					mixer.music.load('WING.wav')
					mixer.music.play(0)
					clock = pygame.time.Clock()
					clock.tick(10)
					while mixer.music.get_busy():
					    pygame.event.poll()
					    clock.tick(10)
					x = x + 1
				##Update June 8th 2016
				##Coffee Maker
				if (make_coffee == True):
					GPIO.output(coffeepin, True)
					##If I leave it on and exit the program it stays on.
					##So it'll be shut off when next I start the program.
					
				picknum = randint(1, 3)

                                if (picknum == 1):
                                        mixer.music.load('WING.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
                                if (picknum == 2):
                                        mixer.music.load('typeZERO.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
				picknum = randint(1, 2)

                                if (picknum == 1):
                                        mixer.music.load('WING.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
                                if (picknum == 2):
                                        mixer.music.load('typeZERO.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
				picknum = randint(1, 2)

                                if (picknum == 1):
                                        mixer.music.load('WING.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
                                if (picknum == 2):
                                        mixer.music.load('typeZERO.wav')
                                        mixer.music.play(0)
                                        clock = pygame.time.Clock()
                                        clock.tick(10)
                                        while mixer.music.get_busy():
                                            pygame.event.poll()
                                            clock.tick(10)
				
				break
			time.sleep(10) ##10 second waiting. I just wanted it to be less than a lot a lot of looping, which seemed to me to be irresponsible.
		
		
		#if (abs(hours-hoursgrab) + hourgrab > 24): ##We're going to the next day.
		#	

main()

