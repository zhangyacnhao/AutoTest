#!/bin/bash
###########################################################
# launch.sh
# Use this script to launch program Output
# $1: user password
# $2: output directory
###########################################################

tag="launch.sh"
#获取OS 的名称
osName=`cat /etc/issue | head -1 | awk '{print $(NF-4)}'`
osVer=`cat /etc/issue | head -1 | awk '{print $(NF-2)}'`
#获取CPU 字长
OSBit0=`getconf WORD_BIT`
OSBit1=`getconf LONG_BIT`


function chMode()
{
    	chmod +x -R *
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

function lancher()
{
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

    # 检查参数个数
    if [ $# -ne 2 ]; then
        echo "${tag} Arguments Error; Usage: ./launch.sh password AbsoluteDirectoryPath"    
        return
    fi

    insLDTP "$@"
    launchUI "$@"
}

lancher "$@"
