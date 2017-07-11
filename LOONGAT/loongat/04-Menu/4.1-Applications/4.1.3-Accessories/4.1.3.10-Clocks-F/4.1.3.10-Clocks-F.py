import time
import commands
import shutil
import sys
from ldtp import *
from ldtputils import *
print '##### Test Open and Close Clock App #####'
try:
 	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('gnome-clocks')
		time.sleep(10)
		windowpid = commands.getoutput('xdotool search --name "clocks"')
		if windowpid == '':
			print 'Clock Window does not Exist!!!'
		else:
			print 'Clock Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'Clock' + str(num) + '.' + 'png')
			print 'Screenshot Locate: '+ path_save_picture
#			commands.getoutput('xdotool search --name "clocks" windowkill')
#			time.sleep(3)
			windowpid = commands.getoutput('xdotool search --name "clocks" windowkill')
			if windowpid == '':
				print 'Clock Window Already Closed !'
			else:
				print 'There is an Error !!!'
			time.sleep(3)

except Exception,e:
	print e
print '##### Test Clock App End ! #####'
