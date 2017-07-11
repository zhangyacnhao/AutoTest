#!/bin/bash
#Fedora 13/21 ldtp 安装脚本
#Author:Vans

password=$1
osInfo=`head -n +1 /etc/issue` 
hasLdtp=`whereis ldtp`
savePath=`$pwd`
BASEDIR=`dirname $0`

function helpMsg()
{
	if [ $# -ne 1 ]; then
		echo "Arguments Error; Usage: $0 <password>"
		exit 1
	fi 

}

function Work()
{
	helpMsg $@
	if [ "$hasLdtp" != "ldtp:" ]; then
		echo "LDTP installed!"
	else    
	
		case $osInfo in 
        *"release 13"*) echo "Fedora 13"
            if [ $(getconf WORD_BIT) = '32' ] && [ $(getconf LONG_BIT) = '64' ] ; then
                echo "64 bit computer"
            else
                echo "32 bit computer"
                abspath=$(dirname $(readlink -f $0))
                pkgpath="${abspath}/ldtp-3.5.0/ldtp-offline-for-F13/ldtp-rpm"
                cd "${pkgpath}"
                echo "$password" | sudo -S chmod a+x ldtp-offline-install.sh
                ./ldtp-offline-install.sh $password 
            fi ;;
            
        *"release 21"*) echo "Fedora 21"
            if [ $(getconf WORD_BIT) = '32' ] && [ $(getconf LONG_BIT) = '64' ]; then
                echo "64 bit computer"             
				cd "$BASEDIR/ldtp-3.5.0/ldtp-offline-for-F21/ldtp-rpm"
                echo "$password" | sudo -S chmod a+x ldtp4F21.sh
                ./ldtp4F21.sh $password
            else 
                echo "32 bit computer"

            fi;; 
            
		esac

		cd "$savePath"
		hasLdtp=`whereis ldtp`
		if [ "$hasLdtp" != "ldtp:" ]; then
			echo "LDTP installed!"
		fi
    
	fi
}

Work $@






 












