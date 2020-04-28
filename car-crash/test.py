import pickle
from time import time

import cv2


# cap = cv2.VideoCapture('dataset/Accidents/subvideos/25.avi')
from VIF.vif import VIF

crash = 0
no_crash = 0
clf = pickle.load(open('models/model-svm1.sav', 'rb'))

for i in range(1,100):
    #"E:\Projects\GP_Crash_Saviour\dataset\BD_no_choques\subvideos\*.avi"
    dir = '..\dataset\BD_no_choques\subvideos\\best\\'+str(i)+'.avi'
    cap = cv2.VideoCapture(dir)
    frames = []

    while True:
        ret, frame = cap.read()

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray)

        else:
            break
    print(len(frames))
    t = time()
    obj = VIF()
    feature_vec = obj.process(frames)
    result = clf.predict(feature_vec.reshape(1, 304))
    if result[0] == 0.0:
        no_crash+=1
    else:
        crash +=1

print(crash,no_crash)

#
# dir = 'dataset/Accidents/subvideos/best/15.avi'
# # dir = 'dataset/BD_no_choques/subvideos/best/15.avi'
# cap = cv2.VideoCapture(dir)
# frames = []
# vif = ViF()
#
# while True:
#     ret, frame = cap.read()
#
#     if ret:
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         frames.append(gray)
#
#     else:
#         break
#
# t = time()
# obj = VIF()
# feature_vec = obj.process(frames)
#
# result = clf.predict(feature_vec.reshape(1, 304))
# if result[0] == 0.0:
#     no_crash+=1
# else:
#     crash +=1
#
# print(crash,no_crash,time() - t)