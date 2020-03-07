# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:20:27 2020

@author: nour
"""

import zmq
#import time
#import cv2
#import sys

port = "5557"
#if len(sys.argv) > 1:
#    port =  sys.argv[1]
#    int(port)
    
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

#socket.bind("tcp://*:%s" % port)
message = socket.recv_string();
print ("Received request: ", message)
video = message
vid = open(video,'rb')
vi = vid.read()
dic = {'video':vi}
socket.send_pyobj(dic)
    
#while True:
    #  Wait for next request from client
#    message = socket.recv_json()
#    message = socket.recv_string();
#    print ("Received request: ", message)
#    video = message
#    vid = open(video,'rb')
#    vi = vid.read()
#    dic = {'video':vi}
#    socket.send_pyobj(dic)
#    loop on files to find the wanted file.
#    cap = cv2.VideoCapture(message)
#    frame_num=0
#    while(cap.isOpened()):
#	  # Capture frame-by-frame
#      ret, frame = cap.read()
#      msg = {'frame': frame,'number': frame_num}
#      if ret:
#            socket.send_pyobj(msg)
#            print(frame_num)
#            frame_num = frame_num+1
#      else:
#         break
#    socket.send_pyobj(0)
#    cap.release()
#    socket.send_json("success")