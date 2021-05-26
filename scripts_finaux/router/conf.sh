#!/bin/bash
read string
echo -e "MSG-RECEIVED: ${string}"

PROTOCOL=udp

src_ip=`echo $string | awk 'BEGIN{FS=";"} {print $1}'`
dest_ip=`echo $string | awk 'BEGIN{FS=";"} {print $2}'`
dest_port=`echo $string | awk 'BEGIN{FS=";"} {print $3}'`
bw=`echo $string | awk 'BEGIN{FS=";"} {print $4}'`
mark=$((`echo $string | awk 'BEGIN{FS=";"} {print $5}'`+2))
del=`echo $string | awk 'BEGIN{FS=";"} {print $6}'`

if (( $del == 0 ))
then
	iptables -t mangle -I CDSCP 1 -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j DSCP --set-dscp-class EF
	iptables -t mangle -I CMARK 1 -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j MARK --set-mark $mark
	iptables -t mangle -I CMARK 2 -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j RETURN

	tc class add dev eth1 parent 1:1 classid 1:1$mark htb rate ${bw}kbit ceil ${bw}kbit
	tc filter add dev eth1 parent 1:1 protocol ip prio 1 handle $mark fw flowid 1:1$mark
else
	iptables -t mangle -D CDSCP -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j DSCP --set-dscp-class EF
	iptables -t mangle -D CMARK -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j MARK --set-mark $mark
	iptables -t mangle -D CMARK -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j RETURN
	tc filter del dev eth1 parent 1:1 protocol ip prio 1 handle $mark fw flowid 1:1$mark
	tc class del dev eth1 parent 1:1 classid 1:1$mark htb rate ${bw}kbit ceil ${bw}kbit
fi
