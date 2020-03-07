import zmq
from utils import *
import sys
import pandas as pd
import time

N = 0
lookupTble = pd.DataFrame ( columns = ('userId', 'fileName' , 'dataNodeNumber', 'filePath', 'ifNodeAlife') )
State = ['offline'] * N  #State of the Data Nodes, Intilally all Machines are offline.
LastTime = [0] * N        #Last Time Machine sent an Alive message.
MinumumNumberOfCopies = 1
ports = []
for i in range(N):
    ports[i] = i * 100 + 600       #Representitive Ports of the Data Nodes with master.
# print(ports)

DataNodePorts = []
for i , x in range(ports):
    DataNodePorts[i]=[x,x+1,x+2]
# print(DataNodePorts)

TransferPorts = {'6001':'free' , '6002':'free' , '6003':'free' , '7001':'free' , '7002':'free' , '7003':'free' , '8001':'free' , '8002':'free' , '8003':'free'}

msg = []
subscribers = []        #nodes of data keeper
IP = ['localhost'] *N              #IP's of the Data Nodes
MasterPort = '5555'     # Master Port is the port which the users connect with
context = zmq.Context()

Server = context.socket(zmq.REP)
Server.bind("tcp://*:%s" % MasterPort)    #bind port that will connect with clients

for i in range(0,N):                     #connect data keepers with master
    subscribers.append(context.socket(zmq.SUB))
    subscribers[i].connect('tcp://%s:%s' %(IP[i],ports[i]) )
    subscribers[i].setsockopt(zmq.SUBSCRIBE, b'')
    msg.append('')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def UpdateLookupTable(portsArr,NodeNo, video_name):
    lookupTble





#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def Connect(ID):
    msg[ID] = subscribers[ID].recv_string()
    if(msg[ID] == 'Alive'):
        print('Connected to Data Node ')
        LastTime[ID] = time.time()
        State[ID] = 'online'
    while True:
        msg[ID] = subscribers[ID].recv_string()
        if(msg[ID] == 'Alive'):
            LastTime[ID] = time.time()
        # else:

           #update data

#----------------------------------------------------------------------------------------------


def GetFreePort(idx):
    if (State[idx] == 'offline'):
        return 'none', 'none'

    for p in DataNodePorts[idx]:
        if (TransferPorts[p] == 'free'):
            return p, IP[idx]
    return 'none', 'none'
# ----------------------------------------------------------------------------------------------


def ClientsHandler():
    while True:
        request = Server.recv_string()  # Waiting for request from any client.
        if (request == 'check'):
            Server.send_string('')
            continue

        print('Received %s request from a user..' % request)  # There is a client sent a request.
        print('Finding Free Port..')
        FreePort = 'none'
        PortIP = 'none'
        if (request == 'Upload'):
            idx = 0
            while (FreePort == 'none'):
                FreePort, PortIP = GetFreePort(idx)
                idx += 1
                idx %= len(ports)
            print('Port Found')
            Server.send_string(PortIP + ' ' + FreePort)
            TransferPorts[FreePort] = 'busy'
        # else:  # Download.

           #here write code for case download and collect the data of info
            # function get free ports will be called here

            print('Ports Found')
            # Server.send_string(Info)
# ----------------------------------------------------------------------------------------------