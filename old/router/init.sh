#!/bin/bash

RN=$1 # Router id
NFCONF="iptables.init"

OK='[  \033[0;32mOK\033[0m  ] '
ERR='[ \033[0;31mERRO\033[0m ] '
BLUE='\033[0;34m'
NC='\033[0m'

run () {
	if ${1}; then
		echo -ne "${OK}"
	else
		echo -ne "${ERR}"
	fi
	echo -e ${BLUE}${1}${NC}
}

if [ -z "$1" ]
then
	echo -e "${ERR} ${BLUE}Usage: ./init.sh <router-id>${NC}"
	exit 1
fi




echo "#### IP-Address and Route configuration ####"
run "ip address add 192.168.$RN.254/24 dev eth0"
run "ip address add 10.$RN.$RN.1/24 dev eth1"
run "ip link set eth0 up"
run "ip link set eth1 up"
run "ip route add default via 10.$RN.$RN.254"

echo -e "\n#### Load iptables init configuration ####"
run "iptables-restore $NFCONF"

