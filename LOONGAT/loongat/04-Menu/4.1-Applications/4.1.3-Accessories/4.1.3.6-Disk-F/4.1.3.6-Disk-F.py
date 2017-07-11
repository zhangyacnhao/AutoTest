import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *
print '##### Test Open and Close Disk App #####'
try:
 	path_current =  sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -f  ' + path_save_picture + '*')
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('gnome-disks')
		time.sleep(3)
		windowpid = commands.getoutput('xdotool search --name "Disk"')
		if windowpid == '':
			print 'Disk window does not exist!!!'
		else:		
			print 'Disk Window Already Opened.'
			image = imagecapture()			
			shutil.move(image,path_save_picture + 'Disk' + str(num) + '.' + 'png')
			print 'Screenshot Locate: ' + path_save_picture	
			windowpid = commands.getoutput('xdotool search --name "Disk" windowkill')
			time.sleep(3)			
			if windowpid == '':
				print 'Disk window Already Closed !'
			else:			
				print 'There is an Error !!!'
except Exception as err:
	print err
print '##### Test Disk App End ! #####'

