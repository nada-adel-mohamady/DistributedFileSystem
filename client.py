import zmq 
import time 
import cv2
import sys
import os



#Initializing Variables.
MasterPort = '5555'
MasterIP = '127.0.0.1'
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



def upload(MasterIP, MasterPort, FileName):
    #here client communicate with the master 
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s:%s"%(MasterIP, MasterPort))
    print("client connecting to server....")

   # format of msg sent to a master to request uploading file 
    msg = {"opp":"Upload", "file_name":FileName}
    socket.send_pyobj(msg)
    print("client has sent upload msg to the master..")
    # HERE CLIENT WILL RECIEVE A MSG CONTAIN IP AND PORT OF DataKeeper
    recvMasterMsg = socket.recv_pyobj()
    socket.close()
    # just to debug 
    print(recvMasterMsg)
    #
    DKip = recvMasterMsg["ip"]
    #just to debug 
    print(DKip)
    DKport = recvMasterMsg["port"]
    print(DKport)
    print("client has recieved  ip and port of DK from the master")
    #after that client will communicate with the datakeeper port and send the mp4 file to it 
    DataNodeSocket = context.socket(zmq.REQ)
    print(DKport)
    DataNodeSocket.connect("tcp://%s:%s"%(DKip, DKport))

   #  DataNodeSocket.send_string(FileName)
   # the following code is to transfere a file 
    target = open(FileName, 'rb')
    data = target.read()
  #  target.close()
    DataNodeSocket.send(data)
    DataNodeSocket.close()
    print("client has sent video to the datakeeper")

    #---finish transfere ---------------

    
# just to test it     
upload("127.0.0.1", 5551, "video.mp4")

    
    