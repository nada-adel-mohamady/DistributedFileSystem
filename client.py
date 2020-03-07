import zmq 
import time 
import cv2
import sys
import os



#Initializing Variables.
MasterPort = '5555'
MasterIP = 'localhost'
FileName = ''
context = zmq.Context()

MasterSocket = context.socket(zmq.REQ)
MasterSocket.connect("tcp://%s:%s" % (MasterIP, MasterPort))

DataNodeSocket = context.socket(zmq.REQ)

#----------------------------
client_id = 0
#------------------------------------------------------------------

def sendReqToMaster():
    print('Welcome..')
    print('Choose type of operation:\n(1)Upload.\n(2)Download.')
    Operation = input()
    #------------------------------------------------
    while True:
        if Operation == '1':
            print('Now Please enter the file name')
            FileName = input()
            print('Establishing connection, Please wait..')
            MasterSocket.send_string('Upload')          #Make an Upload request.
            NumberOfConnectedServers = MakeConnectionWithDataNodes()     #this function to connect with data node with values received from master tracker

            # here write the function that apply upload Upload(FileName)

            break

        elif Operation == '2':
            MasterSocket.send_string('Download')          #Make a Download request.

            # here write code that deal with download (receive list send file name and others)

            NumberOfConnectedServers = MakeConnectionWithDataNodes() # this to receive connection porst adn DK from master

            #here write the download finction logic

            break
        else:
            print('Please Enter a vaild operation :)')


    os.system('pause')


def MakeConnectionWithDataNodes():
    Info = MasterSocket.recv_string().split()
    # NOTE: even indices of Info are IP's and odd are ports. ex: Info[0] = IP,Info[1] = Port,Info[2] = IP and so on.
    for i in range(0, len(Info), 2):  # NOTE: User will connect to more than one Data Node in case of download
        DataNodeSocket.connect("tcp://%s:%s" % (Info[i], Info[i + 1]))

    x = int(len(Info) / 2)

    print('number of servers: ' + str(x))
    print(Info)
    return x



def upload(IP, port, FileName):
    #here client communicate with the master 
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s:%s"%(IP, port))
    print("client connecting to server....")
    #send a string to indicate that the client want to upload a file 
    socket.send_string("upload") 
    print("client has sent upload msg to the master..")
    #master will send back the port of one of the datakeeper 
    datakeeper_port = socket.recv_string()
    print("client has recieved a port number from the master")
    #after that client will communicate with the datakeeper port and send the mp4 file to it 
    DataNodeSocket = context.socket(zmq.REQ)
    print(datakeeper_port)
    DataNodeSocket.connect("tcp://%s:%s"%(IP, datakeeper_port))
  #  DataNodeSocket.send_string(FileName)
    # the following code is to transfere a file 
    target = open(FileName, 'rb')
    data = target.read()
  #  target.close()
    DataNodeSocket.send(data)

    
#    #---finish transfere ---------------
#    DataNodeSocket.recv()
#     # client will recieve a notification from the master which indicate the transfer was success
#    respond = socket.recv()
#    if respond =="ok":
#        print("the file uploaded successfully...")
#    else:
#        print("error occured... transfer failed")
    
# just to test it     
#upload("127.0.0.1", 5553, "video.mp4")

    
    