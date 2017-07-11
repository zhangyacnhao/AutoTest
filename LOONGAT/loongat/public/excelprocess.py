#!/usr/bin/python
#coding=utf-8
#############################################################################
#
# LOONGSON Auto-test Tool Project
# class excelProcess
#This module uses python logging module to process loongat logs
#Version:1.0.1
#Author:Vans
#name style: if multiwords in a name, from sceond word,first letter must be upcase.
#Date:2015-09-02
#############################################################################

import xlwt
import xlrd
import xlutils
from mmap import mmap,ACCESS_READ
from datetime import date,time,datetime
from decimal import Decimal
from xlwt.Utils import *
#from xlrd import open_workbook
#from xlwt import easyxf
from xlutils.copy import copy

g_tag = 'excelprocess'
dateFromat=xlwt.easyxf(num_format_str='D-MMM-YYY')

class excelProcess(object):
	#constructor default result name
	def __init__(self,defname="Result.xls"):
		self.fileName=defname
		self.dateStyle=dateFromat
		#self.currentPath = os.environ['AUTOTEST_PUBLIC_LIB']
		#self.currentPasswdPath = self.currentPath + '/.passwd'

	"""
	@TODO open function	
	@RETN: an xlrd.Workbook instance
    	"""
	
	def openWithFile(self):
		print xlrd.open_workbook(self.fileName)
		return xlrd.open_workbook(self.fileName)

    	def openWithMmap(self):
		try:
			fp=open(self.fileName, 'rb+')
		except Exception ,e:
			print str(e)
			print "Error: Open %s file failed." % self.fileName
		else:
			print xlrd.open_workbook(fileContents=mmap(fp.fileno, 0, access=ACCESS_READ))
			return xlrd.open_workbook(fileContents=mmap(fp.fileno, 0, access=ACCESS_READ))

    	def openWithString(self):
		try:
			aString=open(self.fileName, 'rb+').read()
		except Exception ,e:
			print str(e)
			print "Error: Open %s file failed." % self.fileName
		else:
			print  xlrd.open_workbook(file_contents=aString)
			return xlrd.open_workbook(file_contents=aString)

	"""
	@TODO: get sheet name
	@RETN: the sheet name list in current Workbook		
	"""
    	def getSheetNameList(self, wb):
		try:
			nameList=[]
			for s in wb.sheets():
				print 'Sheet Name:',s.name
				nameList.append(s.name)
		except Exception,e:
			print str(e)
			print "Error: get Sheet name list failed."
		else:
			return nameList
	
   	def getSheetContent(self, sheet):
		try:
			print "Sheet Name:",sheet.name
			for row in range(sheet.nrows):
				values = []
				for col in range(sheet.ncols):
					values.append(sheet.cell(row,col).value)
			#print ','.join(values)
			print values
		except Exception ,e:
			print str(e)
			print "Error: get Sheet Content failed."
		else:
			return None

    	def getContentAll(self, wb):
		try:

			for s in wb.sheets():
				getSheetContent(s)
			print
		except Exception,e:
			print str(e)
			print "Error: get all Content Workbook failed."
		else:
			return None

	"""
		@TODO: via sheetName get content
		@RETN: return specific Sheet content
	"""
    	def getContentByName(self, wb,SheetName):  #
		try:
			s = wb.sheet_by_name(SheetName)
			getSheetContent(s)
		except Exception,e:
			print str(e)
			print "get content by name failed."
		else:
			return None

	def getContentByIndex(wb,Index):
		try:
			s = wb.sheet_by_index(Index)
			getSheetContent(s)
		except Exception,e;
		       print str(e)
		       print "get content by index failed."
		else:
			return None
		
	
	def getNsheets(self, wb):
		print 'workbook  has %d sheets' % wb.nsheets
		return wb.nsheets

	def getsheetNameList(self, wb):
		print 'workbook name list:' wb.sheet_names()
		return wb.sheet_names()

	def getSheetObjects(self, wb):
		for sheet_index in range(wb.nsheets):
			print book.sheet_by_index(sheet_index)

		for sheet_name in wb.sheet_names():
			print book.sheet_by_name(sheet_name)

		for sheet in book.sheets():
			print sheet


	def introspectSheet(self, sheet):
		print "Sheet Name:", sheet.name
		print "Sheet Rows:", sheet.nrows
		print "Sheet COls:", sheet.ncols
		for row_index in range(sheet.nrows):
			for col_index in range(sheet.ncols):
				print cellname(row_index, col_index), '-'
				print sheet.cell(row_index, col_index).value

	def getCellInfo(self, sheet,row_index , col_index):
		cell =sheet.cell(row_index, col_index)
		print "Cell:", cell
		print "Cell Value:", cell.value
		print "Cell Ctype:", cell.ctype 

	def getWholeRowInfo(self, sheet ,row_index):
		print "Row info:",sheet.row(row_index)
		print "Row value:",sheet.row_values(row_index)
		print "Row types:",sheet.row_types(row_index)
		return sheet.row(row_index)

	def getWholeColInfo(self, sheet, col_index):
		print "Row info:",sheet.col(col_index)
		print "Row value:",sheet.col_values(col_index)
		print "Row types:",sheet.col_types(col_index)
		return sheet.col(col_index)

	def cellName(self, row_index, col_index):
		return cellname(row_index, col_index)

	def cellAbsName(self, row_index,col_index):
		return cellnameabs(row_index, col_index)

	def colName(self, col_index):
		return colname(col_index)

	def getCellValue(self, sheet, row_index, col_index):
		return sheet.cell(row_index, col_index).value
		#returen sheet.cell_value(row_index, col_index)

	def getSheetByName(self, wb, sheetName):
		return wb.add_sheet(sheetName,cell_overwrite_ok=True)
	def getSheetbyindex(wb, sheetIndex)
		return wb.get_sheet(sheetIndex)

	def getRowByIndex(self, sheet, row_index):
		return sheet.row(row_index)

	#row obj write method
	def wirteByRow(self, rowNum,col_index, value):
		rowNum.write(col_index,value)
		#sheet2.row(0).write(0,'Sheet 2 A1')

	def writeBySheet(self, sheet, row_index, col_index, value):
		sheet.write(row_index, col_index, value)		

    	def setColWidth(self, colNum, intobj):
		"""
		:type colNum: object
		"""
		colNum.width(intobj)
	
	def setColHidden(self, colNum, boolen):
		colNUm.hidden(boolen)	

	def workSave(self, wb, saveName):
		print "Current file will be saved to %s" % saveName
		wb.save(saveName)

	def flushRowData(self, sheet):
		sheet.flush_row_data()
	
	def setCellNum(self, rowobj,col_index, value):
		rowobj.set_cell_number(col_index,value)

	def setCellBool(self,rowobj,col_index,value):
		rowobj.set_cell_boolean(col_index,value)

	def setCellError(self, rowobj,col_index,value):
		rowobj,set_cell_error(col_index, value)

	def setCellDate(self, rowobj,col_index,value):
		rowobj.set_cell_date(col_index,datetime.now(),self.dateFromat)

	def setCellBlank(self, rowobj, col_index, easyxf):
		rowobj.set_cell_blank(col_index,easyxf)

	def setCellMulblank(rowobj,start, end,easyxf):
		rowobj.set_cell_mulblank(start,end,easyxf)

	def colByName(colname):
		return col_by_name(colname)

	def cellToRowCol(cell):
		return cell_to_rowcol(cell)

	def cellToRowCol2(cell):  #A1 -->(0,0)
		return cell_to_rowcol2(cell)

	def rowColToCell(rowx, colx):   #(0,0) -->A1
		return rowcol_to_cell(rowx,colx)
	"""
	@convert a xlrd workbook obj to xlwt  workbook obj
	"""
	def convertWookbook(xlrdWb):
		return copy(xlrdWb)

"""
if __name__ == '__main__'
	result=Unixbench.xls
	#instance 
	obj = Excelprocess(g_tag, g_currentPath + '/' + g_tag + 'result/Unixbench.xls')
"""

