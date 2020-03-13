import zmq
import sys
import time
import multiprocessing
from multiprocessing import Manager
import numpy as np

number_of_tracker_processes = 3
number_of_Data_keepers =  3
number_of_Data_keeper_ports = 3
start_address_of_ports = 4000         # for tracker with clients (the procecess Ids will be 4000 + i )
start_address_of_DataKeepers =3000
file_tracker_port_address = 6000
check_alive_port_address =  5000
Machines_IP = ['127.0.0.1' , '127.0.0.1' , '127.0.0.1' ]



def Operation_confirmation(Table_Ip , Table_files , Lock_Ip_table , Lock_file_table , file_tracker_port_address):
    print("File Tracker Started..")
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PULL)
    zmq_socket.bind("tcp://192.168.43.118:"+str(file_tracker_port_address))
    while True:
        message = zmq_socket.recv_pyobj()
        if "Type" in message:
            type = message["Type"]
            ip = message["ip"]
            port = message["port"]
            if (type == "Uploaded"):
                file_N = message["file_name"]
                Lock_file_table.acquire()
                if file_N not in Table_files.keys():
                    Table_files[file_N] = []
                if ip not in Table_files[file_N]:
                    tmp = Table_files[file_N]
                    tmp.append(ip)
                    Table_files[file_N] = tmp
                Lock_file_table.release()
            Lock_Ip_table.acquire()
            tmp = Table_Ip[ip]
            tmp[1] += 1
            tmp[2][int(port) - start_address_of_DataKeepers] = 1
            Table_Ip[ip] = tmp
            Lock_Ip_table.release()


def Check_If_Alive(Table_Ip, Lock_Ip_table):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    for ip in Table_Ip.keys():
        socket.connect("tcp://" + ip + ":" + str(check_alive_port_address))   # connect on port with data keeper
    socket.subscribe("")
    socket.RCVTIMEO = 1000 // len(Table_Ip)       #to receive all alive messages in 1 second
    while True:
        startTime = time.time()
        Lock_Ip_table.acquire()
        for machine_ip in Table_Ip.keys():
            tmp = Table_Ip[machine_ip]            #to modify any thing in shared memory modify an coppy of it and replace the new coppy
            tmp[0] = 0                            #Table[0] contain 0 if machine is killed and 1  if alive
            Table_Ip[machine_ip] = tmp            #Kill all machines
        for i in range(len(Table_Ip)):
            try:
                message = socket.recv_pyobj()      # message will contain machine IP
                if "ip" in message:
                    rec_ip = message["ip"]
                    tmp = Table_Ip[rec_ip]
                    tmp[0] = 1                      # if machine send it's ip so it's alive (set bit)
                    Table_Ip[rec_ip] = tmp          #return the updated version of IP_Table
                else:
                    print("Error in sent Message in Check_If_Alive function")
            except:
                print("Message in check Alive function not received")

        Lock_Ip_table.release()
        endTime = time.time()
        if (endTime - startTime < 1):              # to make sure that the check will be repeated every 1 second
            time.sleep(1 - (endTime - startTime))




def MasterTracker(Table_Ip, Table_files, Lock_Ip_table, Lock_file_table, port):
    context = zmq.Context()
    server = context.socket(zmq.REP)
    server.bind("tcp://192.168.43.118:" + port)
    while True:
        result = server.recv_pyobj()  #receive request from clinet to uplad or to download  Dict {opp : Download or Upload}
        Send_message = {}
        if 'opp' in result:
            operation = result["opp"]
            if operation == "Upload":  # START UPLOAD PROCESS
                check_IF_Found = False
                Lock_Ip_table.acquire()
                for ip, IF_Alife in Table_Ip.items():            # Search For available Port
                    if (IF_Alife[0] == 0) or (IF_Alife[1] == 0):  # This Machine is not alive or doesnt have any free ports  (IF_alive[0]check if alive , IF_Alive[1] have NO of free ports )
                        continue                                   #check another IP
                    ports = IF_Alife[2]                             #IF_ALIVE[2] have list of ports
                    available_port_index = np.argmax(ports)         # get port it's status is 1 index
                    sendip = ip
                    senddport = str(available_port_index + start_address_of_DataKeepers)
                    check_IF_Found = True
                    temp = Table_Ip[ip]
                    temp[1] -= 1                        #decrement no of free ports
                    temp[2][available_port_index] = 0   #set status of port to 0
                    Table_Ip[ip] = temp             
                    break

                Send_message["check"] = check_IF_Found
                if check_IF_Found:
                    Send_message["ip"] = sendip
                    Send_message["port"] = senddport
                Lock_Ip_table.release()
                #call upload function ----HERE ----
                upload(available_port_index,sendip)
                print("Uploading Done")

            elif operation == "Download":
                print("Downloading..")
                check_IF_Found = False
                download_ips = []
                Lock_file_table.acquire()
                try:
                    download_ips = Table_files[result["file_name"]]
                except KeyError:
                    print("File not found !")
                    Send_message["check"] = False

                    # here write code to download

                Lock_file_table.release()
                print("Downloading Done")

            else:
                Send_message["check"] = False
        else:
            Send_message["check"] = False
        server.send_pyobj(Send_message)



#--------------------------------------------------------------------#
# -----------------------UPLOAD FILE --------------------------------#
#--------------------------------------------------------------------#
def upload(fielname, Table_files, DataKeeperPort, IP):

    #here master should update the look up table and add the filename to look up table 
    updateLookUp(filename, Table_files, IP)    
    # master should recive notification from the datakeeper 
    DataNodeSocket = context.socket(zmq.REP)
    DataNodeSocket.bind("tcp://%s:%s"%(IP, DataKeeperPort))
    response = DataNodeSocket.recv()
    print(response)
    DataNodeSocket.close()
        
#-------------------------------------------------------------------#
#---------------------UPDATE LOOK UP TABLE TO INSERT NEW FILE ------#
#-------------------------------------------------------------------#
def updateLookUp(filename, Table_files, DataKeeperIP ):
    #insert the file the ip of the datakeeper     
       Table_files[filename].append(DatakeeperIP)
       
    
    
    
    
    
    
 
    
if __name__== "__main__":
    My_Manager = Manager()
    Table_Ip= My_Manager.dict()
    Table_files = My_Manager.dict()
    Lock_Ip_table = My_Manager.Lock()
    Lock_file_table=My_Manager.Lock()

    for i in range(1, number_of_Data_keepers+1):
        ip = Machines_IP[i-1]
        ports = []
        for j in range(1, number_of_Data_keeper_ports+1):  # initialize them all ports are free
            ports.append(1)
        Table_Ip[ip] = [1, number_of_Data_keeper_ports, ports]  #number_of_Data_keeper_ports variable will indicate the no of free(available) ports


    ID_List=[]
    for i in range (number_of_tracker_processes):
        ID = multiprocessing.Process(target= MasterTracker ,args=() )
        ID_List.append(ID)
        ID.start()
    multiprocessing.Process(target=Check_If_Alive, args=(Table_Ip, Lock_Ip_table)).start()
    multiprocessing.Process(target=Operation_confirmation, args=(Table_Ip, Table_files, Lock_Ip_table, Lock_file_table, file_tracker_port_address)).start()

    for i in range (number_of_tracker_processes):
        ID_List[i].join()