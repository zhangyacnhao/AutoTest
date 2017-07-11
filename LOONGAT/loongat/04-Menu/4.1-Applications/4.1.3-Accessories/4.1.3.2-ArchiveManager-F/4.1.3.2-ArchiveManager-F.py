from ldtp import *
from ldtputils import *
import commands
import shutil
import time
import sys

print '##### Test Open and Close ArchiveManager App #####'
try:
	path_current = sys.path[0]
 	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -f  ' + path_save_picture + '*' )
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('engrampa')
		time.sleep(3)
		activatewindow('*ArchiveManager')
		windowpid = commands.getoutput('xdotool search --name "Archive Manager" ')
		time.sleep(3)
		if windowpid == '' :
			print 'Archive Manager Window does not Exist !!!'
		else:
			print 'Archive Manager Window Already Opened !'
			image = imagecapture()
			shutil.move(image ,path_save_picture + 'archivemanager' + str(num) + '.' + 'png')	
			print 'Screenshot Locate:' + path_save_picture
#			commands.getoutput('xdotool search --name "Archive Manager" windowkill')
#			time.sleep(3)
			window_pid = commands.getoutput('xdotool search --name "Archive Manager" windowkill')
			time.sleep(3)			
			if window_pid == '':
				print 'Archive Manager Window Already Closed !'
			else:
				print 'There is an Error !!!'
			time.sleep(1)
except Exception,e:
	print e
print '##### Test ArchiveManager App End ! #####'

