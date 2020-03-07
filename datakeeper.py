import zmq 
import sys

def upload(IP, port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"%(IP, port))
   # FileName = socket.recv_string()
    print("dataNode has recieved the file name ...")
   # print("the file which is recieved ",FileName)
    # recieve the mp4 file
    data = socket.recv()
    f = open('new.mp4','wb') # open the file
    f.write(data)
    f.close()
    # finish the transfering of file 
    # here datakeeper must notify the master -- call a function which notify the master --later


# teesssst    
#upload("127.0.0.1", 5545)