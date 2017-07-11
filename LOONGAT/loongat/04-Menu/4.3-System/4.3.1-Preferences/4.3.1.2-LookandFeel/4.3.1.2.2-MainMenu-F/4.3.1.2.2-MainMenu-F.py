#!/usr/bin/env python
#coding=utf-8
from ldtp import *
from ldtputils import *
from time import sleep 
import sys
import os

reload(sys)
#sys.setdefaultencoding("utf8")

#路径添加
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)
#导入框架 库
from logcase import Logcase
from caseobject import CaseObject
from screenshot import Screenshot
#########################################################################
#全局变量区域
g_tag ="4.3.1.2.2-MainMenu-F" #####
mylog = Logcase()
Sshot = Screenshot()
winName = "未命名 - MainMenu-F" #####
global passwd
######################################################################
def Openwin():
	try: 
		pid = launchapp('mozo')  #####
  		print pid,type(pid)

	except (Exception, NameError) as Error:
		print Error
	finally:
		return
#######################################################################
def ChekAndClosWin():
	try:
		res = waittillguiexist('dlgMainMenu')
		print res
		if res==1:
			mylog.ilog(g_tag,'i catch the window')
			activatewindow('dlgMainMenu')
			sleep(5)
			Sshot.scrprint(g_tag, 'After_MainMenu', g_currentPath)
			sleep(5)
		else: mylog.elog(g_tag,'the window not exist') 
	except (Exception, NameError) as Error:
		print Error
	finally:
		return
#######################################################################	
def CloeWin():
	try:
		print 'will be close the window'
		closewindow('dlgMainMenu')
		result = waittillguiexist('dlgMainMenu')
		if result==0:
			print mylog.ilog(g_tag,'closing window successifully!')
		else:
			kcmd = "kill -9 %d" % pid
			os.system(kcmd)
		

	####### 判断窗口是否存在
	####### ('frmXXXX')
	####### waittillguiexist



	
	#sleep(5)

	#######

	
	##### Pic=g_currentpath+'/screenshot/'+1.png
	##### os.system('gnome-screenshot -f %s' % Pic)
	###### 

	#kcmd = "kill -9 %d" % pid
	#os.system(kcmd)
	except (Exception, NameError) as e: #####
		print  e ###
	finally:
		return
###### closewindow wcnk w.close()

###33 可选 检测窗口是否消失 

##### guiexist() waittillguiexist()
#### print mylog.ilog(g_tag,'closing window successifully!')



	
#else:
	#mylog.elog(g_tag,'catch the window False')
	
#main Entrance
def main():
	Openwin()
	ChekAndClosWin()
	CloeWin()
if __name__ == '__main__':
	main()
