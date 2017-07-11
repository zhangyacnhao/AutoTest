#!/usr/bin/python
#coding=utf-8

#############################################################################
# LOONGSON Auto-test Tool Project
# class Logcase
# This module uses python logging module to process loongat logs
# Version:1.0.1
# Author:Vans
# Date:2015-08-22
#############################################################################

import os
import sys
import time
import logging

g_tag = 'logcase'

#class Logcase
class Logcase(object):
    def __init__(self):
      g_publicFileDirPath = os.environ['AUTOTEST_PUBLIC_LIB']
      publicIndex = g_publicFileDirPath.find('/public')
      self.logFileDirPath = g_publicFileDirPath[0:publicIndex] + '/log'

      if not os.path.exists(self.logFileDirPath):
            os.makedirs(self.logFileDirPath)
            print 'make log dir %s' %self.logFileDirPath

      self.logInfoPath = self.logFileDirPath + '/info.log'
      self.logWarnPath = self.logFileDirPath + '/warn.log'
      self.logErrorPath = self.logFileDirPath + '/error.log'

      self.createLogFile(self.logInfoPath)
      self.createLogFile(self.logWarnPath)
      self.createLogFile(self.logErrorPath)

      self.infologger = self.initLogger('INFO', self.logInfoPath)
      self.warnlogger = self.initLogger('WARN', self.logWarnPath)
      self.errorlogger = self.initLogger('ERROR', self.logErrorPath)
    
    def initLogger(self, levelTag, logFilePath):
      logger = logging.getLogger(levelTag)
      # do not regist the same logger twice
      if logger.handlers:
	return logger

      logger.setLevel(logging.ERROR)
      fh = logging.FileHandler(logFilePath)
      fh.setLevel(logging.ERROR)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
      fh.setFormatter(formatter)
      logger.addHandler(fh)

      return logger

    def createLogFile(self, filePath):
      if not os.path.exists(filePath):
            cmdStr = 'touch ' + filePath
            os.system(cmdStr)

    def ilog(self,tag,msg):
      self.commonlog(tag, msg, 'INFO')

    def wlog(self,tag,msg):
      self.commonlog(tag, msg, 'WARN')

    def elog(self,tag,msg):
      self.commonlog(tag, msg, 'ERROR')

    def commonlog(self, tag, msg, logtype):
            currentLogger = None
            if logtype == 'INFO':
                  currentLogger = self.infologger
            elif logtype == 'WARN':
                  currentLogger = self.warnlogger
            elif logtype == 'ERROR':
                  currentLogger = self.errorlogger

            totalMsg = tag + '-' + msg
            currentLogger.error(totalMsg)

    def renameWithTimeStampPrefix(self, timeStamp, directory, fileName):
      fileOldName = os.path.join(directory, fileName)
      fileNewName = os.path.join(directory, timeStamp + fileName)
      print 'fileNewName %s' %fileNewName
      try:
            os.rename(fileOldName, fileNewName)
      except:
            print '%s: Rename with wrong log file %s' %(g_tag, fileOldName)

    '''
	#对上一次运行的log进行更名，添加时间戳
    '''
    def renameLogs(self):
      print '%s: in renameLogs' %g_tag
      logDir = self.logFileDirPath
      timeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
      self.renameWithTimeStampPrefix(timeStamp, logDir, 'info.log')
      self.renameWithTimeStampPrefix(timeStamp, logDir, 'warn.log')
      self.renameWithTimeStampPrefix(timeStamp, logDir, 'error.log')

    '''
    clearlog: clear all logs 
    WARNING: this function will clear all logs under log directory
    '''
    def clearlog(self):
    	if os.path.exists(self.logFileDirPath):            
            timeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            command = 'rm -fr ' + self.logFileDirPath + '/*'
            os.system(command)
            print 'clearlog: rename old log dir in %s' %self.logFileDirPath
''' 
if __name__ == '__main__':
      g_log = Logcase()
'''
