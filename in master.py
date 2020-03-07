# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:58:20 2020

@author: nour
"""

import zmq
import time
#import sys

port = "5556"
#if len(sys.argv) > 1:
#    port =  sys.argv[1]
#    int(port)
    
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

#socket.bind("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv_json()
    print ("Received request: ", message)
#    if(message['req']=='Download'):
#        loop on all files on look-up table and get the IP and port 
#        for data keeper which has the file if data keeper was alive.
    print(message['req'])
    keeper={'IP':"localhost",'port':"5557"}
    time.sleep (1)  
    socket.send_json(keeper)
#    socket.send("World from %s" % port)
    
