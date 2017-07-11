import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *

print '##### Test Open and Close Password App #####'
try:
 	path_current =  sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*' )
	for num in range(2):
		print '##### The Num.' + str(num) + ' Test #####'
		launchapp('seahorse')
		time.sleep(5)
		windowpid = commands.getoutput('xdotool search --name "Keys"')
		time.sleep(3)
		if windowpid == '' :
			print 'Password Window does not Exist !!!'
		else:
			print 'Password Window Already Opened !'		
			image = imagecapture()				
			shutil.move (image , path_save_picture + 'password' + str(num) + '.' + 'png')
			print 'Screenshot Locate: ' + path_save_picture
	#		commands.getoutput('xdotool search --name "Passwords" windowkill')
	#		time.sleep(3)
			windowpid = commands.getoutput('xdotool search --name "Passwords" windowkill')
			time.sleep(3)	
			if windowpid == '':
				print 'Seahorse Window Already Closed!'
			else:
				print 'There is an Error !!!'
								
except Exception,e:
	print e
print '##### Test Password App End ! #####'

