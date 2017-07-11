from ldtp import *
from ldtputils import *
import time
import commands
import shutil
import sys

print '##### Test Open and Close Gnote App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('gnote')
		time.sleep(3)
		status = commands.getoutput('xdotool search --name "Gnote"')
		time.sleep(3)
		if status == '':
			print 'Gnote Window does not Exist !!!'
		if status :
			print 'Gnote Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'Gnote' + str(num) + '.' + 'png')
			print 'Screenshot Locate :' + path_save_picture
	#		status = closewindow('*Gnote')
			window_pid = commands.getoutput('xdotool search --name "Gnote" windowkill')
			time.sleep(3)
			if window_pid == '':
				print 'Gnote Window Already Closed !'
			else:
				print 'There is an Error !!!'
			time.sleep(3)
except Exception,e:
	print e
print '##### Test Gnote APP End ! #####'

