#!/bin/bash
read string

PROTOCOL=udp

src_ip=`echo $string | awk 'BEGIN{FS=";"} {print $1}'`
dest_ip=`echo $string | awk 'BEGIN{FS=";"} {print $2}'`
dest_port=`echo $string | awk 'BEGIN{FS=";"} {print $3}'`
bw=`echo $string | awk 'BEGIN{FS=";"} {print $4}'`

echo $src_ip
echo $dest_ip
echo $dest_port
echo $bw

iptables -t mangle -I CDSCP 1 -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j DSCP --set-dscp-class EF
iptables -t mangle -I CMARK 1 -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j MARK --set-mark 42
iptables -t mangle -I CMARK 2 -s $src_ip -d $dest_ip -p $PROTOCOL --dport $dest_port -j RETURN

#Conr
