import imagezmq
import cv2 as cv
image_hub = imagezmq.ImageHub()

sender_name, image = image_hub.recv_image()

cv.namedWindow("result", cv.WINDOW_NORMAL)
cv.imshow("result", image)
ch = cv.waitKey(0)
cv.imwrite('f.png', image)
print(image)
image_hub.send_reply(b'OK')