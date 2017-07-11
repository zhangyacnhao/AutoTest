import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *
print '##### Test Open and Close Weather App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf ' + path_save_picture + '*')
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('/usr/share/org.gnome.Weather/org.gnome.Weather.Application')
		time.sleep(6)
		windowpid = commands.getoutput('xdotool search --name "Location"')
		time.sleep(3)
		if windowpid == '':
			print 'Weather Window does not Exist !!!'
		else:
			print 'Weather Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'weather' + str(num) + '.' + 'png')
			print 'Screenshot Locate:' + path_save_picture
#			commands.getoutput('xdotool search --name "Location" windowkill')
#			time.sleep(5)
			windowpid = commands.getoutput('xdotool search --name "Location" windowkill')
			time.sleep(5)
			if windowpid =='':
				print 'Weather Window Already Closed !'
			else:
				print 'There is an Error !!!'
			commands.getoutput('sync')
except Exception,e:
	print e
print '##### Test Weather App End !#####'

