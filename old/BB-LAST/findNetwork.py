def networkAddr(ip_str):
    return_msg = 0
    ip_bytes=ip_str.split(".")
    ip=[] #list of int which contains the ip addr
    for i in ip_bytes:
        ip.append(int(i))
          
    ip_b=[]#list of byte
    for i in ip:
        ip_b.append("{0:b}".format(i))
                    
    if ip_b[0] == "{0:b}".format(192) and ip_b[1] == "{0:b}".format(168) and ip_b[2] == "{0:b}".format(2):
        print("ip from network 192.168.2.0")
        return_msg = 2
    elif ip_b[0] == "{0:b}".format(192) and ip_b[1] == "{0:b}".format(168) and ip_b[2] == "{0:b}".format(1):
        print("ip from network 192.168.1.0")
        return_msg = 1
    else :
        print("error ip not known")
    return return_msg
