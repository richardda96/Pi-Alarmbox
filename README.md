# Pi-Alarmbox
##
##Daniel Richard - 2016

Some scripts to work with an alarm clock based on a Raspberry Pi, and housed inside
of an analytical scale. Initially written to work with just ssh-ing in and setting the alarm
with 'pi-alarm.py'.

Additional functionality was then added to allow for automated coffee production using GPIO, a relay set and a hacked power bar.

In order to allow for the Alarmbox to run without the need for ssh-ing in (which was becoming a pain
when trying to turn off the alarm after ssh-ing into the Pi whilst half-asleep) I added a keypad
using the 'pad4pi' (https://github.com/brettmclean/pad4pi) library, heavily relying on 'espeak' in order to avoid having to add an LED numeric display (and all the GPIO pins or a mux board that I would need to get).

Any questions can be directed to daniel@danielrichard.net
