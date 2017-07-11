import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *
print '##### Test Open and Close Unicode App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf ' + path_save_picture + '*')
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('gucharmap')
		time.sleep(3)
		windowpid = commands.getoutput('xdotool search --name "Map"')
		time.sleep(3)
		if windowpid =='':
			print 'Char Window does not Exist !!!'
		else:
			print 'Char Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'unicode' + str(num) +  '.' + 'png')
			print 'Screenshot Locate:' + path_save_picture
#			commands.getoutput('xdotool search --name "map" windowkill')
#			time.sleep(3)
			windowpid = commands.getoutput('xdotool search --name "Map" windowkill')
			if windowpid == '':
				print 'Char Window Already Closed !'
			else:
				print 'There is an Error !!!'		
		time.sleep(3)	
	
except Exception,e:
	print e
print '##### Test Unicode App End ! #####'
