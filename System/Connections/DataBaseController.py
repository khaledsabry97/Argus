import requests

from Data.Links import Links


class DatabaseController:
    ################################
    #Essential Methods#

    #for all inserts, deletes and update queries
    @staticmethod
    def inUpDL(link,data={}):
        try:
            r = requests.post(url=link, data=data)
            result = r.json()


            if (result["server_response"] == True):
                return True
        except:
            pass
        return False

    #for all select queries
    def select(link,data={}):
        try:
            r = requests.post(url=link, data=data)
            result = r.json()
            array = []

            if (result["server_response"] != "server down" and result["server_response"] != False):
                array = result["server_response"]
        except:
            return [],False
        return array,True
    #Essential Methods#
    ################################


    #to add file after success upload
    @staticmethod
    def addFile(userId,nodeId,fileName,fileSize):
        data = {"user_id":userId,
                "node_id":nodeId,
                "file_name":fileName,
                "file_size":fileSize,
                "current_available":True}
        return DatabaseController.inUpDL(Links.addFileDup, data)

    #get all the files for user id
    @staticmethod
    def getFiles(userId):
        data = {"user_id": userId}
        array,state = DatabaseController.select(Links.getFiles,data)
        if state == False:
            return []
        return array

    #get all the nodes ids that has the filename for specific user id
    @staticmethod
    def getNodesContainsFile(userId,fileName):
        data = {"user_id": userId,
                "file_name":fileName}
        array,state = DatabaseController.select(Links.getNodesContainsFile,data)
        if state == False:
            return []
        return array



    ################################
    #Duplication Methods#
    @staticmethod
    def getLessThan3Duplication():
        array,state = DatabaseController.select(Links.getLessThan3Duplication)
        if state == False:
            return []
        return array


    @staticmethod
    def addDuplicateNoSuccess(userId,nodeId,fileName,file_size):
        data = {"user_id":userId,
                "node_id":nodeId,
                "file_name":fileName,
                "file_size":file_size,
                "current_available":False}
        return DatabaseController.inUpDL(Links.addFileDup, data)

    @staticmethod
    def deleteDuplicateMoreThan6HoursNoSuccess():
        return DatabaseController.inUpDL(Links.deleteNoDuplicationHappend)

    @staticmethod
    def updateDuplication(userId,nodeId,fileSize,fileName):
        data = {"user_id":userId,
                "node_id":nodeId,
                "file_name":fileName,
                "file_size":fileSize}
        return DatabaseController.inUpDL(Links.updateDuplication,data)

    # Duplication Methods#
    ################################
    @staticmethod
    def deleteDuplicate(node_id):
        data = {"node_id": node_id}
        return DatabaseController.inUpDL(Links.deleteNode,data)
