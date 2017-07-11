import os
import sys
import logcase
from ldtp import *
from ldtputils import *
from moduleobject import Module

g_tag='4.1.9.1-iagno'
#public path

#jie tu
Sshot=Sshot()


#log 
mylog=LogCase()



#da kai 
launchapp('iagno') ----first
os.system('iagno')
commands.getstatusoutput('iagno')
cnee 


#exist
activatewindow(winname)   
guiexist(winname)
waittillguiexist(winnaome)

log 
mylog.ilog(g_tag, 'I catch the window!')
Sshot.sprintf(g_tag,'iano-exist','./')

mylog.elog(g_tag, '')





#guan bi 
act ivatewindow()
closewindow()
keypress('<Alt>')
<F4>
keyrelease('<Alt>')
<F4>

#guan bi an niu 
mousemove('winnamne','btnClose')
mouseleftclick()

act ivatewindow(winname,objname)
click()



os.system('kill -9 ')
commands.getstatusoutput('')

def work(n):	
	try:
		pass
		....
		
	except (NameError ,Exception ) as e:
		print e
		mylog.elog(g_tag,'error')
		sys.exit()
	finally/else
	
	






















