import threading

import time

from Connections.DataBaseController import DatabaseController
from Data.Datakeepers import DataKeepers
from Controller.JsonEncoder import JsonEncoder


class Duplicate(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            self.checkPeriodic()
            time.sleep(2)


    #check periodic if file not in 3 data nodes
    def checkPeriodic(self):
        array = DatabaseController.getLessThan3Duplication() #get all the files that has less than 3 records in the database
        userIdMap = {}

        #adding the structure of maps
        for i in range(len(array)): #sort them in map inside a map first we make a key by userid then an array of the files he has then an array of nodes that contains these files
            userId = array[i]["user_id"]
            nodeId = array[i]["node_id"]
            fileName = array[i]["file_name"]
            if userId not in userIdMap:
                userIdMap[userId] = {}
            fileMap = userIdMap[userId]
            if fileName not in fileMap:
                userIdMap[userId][fileName]= []
            userIdMap[userId][fileName].append(int(nodeId))

        userIdKeys = list(userIdMap.keys())
        for i in range(len(userIdKeys)): # lets roll on all the userids
            currentUserId = userIdKeys[i]
            fileKeys = list(userIdMap[currentUserId].keys())
            for j in range(len(fileKeys)): #lets get one file and see
                currentFileName = fileKeys[j]

                nodeIds = userIdMap[currentUserId][currentFileName] #get the nodes contains this file
                currentAvailableNodes = DatabaseController.getNodesContainsFile(int(currentUserId),currentFileName) #get now only current_available of nodes
                availableNodes = []
                for i in range(len(currentAvailableNodes)):
                    availableNodes.append(int(currentAvailableNodes[i]["node_id"]))
                senderNodeId,found = DataKeepers.getNodeIdAliveInclude(availableNodes) #get alive sender node
                if found == False:
                    continue
                senderNodeId = int(senderNodeId)
                senderIp = DataKeepers.getDataNodeIp(senderNodeId)
                senderPort = DataKeepers.getRandomPort(senderNodeId)
                newNodeIdList,_= DataKeepers.getAliveDataNodesExclude(nodeIds)
                if(len(newNodeIdList) >2):
                    newNodeIdList = newNodeIdList[0:2]
                for k in range(len(newNodeIdList)):
                    print("[Duplicating] Node " + str(senderNodeId)+ " to "+ str(newNodeIdList[k]) + " file name : "+ str(currentFileName))
                    receiverNodeId = newNodeIdList[k]
                    receiverIp = DataKeepers.getDataNodeIp(receiverNodeId)
                    receiverPort = DataKeepers.getRandomPort(receiverNodeId)
                    jsonGenerator = JsonEncoder()
                    DatabaseController.addDuplicateNoSuccess(currentUserId,receiverNodeId,currentFileName,0)
                    jsonGenerator.duplicate(currentUserId,currentFileName,senderIp,senderPort,receiverIp,receiverPort)

        DatabaseController.deleteDuplicateMoreThan6HoursNoSuccess()


    def duplicateComplete(self,userId,fileName,fileSize,nodeId):
        print("[Duplicate Complete] Node "+str(nodeId)+ " file name : "+ str(fileName))
        DatabaseController.updateDuplication(userId,nodeId,fileSize,fileName)






