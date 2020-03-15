#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 22:06:43 2020

@author: nada
"""


# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:59:01 2020

@author: bia3
"""
import zmq
#import time
import multiprocessing
from  multiprocessing import Process
from  multiprocessing import Manager
#client_num=2


output = "fuck"
def sendRequestToMaster(portM,operation,FileName):
    context = zmq.Context()
    MasterSocket = context.socket(zmq.REQ)
    MasterSocket.connect("tcp://%s:%s" % ("127.0.0.1",portM))
    DKip=0
    DKport=0
    if(operation=="upload"):
        msg = {"opp":"Upload", "file_name":FileName}
        MasterSocket.send_pyobj(msg)
        print("client has sent upload msg to the master..")
        # HERE CLIENT WILL RECIEVE A MSG CONTAIN IP AND PORT OF DataKeeper
        recvMasterMsg = MasterSocket.recv_pyobj()
        print(recvMasterMsg)
        if recvMasterMsg["check"] or True:
            DKip = recvMasterMsg["ip"]
            DKport = recvMasterMsg["port"]
#            connectWithDataKeeper(DKport,DKip,FileName,operation)
        else:
            print("something wrong happend please try again later")
    else:
        msg = {'opp':"Download",'file_name':FileName}
    
        print ("Sending download request.... ")
        MasterSocket.send_pyobj(msg)
        #  Get the reply.
        recvMasterMsg = MasterSocket.recv_pyobj()
        if recvMasterMsg['check'] or True:
            print ("Received reply ", 1, "[", recvMasterMsg, "]")
            DKip = recvMasterMsg["ip"]
            DKport = recvMasterMsg["port"]
#            connectWithDataKeeper(DKport,DKip,FileName,operation)
        else:
            print("something wrong happend please try again later")
    return recvMasterMsg['check'],DKip,DKport

def connectWithDataKeeper(port,ip,fileName,operation):
    context2 = zmq.Context()
    print ("Connecting to datakeeper...")
    DataNodeSocket = context2.socket(zmq.REQ)
    DataNodeSocket.connect ("tcp://%s:%s" % (ip,port))
    print("da el port bta3 e datakeeper",port)
    if operation=="download":
        print("tcp://%s:%s" % (ip,port))   
        #socket2.send_json(video)
        DataNodeSocket.send_string(fileName)
        
        message = DataNodeSocket.recv_pyobj()
        mes_video = message['video']
        f = open("output.mp4",'wb')
        f.write(mes_video)
        DataNodeSocket.close()
        f.close()
        print("client has sent video to the datakeeper")
    else:
        #  DataNodeSocket.send_string(FileName)
        # the following code is to transfere a file 
        target = open(fileName, 'rb')
        data = target.read()
        DataNodeSocket.send(data)
        DataNodeSocket.close()
        target.close()
        print("client has sent video to the datakeeper")

def checkMaster(portM,return_dict):
    print("check master........")
    context = zmq.Context()
    MasterSocket = context.socket(zmq.REQ)
    MasterSocket.connect("tcp://%s:%s" % ("127.0.0.1",portM))
    MasterSocket.send_string("begin transfer")
    message = MasterSocket.recv_string()
    return_dict[0] = message
    print(message)

if __name__ == "__main__":
    # Now we can run a few servers 
#    server_ports = range(5550,5556,2)
#    for server_port in server_ports:
#        Process(target=server, args=(server_port,)).start()
        
    # Now we can connect a client to all these servers
    manager = Manager()
    return_dict = manager.dict()
    
    portM="5559"
    operation="download"
    fileName="video.mp4"
    check,DKip,DKport=sendRequestToMaster(portM,operation,fileName)
    print(check,DKip,DKport)
    
    p1 = Process(target=connectWithDataKeeper,args=(DKport,DKip,fileName,operation,)) 
    p2 = Process(target=checkMaster,args=(portM,return_dict))
    p1.start()
    p2.start()
    
    p2.join()
    if return_dict[0]=="True":        
        print(return_dict[0]+"dee if")
        p1.join()
    else:
        print("dee else")
        p1.terminate()
    print("We're fucking done")
#    print(return_dict.values())
#    if check:
#        MasterSocket.send_string("begin transfer")
#        print("d5lt")
#        one = Process(target=connectWithDataKeeper,args=(DKport,DKip,fileName,operation)).start()  
#        out = Process(target=checkMaster,args=(return_dict)).start()
#        out.start()
#        one.start()
#        one.join()
#        print("7saaaaaaaaaaaaaaaal")
#    print(return_dict.values())
#    Process(target=client, args=(server_ports,)).start()