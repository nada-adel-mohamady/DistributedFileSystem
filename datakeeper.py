import zmq 
import sys
import random
import time
import socket

#----------------------------------------------------------------
#--------------------VARIABLE INITILIZATION ---------------------
#----------------------------------------------------------------
MasterIP = "127.0.0.1"
MasterPort = "5557"
DKip = "127.0.0.1"
DKport = "5525"
port = "5000"
portNotifications="6000"
ip='127.0.0.1' 
mp4File='video.mp4'

# context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socketFiles=context.socket(zmq.PAIR)
# socketNotification=context.socket(zmq.PAIR)
# socket.bind("tcp://127.0.0.1:%s" % port)
# socketNotification.bind("tcp://127.0.0.1:%s" % portNotifications)
# # ----------------------------------------------------------------
# # ----------------------------------------------------------------
# # ----------------------------------------------------------------
# while True:
#     socket.send_pyobj({'ip':ip})
#     time.sleep(1)
#     msg=socketNotification.recv_pyobj()
#     if "ip_toCopyTo" in msg:
#         ip_toCopyTo=msg["ip_toCopyTo"]
#         port_toCopyTo=msg["port"]
#         socketFiles.bind("tcp://127.0.0.1:%s"% port_toCopyTo)
#         socketFiles.send_pyobj({'file':mp4File})

#     if"ip_toReceiveFrom" in msg:
#         ip_toRecFrom=msg["ip_toReceiveFrom"]
#         port_toRecFRom=msg["port"]
#         socketFiles.connect("tcp://"+  str(ip_toRecFrom) 
#         +":"+str(port_toRecFRom))
#         received=socketFiles.recv_pyobj()
#         mp4file=received['file']
    
    




#------------------------------------------------------------
#---------------------UPLOAD---------------------------------
#------------------------------------------------------------


def upload(DKip, DKport):
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
#    MasterSocket = context.socket(zmq.REQ)
#    MasterSocket.connect("tcp://%s:%s"%(MasterIP, MasterPort))
#    #DK MUST SEND A MESSAGE TO CONFORM DONE OF OPERATION 
#    msg = {"Type":"Up","IP":DKip, "port":DKport}
#    MasterSocket.send_pyobj(msg)
#    MasterSocket.close()
    
    
#--------------------------------------------
#--------------------------------------------
#--------------Downoad-----------------------
#--------------------------------------------
#--------------------------------------------

    
def download(DKip,DKport):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s" % (DKip,DKport))
    print("after binding...")
    # --------------JUST FOR TEST --------------#
    #----------------REMOVE THE COMMENT LATER----#
    
    
    # context2 = zmq.Context()
    # socket2 = context2.socket(zmq.REQ)
    # socket2.connect("tcp://%s:%s" % (MasterIP,MasterPort))

    message = socket.recv_string();
    print ("Received request: ", message)
    video = message
    vid = open(video,'rb')
    vi = vid.read()
    dic = {'video':vi}
    socket.send_pyobj(dic)
    mess={'Type':'Downloaded','ip':DKip,'port':DKport}
    
     # --------------JUST FOR TEST --------------#
    #----------------REMOVE THE COMMENT LATER----#
    
    
    # socket2.send_pyobj(mess)
# teesssst   
    
if __name__== "__main__":
    upload("127.0.0.1", 5525)