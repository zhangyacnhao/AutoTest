#!/usr/bin/env python 
#coding=utf-8 

#import modules
import os
import sys
import commands
import threading 
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
#用来保存测试的通用信息
eLog = 'touch %s/result/envInfo.log' % g_currentPath
Elog = '%s/result/envInfo.log' % g_currentPath
#用来保存glxgears运行日志
uLog = 'touch %s/result/lmbench.log' % g_currentPath
Ulog = '%s/result/lmbench.log' % g_currentPath
#用来保存shell 处理的数据
Gout = '%s/result/glxgears.out' % g_currentPath
#用来定义lmbench 目标文件
benchMark='%s/resource/lmbench3-edit.tar.gz' % g_currentPath
global passwd
global core_num
#*****************************************   

#case label
g_tag = '90.5-lmbench-S'  
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
		res = commands.getstatusoutput(uLog)[0]
		if cmp(res,0):
			print 'Create lmbench.log failed,please check the authority'
	except (IOError,Exception) as e:
		print e
		mylog.elog(g_tag,'create log failed and return False!')
		return False
	finally:
		return True


def writeEnv():
	fp = open(Elog, 'w')
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
		if not os.path.exists(Elog):
			print "In writeEnv Elog is not exist!"
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
		mylog.elog(g_tag, 'write env to Elog failed!')
		return False
	finally:
		fp.close()
		return True
	
						

#处理日志接口
def logProcess(begNum=0, tolNum=0):
	try:
		print 'benNum and tol Num are:', begNum, tolNum
		Awk = "awk '{print $7}' %s > %s " % (Ulog, Gout)
		res = commands.getstatusoutput(Awk)[0]
		total = int(commands.getoutput('wc -l  %s' % Gout).split()[0])
		if cmp(total, 0) ==0:
			print 'glxglears.out is an empty file!'
			mylog.elog(g_tag, 'glxglears.out is an empty file!')
			return False
	
		#如果总数小于开始行号
		if total <=begNum:
				begNum =2
				tolNum = total
		elif total <= tolNum:
				tolNum = total
		#计算出求平均的行--包含起始行
		AvgCount = tolNum - begNum
		AvgCount +=1
		print 'need %d lines to caculate Avg value' % AvgCount
		os.system('chmod a+x %s/resource/AvgCaluate.sh' % g_currentPath)
		rst = os.system('sh %s/resource/AvgCaluate.sh %d %d' % (g_currentPath, begNum, tolNum))
		if cmp(rst, 0) !=0:
			print 'AvgCaluate.sh exec failed!'
			mylog.elog(g_tag, 'AvgCaluate.sh exec failed!')
	except (ValueError,Exception) as e:
		print 'logProcess func exec failed',e
	finally:
		return True
	
	

#make results 
#make see |tee $result
#用来执行lmbench 测试
def work():
	try:
		print 'The current Path0:', commands.getstatusoutput('pwd')[1]
		resDir = g_currentPath + '/resource' 
		cmpDir = g_currentPath + '/resource/lmbench3' 
		os.chdir(resDir)
		print 'The current Path1:', commands.getstatusoutput('pwd')[1]
		os.system('tar xvf %s' % benchMark)
		if not os.path.exists('%s/resource/lmbench3' % g_currentPath):
			print 'tar package decompress failed'
		else: 
			os.chdir(cmpDir)
		print 'The current Path2:', commands.getstatusoutput('pwd')[1]
		res0 = os.system('make results')
		res1 = os.system('make see | tee -a %s' % Ulog)
		if (cmp(res, 0) !=0) or (cmp(res1, '0') !=0):
			print 'lmbench exec failed!'
		print 'Start lmbench  successfully!'
	except (IndexError, ValueError) as e:
		print 'work function exec failed!'
		mylog.elog(g_tag, 'work function exec failed!')
		return False
	finally:
		return True
	

#define main function
def main():
	global passwd
	global core_num

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
	#运行次数
	dataNode = obj.getXMLNode(doc, 'data',0)
  	tdNode = obj.getXMLNode(dataNode, 'count', 0)
 	Cnode = obj.getXMLNodeValue(tdNode, 0)
	print "lmbench will run with %dtimes." % Cnode
	checkDir(g_currentPath + '/resource')
	createLog()
	writeEnv()
	print 'Entering work function!.....'
	work()
	#Sshot.scrprint(g_tag,'Before_Test',g_currentPath)
	#for item in range(cntNode):
		#执行unix bench的函数
	#	Sshot.scrprint(g_tag,'The-%dth-test' % item,g_currentPath)
	#	work()
	#Sshot.scrprint(g_tag,'After_Test',g_currentPath)

	os.system('rm -rf %s/resource/lmbench3' % g_currentPath)
	#logProcess(begNum, tolNum)
	time.sleep(1)
	sys.exit()

if __name__ == "__main__":
	main()





