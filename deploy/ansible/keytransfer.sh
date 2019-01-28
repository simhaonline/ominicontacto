#!/bin/bash

#
# Shell script para pasar a esquema deployer-deployed
#
# Autor: Andres Felipe Macias
#
arg1=$1
current_directory=`pwd`
SSHtransfer() {
  while true; do
      echo -e "Transfering the public key to $servidor server \n"
      ssh-copy-id -p $ssh_port -i ~/.ssh/id_rsa.pub -o ConnectTimeout=10 root@$ip
      ResultadoSSH=`echo $?`
      sleep 2
      if [ $ResultadoSSH -eq 0 ];then
          echo "######################################################"
          echo "##   The public key was transferred successfully    ##"
          echo "######################################################"
          echo -e "\n"
          break
      else
          echo -e "\n"
          echo "########################################################################"
          echo "##  There was a problem transfering the key, check it and try again   ##"
          echo "########################################################################"
          echo -e "\n"
          exit 1
      fi
  done
}

Info() {
  cd $current_directory
  if [ "$arg1" == "--aio" ]; then
    servers_ammount="`cat inventory | grep ansible_ssh_port | grep -v \"cluster server\" |wc -l`"
  elif [ "$arg1" == "--cluster" ]; then
    servers_ammount="`cat inventory | grep ansible_ssh_port | grep \"cluster server\" |wc -l`"
  fi
  for i in `seq 1 $servers_ammount`; do
    if [ "$arg1" == "--aio" ]; then
      line="`cat inventory | grep ansible_ssh_port | grep -v \"cluster server\" | sed -n ${i}p`"
    elif [ "$arg1" == "--cluster" ]; then
      line="`cat inventory | grep ansible_ssh_port | grep \"cluster server\" | sed -n ${i}p`"
    fi
    servidor="`echo $line |awk -F \" \" '{print $1}'`"
    ip="`echo $line |awk -F \" \" '{print $4}' |awk -F "=" '{print $2}' `"
    ssh_port="`echo $line |grep ansible_ssh_port |awk -F " " '{print $2}'|awk -F "=" '{print $2}'`"
    is_localhost="`cat inventory |grep ansible_connection|awk -F " " '{print $2}'`"
    if [ "$arg1" == "--aio" ]; then
      if [ "$is_localhost" != "ansible_connection=local" ]; then
        sed -i "s/\(^localhost\).*/localhost=1/" $current_directory/inventory
        SSHtransfer
      fi
    elif [ "$arg1" == "--cluster" ]; then
      SSHtransfer
    fi
  done
  printf "\033c"
}
Info