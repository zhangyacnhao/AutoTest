#!/usr/bin/env python
from ldtp import *
from ldtputils import *
import commands
import time
import shutil
import os
import sys


print '##### Testing WPS-Calc Base Functions #####'

#Define Function for Maxsize WPS Window
def max_win():
	keypress('<alt>')
	keypress('<f10>')
	keyrelease('<alt>')
	keyrelease('<f10>')

#Define Funciotn for Close WPS Window
def close_win():
	keypress('<alt>')
	keypress('<f4>')
	keyrelease('<alt>')
	keyrelease('<f4>')

try:
#Define Saving Imagecapture Path
	path_current = sys.path[0] 
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	os.chdir(path_current)
# Loop Testing	
	for num in range(3):
		print '##### The Num.' + str(num) + ' Test #####'
		(status,output) = commands.getstatusoutput('xdg-open document.et')
		time.sleep(5)
		if status == 0:		
			commands.getoutput('xdotool search --name "document" windowactivate')
			time.sleep(5)
			max_win()
			time.sleep(3)
			(sta,output) = commands.getstatusoutput('cnee -rep -f wpscalc.xns')
			time.sleep(1)		
			if sta != 0:
				print 'There is an Error !!!'
			if sta == 0:
				print 'Testing Finished !'
				image = imagecapture()	
				shutil.move(image, path_save_picture + 'wps' + str(num) + '.png')
				print 'Screenshot Locate: ' + path_save_picture
				commands.getoutput('xdotool search --name "document" windowactivate')				
				close_win()
				time.sleep(3)
		else:
			print 'WPS Document does not Exist !!!'
			break
		
except Exception , e :
	print e
print '##### Test WPS-Calc Base Functions End ! #####'

