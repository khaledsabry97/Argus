from os import listdir,mkdir
from os.path import join, isfile

import cv2


#put your ur video in the inputs file
onlyfiles = [join(".\Inputs", f) for f in listdir(".\Inputs") if isfile(join(".\Inputs", f))]

# for i in range(1545,1560):
#     dir = ".\Outputs" + "\\" + str(i)
#     mkdir(dir)

for i in range(len(onlyfiles)):
    x = onlyfiles[i]
    vid = cv2.VideoCapture(x)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")
    video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fps       = vid.get(cv2.CAP_PROP_FPS)
    video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    isOutput = True
    dir = ".\Outputs" + "\out_" + str(i)
    mkdir(dir)
    j = 0
    while True:
        return_value, frame = vid.read()
        if return_value == False:
            break;

        cv2.imwrite(".\Outputs" + "\out_" + str(i)+"\\"+str(j)+".jpg", frame);

        j+=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
