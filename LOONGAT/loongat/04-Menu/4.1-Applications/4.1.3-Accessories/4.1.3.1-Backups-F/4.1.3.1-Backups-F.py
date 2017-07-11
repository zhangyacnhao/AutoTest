import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *
print '##### Test Open and Close Backups App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -f  ' + path_save_picture  + '*' ) 	
	for num in range(2):
		print '##### The Num.'+ str(num)+ ' Test #####'
		launchapp('/usr/bin/deja-dup-preferences')
		time.sleep(5)
		window_name = commands.getoutput('xdotool search --name "Backups"')
		if window_name == '':
			print 'Backups Window does not Exist !!!'
		else:
			print 'Backups Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'Backups' + str(num) + '.' + 'png')
			print 'Screeenshot Locate: ' + path_save_picture
			window_pid = commands.getoutput('xdotool search --name "Backups" windowkill')
			time.sleep(3)	
			if window_pid == '':
				print 'Backups Window Already Closed !'
			else:
				print 'There is an Error !!!'
except Exception as err:
	print err 
print '##### Test Backup App End ! #####'
