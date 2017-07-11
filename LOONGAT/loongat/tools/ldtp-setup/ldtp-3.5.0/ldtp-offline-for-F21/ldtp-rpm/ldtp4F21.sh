#!/bin/bash

currentPath=`pwd`
passwd=$1

function helpMsg()
{	
	if [ $# -ne 1 ]; then
		echo "Arguments Error; Usage: $0 password"
		exit 1
	fi 
}

function Work()
{
	helpMsg $@
	#install deps 
	#echo "$passwd" | sudo -S rpm -ivh *.rpm		   
	echo "$passwd" | sudo -S yum -y localinstall *.rpm
	if [ ! -f ldtp-ea.tar.bz2 ];then
		echo "Not Find ldtp-ea.tar.bz2"
		exit 0
	fi

	tar jxvf ldtp-ea.tar.bz2
	cp ldtp-ea/.bashrc /home/$USER/ -f
	echo "$passwd" | sudo -S mv ldtp-ea/ldtp0 /usr/bin/ 
	echo "$passwd" | sudo -S mv /usr/bin/ldtp0 /usr/bin/ldtp 
	echo "$passwd" | sudo -S cp -r ldtp-ea/ldtp* /usr/lib/python2.7/site-packages/ -f 
	echo "Ldtp install completed."
	rm -rf ldtp-ea
	exit 
}

Work "$@"
