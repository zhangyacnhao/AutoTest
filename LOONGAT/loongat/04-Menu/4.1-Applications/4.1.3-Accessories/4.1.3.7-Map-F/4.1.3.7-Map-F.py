import commands
import shutil
import time
import sys
from ldtp import *
from ldtputils import *
def closewin():
	keypress('<alt>')
	keypress('<f4>')
	keyrelease('<alt>')
	keyrelease('<f4>')
print '##### Test Open and Close Map App #####'
try:
 	path_current =  sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -f  ' + path_save_picture + '*' )
	for num  in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('/usr/bin/gnome-maps')
		time.sleep(5)		
		image = imagecapture()
		winname = getwindowlist()
		if 'frm0' in winname:
			print 'Map Window Aready Opened.'
			shutil.move(image,path_save_picture + 'Map' + str(num) + '.' + 'png')
			print 'Screenshot Locate: ' + path_save_picture
			closewin()
		else:
			print 'Map Window does not exist!!!'
		winname = getwindowlist()
		if 'frm0' in winname:
			print 'There is an Error!!!'
		else:
			print 'Map Window Already Closed.'
		time.sleep(3)	
except Exception, e:
	print e
print '##### Test Map App End ! #####'

