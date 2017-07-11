import commands
import shutil
import time
import sys
from ldtp import *
from ldtputils import *

print '##### Test Open and Close DVDRecorder App #####'
try:
 	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(2):
		print '##### The No.' + str(num) + ' Test #####'
		launchapp('xfburn')
		time.sleep(5)
		win = getwindowlist()
		if win.index('dlgWarning'):
			click('dlgWarning','btnClose')	
		if waittillguiexist == 0:
			print 'Xfburn Window does not Exist !!!'
		else:
			print 'Xfburn Window Already Opened !'
			image = imagecapture()
			shutil.move(image, path_save_picture + 'Xfburn' + str(num) + '.' + 'png')
			print 'Screenshot Locate: ' + path_save_picture
			closewindow('Xfburn')
			time.sleep(3)
			win = getwindowlist()
			time.sleep(1)		
			if 'Xfburn' in win:
				print'There is an Error !!!'
			else: 
				print 'Xfburn Window Already Closed !'
except Exception ,e:
	print e
print '##### Test DVDRecorder App End ! #####'

