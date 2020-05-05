import cv2
import numpy as np

cap = cv2.VideoCapture('videos/Easy.mp4')  # 0=camera

width = 1
height = 1
fps = 1
if cap.isOpened():
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    fps = cap.get(cv2.CAP_PROP_FPS)  # float
    print(width, height)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, fps, (480, 360))

while True:
    ret, frame = cap.read()
    if ret == True:
        b = cv2.resize(frame, (480, 360), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
        out.write(b)
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()