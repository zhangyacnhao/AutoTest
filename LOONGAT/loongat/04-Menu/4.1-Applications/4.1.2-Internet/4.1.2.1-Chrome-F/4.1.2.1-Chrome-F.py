import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *


print '##### Test Open and Close Chrome App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(10):
		print '##### The Num.' + str(num) +' Test #####'
		launchapp('/usr/bin/chrome39.sh')
		print 'Please Wait for 20 Seconds ...'
		time.sleep(30)
		commands.getoutput('xdotool search --name "New Tab" windowactivate')		
		window_pid = commands.getoutput('xdotool search --name "New Tab" ')
		time.sleep(3)
		if window_pid == '':
			print 'Chrome Window does not Exist!!!'
		else:
			print 'Chrome Window Already Opened!'
			image = imagecapture()
			shutil.move(image, path_save_picture  + 'chrome' + str(num) + '.' + 'png')
			print 'Screenshot Locate:' + path_save_picture 
			commands.getoutput('xdotool search --name "New Tab" windowkill ')
			time.sleep(3)			
			window_pid = commands.getoutput('xdotool search --name "New Tab" ')
			time.sleep(3)
			if window_pid == '':
				print 'Chrome Window Already Closed!'
			else:
				print 'There is an Error !!!'
		time.sleep(3)
except Exception,e:
	print e
print '##### Test Chrome End ! #####'

