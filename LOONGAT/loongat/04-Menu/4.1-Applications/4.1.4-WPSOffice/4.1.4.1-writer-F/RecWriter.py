from ldtp import *
from ldtputils import *
import commands
import time

def max_window():
	keypress('<alt>')
	keypress('<f10>')
	keyrelease('<alt>')
	keyrelease('<f10>')

commands.getstatusoutput('xdg-open document.wps')
time.sleep(6)
max_window()
# Run Cnee Record Command
(status,output) = commands.getstatusoutput('cnee -rec --all-events --keyboard --mouse -o wpswriter.xns -sk End -t 3 ')

# Jugement
if status != 0 :
	print "There is An Error!!!!!!!!!!"
else:
	print "Record Succeed!"

