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
gLog = 'touch %s/result/glxgears.log' % g_currentPath
Glog = '%s/result/glxgears.log' % g_currentPath
#用来保存shell 处理的数据
Gout = '%s/result/glxgears.out' % g_currentPath
global passwd
global core_num
global second
global thread
#*****************************************   
#case label
g_tag = '90.3-glxgears-S'  
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
		res0 = commands.getstatusoutput(eLog)[0]
		if cmp(res0,0):
			print 'Create envInfo.log failed,please check the authority'
		res1 = commands.getstatusoutput(gLog)[0]
		if cmp(res1,0):
			print 'Create glxgears.log failed,please check the authority'
		
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

#默认情况
def glxPress():
	try:
		print 'Begining to glxgears S-press test!'
		#执行glxgears 测试
		res = os.system('vblank_mode=0 glxgears | tee -a %s' %  Glog)
		if not cmp(res, '0'):
			print "glxgears S-press test failed!"
	except (StandardError,Exception) as e:
		mylog.elog(g_tag, 'glexgears benchmark test failed.')
		return False
	finally:
		return True



#关闭glxgears
def closeGlx():
	try:
		winlst = commands.getstatusoutput('xdotool search --onlyvisible --name glxgears')[1].split('\n')
		print 'Associated window list is:', winlst
		for item in winlst:
			commands.getstatusoutput("xdotool windowactivate --sync %s sleep 1 key 'Escape'" % item)
		
		#最后比较保守的方法
		res = os.system('pkill glxgears')
		if  cmp(res, 256) == 0:
			print 'close glxgears normally!'
	except (ValueError, Exception) as e:
		print e
		mylog.elog(g_tag, 'closeGlx function exec failed!')
	finally:
		return True

					

#处理日志接口
def logProcess(begNum=0, tolNum=0):
	try:
		print 'benNum and tol Num are:', begNum, tolNum
		Awk = "awk '{print $7}' %s > %s " % (Glog, Gout)
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
	
				
# xdotool search --onlyvisible --name glxgears sleep 1 windowactivate key "Escape"

#关闭glxgears
def clsGlxgears():
	try:
		print 'Begining to close glxgears window!'
		Escape = 'xdotool search --onlyvisible --name glxgears sleep 1 windowactivate --sync key "Escape"'
		Search = 'xdotool search --onlyvisible --name glxgears'
		Count  = 'xdotool search --onlyvisible --name glxgears | wc -l'
		commands.getstatusoutput(Escape)
		commands.getstatusoutput(Escape)
		res = commands.getstatusoutput(Search)[1]
		if cmp(res, ''):
			#统计有多少个窗口
			count = commands.getstatusoutput(Search)[1]
			print 'You have to minimize %d windows!'
	except (ValueError,Exception) as e:
		print e
		os.system('pkill glxgears')
	finally:
		return True
		
			

#define main function
def main():
	global passwd
	global core_num
	global second
	global thread
	# def __init__(self, caseName, xmlFileName = None):
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
	#开始行号
	rowNode0 = obj.getXMLNode(doc, 'data',0)
  	BegNode = obj.getXMLNode(rowNode0, 'begRow', 0)
 	begNum = obj.getXMLNodeValue(BegNode, 0)
	#抽取行数
	rowNode1 = obj.getXMLNode(doc, 'data',0)
  	CntNode = obj.getXMLNode(rowNode1, 'cntRow', 0)
 	tolNum = obj.getXMLNodeValue(CntNode, 0)
	#运行时间
	dataNode0 = obj.getXMLNode(doc, 'data', 0)
	durNode = obj.getXMLNode(dataNode0, 'duration', 0)
	duration = obj.getXMLNodeValue(durNode, 0)
	
	print 'For Debug: begin row : %d, total rows: %d, rum time: %s' % (begNum, tolNum, duration)
	second = timeProcess(duration)
	print  'glxgears will run %dS:.' % second
	checkDir(g_currentPath + '/resource')
	createLog()
	writeEnv()
	Sshot.scrprint(g_tag,'Before_Test',g_currentPath)
	#线程控制
	thread = threading.Timer(second, closeGlx)
	thread.start()
	#启动测试
	glxPress()
	#thread.join()
	Sshot.scrprint(g_tag,'After_Test',g_currentPath)
	logProcess(begNum, tolNum)
	time.sleep(1)
	sys.exit()

if __name__ == "__main__":
	main()





