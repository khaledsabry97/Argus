import socket
import imagezmq
import cv2
import time
sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')

sender_name = socket.gethostname() # send your hostname with each image

# image = open("C:/Users/H S/PycharmProjects/Kivy/Untitled.png", 'rb')
image = cv2.imread("C:/Users/H S/PycharmProjects/Kivy/Untitled.png")
print(image)
print(sender_name)
s = time.time()
sender.send_image(sender_name, image)
e = time.time()
print('it took- ', e-s, ' sec')