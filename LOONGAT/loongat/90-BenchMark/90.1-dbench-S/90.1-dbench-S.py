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
dLog = 'touch %s/result/dbench.log' % g_currentPath
Dlog = '%s/result/dbench.log' % g_currentPath
global passwd
global core_num
global second
#*****************************************   
#case label
g_tag = '90.1-dbench-S'  
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
		res = commands.getstatusoutput(dLog)[0]
		if cmp(res,0):
			print 'Create dbench.log failed,please check the authority'
	except (IOError,Exception) as e:
		print e
		mylog.elog(g_tag,'create log failed and return False!')
		return False
	finally:
		return True


def writeEnv():
	fp = open(Dlog, 'w')
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
		if not os.path.exists(Dlog):
			print "In writeEnv Dlog is not exist!"
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
		mylog.elog(g_tag, 'write env to dLog failed!')
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


def Work():
	try:
		logname=commands.getstatusoutput('logname')[1]
		#电源管理
		os.system('echo %s | sudo -S xset -dpms' % passwd)
		os.chdir('%s/resource/' % g_currentPath)
		os.system('chmod a+x %s/resource/dbench.sh' % g_currentPath)
		os.system('echo %s | sudo -S %s/resource/dbench.sh %d %s %s' % (passwd, g_currentPath, second, core_num, passwd))
		res = os.system('echo %s | sudo -S chown %s %s' % (passwd, logname, Dlog))
		if not cmp(res,'0'):
			print "chown logname Dlog failed"
			mylog.wlog(g_tag, 'chown logname Dlog failed!')
	except Exception as e:
		print e
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
	dataNode = obj.getXMLNode(doc, 'data',0)
  	duraNode = obj.getXMLNode(dataNode, 'duration', 0)
 	duration = obj.getXMLNodeValue(duraNode, 0)
	print  'dbench will be run: ',duration
	second = timeProcess(duration)
	checkDir(g_currentPath + '/resource')
	createLog()
	print '*'*30
	writeEnv()
	print '*'*30
	if not (Work()):
		print "Work function exec failed!\n"
		mylog.elog(g_tag, 'work function exec failed!')

	time.sleep(1)
	sys.exit()

if __name__ == "__main__":
	main()





