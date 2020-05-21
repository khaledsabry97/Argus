from Connections.DataBaseController import DatabaseController
from Controller.JsonEncoder import JsonEncoder
from Data.Datakeepers import DataKeepers


class Download:
    def __init__(self):
        pass


    def showFiles(self,userId,receiverIp):
        arr = DatabaseController.getFiles(userId)

        file_Names = []
        fileSize = []
        for i in range(len(arr)):
            file_Names.append(arr[i]["file_name"])
            fileSize.append(arr[i]["file_size"])


        jsonEncoder = JsonEncoder()
        jsonEncoder.showFiles(file_Names,fileSize,receiverIp)



    def downloadFile(self,userId,fileName,clientIp):
        arr = DatabaseController.getNodesContainsFile(userId,fileName)


        structure = []
        for i in range(len(arr)):
            nodeId = arr[i]["node_id"]
            print(nodeId)
            structure.append(int(nodeId))

        if len(structure) != 0:
            ips,ports,_,_ = DataKeepers.getIpsandPorts(structure)
            if len(ips) == 0:
                self.noNodesAlive ( fileName , clientIp )

            jsonEncoder = JsonEncoder()
            jsonEncoder.downloadIpsPorts(ips, ports, clientIp)


    def noNodesAlive(self, fileName, clientIp):
        msg = "Servers are down!"

        jsonEncoder = JsonEncoder()
        jsonEncoder.downloadReqFailed(msg, fileName, clientIp)
