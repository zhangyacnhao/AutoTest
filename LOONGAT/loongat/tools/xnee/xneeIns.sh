#!/bin/bash
#set encoding=utf-8
#Author: vans
#E_mail: muwang86@126.com
#QQ_info: 244922979
#Function: install xnee-3.19
#version:1.0.0-for test


#input password
passWD=$1
#Date
Date=$(date +%D-%H:%M)
#deps 
deps=xnee-deps.tar.bz2
source=xnee-3.19.tar.gz


function helpMsg()
{
	if [ $# -ne 1 ];then
		echo "${Date}-Usage: ${0} passwd ."
		exit 0
	fi 
	return 0
}


function xneedepIns()
{
	echo "In function xneedepIns ... ..."
	if [ ! -f $deps ];then
		echo "${Date}-${deps} file not found." | tee -a xneeIns.log
		exit -1	
	fi
	tar jxvf $deps || {
		echo "${Date}-decompress ${deps} failed." | tee -a xneeIns.log
		echo  "Please check the tar package:${deps} is complete or not." | tee -a xneeIns.log
		exit -2
	}

	echo $passWD | sudo -S yum -y localinstall xnee-deps/*.rpm
	if [ $? != 0 ]; then 
	{
		echo "${Date}-install xnee deps failed" | tee -a xneeIns.log
		echo "Please check the Authority."
	}
	fi
	echo "Install xnee deps successifully"
	return 0
	
}


function xneeIns()
{
	local path=$(pwd)
	echo "In function xneedep Ins ... ..."
	if [ ! -f $source ]; then
		echo "${Date}-${source} file not found." | tee -a xneeIns.log
		exit -1	
	fi
	
	tar xvf $source || {
		echo "${Date}-decompress ${source} failed." | tee -a xneeIns.log
		echo  "Please check the tar package:${source} is complete or not."
		exit -2
	}
	
	cd xnee-3.19 && ./configure 
	if [ $? != 0 ]; then
		echo "${Date}-xnee-3.19 configure failed." | tee -a xneeIns.log
	fi
	make  &&  echo $passWD | sudo -S make install  
	if [ $? != 0 ]; then
		echo "${Date}-xnee-3.19 make or install  failed." | tee -a xneeIns.log
	fi
	cd $path
	echo "The current path:" ${path}
	echo "xnee install finished."
	return 0
		
}

function xneeClean()
{
	echo " In xneeClean function ... ... "
	echo $passWD | sudo -S rm -rf xnee-deps xnee-3.19 
	[ $? != 0 ] || {
		echo "remove xnee temp directory failed" | tee -a xneeIns.log
		echo "Please check the Authority."
	}
	echo "xnee clean work finished."
	return 0
}


function Main()
{
	helpMsg $@
	xneedepIns
	xneeIns
	xneeClean
	echo "Xnee-3.19 install completed."
}

Main $@



