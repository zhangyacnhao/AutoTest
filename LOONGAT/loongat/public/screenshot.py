#!/usr/bin/python
#coding=utf-8
#########################################################################
# LOONGSON Auto-test Tool Project
# class Logcase
# This module uses gnome-screenshot/scrot(fedora 13) to capture desktop
# Version:1.0.1
# Author:Vans
# Date:2015-09-25
# Author:Vans
#########################################################################
import os
import sys
import time
import logcase
import commands

g_tag = 'Screenshot'
systemNameFile = '/etc/issue'

def chFlag():
	global flag
	systemFile=open(systemNameFile, 'r') 
	fileBuffer = systemFile.read()
	if fileBuffer.find('13') != -1:
		flag=1
	elif fileBuffer.find('21')!= -1: 
		flag=2
	else:
		print 'Not supported os!'
	return 
			

class Screenshot():
    def __init__(self, shotFileName = None):
        pass

    # call this function to get screen print
    def scrprint(self, caseName, shotFileName, shotFilePath, format = "png"):
        if self.getScreenshot():
            self.saveFile(caseName, shotFileName, shotFilePath, format)

    def getScreenshot(self):
        return True
        
    def saveFile(self, caseName, shotFileName, shotFilePath, format):
	timeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
	saveTotalDirPath = shotFilePath
	if shotFilePath[len(shotFilePath) - 1] != '/':
		saveTotalDirPath += '/'
	saveTotalDirPath += 'screenshot' 

	if not os.path.exists(saveTotalDirPath):
		os.makedirs(saveTotalDirPath)

	saveTotalFilePath = saveTotalDirPath + '/' + shotFileName + timeStamp + '.' + format
	if os.path.exists(saveTotalFilePath):
		print '%s: Error: has screenshot file %s' % (g_tag, saveTotalFilePath)

	#res=commands.getstatusoutput('whereis scrot')[1]
	#Fedora 13 系统截图
	#if res != 'scrot:': 
	#	print 'saveTotalPath is :',saveTotalFilePath
	#if os.system('scrot '  + saveTotalFilePath + '.png') ==0:
	#	print '%s: save screenshot file %s ok' % (g_tag, saveTotalFilePath)
	#	print '%s: Info: Screenshot saved to %s' % (g_tag, saveTotalFilePath)
	#else:
	#	print '%s: cannot save screenshot file %s' % (g_tag, saveTotalFilePath)
	#Fedora 21 use gnome-screenshot 进行截图
	# test, use gnome-screenshot to save file 
        if os.system('gnome-screenshot -f ' + saveTotalFilePath) == 0:
               	print '%s: save screenshot file %s ok' % (g_tag, saveTotalFilePath)
         #self.pixbuf.save(saveTotalFilePath, "png")
                print '%s: Info: Screenshot saved to %s' % (g_tag, saveTotalFilePath)
        else:
                print '%s: cannot save screenshot file %s' % (g_tag, saveTotalFilePath)

		
'''
#for test
if __name__ == '__main__':
    	screenshot = Screenshot()

'''
