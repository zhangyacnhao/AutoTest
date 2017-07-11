#!/usr/bin/env python
#coding=utf-8

#########################################################################
# 4.1.1.2-PrjMangement.py
# Module for Planner(Project management software)test
#########################################################################

# 导入 python 库
import os
import sys
import time
import commands

reload(sys)
sys.setdefaultencoding("utf8")

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
g_tag ="4.1.1.1-Evolution"
mylog = Logcase()
Sshot = Screenshot()
winName = "未命名 - Planner"
global passwd
#########################################################################
#定义功能函数

def chkdir(dir):
	try:
		if not os.path.exists(dir):
			mylog.ilog(g_tag, 'Begin to create Pics Directory')
			if commands.getstatusoutput('mkdir resource screenshot result')[0] == 0:
				mylog.ilog(g_tag, 'Create target dirs successfully!')
			else:
				mylog.elog(g_tag, 'Create target dirs failed!')
				return False
		else:
			res=os.system('rm -rf screenshot/* result/*')
			if res !=0:
				mylog.ilog(g_tag,'Delete target dirs Failed!')
			mylog.ilog(g_tag,'./resouce has existed!' )
	except (NameError,Exception) as e:
		mylog.elog(g_tag,'chkdir function Exited False')
		print e
		return False
	finally:
		return True

def ckWin(winName):
	try:
		while True:
			while gtk.events_pending():
				gtk.main_iteration()
				screen = wnck.screen_get_default()
				screen.force_update()
				wins = screen.get_windows()
		
			time.sleep(0.1)
			for w in wins:
				tName = w.get_name()
				if cmp(winName,tName) ==0:			
					break
	except (NameError ,Exception) as e:
		print e
	finally:
		return True
	

def work():
	try:
		#res = os.system('planner &')
		#if res !=0:
		#	print 'Lanch Failed!'
		#	mylog.elog(g_tag,'lanch palnner failed!')
		#	return 
		#time.sleep(2)
		#ckWin(winName)
		os.system('chmod a+x resource/Evolution.sh')
		Sshot.scrprint(g_tag, 'Before_Evolution.sh', './')	
		time.sleep(1)
		print 'The current path is :', commands.getstatusoutput('pwd')[1]
		res =os.system('sh resource/Evolution.sh')
		if res !=0:
			print 'Excute resource file Evolution.sh Failed!'
			mylog.elog(g_tag,'Excute Evolution.sh resource failed!')
		Sshot.scrprint(g_tag, 'After_Evolution.sh', './')
		time.sleep(1)
	except (IOError ,Exception) as e:
		mylog.elog(g_tag,'work function excute Failed!')
		print e
	finally:
		return
	

#main function
def main():
	global passwd
	obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	passwd = obj.getPasswd()
	os_type = obj.getOSName()
	print 'You curretn os is:', os_type
	if cmp('Fedora 13',os_type) !=0:
		print 'Case not for the current OS!'
		sys.exit()

	#xml pharser
	doc = obj.getDocumentNode()  
	data_node = obj.getXMLNode(doc,'data',0)
	time_node = obj.getXMLNode(data_node,'times',0)
	count =  obj.getXMLNodeValue(time_node, 0)
	
	print 'Exc times:', count
	
	#chkdir 
	print 'g_currentPath is:',g_currentPath
	os.chdir(g_currentPath)
	res = chkdir('resource')
	
	if res !=True:
		print 'Target dirs not exist!'
		mylog.elog(g_tag,'Target dirs not exist!')
		sys.exit()
	
	
	#for circle
	for i in range(count):
		mylog.ilog(g_tag,'Call work function~!')
		work()
		time.sleep(2)
		

	mylog.ilog(g_tag,'Main function exit')
	sys.exit()
	
if __name__ == '__main__':
    main()
