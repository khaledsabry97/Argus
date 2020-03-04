import pickle
from time import time

import cv2

from vif import ViF

# cap = cv2.VideoCapture('dataset/BD_choques/subvideos/25.avi')
crash = 0
no_crash = 0
clf = pickle.load(open('models/model-svm1.sav', 'rb'))

# for i in range(1,100):
#     dir = 'dataset/BD_no_choques/subvideos/'+str(i)+'.avi'
#     cap = cv2.VideoCapture(dir)
#     frames = []
#     vif = ViF()
#
#     while True:
#         ret, frame = cap.read()
#
#         if ret:
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             frames.append(gray)
#
#         else:
#             break
#
#     t = time()
#     obj = ViF()
#     feature_vec = obj.process(frames)
#     result = clf.predict(feature_vec.reshape(1, 304))
#     if result[0] == 0.0:
#         no_crash+=1
#     else:
#         crash +=1

# print(crash,no_crash)


dir = 'dataset/BD_choques/subvideos/best/15.avi'
# dir = 'dataset/BD_no_choques/subvideos/best/15.avi'
cap = cv2.VideoCapture(dir)
frames = []
vif = ViF()

while True:
    ret, frame = cap.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray)

    else:
        break

t = time()
obj = ViF()
feature_vec = obj.process(frames)

result = clf.predict(feature_vec.reshape(1, 304))
if result[0] == 0.0:
    no_crash+=1
else:
    crash +=1

print(crash,no_crash,time() - t)