#!/bin/sh

#*************************************
# Firefox test on Fedora 13
# Date:2015.07.29
# Author: Loongson
# version: 1.0.0
#*************************************

path=`pwd`
echo "The current path is:"
echo $path

cd $path/resource/
#log=../result/Firefox.log
#elog=../result/FirefoxE.log

os=`cat /etc/issue | head -1 | awk '{ print $1}'`
ver=`cat /etc/issue | head -1 | awk '{ print $3} '`
[ -e ~/下载/百度一下，你就知道.html ] && rm -f ~/下载/百度一下，你就知道.html
if [ -e $path/result/ Firefox.log ]; then
	rm -f $path/result/Firefox.log
	touch $path/result/Firefox.log
	echo "create Firefox.log successfully!"
else
	touch $path/result/Firefox.log
	echo "create Firefox.log successfully!"
fi


if [ $os != "Fedora" ] && [ $ver != 13 ]; then
	echo "This script is for Fedora 13" | tee -a Firefox.log
	exit 0
fi



if [ ! -e Firefox.xns ];then
	echo "Macro file is not exist!" | tee -a Firefox.log
	exit 0

fi

cnee -rep -f Firefox.xns -e $path/result/FirefoxE.log -t 2s

if [ $? != 0 ];then
	echo "cnee excute failed!" >> $path/result/FirefoxE.log
	exit 0
fi

exit 0




