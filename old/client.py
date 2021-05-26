import socket

hote = "192.168.1.1"
port = 9000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mask= "255.255.255.0"
ipR1 = "193.168.1.0"
ipR2 = "193.168.2.0"

ipS = "193.168.1.1"

#ipD="193.168.2.1"
#if ((mask & ipS) == ipR1) :
#    print("ipS au R1")

def networkAddr(ip_str):
    ip_bytes=ip_str.split(".")
    ip=[]
    for i in ip_bytes:
        ip.append(int(i))
    print(ip)

networkAddr("192.168.1.1")


socket.connect((hote, port))
print("Connection on {}".format(port))

msg = "192.168.1.1;192.168.1.2;6005;64"
bytes_msg = bytes(msg,'utf-8')
socket.send(bytes_msg)

print("Close")
socket.close()

