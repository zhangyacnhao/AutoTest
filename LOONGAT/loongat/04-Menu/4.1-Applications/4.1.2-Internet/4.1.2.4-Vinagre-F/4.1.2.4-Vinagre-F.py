from ldtp import *
from ldtputils import *
import time
import commands
import shutil
import sys

print '##### Test Open and Close Vinagre App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(10):
		print '##### This is the Num.' + str(num) + ' Test #####'	
		launchapp('vinagre')
		time.sleep(5)
		activatewindow('*RemoteDesktopViewer')
		window_pid=commands.getoutput('xdotool search --name "Remote"')
		time.sleep(3)
		if window_pid == '':
			print 'Remote Desktop Window does not Exist'
		else:
			print 'Remote Desktop Window Already Opened!'
			image = imagecapture()
			shutil.move(image,path_save_picture  + 'Vinagre' + str(num) + '.' + 'png')
			print 'Screenshot Locate: '+ path_save_picture 
			window_pid=commands.getoutput('xdotool search --name "Remote" windowkill')
			time.sleep(3)			
			if window_pid == '':
				print 'Remote Desktop Window Already Closed!'	
			else:
				print 'There is an Error !!!'		
		time.sleep(3)
except Exception,e:
	print e
print '##### Test Vinagre App End ! #####'




