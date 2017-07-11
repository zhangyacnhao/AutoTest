import time
import commands
import shutil
import sys
from ldtp import *
from ldtputils import *

print '##### Test Open and Close Mate-Calc App #####'
try:
 	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('mate-calc')
		time.sleep(5)
		status = activatewindow('*Calculator')
		if status == 0:
			print 'Mate Calc Window does not Exist !!!'
		if status == 1:
			print 'Mate Calc Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'MateCalc' + str(num) + '.' + 'png')
			print 'Screenshot Locate :' + path_save_picture
#			commands.getoutput('xdotool search --name "culator" windowkill')
#			time.sleep(3)		
			window_pid = commands.getoutput('xdotool search --name "culator" windowkill')
			time.sleep(1)		
			if window_pid == '':
				print 'Mate Calc Window Already Closed !'
			else:
				print 'There is an Error !!!'
		time.sleep(1)
except Exception,e:
	print e
print '##### Test Mate Calc End ! #####'

