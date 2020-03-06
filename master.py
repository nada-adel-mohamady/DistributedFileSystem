import zmq 
import sys


def upload():
    #HERE MASTER RESPONSE WITH THE PORT OF ONE OF THE DATA KEEPER
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"%(server, port))
    #pick port randomly , assume here the port we will send is port
    msg = socket.recv()
    socket.send(port)
    filename = socket.recv_string()
    
