#!/bin/bash
###################################################
# This script is used to copy system logs
##################################################

#拷贝/var/log 
function cpSysLogs()
{
	#定义函数的局部变量
	local outputDir="${1}"
	local passwd="${2}"

	#打包完成后日志名称
	varFileName="varlog.tar.gz"
	#打包系统/var/log 目录下的所有日志
	echo "${passwd}" | sudo -S tar czvf "${varFileName}" /var/log
	echo "${passwd}" | sudo -S chmod 666 "${varFileName}"
	#拷贝打包后的日志到输出目录并删除压缩包
	cp "${varFileName}" "$outputDir"
	echo "${passwd}" | sudo -S rm "${varFileName}"
	echo "System log copy ok."
}

#备份日志
function cpLogs()
{
	#定义局部变量
	local outputDir="$1"
	local loongatFolderPath="$2"
	local logDir="$outputDir/log"

	mkdir -p "${logDir}"
	
	if [ $? -eq 0 ]; then
		echo "Create log backup directory Failed!"
	fi
	
	#拷贝上次运行的日志到备份目录
	cp -r "$loongatFolderPath/log" "${logDir}"
	
	#判断是否执行成功
	if [ $? -eq 0 ]; then
		echo "Loongat log copy ok."
		return 0
	else
		echo "ERROR: for copy and remove log"
		return 1
	fi
}

#拷贝所有测试用例的result和screenshot目录里的文件
#备份case测试结果 
function caseResults()
{
	local outputDir="$1"
	local loongatFolderPath="$2"

	cd "${loongatFolderPath}" # in "loongat" dir root path
	find . -name "result" | xargs -i  cp --parent -fr {} "${outputDir}"
	find . -name "screenshot" | xargs -i cp --parent -fr {} "${outputDir}"

	echo "Result and screenshot copy ok."

}

#完成拷贝之后进行打包
function tarLogs()
{
	local outputDir="$1"
	local tarOutputFolder="$2"
	cd "`dirname "${outputDir}"`"

	local baseDir="`basename $outputDir`"
	#打包日志
	tar czvf "$tarOutputFolder/log-loongat-$label.tar.gz" "${baseDir}"

	if [ $? -eq 0 ]; then
		rm -r "${baseDir}"
	else
		echo "Error: Cannot tar the log folder $outputDir"
	fi
}

#删除日志目录
function deleteFolderFiles()
{
	local folderList="${1}"

	for folder in "${folderList}"; do
		if [ -d "${folder}" ]; then
			echo "folder is ${folder}"
			rm -r "${folder}"
			mkdir "${folder}"
		fi
	done
}

#删除日志
function deltLogs()
{
	local loongatFolderPath=${1}
	# delete log in "log" folder
	echo "${loongatFolderPath}"
	rm -r "${loongatFolderPath}/log"
	mkdir "${loongatFolderPath}/log"

	# ####################################################
	# 删除存在测试用例screenshot 和result 目录的log文件
	local folderResult=`find "${loongatFolderPath}" -name "result"`
	deleteFolderFiles "${folderResult}"
	# #####################################################
	local folderScreen=`find "${loongatFolderPath}" -name "screenshot"`
	deleteFolderFiles "${folderScreen}"
}

if [ $# -ne 4 ]; then 
	echo "Usage: ./tarlog.sh loongatFolderAbsolutePath tarOutputFileFolderAbsolutePath label passwd"
else
	loongatFolderPath="$1"
	tarOutputFolder="$2"
	label="$3"
	passwd="$4"
	#备份日志输出目录
	outputDir="`dirname ${loongatFolderPath}`/loongat-log-bak"
	echo "The folder stored logs might under the folder ${outputDir}"

	# make backup directory to store logs, tar this folder when copy action finished
	mkdir -p "${outputDir}"

	# 拷贝系统日志/var/log
	cpSysLogs "${outputDir}" "${passwd}"

	# 备份拷贝好的日志
	cpLogs "${outputDir}" "${loongatFolderPath}"

	# 备份用例的result && screenshot files
	caseResults "${outputDir}" "${loongatFolderPath}"
	#打包备份好的log
	tarLogs "${outputDir}" "${tarOutputFolder}"
	#删除log目录，只留打包好的日志压缩包
	deltLogs "${loongatFolderPath}"
fi
