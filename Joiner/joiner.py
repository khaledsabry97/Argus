import cv2
import numpy as np
import os

from os.path import isfile, join


def convert_frames_to_video(pathIn, pathOut, fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    if len(files) == 0:
        return
    ext = files[0].split('.')[1]
    files = [int(f.split('.')[0]) for f in files]
    files.sort()
    # print(files)
    # for sorting the file names properly

    for i in range(len(files)):
        filename = pathIn + str(files[i]) + '.' + ext
    #     reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        print(filename)
        # inserting the frames into an image array
        frame_array.append(img)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'XVID'), fps, size)
    for i in range(len(frame_array)):
    #     writing to a image array
        out.write(frame_array[i])
    out.release()


def main():
    # os.walk('./ data/')
    directories = [x[0] for x in os.walk('data/')]
    print(directories)
    for X in range(1, len(directories)):
        pathIn = directories[X] + '/'
        pathOut = 'vids/' + directories[X].split('data/')[1] + '.mp4'
        fps = 30
        convert_frames_to_video(pathIn, pathOut, fps)

    # pathIn = './data/'
    # pathOut = 'video.avi'
    #

if __name__ == "__main__":
    main()
