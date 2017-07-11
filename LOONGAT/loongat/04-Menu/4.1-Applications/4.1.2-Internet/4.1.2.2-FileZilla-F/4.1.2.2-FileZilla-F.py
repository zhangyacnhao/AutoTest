from ldtp import *
from ldtputils import *
import time
import commands
import shutil
import sys

print '##### Test Open and Close FileZilla App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(10):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('filezilla')
		time.sleep(5)
		#status = activatewindow('*FileZilla')
		window_pid = commands.getoutput('xdotool search --name "FileZilla"')
		time.sleep(5)
		if window_pid == '':
			print 'FileZilla Window does not Exist'
		if window_pid:
			print 'FileZilla Window Already Opened!'			
			image = imagecapture()
			path = commands.getoutput('pwd')
			shutil.move(image,path_save_picture + 'FileZilla' + str(num) + '.' + 'png')
			print 'Screenshot Locate: ' + path_save_picture
			time.sleep(3)
			window_id = commands.getoutput('xdotool search --name "FileZilla" windowkill')
			time.sleep(3)			
			if window_id == '':
				print 'FileZilla Window Already Closed!'
			else:
				print 'There is an Error !!!'	
		time.sleep(3)
except Exception,e:
	print e
print '###### Test FileZilla App End ! #####'





