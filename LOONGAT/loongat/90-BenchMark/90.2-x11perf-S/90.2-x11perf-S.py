#!/usr/bin/env python 
#coding=utf-8 

#import modules
import os
import sys
import commands
from ldtp import *
from ldtputils import *
from time import ctime,sleep

reload(sys)   
sys.setdefaultencoding('utf8')  
#path control
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath) 
g_currentPath = sys.path[0]

from logcase  import Logcase
from caseobject import CaseObject
from screenshot import Screenshot

#global variable
mylog=Logcase()   
Sshot=Screenshot()
xLog = 'touch %s/result/x11Perf.log' % g_currentPath
Xlog = '%s/result/x11Perf.log' % g_currentPath
global passwd
global core_num
global second
#*****************************************   
#case label
g_tag = '90.2-x11perf-S'  
#define function
#fun1 check case directory
def checkDir(dirName):
	try:
		if not os.path.exists(dirName):
			if commands.getstatusoutput('mkdir %s' % dirName)[0] == 0:
				os.system('mkdir %s' % (g_currentPath + '/result'))
				os.system('mkdir %s' % (g_currentPath + '/screenshot'))
				pass #add mylog
			else:
				print 'Create ./resource failed!'
				pass #add mylog
				return False
		else:
				os.system('rm -rf  %s/*' % (g_currentPath + '/result'))
				os.system('rm -rf  %s/*' % (g_currentPath + '/screenshot'))
	except (IOError,Exception) as e:
		print e
	finally:
		return True


#func2 
def createLog():
	try:
		res = commands.getstatusoutput(xLog)[0]
		if cmp(res,0):
			print 'Create dbench.log failed,please check the authority'
	except (IOError,Exception) as e:
		print e
		mylog.elog(g_tag,'create log failed and return False!')
		return False
	finally:
		return True


def writeEnv():
	fp = open(Xlog, 'w')
	try:		
		#motherBoard
		boardLine = commands.getstatusoutput("cat /proc/boardinfo | grep 'Board name'")[1]
		boardName = boardLine.split(':')[1].split()
		#pmon
		pmonLine = commands.getstatusoutput("echo %s | sudo -S dmidecode | grep 'PMON'" % passwd)[1]
		pmonInfo = pmonLine.split(':')[1].split()
		#kernel info
		kernelInfo = commands.getstatusoutput('uname -v')[1]
		#mem info
		#内存条根数
		mem_num = commands.getstatusoutput("echo %s | sudo -S dmidecode | grep -i '^\s\Size'| grep 'MB' | wc -l" % passwd)[1]
		#单根内内存条大小
		single_size = commands.getstatusoutput("echo %s | sudo -S dmidecode | grep -i '^\s\Size' | grep 'MB' | awk '{print $2}' | uniq" % passwd)[1]
		#内存总容量
		total_size = int(mem_num)*int(single_size)
		#测试时间
		date = commands.getstatusoutput('date +%G-%m-%d-%H-%M')[1]	
		if not os.path.exists(Xlog):
			print "In writeEnv xLog is not exist!"
			return False
	
		fp.truncate(0)
		fp.write('测试时间: ' +date+'\n')		
		fp.write('版卡信息: ' + boardName[0] + '\n')			
		fp.write('PMON信息: ' + pmonInfo[0] + '\n')
		fp.write('内核信息: ' + kernelInfo + '\n')
		fp.write('cpu核心数: ' + core_num + '\n')
		fp.write('内存条数: ' + mem_num + '\n')
		fp.write('内存总量: ' + str(total_size) + '\n')
		fp.flush()
	except (ValueError, IOError) as e:
		print "writeEnv excute Failed!"
		mylog.elog(g_tag, 'write env to xLog failed!')
		return False
	finally:
		fp.close()
		return True
	
			

def timeProcess(duration):
	try:
		if duration[-1] == 'H':
			m = re.findall(r'(\w*[0-9]+)\w*',duration)
			seconds = int(m[0])*3600
			return seconds
		elif duration[-1] == 'M':
			m=re.findall(r'(\w*[0-9]+)\w*',duration)
			seconds = int(m[0])*60
			return seconds
		elif duration[-1] == 'S':
			m=re.findall(r'(\w*[0-9]+)\w*',duration)
			seconds = int(m[0])
			return seconds
		else:
			print "duration (time - parameter) not has an invalid identifier!"
	except (ArithmeticError, Exception) as e:
		print "timeProcess func exec failed!"
		mylog.elog(g_tag, 'timeProcess exec failed:%s' % e)
		return None


def x11perfBench():
	try:
		print 'Begining to X11perf benchmark test!'
		res = os.system('x11perf -all | tee -a %s' % Xlog)
		if not cmp(res, '0'):
			print "x11perf benchmark test failed!"
	except (StandardError,Exception) as e:
		mylog.elog(g_tag, 'x11perf benchmark exec failed.')
		return False
	finally:
		return True


#默认情况
def x11perfPress(time=5, repeat=1):
	try:
		print 'Begining to X11perf S-press test!'
		res = os.system('x11perf -all -time %d  -repeat %d | tee -a %s' % (time, repeat, Xlog))
		if not cmp(res, '0'):
			print "x11perf S-press test failed!"
	except (StandardError,Exception) as e:
		mylog.elog(g_tag, 'x11perf benchmark exec failed.')
		return False
	finally:
		return True
			

#define main function
def main():
	global passwd
	global core_num
	global second
	obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	os_type = obj.getOSName()
	if cmp(os_type, 'Fedora 21') !=0:
		print "This case only run Fedora 21"
		mylog.elog(g_tag,'OS matched failed!')
		sys.exit()
	passwd = obj.getPasswd()
	#cpu 核数
	core_num = commands.getstatusoutput("lscpu | grep 'CPU(s)' | awk '{print $2}'")[1]
	#parse XML
   	doc = obj.getDocumentNode()  
	dataNode0 = obj.getXMLNode(doc, 'data',0)
  	timeNode = obj.getXMLNode(dataNode0, 'tstTime', 0)
 	duration = obj.getXMLNodeValue(timeNode, 0)
	#repeat
	dataNode1 = obj.getXMLNode(doc, 'data', 0)
	repeatNode = obj.getXMLNode(dataNode1, 'repTime', 0)
	repeat = obj.getXMLNodeValue(repeatNode, 0)
		
	second = timeProcess(duration)
	print  'x11Perf will be repeat %d times and %dS for each test!' % (repeat, second)
	checkDir(g_currentPath + '/resource')
	createLog()
	writeEnv()
	Sshot.scrprint(g_tag,'Before-x11Perf-Test',g_currentPath)
	x11perfPress(second, repeat)
	Sshot.scrprint(g_tag,'After-x11Perf-Test',g_currentPath)
	time.sleep(1)
	sys.exit()

if __name__ == "__main__":
	main()





