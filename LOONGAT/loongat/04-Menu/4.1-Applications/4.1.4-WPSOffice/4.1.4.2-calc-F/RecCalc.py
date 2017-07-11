from ldtp import *
from ldtputils import *
import commands
import time

def max_window():
	keypress('<alt>')
	keypress('<f10>')
	keyrelease('<alt>')
	keyrelease('<f10>')
print 'Please Waite for a moment :)'
commands.getstatusoutput('xdg-open document.et')
time.sleep(6)
max_window()
time.sleep(1)
print 'Begin Recording After 3 Seconds !'  
# Run Cnee Record Command
(status,output) = commands.getstatusoutput('cnee -rec --all-events --keyboard --mouse -o wpscalc.xns -sk End -t 3 ')

# Jugement
time.sleep(1)
if status != 0 :
	print "There is An Error!!!!!!!!!!"
else:
	print "Record Succeed End !"

