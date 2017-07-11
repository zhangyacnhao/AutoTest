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
g_tag ="4.1.2.1-Chrome39"
mylog = Logcase()
Sshot = Screenshot()
winName = "未命名 - Chrome39"
global passwd

pid = launchapp('chrome39.sh')
print pid,type(pid)
res = waittillguiexist('frmWelcome')
print res

if res==1:
 	mylog.ilog(g_tag,'i catch the window')
sleep(3)
Sshot.scrprint(g_tag, 'After_Atril', '/home/loongson/loongat/04-Menu/4.1-Application/4.1.1-Office/4.1.1.3-Claws-Mail/')
sleep(5)
print 'will be close the window'
closewindow('frm4.1.2.1-Chrome39')
#kcmd = "kill -9 %d" % pid
#os.system(kcmd)
	
else:
	mylog.elog(g_tag,'catch the window False')
	
