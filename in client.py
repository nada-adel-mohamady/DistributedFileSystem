# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:04:01 2020

@author: nour
"""

import zmq
#import cv2
#import sys

port = "5556"
video = "video.mp4"
#if len(sys.argv) > 1:
#    port =  sys.argv[1]
#    int(port)

#if len(sys.argv) > 2:
#    port1 =  sys.argv[2]
#    int(port1)
    
context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)

context2 = zmq.Context()
print ("Connecting to server...")
socket2 = context2.socket(zmq.PAIR)

#if len(sys.argv) > 2:
#    socket.connect ("tcp://localhost:%s" % port1)

msg = {'req':"Download",'file_name':video}
    
#  Do 10 requests, waiting each time for a response
#for request in range (1,1):
print ("Sending download request ", 1,"...")
socket.send_json(msg)
    #  Get the reply.
message = socket.recv_json()
print ("Received reply ", 1, "[", message, "]")
    
socket2.connect ("tcp://%s:%s" % (message['IP'],message['port']))
print("tcp://%s:%s" % (message['IP'],message['port']))   
#socket2.send_json(video)
socket2.send_string(video)
# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))
message = socket2.recv_pyobj()
mes_video = message['video']
f = open("output.mp4",'wb')
f.write(mes_video)
#while True:
#    message = socket2.recv_pyobj()
#    mes_video = message['video']
#    f = open("output.mp4",'wb')
#    f.write(mes_video)
    
    # write the frame
#    if message !=0:
#        out.write(message['frame'])
#        cv2.imshow('frame',message['frame'])
#    else:
#        break
#    print(message)
# Release everything if job is finished



















    
      