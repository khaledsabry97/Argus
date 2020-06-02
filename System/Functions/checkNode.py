import threading
import time

from Connections import DataBaseController
from Data.Datakeepers import DataKeepers


class checkNode(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        self.do()


    def do(self):

        while(True):
            time.sleep(2)
            for i in range(1,5):
                  if DataKeepers.checkIfAlive(i) == False:
                      DataBaseController.DatabaseController.deleteDuplicate(i)

