#!/bin/sh
#Date: 2015-10-13
#Author: Vans

#从XML 传递下来的时间参数
time=$1
#从python 文件中传递下来的参数
core_num=$2
#从python 文件传递下来的参数
pass=$3

path=$(dirname $(readlink -f $0))
dLog=$(dirname $path)/result/dbench.log
target=$(dirname $path)/resource/dbench-3.03
function help()
{
	if [ $#  -lt 3 ];then
		echo "Usage: ./dbench.sh -t time core_num passwd"
		exit 0
	else
		echo "Begining  ... ..."
	fi	
} 

function install()
{
	if [ ! -f dbench-3.03.tar.gz ];then
		echo "Source tar file not found!"
		exit 0
	else
		if [ -d dbench-3.03 ];then
			echo "delete history files!"
			echo $pass | sudo -S rm -rf dbench-3.03
		fi
		tar xvf dbench-3.03.tar.gz
		if [ $? != 0 ];then
			echo "Please check source tar file is complete or not?"
			exit 0		
		fi
		cd dbench-3.03
		echo "Begining compling... ..."
		make clean
		./configure && make -j4
		echo $pass | sudo -S make install
		if [ $? != 0 ];then
			echo "dbench install failed"
			exit 0		
		fi		
	fi	
}


function Work()
{
	help $@
	install
	
	if [ ! -f $dLog ];then
		echo "dbench.log doesn't exists!"
		exit 0
	fi
	echo $pass | sudo -S /usr/local/bin/dbench -t $time $core_num | tee -a $dLog
	if [ $? != 0 ]; then
		echo "dbench exec failed"
		exit 0	
	fi
	sync
	sync

	echo $pass | sudo -S rm -rf $target
	if [ $? != 0 ];
	then
		echo "delete target dbench-3.03 failed!"
	fi
	
	exit 0
	
}

Work $@ 
