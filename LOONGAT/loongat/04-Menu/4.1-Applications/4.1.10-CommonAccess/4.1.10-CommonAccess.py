#!/usr/bin/env python
#coding=utf-8

#########################################################################
# 4.1.10-CommonAccess.py
# Module for WPS test
#########################################################################

import os
import sys

g_tag = '4.1.9-Others'
g_currentPath = sys.path[0] # set current running directory
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB'] # set path of public lib directory
sys.path.append(g_publicLibPath) #import file library

from moduleobject import Module
import logcase

def main():
    totalXMLPath = g_currentPath + '/' + g_tag + '.xml'
    moduleObj = Module(g_tag, totalXMLPath, 'case', g_currentPath)
    moduleObj.run()
    
if __name__ == '__main__':
    main()
