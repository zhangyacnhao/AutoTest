#!/bin/bash 
#conding:utf8

#user password
passwd=$1
#os name
osName=$(cat /etc/issue | head -1 | awk '{print $(NF-4)}')
osVern=$(cat /etc/issue | head -1 | awk '{print $(NF-2)}')
#date
Date=$(date +%D-%H:%M)

function helpMsg()
{
	echo $#
	if [ $# -ne 1 ]; then
		echo "Usage: $0 password"
		exit 0
	fi	
	return 
}

function osJudge()
{
	echo "The current os: ${osName} version: ${osVern}."
	[ '$osName' != 'Fedora' -a '$osVern' != '21' ] || {
		echo "${Date}-This script not match current OS." | tee -a excelPro.log
		exit 0
	}
	echo "OS judge pass,beginning to install ... ... "
	return 
}

#function install()
#{
#	echo $passwd | sudo -S yum -y localinstall *.rpm
#	path=$(pwd)
#	if [ ! -f xlutils-1.7.1.tar.gz ];then
#		echo "${Date}-Error: Source tar package not found." | tee -a excelPro.log
#		exit -1
#	fi
#
#	tar xvf xlutils-1.7.1.tar.gz && cd xlutils-1.7.1 || {
#		echo "${Date}-Error: Please check the tar package if complete or not." | tee -a excelPro.log
#	}
#	echo "The current path: ${path}"
#	python setup.py build && echo $passwd | sudo -S python setup.py install
#	if [ $? != 0 ];then
#		echo "${Date}-Install xlutils failed." | tee -a excelPro.log
#	fi
#	
#	return 
#
#}

function pExcelIns()
{
	echo $passwd | sudo -S yum -y localinstall *.rpm
	path=$(pwd)
	if [ ! -f  xlutils-1.7.1.tar.gz ]; then
		echo "${Date}-Error: Source tar package not fount." | tee -a excelPro.log
	fi
	
	tar xvf xlutils-1.7.1.tar.gz && cd  xlutils-1.7.1 || {
		echo "${Date}-Error: Please check the tar package if complete or not." | tee -a excelPro.log
	}
	
	python setup.py build && echo $passwd | sudo -S python setup.py install

	if [ $? != 0 ];then
		echo "${Date}-Install xlutils failed." | tee -a excelPro.log
	fi
	cd $path
	return 
}

function clean()
{
	echo "Beginning to remove old directory(passwd:${passwd})...... "
	echo $passwd | sudo -S rm -rf xlutils-1.7.1 || {
		echo "${Date}-clean work exec failed." | tee -a excelPro.log
	}
	echo "clean work finished ... ... "
}

function Main()
{	
	if [ -f excelPro.log ];then
		echo "" > excelPro.log
	else
		touch excelPro.log
	fi
	helpMsg $@
	osJudge
	pExcelIns
	clean 
	echo "python Excel packages install completely."
	exit 0

}

#call Entry
Main $@
