import zmq 
import sys


def ClientRequest(IP, port):
    #here master response with the port of one of the data keeper
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"%(IP, port))
    print("master bind to the port and ip of the client")
    #pick port randomly , assume here the port we will send is port
    msg = socket.recv_string()
    print(msg)
    if msg =="upload":
         # here i use just a port number as an datakeeper port --remove it later--
         print("inside if block")
         socket.send_string("5545")

    #here master should update the look up table and add the filename to look up table 
    
    
    
    # master should recived notification from the datakeeper 
    
    
    
    # master will notify the client with successful message 
    
    
# teeesssssssst    
#ClientRequest("127.0.0.1", 5553)