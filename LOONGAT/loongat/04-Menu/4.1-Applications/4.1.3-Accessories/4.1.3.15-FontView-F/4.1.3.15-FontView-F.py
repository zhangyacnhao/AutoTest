import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *
print '##### Test Open and Close Fontview App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf ' + path_save_picture + '*')
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('gnome-font-viewer')
		time.sleep(3)
		windowpid = commands.getoutput('xdotool search --name "Fonts"')
		time.sleep(3)
		if windowpid == '':
			print 'Fontview Window does not Exist !!!'
		else:
			print 'Fontview Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'fontview' + str(num) + '.' + 'png')
			print 'Screenshot Locate:' + path_save_picture
#			commands.getoutput('xdotool search --name "Fonts" windowkill')
#			time.sleep(3)
			windowpid = commands.getoutput('xdotool search --name "Fonts" windowkill')
			time.sleep(3)
			if windowpid == '':
				print 'Fontview Window Already Closed !'
			else:
				print 'There is an Error !!!'
			time.sleep(1)
except Exception, e:
	print e
print '##### Test Fontview App End ! #####'

