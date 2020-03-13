import zmq 
import sys
MasterIP = "127.0.0.1"
MasterPort = "5551"
DKip = "127.0.0.1"
DKport = "5525"

def upload(DKip, DKport):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"%(DKip, DKport))
    print("before recv")
    # recieve the mp4 file
    data = socket.recv()
    socket.close()
 #   socket.send("")
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
# teesssst    
upload("127.0.0.1", 5525)