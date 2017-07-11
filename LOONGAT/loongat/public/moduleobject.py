#!/usr/bin/env python
#coding=utf-8
#############################################################################
# LOONGSON Auto-test Tool Project
# class Module
# This module is used to get running case list and run case from the list.
# Version:1.0.1
# Author:Vans
# Date:2015-09-12
#############################################################################
import re
import os
import sys 
import time
import signal
import codecs

g_tag = 'moduleobject'
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)  

from caseobject import CaseObject
from logcase import Logcase
g_log = Logcase()

class Module(CaseObject):
    def __init__(self, moduleName, xmlFileName = None, dataType = None, sysPath = None): # Reserve
        CaseObject.__init__(self, moduleName, xmlFileName) # Reserve
        self.moduleName = moduleName
        self.doc = self.getDocumentNode()
	self.cfgFileName = xmlFileName   # TEST: for remove child
        if self.doc != None:
            self.commonNode = self.getXMLNode(self.doc, 'common', 0) # Reserve
            self.countNode = self.getXMLNode(self.commonNode, 'count', 0) #Reserve
            self.count = self.getCycleCount(self.commonNode)
            self.exectime = self.getExecTime(self.commonNode)
	print '%s: In module %s, running begin' %(g_tag, self.moduleName)
        self.tempPath = sysPath
        self.dataNode = self.getXMLNode(self.doc, 'data', 0)
        self.ConfigList = [] 

        self.caseNodeList = None
        self.moduleNodeList = None
	self.dataType = dataType #TEST: for remove nodes
          
        if dataType == 'case':
            self.appendCaseList()
        elif dataType == 'module':
            self.appendModuleList()
	"""
	获取case 的python 和XML 文件的绝对路径，并将其作为全局数据配置列表ConfigList 的元素
	"""
    def appendCaseList(self):
        self.caseNodeList = self.getXMLNodeList(self.dataNode, 'case')
        for case in self.caseNodeList:  
            singleCase = []
            caseName = self.getXMLNodeValue(case, 0)
			#case python  文件的绝对路径
            caseTotalScript = self.tempPath + '/' + caseName + '/' + caseName + '.py'
            print ' caseTotalScript %s' %caseTotalScript
            if self.fileExists(caseTotalScript):
                singleCase.append(caseTotalScript)
			#case XML 配置文件的绝对路径
                caseTotalConfig = self.tempPath + '/' + caseName + '/' + caseName + '.xml'
                print 'caseTotalConfig %s' %caseTotalConfig
                if self.fileExists(caseTotalConfig):
                    singleCase.append(caseTotalConfig)
                else:
                    print '%s Warning: case %s seems not has a config file named %s' %(g_tag, caseName)
            #将case 的python文件和XML 文件的绝对路径作为列表，添加到全局的配置列表中
            self.ConfigList.append(singleCase)
	"""
	获取module 的python 和XML 文件的绝对路径，并将其作为全局数据配置列表ConfigList 的元素
	"""
    def appendModuleList(self):
        self.moduleNodeList = self.getXMLNodeList(self.dataNode, 'module')
        for module in self.moduleNodeList:
            childModuleName = self.getXMLNodeValue(module, 0)
            moduleScriptPath = self.tempPath + '/' + childModuleName + '/' + childModuleName + '.py'
            if self.fileExists(moduleScriptPath):
                singleCase = []
                singleCase.append(moduleScriptPath)
                moduleConfigPath = self.tempPath + '/' + childModuleName + '/' + childModuleName + '.xml'
                if self.fileExists(moduleConfigPath):
                    singleCase.append(moduleConfigPath)
                else:
                    print 'Warning: child module %s seems not has a config file named %s' %(childModuleName, moduleConfigPath) 
                self.ConfigList.append(singleCase)
            else:
                print 'Error: Module %s has error child module %s' % (self.moduleName, childModuleName)
                continue
	"""
	判断absFileName是否存在
	"""
    def fileExists(self, absFileName):
        if os.path.exists(absFileName):
            print 'Debug: file %s exists' % absFileName
            return True
        else:
            print 'Error: file %s doesn\'t exists' % absFileName
            return False

    
	"""
	开始执行case
	"""
    def run(self):
        CaseObject.run(self, self.runCase)

  
	
    """ 
    Temp Function: 
	execute copy log after running
    """
    def copylog(self):
	timeStamp = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
	currentOS = self.getOSName()
	label = timeStamp + '-' + currentOS
	passwd = self.getPasswd()
	scriptPath = os.environ['AUTOTEST_DIR'] + '/tools/scripts/tarlog.sh'
	loongatPath = os.environ['AUTOTEST_DIR']
	tarFilePath = os.path.dirname(os.environ['AUTOTEST_DIR'])
	ret = os.system('bash ' + scriptPath + ' ' + loongatPath + ' ' + tarFilePath + ' ' + label + ' ' + passwd)
	if ret != 0:
		g_log.elog(g_tag, 'Cannot copy log')

	"""
	执行case 功能的函数
	"""
	
    def runCase(self):
	print 'TEST: moduleName', self.moduleName
    	caseLen = len(self.ConfigList)
	print 'caseLen ', caseLen	
	passwd = self.getPasswd()
        for caseIndex in range(caseLen):
            if len(self.ConfigList[caseIndex]) == 1:
                command = 'python ' + self.ConfigList[caseIndex][0]
            elif len(self.ConfigList[caseIndex]) == 2:
                command = 'python ' + self.ConfigList[caseIndex][0] + ' ' + self.ConfigList[caseIndex][1]
	    logStr = 'module ' + g_tag + ' begin run ' + command 
	    g_log.ilog(g_tag, logStr)
            print '%s: Debug: %s' %(g_tag,command)
            os.system(command)
	
	sys.exit()
		


