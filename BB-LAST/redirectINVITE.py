# -*- coding: utf-8 -*-

import re

def regexFind(fichier):

    bye = re.match(".*BYE.*", fichier)
    if bye:
        callId = re.findall("callid(.*?)callid", fichier)[0]
        return ("x", 0, "x", "x", 0, callId, 1)
    else:
        fichier1=fichier.split("###")[0]
        fichier2=fichier.split("###")[1]
        #print(fichier2)
        callId = re.findall("callid(.*?)callid", fichier1)[0]
        
        # invite    
        IP4Src = re.findall("(([0-9]{1,3}\.){3}[0-9]{1,3})",fichier1)[0][0]
        PortSrc = re.findall("audio (.*?) RTP",fichier1)[0]
        
        # invite response
        IP4Dst = re.findall("(([0-9]{1,3}\.){3}[0-9]{1,3})",fichier2)[0][0]
        PortDst = re.findall("audio (.*?) RTP",fichier2)[0]
        

        
    ############ bandwidth to reserve ############
        #           G722--------silk---------silk------speex-------speex------g711--------g711-------iLBC----
        dictBW = {"9": "88", "96":"40", "97":"40", "98":"44", "100":"15", "0":"87.5", "8":"87.5", "102":"15"}
        
        ### comparaison codec ###
        try:
            list1aux = re.search("AVP ([0-9]* )*([0-9]*)",fichier1)[0]
            list1=list1aux.split(" ")
            list1.remove("AVP")
            
            list2aux = re.search("AVP ([0-9]* )*([0-9]*)",fichier2)[0]
            list2=list2aux.split(" ")
            list2.remove("AVP")
            
            common = list(set(list1).intersection(list2))
            for i in list1: 
                if i in common:
                    bw = dictBW[i]
                    break
        except:
            bw = 88 # for G722 by default
        ### comparaison codec ###
    ############ bandwidth to reserve ############
        return (IP4Src, PortSrc, IP4Dst, PortDst, bw, callId, 0)

