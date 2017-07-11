import commands
import time
import shutil
import sys
from ldtp import *
from ldtputils import *
print '##### Test Open and Close SearchFile App #####'
try:
	path_current = sys.path[0]
	path_save_picture = path_current + '/' + 'screenshot/'
	commands.getoutput('rm -rf  ' + path_save_picture + '*')
	for num in range(2):
		print '#### The Num.' + str(num) + ' Test #####'
		launchapp('mate-search-tool')
		time.sleep(5)
		windowpid = commands.getoutput('xdotool search --name "Search"')
		time.sleep(3)		
		if windowpid == '':
			print 'SearchFile Window does not Exist !!!'
		else:
			print 'SearchFile Window Already Opened !'
			image = imagecapture()
			shutil.move(image,path_save_picture + 'searchfile' + str(num) + '.' + 'png')
			print 'Screenshot Locate:' + path_save_picture
#			commands.getoutput('xdotool search --name "Search" windowkill')
#			time.sleep(3)
			windowpid = commands.getoutput('xdotool search --name "Search" windowkill')
			time.sleep(3)
			if windowpid == '':
				print 'SearchFile Window Already Closed !'
			else :
				print 'There is an Error !!!'
except Exception,e:
	print e
print '##### Test SearchFile App End ! #####'

