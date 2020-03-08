import glob

import cv2
import numpy as np

from VIF.vif import VIF



def makeTrainSet(folderDir ="E:\Projects\GP_Crash_Saviour\dataset\BD_no_choques\subvideos\*.avi", outputFileDir="data_no_accidents.csv"):
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
        print(str(count)+" of "+str(size) + " =====> " + str(int(count*100/size))+"%")
        trainSet.append(featureVector)

    np.savetxt(outputFileDir, trainSet, delimiter=",")



if __name__ == '__main__':
    # no Accident dataset
    print("No Accidents Starting...")
    makeTrainSet(folderDir ="..\dataset\\No_Accidents\subvideos\*.avi", outputFileDir="data_no_accidents.csv")
    print("No Accidents Completed Successfully!")

    #Accident Dataset
    print("Accidents Starting...")
    makeTrainSet(folderDir ="..\dataset\Accidents\subvideos\\best\*.avi", outputFileDir="data_accidents.csv")
    print("Accidents Completed Successfully!")
