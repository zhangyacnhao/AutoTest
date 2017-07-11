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
g_tag ="4.3.1.1.3-Mouse-F"
mylog = Logcase()
Sshot = Screenshot()
winName = "未命名 - Mouse-F"
global passwd
################################################
def OpenWin():
	try:	
		pid = launchapp('mate-mouse-properties')
		print pid,type(pid)
	except(Exception,NameError)as Error:
		print Error
	finally:
		return
#################################################
def ChekWin():
	try:		
		res = waittillguiexist('dlgMousePreferences')
		print res
		if res==1:
 			mylog.ilog(g_tag,'i catch the window')
			activatewindow('dlgMousePreferences')
			Sshot.scrprint(g_tag, 'After_Mouse', g_currentPath)
		else:	mylog.elog(g_tag,'the window not exist')	
	except(Exception,NameError)as Error:
			print Error
	finally:
			return
###############################################
def ClosWin():
	try:
		print 'will be close the window'
		sleep(5)
		closewindow('dlgMousePreferences')	
	except (Exception, NameError) as e: #####
		print  e ###
	finally:
		return
############################################
def main():
	OpenWin()
	ChekWin()
	ClosWin()
if __name__=='__main__':
	main()
