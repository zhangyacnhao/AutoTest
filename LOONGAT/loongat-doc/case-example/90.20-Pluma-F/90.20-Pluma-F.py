#!/usr/bin/env python 
#codeing:utf-8 

#import modules
import os
import sys
import commands
from ldtp import *
from ldtputils import *
from time import ctime,sleep

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
global passwd
global count
global plumaPid


#*****************************************   
g_tag = '90.20-Pluma-F'  

#define function

#fun1 check case directory
def ckDir(dirName):
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
def showHelp():
	try:
		winName = 'frmUnsavedDocument1-pluma'
		activatewindow(winName)
		if waittillguiexist(winName) ==1:
			print 'Catch target window!--showHelp'
			res = selectmenuitem(winName,'mnuHelp;mnuAbout')
			if res !=1:
				print 'pluma help window show failed'
			time.sleep(0.5)
			#screenshot
			Sshot.scrprint(g_tag,'showHelp',g_currentPath)
			activatewindow('dlgAboutPluma')
			if  waittillguiexist('dlgAboutPluma'):
				closewindow('dlgAboutPluma')
		if waittillguiexist('dlgAboutPluma') ==0:
			print 'close window successifully!'
			#os.system('echo %s | sudo -S kill -9 %d')
	except (IOError , Exception) as e:
			#addlog
			print e
	finally:
			return True

#func3 
def showContents():
	try:
		winName = 'frmUnsavedDocument1-pluma'
		activatewindow(winName)
		if waittillguiexist(winName) ==1:
			print 'Catch target window--showContents!'
			res = selectmenuitem(winName,'mnuHelp;mnuContents')
			time.sleep(2.5)
			if res !=1:
				print 'show contents failed'
			Sshot.scrprint(g_tag,'showCoutents',g_currentPath)
			activatewindow('frmPlumaManual')
			if waittillguiexist('frmPlumaManual') ==1:
				closewindow('frmPlumaManual')
		if waittillguiexist('frmPlumaManual') ==0:
			print 'show contents window successifully!'
			#os.system('echo %s | sudo -S kill -9 %d')
	except (IOError , Exception) as e:
			#addlog
			print e
	finally:
			return True
 
#func4
def writeCase():
	try:
		frm = 'frmUnsavedDocument1-pluma'
		activatewindow(frm)
		if waittillguiexist(frm) ==1:
			print 'catch target window!--writeCase'
			res =enterstring(frm,'txt1','This is a test case!')
			time.sleep(1)
			if res !=1:
				print 'enterstring failed'
				mylog.ilog(g_tag,'enter string failed!')
		print "enter content successifully"
		activatewindow(frm)
		keypress('<enter>')
		keyrelease('<enter>')
		#addlog
		activatewindow(frm)
	    	selectmenuitem(frm,'mnuEdit;mnuSelectAll')
		selectmenuitem(frm,'mnuEdit;mnuCopy')
		selectmenuitem(frm,'mnuEdit;mnuPaste')
		selectmenuitem(frm,'mnuEdit;mnuCopy')
		selectmenuitem(frm,'mnuEdit;mnuPaste')	
		Sshot.scrprint(g_tag,'writeCase',g_currentPath)
	except (IOError, Exception) as e:
		print e
	return True


#func5 
def saveAll():
	try:
    		frm = 'frmUnsavedDocument1-pluma'
		dlg = u'dlgSaveAs\u2026'
		activatewindow(frm)
		if waittillguiexist(frm) ==1:
			print 'catch target window!--saveAll'
			res = selectmenuitem(frm,'mnuDocuments;mnuSaveAll')
			if res != 1:
				print "show dlgSaveAll failed! "
				return False
		time.sleep(2)
		activatewindow(dlg)
		if waittillguiexist(dlg) ==1:
			settextvalue(u'dlgSaveAs\u2026','txtName',g_currentPath + '/result/SaveAll') #chgpath
		time.sleep(0.5)
		#if verifysettext(u'dlgSaveAs\u2026','txtName',g_currentPath + '/result/SaveAll') !=1:
		#	print "Enter File name failed!"
		#	mylog.wlog(g_tag,'saveAll-Failed')
		activatewindow(dlg)
		closewindow(dlg)
		mouseleftclick(dlg,'btnSave')
		closewindow(dlg)
		#sav = waittillguiexist(dlg)
		#if sav ==1:
		#	print "close dlg failed"
		closewindow(dlg)
	except (IOError, Exception) as e:
		print e
	finally:
			return True
		


