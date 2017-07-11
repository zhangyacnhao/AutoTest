#!/usr/bin/env python
#coding=utf-8
#############################################################################
#
# LOONGSON Auto-test Tool Project
# class CaseObject
# Date:2015-08-18
#############################################################################

import re
import os
import sys
import signal
import xml.dom.minidom
import time
import datetime
import getpass
import commands

g_tag = 'CaseObject'
OS = "cat /etc/issue | head -1 | awk '{print $(NF-4)}'"
Ver ="cat /etc/issue | head -1 | awk '{print $(NF-2)}'"
Longbit = "getconf LONG_BIT"
Wordbit = "getconf WORD_BIT"

class CaseObject(object):
    """
    Base function for test case.
    Function:
    1. Parse the XML config file for test case;
    2. Get the value of tag, and return it to the caller.
    """
    def __init__(self, caseName, xmlFileName = None):
        # initialize basic arguments
        self.hasConfig = False 
        self.caseName = None
        self.configFileName = None
        self.commonNode = None
        self.count = None               
        self.exectime = None            
        self.functionList = []
        self.caseName = caseName
        self.configFileName = os.path.abspath (xmlFileName)
	self.currentPath = os.environ['AUTOTEST_PUBLIC_LIB'] 
	self.currentPasswdPath = self.currentPath + '/.passwd'

        self.doc = None
        try:
            self.doc = xml.dom.minidom.parse (self.configFileName)
        except xml.parsers.expat.ExpatError:
            print 'XML File %s Error' %self.configFileName
            return
        except IOError:
            print 'XML "%s" file not found' % xmlFileName
            return

        self.hasConfig = True
        self.commonNode = self.getXMLNode(self.doc, 'common', 0) 

    """
		Via shell commands return OS Name
    """
    def getOSName(self):
		osName = commands.getoutput(OS)
		osVern = commands.getoutput(Ver)
		if not (cmp(osName,'Fedora') and cmp(osVern,21)):
			return 'Fedora 21'
		elif not (cmp(osName,'Fedora') and cmp(osVern,21)):
			return 'Fedora 13'
		else:	 
			print 'Match OS-Name Failed!'

		"""
		Write passwd (from terminal)  to public/.passwd file
		"""
    def setPasswd(self, passwd):	
	try:
		with open(self.currentPasswdPath, 'w') as fp:
			print '%s: open passwd file %s' %(g_tag, self.currentPasswdPath)
			fp.write(passwd)
			return True
	except:
		print '%s: cannot open password file to write in %s' %(g_tag, self.currentPasswdPath)
		return False

    """
    Via reading public/.passwd file to return passwd  
    """
    def getPasswd(self):
	try:
		if not os.path.exists(self.currentPath):
			print '%s: passwd file not exist in %s' % (g_tag, self.currentPasswdPath)
			return None
		with open(self.currentPasswdPath, 'r') as fp:
			print '%s: open passwd file in %s' %(g_tag, self.currentPasswdPath)
			passwd = fp.read()
			return passwd
	except:
		print '%s: cannot open password file in %s' %(g_tag, self.currentPasswdPath)
		return None


    """
    Enable or disable mouse and keyboard
    Success: return True
    Failure: return False
    """
    def enableUsbInput(self, enableFlag):
	passwd = self.getPasswd()
	filePath = os.envrion['AUTOTEST_PUBLIC_LIB'] + '/UsbInput.sh'
	
	os.system('chmod +x %s' % filePath)
	if not enableFlag:
		os.system('echo %s| sudo -S %s disable' %(passwd, filePath))
	else:	
		os.system('echo %s| sudo -S %s enable'  %(passwd, filePath))		

  
	"""
	执行shell 命令
	"""
	def execCommand(enableFlag):
		value = '0'
		if enableFlag == True:
			value = '1'

    	   	for deviceId in deviceIDList:
    		    command = 'xinput set-prop ' + deviceId + ' \'Device Enabled\' ' + value  
		    if os.system(command) != 0:
			return False
		return True
		
        return execCommand(enableFlag) 
    
  

    """
    Return the os bit.
    """
    def getOSBit(self):
		Long = commands.getoutput('getconf LONG_BIT')
		Word = commands.getoutput('getconf WORD_BIT')
		if not (cmp(Long, '64') and cmp(Word, '32')):
			return 64
		elif not (cmp(Long, '32') and cmp(Word, '32')):
			return 32
		else:	 
			print 'Match OS-Bit Failed!'


    """
   	XML Parse interface
    Success: return node
    Failure: return None
    """
    def getDocumentNode(self):
        if self.hasConfig:
            return self.doc
        else:
            print '%s Warning: \'%s\' does not has xml config file, cannot use this function' % (g_tag, self.caseName)
            return None

	"""
	XML 文件中节点 的属性Value
	"""
    def getAttributeValue(self, node, attrname):
        if not self.hasConfig:
            print '%s Warning: \'%s\' does not has xml config file, cannot use this function' % (g_tag, self.caseName)
            return None

        if node:
            return node.getAttribute(attrname)
        else:
            print '%s Error: node does not has the attribute %s' % (g_tag, attrname)
            return ''
	"""
	获取XML 节点的名称
	"""
    def getXMLNodeList(self, node, childNodeName):
        if node:
            return node.getElementsByTagName(childNodeName)
        else:
            print 'Error: getXMLData,node does not exist'
            return []
	"""
	获取XML 节点的索引
	"""
    def getXMLNode(self, node, childNodeName, index):
        if node:
            try:
                childNode = node.getElementsByTagName(childNodeName)[index]
                return childNode
            except:
                print '%s: Error: get child node %s for index %d error' %(g_tag, childNodeName, index)
                return None
        else:
            print 'Error: getXMLData,node does not exist'
            return None
	
	"""
	获取XML 节点的类型 type=int/string/intarray
	"""
    def getXMLNodeType(self, node, index):
        if node:
            typename = node.getAttribute('type')
            if typename == 'int':
                return 0
            elif typename == 'string':
                return 1
            elif typename == 'intarray':
                return 2

        else:
            print 'Error: getXMLNodeType, node does not exist'
            return -1

	"""
	解析运行时间空之测试运行时间
	"""
    def parseRunningTime(self, timeStr):
        hour = '0'
        minute = '0'
        second = '0'

        timeMatchObj = re.match(r'(\d*h){0,1}(\d*M){0,1}(\d*S){0,1}$', timeStr)
        if timeMatchObj:
            if timeMatchObj.group(1):
                hour = timeMatchObj.group(1)[:-1]
            if timeMatchObj.group(2):
                minute = timeMatchObj.group(2)[:-1]
            if timeMatchObj.group(3):
                second = timeMatchObj.group(3)[:-1]
        else:
            print '%s: Error: not match any execute time' % g_tag
            return -1  
        totalSecond = int(hour) * 3600 + int(minute) * 60 + int(second)         
        return totalSecond 
	"""
	获取XML 文件中节点的Value
	"""
    def getXMLNodeValue(self, node, index):
        if node != None:
            typename = node.getAttribute('type')
            if len(typename) == 0:
                print '%s: Error: get XML node type error' %g_tag
                return None
            try:
                if typename == 'int':
                    return int(node.childNodes[index].nodeValue)
                elif typename == 'string':
                    return node.childNodes[index].nodeValue
                elif typename == 'intarray':
                    str = node.childNodes[index].nodeValue
                    strList = str.split(',')
                    intArray = []
                    for i in range(len(strList)):
                        intArray.append(int(strList[i]))
                    return intArray
                elif typename == 'time':  #time for execute file
                    str = node.childNodes[index].nodeValue
                    return self.parseRunningTime(str)
                else:
                    print '%s: Error: XML node type is error' %(g_tag, typename)
                    return None
            except:
                print '%s: Error: get XML node type error' %g_tag
                return None
        else:
            print 'Error: getXMLValue, node does not exist'
            return None
	"""
    #执行一定次数/时间
	"""
    def run(self, execFunction, postFunction = None):
        if self.count != None and self.count > 0:
            #print 'in count = %d' %self.count
            if self.exectime > 0:
                print '%s: Warning: only execute as xml \'count\' tag' % g_tag
            self.runInCount(execFunction, self.count)
        elif self.exectime != None and self.exectime > 0:
            print 'in time = %d' %self.exectime
            self.runInExecTime(execFunction, self.exectime)
        else:
            print '%s: Warning: Module %s seems has no execute time' % (g_tag, self.caseName)
	
	"""
	获取循环次数
	"""
    def getCycleCount(self, commonNode):
        count_node = self.getXMLNode(commonNode, 'count', 0)
        if count_node:
            count = self.getXMLNodeValue(count_node, 0)
            return count
        else:
            print '%s: Error: count number' %(g_tag)
            return -1

	"""
	获取执行时间
	"""
    def getExecTime(self, commonNode):
        exectime_node = self.getXMLNode(commonNode, 'exectime', 0)
        if exectime_node:
            exectime = self.getXMLNodeValue(exectime_node, 0)
            if exectime == -1:
                return 0
            else:
                return exectime
        else:
            print '%s: Error: count number' %(g_tag)
            return -1

	"""
	执行execFunction 一定时间
	"""
    def runInExecTime(self, execFunction, Timeout = 1): 
        # 定义信号处理函数
        def myHandler(signum, frame):
            print "%s: Now, it's the time %d" %(g_tag, Timeout)
            exit()
        if Timeout == 0:
            print '%s: Error: cannot set timeout=0' %g_tag

        starttime = datetime.datetime.now()
        while True:
            execFunction()
            endtime = datetime.datetime.now()
	    sec = (endtime -starttime).seconds 
	    if (endtime - starttime).seconds > Timeout:
                break
        
	return True

	"""
	执行ececFunction count次
	"""
    def runInCount(self, execFunction, count):
        if count >= 0:
            for countIndex in range(count):
                execFunction()

    def workEternal(self, function):
        starttime = datetime.datetime.now()
        while True:
            function()
            endtime = datetime.datetime.now()


    """
	按照用户自定义的函数，执行函数列表中的函数
	"""
    def execFunctionListInOrder(self, order): 
        if len(self.functionList) == 0:
            print '%s: Warning: It seems that this object does not has a function list.' % g_tag
            return
        for i in order:
            self.functionList[i]()
	"""
	将execFunc 添加进函数列表
	"""
    def addFunctionList(self, execFunc):
        self.functionList.append(execFunc)

	"""
	打印待执行的函数列表中函数名称
	"""
    def printFunctionList(self):
        print '%s Function list:' % caseName
        for func in self.functionList:
            print '%s' % func.__name__

''' 
if __name__ == '__main__':
    obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	os_type = obj.getOSName()
'''

