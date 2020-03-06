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

def upload(server, port, FileName):
    #here client communicate with the master 
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s:%s"%(server, port))
    socket.send()
    datakeeper_port = socket.recv()
    datakeeper_port.send_string()
    
    