from ldtp import *
from ldtputils import *
import time
import commands
import shutil

def maxwindow():
	keypress('<alt>')
	keypress('<f10>')
	keyrelease('<alt>')
	keyrelease('<f10>')

def closewindow():
	keypress('<alt>')
	keypress('<f4>')
	keyrelease('<alt>')
	keyrelease('<f4>')
try:
	path = '/home/loongson/loongat/04-Menu/4.3-System/4.3.1-Preferences/4.3.1.1-Hardware/4.3.1.1.1-Keyboard/screenshot'
	pid = launchapp('mate-keyboard-properties')
	maxwindow()
	time.sleep(2)
	image = imagecapture()
	shutil.move(image,path + '/' + 'keyboard.png')
	if pid == 0:
		print "There is an Error!!!"
	else:
		print "Test Succeed!"
		print "Screenshot is locate: " + path
	closewindow()
except LdtpExecutionError,msg:
	raise


