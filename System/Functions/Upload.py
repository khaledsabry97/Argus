from Connections.DataBaseController import DatabaseController
from Controller.JsonEncoder import JsonEncoder
from Data.Datakeepers import DataKeepers


class Upload:
    def __init__(self):
        pass

    def uploadRequest(self,user_id,fileName,clientIp):
        arr = DatabaseController.getFiles(user_id)

        print("[Upload Request] User id: "+str(user_id)+" to insert "+ str(fileName))
        structure = {}
        for i in range(len(arr)):
            nodeId = int(arr[i]["node_id"])
            file_Name = arr[i]["file_name"]

            if file_Name not in structure:
                structure[file_Name] = []
            structure[file_Name].append(nodeId)

        if fileName in structure:
            self.changeFileName(fileName, clientIp)
        else:
            id,_ = DataKeepers.getAliveDataNodesExclude()
            if len(id) >0:
                ip = DataKeepers.getDataNodeIp(id[0])
                port = DataKeepers.getRandomPort(id[0])

                print("[Upload Request] User id: " + str(user_id) + " grant it to node id: " + str(id[0]))
                jsonEncoder = JsonEncoder()
                jsonEncoder.uploadReqSuccess(ip, port, clientIp)
            else:
                print("No Current Data Node Found")
                self.nodesDown("sfsdf",clientIp)





    def changeFileName(self, fileName, clientIp):
        msg = "you have the same file name in the directory, please change your file name"
        reason = "Found Same Filename"
        jsonEncoder = JsonEncoder()
        jsonEncoder.uploadReqFailed(msg,reason, fileName, clientIp)


    def uploadComplete(self,user_id,file_name,fileSize,nodeId):
        print("Upload User_id : "+str(user_id)+ " - file name : "+str(file_name)+" has been completed successfully")
        DatabaseController.addFile(user_id,nodeId,file_name,fileSize)

    def nodesDown(self,fileName,clientIp):
        msg = "Data Nodes Are down, please try later..."
        reason = "Data Nodes"
        jsonEncoder = JsonEncoder()
        jsonEncoder.uploadReqFailed(msg,reason, fileName, clientIp)
