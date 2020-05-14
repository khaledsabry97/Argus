import random
import time


class DataKeepers:
    __instance = None

    global dks
    global ports

    dks = {}
    ports = {}

    @staticmethod
    def inialize():
        dks[1] = [0,"localhost" ]
        ports[1] = [6000, 6002, 6004]
        dks[2] = [0, "localhost" ]
        ports[2] = [7000, 7002, 7004]
        dks[3] = [0,"localhost"  ]
        ports[3] = [8000, 8002, 8004]
        dks[4] = [0,"localhost"  ]
        ports[4] = [9000, 9002, 9004]

    #update time for selected port id
    @staticmethod
    def updateTime(id):
        if id in dks:
            #print("Data Node "+str(id)+" : "+str(dks[id][0])+" to "+str(int(time.time() * 1000)))
            dks[id][0] = int(time.time() * 1000)
        else:
            print("didn't fint that id")

    #get random port for selected node id
    @staticmethod
    def getRandomPort(id):
        if id in ports:
            portid = random.randint(1,len(ports[id] )-1)
            return ports[id][portid]
        else:
            print("didn't fint that id")
            return -1

    #get random alive data nodes
    #you can pass the ids of nodes that you don't want to see in the result by defualt empty
    @staticmethod
    def getAliveDataNodesExclude(id=[]):
        # assign it if you put one or two nodes that you don't want to see them
        node1 = -1
        node2 = -1
        if len(id) == 1:
            node1 = int(id[0])
        elif len(id) == 2:
            node1 = int(id[0])
            node2 = int(id[1])

        arr = [] #array to insert all the potential selected ids for the node
        for i in range(1, len(list(dks.keys())) + 1):
            if DataKeepers.checkIfAlive(i) and i != node1 and i != node2:
                arr.append(i)
        if len(arr) > 0:
            random.shuffle(arr) #randomize the array of nodes
            return arr,True
        else:
            #print("no nodes found")
            return [],False

    #pass node id and see if it's alive or not
    @staticmethod
    def checkIfAlive(id):
        if(int(id) > 4 or id <0):
            return False
        if int(time.time() * 1000) - dks[int(id)][0] <= 1100:
            return True
        return False

    #get ports to send it to user
    #you must path the nodes ids that you want to get the ports for it
    #you should path the size you want by defult = 6
    #first output 'll be an array of ports
    #sec. output 'll be true if the size you sent back to you if less than the size you sent then it 'll return false
    #third output 'll be the size of the comming array of ports
    @staticmethod
    def getPorts(nodeIds,size = 6):
        arr = []
        for i in range(len(nodeIds)):
            if DataKeepers.checkIfAlive(nodeIds[i]):
                for j in range(len(ports[nodeIds[i]])):
                    arr.append(ports[nodeIds[i]][j])

        random.shuffle(arr)
        if len(arr) >= size:
            return arr[0,size],True,size
        else:
            return arr,False,len(arr)


    #return DataNodeIp for node id
    @staticmethod
    def getDataNodeIp(nodeId):
        if nodeId in dks:
            return dks[nodeId][1]
        else:
            return  "-1" # not found

     #return if one of the nodeIds Sent if it's alive
    @staticmethod
    def getNodeIdAliveInclude(nodeIds = []):

        arr = []  # array to insert all the potential selected ids for the node
        for i in range(len(nodeIds)):
            if DataKeepers.checkIfAlive(nodeIds[i]) :
                arr.append(nodeIds[i])
        if len(arr) > 0:
            random.shuffle(arr)  # randomize the array of nodes
            return arr[0],True
        else:
            print("no nodes found")
            return arr,False



     #return if array of the nodeIds Sent if it's alive
    @staticmethod
    def getNodeIdsAlive(nodeIds):

        arr = []  # array to insert all the potential selected ids for the node
        for i in range(len(nodeIds)):
            if DataKeepers.checkIfAlive(nodeIds[i]) :
                arr.append(nodeIds[i])
        if len(arr) > 0:
            random.shuffle(arr)  # randomize the array of nodes
            return arr,True
        else:
            print("no nodes found")
            return arr,False

    @staticmethod
    def getIpsandPorts(nodeIds,size = 6):
        ips = []
        portss = []
        for i in range(len(nodeIds)):
            if DataKeepers.checkIfAlive(nodeIds[i]):
                for j in range(len(ports[nodeIds[i]])):
                    portss.append(ports[nodeIds[i]][j])
                    ips.append(DataKeepers.getDataNodeIp(nodeIds[i]))

        return ips,portss,True,len(ips)







