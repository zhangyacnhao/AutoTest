#!/usr/bin/env python
#coding=utf-8
from ldtp import *
from ldtputils import *
from time import sleep 
import sys
import os
import commands
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
g_tag ="4.1.1.1-Evolution-F" #####
mylog = Logcase()
Sshot = Screenshot()
winName = "未命名 - Evolution" #####
global passwd
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
			mylog.ilog(g_tag,'./resource has existed!' )
	except (NameError,Exception) as e:
		mylog.elog(g_tag,'chkdir function Exited False')
		print e
		return False
	finally:
		return True
def work():
	try: 
		pid = launchapp('evolution')  #####
  		print pid,type(pid)




		#res = waittillguiexist('frmWelcome')
		#print res
	
		#if res==1:
		# 	mylog.ilog(g_tag,'i catch the window')
		sleep(12)
	
		####### 判断窗口是否存在
		####### activatewindow('frmXXXX')
		####### waittillguiexist



		Sshot.scrprint(g_tag, 'After_Evolution', './')
		sleep(5)
	
		#######else elog 

		print 'will be close the window'
		##### Pic=g_currentpath+'/screenshot/'+1.png
		##### os.system('gnome-screenshot -f %s' % Pic)
		###### 

		kcmd = "kill -9 %d" % pid
		os.system(kcmd)
	except (Exception, NameError) as e: #####
		print  e ###
###### closewindow wcnk w.close()

###33 可选 检测窗口是否消失 

##### guiexist() waittillguiexist()
#### print mylog.ilog(g_tag,'closing window successifully!')



	
###else:
		mylog.elog(g_tag,'catch the window False')


def main():
	os.chdir(g_currentPath)
	res = chkdir('resource')
	
	if res !=True:
		print 'Target dirs not exist!'
		mylog.elog(g_tag,'Target dirs not exist!')
		sys.exit()
	work()

if __name__ == '__main__':
    main()

