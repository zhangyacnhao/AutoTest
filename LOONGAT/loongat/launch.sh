#!/bin/bash
###########################################################
# launch.sh
# Use this script to launch program Output
# $1: user password
# $2: output directory
# Date: 2015-10-08
# Author: Vans
###########################################################

tag="launch.sh"
#root Path
rootDir=`pwd`
toolsPath="${rootDir}/tools/launchUI64" # default path
#获取OS 的名称
osName=`cat /etc/issue | head -1 | awk '{print $(NF-4)}'`
osVer=`cat /etc/issue | head -1 | awk '{print $(NF-2)}'`
#获取CPU 字长
OSBit0=`getconf WORD_BIT`
OSBit1=`getconf LONG_BIT`


function chMode()
{
    	chmod a+x  launch* libForUI/*
}

function ckOSBit()
{
	if [ $OSBit0 == 32 ] &&  [ $OSBit1 == 32 ]; then
		return 32
	elif [ $OSBit0 == 32 ] &&  [ $OSBit1 == 64 ]; then
		return 64 
	else
		echo "checkOSBit function failed!"
	fi
	return 0

}

function setS4Enable()
{
	#是否要执行case中所提到的S4 休眠
	if [ ${1} -eq 1 ]; then
		export S4_ENABLE='1'
	else
		export S4_ENABLE='0'
	fi
}

#启动QT 程序
function launchUI()
{
    chMode
    if [ $? -ne 0 ]; then
        echo "$tag: Error: chMode excute failed, please check the Authorization!."
        return 1
    fi

    #start UI 
    password=${1}
    directory=${2}
    if [ -f "launchUI" ]; then
        ./launchUI ${password} ${directory} 
    else
        echo "${tag}: Please check if launchUI in current directory"
    fi
}

#执行ldtp 安装脚本
function insLDTP()
{
    curpath=`pwd`
    scriptpath=$(dirname $(readlink -f $0))
    scriptpath=`dirname ${scriptpath}`
    scriptpath=${scriptpath}/ldtp-setup/install.sh

    cd `dirname ${0}`
    echo "${1}" | sudo -S chmod a+x ${scriptpath}
    ${scriptpath} ${1}
    cd ${curpath}
}


function usage()
{
    echo "${tag} Arguments Error; Usage: ./launch.sh password [-s4]"    
}

function launcher()
{
    #check para
    if [ $# -lt 1 ]; then
	usage
  	return
    fi

    #if ${2} exists
    if [ -n "${2}" ]; then
	if [ "${2}" != "-s4" ]; then
		usage
		return
	else
		set"${1}" "${rootDir}"
 	fi
    else
	setS4Enable "0"
    fi
   
    #保留函数返回    
    ckOSBit 64
    res=$? #保留返回
    if [ "$res" = "64" ]; then
        echo "${tag}: This os is a 64 bit OS"
    elif [ "$res" = "32" ]; then
	echo "${tag}: This os is a 32 bit OS"
    else
	echo "No matched OSBit!"
	return 
    fi

    cd "${toolsPath}"
    echo "S4 status : ${S4_ENABLE}" 
    #判断ldtp 是否安装，否则执行安装操作
    insLDTP "${1}"
    #launch Qt
    launchUI "${1}" "${rootDir}"
}

launcher "$@"
