import zmq 
import sys
import random
import time
import socket
import multiprocessing
from multiprocessing import Manager
#----------------------------------------------------------------
#--------------------VARIABLE INITILIZATION ---------------------
#----------------------------------------------------------------
MasterIP = "127.0.0.1"
MasterPort = "5557"
DKip = "127.0.0.1"
DKport = "5525"
port = 5000
portNotifications=6000
ip='127.0.0.1' 
mp4File='video.mp4'
number_of_tracker_processes = 3

def datatracker(portNb,portNotif):
 context = zmq.Context()
 socket = context.socket(zmq.PUB)
 socketFiles=context.socket(zmq.PAIR)
 socketNotification=context.socket(zmq.PAIR)
 socket.bind("tcp://127.0.0.1:%s" % portNb)
 socketNotification.bind("tcp://127.0.0.1:%s" % portNotif)
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
 while True:
   print('sending i am alive')
   socket.send_pyobj({'ip':ip})
   try: 
    msg=socketNotification.recv_pyobj(zmq.NOBLOCK)
    if "ip_toCopyTo" in msg:
        ip_toCopyTo=msg["ip_toCopyTo"]
        port_toCopyTo=msg["port"]
        socketFiles.bind("tcp://127.0.0.1:%s"% port_toCopyTo)
        socketFiles.send_pyobj({'file':mp4File})

    if"ip_toReceiveFrom" in msg:
        ip_toRecFrom=msg["ip_toReceiveFrom"]
        port_toRecFRom=msg["port"]
        socketFiles.connect("tcp://"+  str(ip_toRecFrom) 
        +":"+str(port_toRecFRom))
        received=socketFiles.recv_pyobj()
        mp4file=received['file']
   except zmq.Again as e:
        pass
   time.sleep(1)
    
    




#------------------------------------------------------------
#---------------------UPLOAD---------------------------------
#------------------------------------------------------------


def upload(DKip, DKport):
 try:
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"%(DKip, DKport))
    print("before recv")
    # recieve the mp4 file
    data = socket.recv()
    socket.close()
    print("datanode has recieved")
    f = open('new.mp4','wb') # open the file
    f.write(data)
    f.close()
    # finish the transfering of file 
    # here datakeeper must notify the master -- call a function which notify the master --later
    
    #----------------------------------
    #--------just to debug 
    #------remove the comments later----
    MasterSocket = context.socket(zmq.REQ)
    MasterSocket.connect("tcp://%s:%s"%(MasterIP, MasterPort))
    print("after connect")
    #DK MUST SEND A MESSAGE TO CONFORM DONE OF OPERATION 
    msg = {"Type":"Up","IP":DKip, "port":DKport}
    MasterSocket.send_pyobj(msg)
    MasterSocket.close()
 except zmq.Again as e:
        pass
    
    
#--------------------------------------------
#--------------------------------------------
#--------------Downoad-----------------------
#--------------------------------------------
#--------------------------------------------

    
def download(DKip,DKport):
   try:
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s" % (DKip,DKport))
    print("after binding...")
 
    message = socket.recv_string(zmq.NOBLOCK);
    print ("Received request: ", message)
    video = message
    vid = open(video,'rb')
    vi = vid.read()
    dic = {'video':vi}
    socket.send_pyobj(dic)
    mess={'Type':'Downloaded','ip':DKip,'port':DKport}
    
     # --------------JUST FOR TEST --------------#
    #----------------REMOVE THE COMMENT LATER----#
       
    context2 = zmq.Context()
    socket2 = context2.socket(zmq.REQ)
    socket2.connect("tcp://%s:%s" % (MasterIP,MasterPort))
    socket2.send_pyobj(mess)
   except FileNotFoundError as e:
        print('file not found')
   except zmq.Again as e:
        pass
# teesssst   
    
if __name__== "__main__":
 ID_List=[]
 ID_List2=[]
 #download("127.0.0.1", 5525)

 for i in range (0,number_of_tracker_processes):
        portnb=str(port+i);
        portnotif=str(portNotifications+i)
        ID = multiprocessing.Process(
        target=datatracker ,args=(portnb,portnotif,) )
        ID_List.append(ID)
        ID.start()
 multiprocessing.Process(
 target=download ,args=(DKip,5525) )
 

 for i in range (number_of_tracker_processes):
        ID_List[i].join()


 

