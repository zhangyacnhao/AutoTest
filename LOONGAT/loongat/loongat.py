#!/usr/bin/env python
#coding=utf-8

#***********************************************************************
# loongat.py
# LOONGSON Auto-test Tool
# Author ="Loongson"
# Version = 1.0.0
#***********************************************************************

import os
import sys

#global env virable
g_tag = 'loongat'
g_currentPath = sys.path[0]
g_publicLibPath = g_currentPath + '/public'
#设置自动测试目录和共享库导入目录
os.environ['AUTOTEST_DIR'] = g_currentPath
os.environ['AUTOTEST_PUBLIC_LIB'] = g_publicLibPath
sys.path.append(g_publicLibPath) 
from moduleobject import Module
from logcase import Logcase

#class 
class LoongAT(Module):
    def __init__(self, moduleName, xmlFileName, dataType = None, sysPath = None):
        Module.__init__(self, moduleName, xmlFileName, dataType, sysPath)

        # rename all the old logs with time stamp, and save new log
		# 为前一次的log添加时间戳，并保留新生成的日志
        self.log = Logcase()
	#读取运行时对S4 配置--默认情况下不执行case中的S4电源管理功能
    def s4Config(self):
        if self.doc:
            common = self.getXMLNode(self.doc, 'common', 0)
            if common:
                s4Node = self.getXMLNode(common, 's4', 0)
                s4Value = self.getXMLNodeValue(s4Node, 0)
                if s4Value:
                    os.environ['S4_ENABLE'] = str(s4Value)
                    return True

        return False

def main():
    loongatObj = LoongAT(g_tag, g_currentPath + '/' + g_tag+'.xml', 'module', g_currentPath)
    try: 
    	print 'S4_ENABLE=%s' %os.environ['S4_ENABLE']
    except KeyError:
	os.environ['S4_ENABLE'] = '0'  

    if len(sys.argv) >= 2:  
	#save os password
        loongatObj.setPasswd(sys.argv[1])
        loongatObj.run()
    else:
        print 'Please input root password for loongat.py'


if __name__ == '__main__':        
    main()


