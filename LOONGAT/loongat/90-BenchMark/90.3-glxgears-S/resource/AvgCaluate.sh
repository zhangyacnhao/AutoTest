#!/bin/sh
#Date: 2015-10-15
#Author: Vans

#
#不要从python 传递任何参数
path=$(dirname $(readlink -f $0))
gOut=$(dirname $path)/result/glxgears.out
#用来保存最终的计算结果
Result=$(dirname $path)/result/Result
#分别表示截至计算平均值的范畴
Bline=$1
Tline=$2
function help()
{
	if [ $#  -lt 2 ];then
		echo "Usage: ./AvgCaluate.sh begin-line total-line!"
		exit 0
	else
		echo "target file is: ${gOut}"
		echo "Begining  ... ..."	
	fi
} 



function Work()
{
	local Sum=0.0
	local Avg=0.0
	local Aline
	help $@

	if [ ! -f $gOut ];then
		echo "${gOut} doesn't exists!"
		exit 0
	fi
	#从Bline 行开始读取内容，然后计算平均值
	#awk '{Sum+=$1}END{print "Avg="Sum/NR"\nMax="Max}' text.txt
	
	#截取指定行
	awk "FNR>=$Bline && FNR <= $Tline{print}" $gOut > $Result
	#计算总和保留3位小数
	Sum=$(cat $Result | awk '{  Sum +=$1 } END {printf "%.3f\n",Sum}')
	echo "the sum is: ${Sum}"
	#计算平均值
	#计算平均值
	Tline=$(($Tline + 1))
	echo "Tline is ${Tline}, Bline is ${Bline}"
	#Tline= let "$Tline+1"
	
	echo "Tline is ${Tline}"
	Aline=$(($Tline - $Bline))
	echo "(************************************)"
	echo "need ${Aline} line to caculate Avg !"
	echo "(************************************)"
	Avg=$(echo "scale=7; $Sum/$Aline" | bc)
	echo "the avg is: ${Avg}"
	echo "平均值(Avg):${Avg}" >> $Result
	sync
	sync	
	rm -f $gOut
	exit 0
	
}

Work $@
