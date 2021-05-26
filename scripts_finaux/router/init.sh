#!/bin/bash

RN=$1 # Router id
NFCONF="iptables.init"

OK='[  \033[0;32mOK\033[0m  ] '
ERR='[\033[0;31mFAILED\033[0m] '
BLUE='\033[0;33m'
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
fi

echo "#### IP-Address and Route configuration ####"
#run "ip address add 192.168.$RN.254/24 dev eth0"
#run "ip address add 10.$RN.$RN.1/24 dev eth1"
#run "ip link set eth0 up"
#run "ip link set eth1 up"
#run "ip route add default via 10.$RN.$RN.254"

echo -e "\n#### Load iptables init configuration ####"
run "iptables-restore $NFCONF"

run "tc qdisc del dev eth1 root"
run "tc qdisc add dev eth1 root handle 1: htb default 20"

run "tc class add dev eth1 parent 1: classid 1:1 htb rate 20mbit ceil 20mbit" 	
run "tc class add dev eth1 parent 1: classid 1:2 htb rate 100mbit ceil 100mbit"
run "tc class add dev eth1 parent 1: classid 1:3 htb rate 10kbit ceil 10kbit"

run "tc filter add dev eth1 parent 1:0 protocol ip prio 2 handle 1 fw flowid 1:2"
run "tc filter add dev eth1 parent 1:0 prio 1 protocol ip u32 match ip tos 0xb8 0xff flowid 1:1"
run "tc filter add dev eth1 parent 1:0 prio 1 protocol ip u32 match ip tos 0x48 0xff flowid 1:3"
