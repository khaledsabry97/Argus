import glob

import cv2
import numpy as np

from VIF.vif import VIF



def makeTrainSet(folderDir ="dataset/BD_no_choques/subvideos/*.avi", outputFileDir="data_no_choques.csv"):
    trainSet = []
    dir = folderDir
    vids = glob.glob(dir)
    count = 0
    size = len(vids)
    for vid in vids:
        cap = cv2.VideoCapture(vid)
        frames = []


        while True:
            ret, frame = cap.read()

            if ret:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

            else:
                #end of video
                break
        vif = VIF()
        featureVector = vif.process(frames)
        count+=1
        # print (feature_vec)
        print(str(count)+" of "+str(size) + " =====> " + str(count*100/size)+"%")
        trainSet.append(featureVector)

    np.savetxt(outputFileDir, trainSet, delimiter=",")



if __name__ == '__main__':
    # no Accident dataset
    makeTrainSet(folderDir ="dataset/BD_no_choques/subvideos/*.avi", outputFileDir="data_no_choques.csv")

    #Accident Dataset
    makeTrainSet(folderDir ="dataset/BD_choques/subvideos/*.avi", outputFileDir="data_choques.csv")

