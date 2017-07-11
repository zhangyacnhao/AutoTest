#!/bin/sh

#*************************************
# Evolution test on Fedora 13
# Date:2015.07.29
# Author: Loongson
# version: 1.0.0
#*************************************

path=`pwd`
echo "The current path is:"
echo $path

cd $path/resource/
#log=../result/Evolution.log
#elog=../result/EvolutionE.log

os=`cat /etc/issue | head -1 | awk '{ print $1}'`
ver=`cat /etc/issue | head -1 | awk '{ print $3} '`


if [ -e $path/result/ Evolution.log ]; then
	rm -f $path/result/Evolution.log
	touch $path/result/Evolution.log
	echo "create Evolution.log successfully!"
else
	touch $path/result/Evolution.log
	echo "create Evolution.log successfully!"
fi


if [ $os != "Fedora" ] && [ $ver != 13 ]; then
	echo "This script is for Fedora 13" | tee -a Evolution.log
	exit 0
fi



if [ ! -e Evolution.xns ];then
	echo "Macro file is not exist!" | tee -a Evolution.log
	exit 0

fi

cnee -rep -f Evolution.xns -e $path/result/EvolutionE.log -t 2s

if [ $? != 0 ];then
	echo "cnee excute failed!" >> $path/result/EvolutionE.log
	exit 0
fi

exit 0




