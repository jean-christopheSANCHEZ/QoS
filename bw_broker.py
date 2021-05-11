import socket
import netifaces

socketS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketS.bind(('', 9000))

while True:
        socketS.listen(5)
        client, address = socketS.accept()
        print("{} connected".format( address ))

        response = client.recv(255)
        if response != "":
                print(response.decode('utf-8'))
                recept = response.decode('utf-8')
                #regex analyse
                ipS = "193.168.1.1"
                portS = "5000"
                ipD = "193.168.2.1"
                portD = "6000"
                bw = "64"
                
                #envoie sur rt1 et rt2 init a client
                a_rt1 = "192.168.1.254"
                p_rt1 = 9000
                a_rt2 = "192.168.2.254"
                p_rt2 = 9000
                socketC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #check on which rt have to send the packet
                mask= "255.255.255.0"
                
                    socketC.connect((a_rt1, p_rt1))
                    print("Connection on {}".format(p_rt1))

                    msg = ipS+";" +ipD+";" +portD+";"+bw
                    bytes_msg = bytes(msg,'utf-8')
                    socketC.send(bytes_msg)
                #close client socket
                
                print("Close")
                socketC.close()



print ("Close")
client.close()
socketS.close()

