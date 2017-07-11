import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *

print '##### Test Open and Close ScreenShot App #####'
try:
 	path_current =  sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*')
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('xfce4-screenshooter')
		time.sleep(3)
		winname = getwindowlist()
		if 'dlgScreenshot' in winname :
			print 'Screenshot App Already Opened!'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'Screenshot' + str(num) + '.' + 'png')
			print 'Screenshot Locates: ' + path_save_picture
		click('dlgScreenshot','btnCancel')
		time.sleep(3)
		winname = getwindowlist()
		if  'dlgScreenshot' in  winname :
			print 'There is an Error !!!'
		else:			
			print 'Screenshot App Already Closed!'
except Exception,e :
	print e
print '##### Test Screenshot App End ! #####'

