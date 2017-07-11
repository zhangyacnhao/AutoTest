import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *
print '##### Test Open and Close Pluma App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf ' + path_save_picture + '*')
	for num in range(2):
		print '##### The Num.'+str(num)+' Test #####'
		launchapp('pluma')
		time.sleep(3)
		windowpid = commands.getoutput('xdotool search --name "pluma"')
		time.sleep(3)
		if windowpid == '':
			print 'Pluma window does not Exist !!!'
		else:
			print 'Pluma Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'pluma' + str(num) + '.' + 'png')
			print 'Screenshot Locate:' + path_save_picture
`#			commands.getoutput('xdotool search --name "pluma" windowkill')
#			time.sleep(3)
			windowpid = commands.getoutput('xdotool search --name "pluma" windowkill')
			time.sleep(3)
			if windowpid == '':
				print 'Pluma Window Already Closed !'
			else:
				print 'There is a Error !!!'
except Exception,e:
	print e
print '##### Test Pluma App End ! #####'
