import zmq 
import time 
import cv2
import sys

#port = 5555
#FileName = ''
#context = zmq.Context()
#DataNode = context.socket(zmq.REQ)
#Master = context.socket(zmq.REQ)
#zmq_socket.bind("tcp://127.0.0.1:%s" % port)



#client send a msg to the port which returned 

def upload(IP, port, FileName):
    #here client communicate with the master 
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s:%s"%(IP, port))
    #send a string to indicate that the client want to upload a file 
    socket.send(b"upload") 
    #master will send back the port of one of the datakeeper 
    datakeeper_port = socket.recv()
    #after that client will communicate with the datakeeper port and send the mp4 file to it 
    DataNodeSocket = context.socket(zmq.REQ)
    DataNodeSocket.connect("tcp://%s:%s"%(IP, datakeeper_port))
    datakeeper_port.send_string(FileName)
    
    