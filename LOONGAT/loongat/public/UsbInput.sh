#!/bin/bash
# 功能：此脚本用来使能或禁止USB 键盘和鼠标在测试过程中的行为
# 日期：2015-08-26
# 作者：Vans

# $1:enable or disable

function helpMsg()
{
	if [ $# -ne 1 ] || [ "$1" != "enable" ] && [ "$1" != "disable" ]; then
		echo "Usage: $0 <enable | disable>"
		exit 1
	fi
}

function usbWork()
{
	# 激活USB 键盘鼠标
	if [ "$1" = "enable" ]; then
		while read LINE 
			do 
			for IF in $LINE
				do
				# echo $IF;
				echo $IF > /sys/bus/usb/drivers/usb/bind;
				done
			done < /tmp/usb
		exit 0
	fi

	# 禁止USB 键盘鼠标
	if [ "$1" = "disable" ]; then
		USBIF=`ls /sys/bus/usb/drivers/usb | grep -`
		echo $USBIF > /tmp/usb
		for IF in $USBIF
			do
			# echo $IF;
			echo $IF > /sys/bus/usb/drivers/usb/unbind;
			done
		exit 0
	fi
}

function Main()
{
	helpMsg $@
	usbWork $@
}


Main $@
