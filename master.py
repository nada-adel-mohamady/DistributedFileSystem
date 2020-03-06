import zmq 
import sys


def upload():
    #here master response with the port of one of the data keeper
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"%(server, port))
    #pick port randomly , assume here the port we will send is port
    msg = socket.recv()
    socket.send(port)

    #here master should update the look up table and add the filename to look up table 
    