#func5
def findCase():
	try:
    		frm = 'frmUnsavedDocument1-pluma'
		dlg = 'dlgFind'
		activatewindow(frm)	
		if waittillguiexist(frm) ==1:
			print 'catch target window!--findCase'
			keypress('<ctrl>')
			keypress('<f>')
			keyrelease('<ctrl>')
			keyrelease('<f>')

		if waittillguiexist('dlgFind') ==1:
			res = enterstring('dlgFind','txt1','case')
			if res !=1:
				print "enter case failed"
				closwindow(dlg)
		time.sleep(0.5)
		Sshot.scrprint(g_tag,'findCase',g_currentPath)
		mouseleftclick(dlg,'btnFind')
		mouseleftclick(dlg,'btnClose')
	except (IOError, Exception) as e:
		print e
	finally:
			return True
 

def quitApp():
	try:
    		frm = 'frmUnsavedDocument1-pluma'
		activatewindow(frm)	
		if waittillguiexist(frm) ==1:
			print 'catch target window!--quitApp'
			selectmenuitem(frm,'mnuFile;mnuQuit')
		if waittillguiexist('dlgQuestion') ==1:
			mouseleftclick('dlgQuestion','btnClosewithoutSaving')
		if waittillguiexist(frm) ==1:
			closewindow(frm)
		time.sleep(0.5)
		Sshot.scrprint(g_tag,'quitApp',g_currentPath)
	except (IOError, Exception) as e:
		print e
	finally:
			return True
 
def lauApp():
	global plumaPid
	closeWin()
	plumaPid=launchapp('pluma')
	maximizewindow('*pluma')
	

#close the preview window
def closeWin():
	try:
		os.system('pkill pluma')
		res = waittillguiexist('*pluma')
		if  res== 0:
			mylog.ilog(g_tag, 'close pluma successfully')
			print 'close pluma successfully'
		elif res ==1:
			mylog.elog(g_tag, 'close pluma failed')
			print 'close pluma failed!'
			return False
	except Exception as e:
			print e
			return False
	finally:
		return True


#
def Work():
	global plumaPid
	lauApp()
	print 'showHlep info!'
	showHelp()
	print 'show Contens info!'
	showContents()
	print 'Write case info!'
	writeCase()
	print 'find case info!'
	findCase()
	print 'Save all info!'
	saveAll()
	print 'quit pluma info!'
	quitApp()
	if waittillguiexist('*pluma') !=0:
		print "pluma app quit failed"
		os.system('kill -9  %d' % plumaPid)
	return True


#define main function
def main():
	global passwd
	global fName
	ckDir(g_currentPath + '/resource')
	obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	os_type = obj.getOSName()
	if cmp(os_type, 'Fedora 21') !=0:
		print "This case only run Fedora 21"
		mylog.elog(g_tag,'OS matched failed!')
		sys.exit()
   	doc = obj.getDocumentNode()  
    	dataNode = obj.getXMLNode(doc, 'data',0)
  	countNode = obj.getXMLNode(dataNode, 'count', 0)
 	count= obj.getXMLNodeValue(countNode, 0)
	print  'You need do times: ',count
	for item in range(count):
		Work()
	time.sleep(0.1)
	sys.exit()

if __name__ == "__main__":
	main()





