import socket
from redirectINVITE import regexFind
from findNetwork import networkAddr

socketS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketS.bind(('192.168.1.20', 9000))
totalBW = 20000 #total bw available 20Mbit
pendingConnection = {}
callIdIndex = {}
#envoie sur rt1 et rt2 init a client
a_rt1 = "192.168.1.254"
p_rt1 = 9000
a_rt2 = "192.168.2.254"
p_rt2 = 9000
a_proxy = "192.168.1.3"
p_proxy = 9000

index=0
try :
    while True:
        print("Listening...")
        socketS.listen(5)
        client, address = socketS.accept()
        print("{} connected".format( address ))
        response = []
        response.append(client.recv(1500))
        if response:
            for r in response:
                #print(response.decode('utf-8'))
                recept = r.decode('utf-8')
                print(recept)
                #regex analyse
                
                ipS, portS, ipD, portD, bw, callId, bye = regexFind(recept)
                if bye==0:
                    print("*****"+callId+"*****")
                    if totalBW - bw >0:
                        pendingConnection[callId]=[ipS, portS, ipD, portD, str(bw)]
                        
                        callIdIndex[callId] = str(index)
                        #ack to proxy
                        socketP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socketP.connect((a_proxy, p_proxy))
                        msg = "ACK"
                        bytes_msg = bytes(msg, 'utf-8')
                        socketP.send(bytes_msg)
                        print("Close")
                        socketP.close()
                        
                        #update total BW
                        totalBW = totalBW -bw
                        
                        #check on which rt have to send the packet
                        network_to_send = 0
                        
                        socketC1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socketC2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        network_to_send = networkAddr(ipS)
                        if network_to_send==1:
                            #to RT1
                            print("avant")
                            socketC1.connect((a_rt1, p_rt1))
                            print("Connection on {}".format(p_rt1))
                            msg = ipS+";" +ipD+";" +portD+";"+str(int(bw))+";"+str(index)+";"+"0"
                            print(msg)
                            bytes_msg = bytes(msg,'utf-8')
                            socketC1.send(bytes_msg)
                            
                            #to RT2
                            socketC2.connect((a_rt2, p_rt2))
                            print("Connection on {}".format(p_rt2))
                            msg = ipD+";" +ipS+";" +portS+";"+str(int(bw))+";"+str(index)+";"+"0"
                            print(msg)
                            bytes_msg = bytes(msg,'utf-8')
                            socketC2.send(bytes_msg)
                            index = int(index) +1
                        elif network_to_send==2:
                        
                            print("avant")
                            #to RT2
                            socketC1.connect((a_rt2, p_rt2))
                            print("Connection on {}".format(p_rt2))
                            msg = ipS+";" +ipD+";" +portD+";"+str(int(bw))+";"+str(index)+";"+"0"
                            print(msg)
                            bytes_msg = bytes(msg,'utf-8')
                            socketC1.send(bytes_msg)
                            
                            #to RT1
                            socketC2.connect((a_rt1, p_rt1))
                            print("Connection on {}".format(p_rt1))
                            msg = ipD+";" +ipS+";" +portS+";"+str(int(bw))+";"+str(index)+";"+"0"
                            print(msg)
                            bytes_msg = bytes(msg,'utf-8')
                            socketC2.send(bytes_msg)
                            index = int(index) + 1
                        elif network_to_send==0:
                            print("error : cannot send msg to router, invalid ip")
                            
                        #close client socket
                        
                        print("Close C1")
                        socketC1.close()
                        
                        print("Close C2")
                        socketC2.close()
                    else :
                        #send no ack to proxy
                        socketP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        soketP.connect((a_proxy, p_proxy))
                        msg = "NACK"
                        bytes_msg = bytes(msg, 'utf-8')
                        socketP.send(bytes_msg)
                        print("Close")
                        socketP.close()
                elif bye==1:
                    #recup the Ips and ports with the callId in the dictionnary
                    print("*****"+callId+"*****")
                    try:
                        ipS=pendingConnection[callId][0]
                        portS=pendingConnection[callId][1]
                        ipD=pendingConnection[callId][2]
                        portD=pendingConnection[callId][3]
                        bw=pendingConnection[callId][4]
                        
                        index = callIdIndex[callId]
                        
                        #del the line from the dist
                        pendingConnection.pop(callId)
                        
                        #del the index on the dict
                        callIdIndex.pop(callId)
                        #update total BW
                        totalBW = totalBW + int(bw)
                            
                        #check on which rt have to send the packet
                        network_to_send = 0
                          
                        socketC1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socketC2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        network_to_send = networkAddr(ipS)
                        if network_to_send==1:
                            #to RT1
                            print("avant")
                            socketC1.connect((a_rt1, p_rt1))
                            print("Connection on {}".format(p_rt1))
                            msg = ipS+";" +ipD+";" +portD+";"+str(int(bw))+";"+str(index)+";"+"1"
                            print(msg)
                            bytes_msg = bytes(msg,'utf-8')
                            socketC1.send(bytes_msg)
                                
                            #to RT2
                            socketC2.connect((a_rt2, p_rt2))
                            print("Connection on {}".format(p_rt2))
                            msg = ipD+";" +ipS+";" +portS+";"+str(int(bw))+";"+str(index)+";"+"1"
                            print(msg)
                            bytes_msg = bytes(msg,'utf-8')
                            socketC2.send(bytes_msg)
                        elif network_to_send==2:
                            
                            print("avant")
                            #to RT2
                            socketC1.connect((a_rt2, p_rt2))
                            print("Connection on {}".format(p_rt2))
                            msg = ipS+";" +ipD+";" +portD+";"+str(int(bw))+";"+str(index)+";"+"1"
                            print(msg)
                            bytes_msg = bytes(msg,'utf-8')
                            socketC1.send(bytes_msg)
                                
                            #to RT1
                            socketC2.connect((a_rt1, p_rt1))
                            print("Connection on {}".format(p_rt1))
                            msg = ipD+";" +ipS+";" +portS+";"+str(int(bw))+";"+str(index)+";"+"1"
                            print(msg)
                            bytes_msg = bytes(msg,'utf-8')
                            socketC2.send(bytes_msg)
                        elif network_to_send==0:
                            print("error : cannot send msg to router, invalid ip")
                                
                        #close client socket
                            
                        print("Close C1")
                        socketC1.close()
                            
                        print("Close C2")
                        socketC2.close()
                    except:
                        print("Erreur no callId into the dictionnary for the bye")
                          


    print ("Close")
    client.close()
    socketS.close()
except KeyboardInterrupt:
    print("Press ctrl-c to terminate while statement")
    pass
