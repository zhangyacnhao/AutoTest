import commands
import shutil
import time
import sys
from ldtp import *
from ldtputils import *

print '##### Test Open and Close Firefox App #####'
try:
	path_current = sys.path[0] 
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(10):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('firefox')
		time.sleep(10)
		win_name = getwindowlist()
		time.sleep(2)
		if 'dlgAuthenticationRequired' in win_name:
			click( 'dlgAuthenticationRequired', 'btnOK')
			time.sleep(3)
		status = commands.getoutput('xdotool search --name "Firefox" ')
		time.sleep(3)
		if status == '':
			print 'Firefox window does not Exist !!!'
		if status:
			print 'Firefox window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'firefox' + str(num) + '.' + 'png')
			print 'Screenshot Locate:' + path_save_picture
			sta = commands.getoutput('xdotool search --name "Firefox" windowkill')
			time.sleep(3)
			if sta:
				print 'There is an Error!!!'
			if sta == '':
				 print 'Firefox Window Already Closed!'
		time.sleep(1)
except Exception as err:
	print err
print '##### Test Firefox End ! #####'
