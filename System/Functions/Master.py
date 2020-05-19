import os

import cv2


class Master:
    def __init__(self):
        pass

    def checkIfCrashed(self,camera_id,crash_dic):
        if camera_id in crash_dic:
            if crash_dic[camera_id] == 5:
                crash_dic.pop(camera_id)
                return False
            else:
                return True
        return False


    def save(self,camera_id,starting_frame_id,frames,frame_width,frame_height,crash_dic):
        self.write(camera_id,frames,starting_frame_id,frame_width,frame_height,False)

        if self.checkIfCrashed(camera_id,crash_dic):
            self.appendSavedCrash(camera_id,starting_frame_id,crash_dic[camera_id])
            crash_dic[camera_id]+=1



    def write(self,camera_id,frames,starting_frame_id,frame_width,frame_height,is_crash = False ):
        if is_crash:
            folder = "saved_crash_vid"
        else:
            folder = "saved_frames_vid"

        file_path = './'+folder+'/' +"(" + str(camera_id) + ") " + str(starting_frame_id) + '.avi'
        if (not os.path.exists(folder)):
            os.makedirs(folder)
        out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))

        size = len(frames)
        for i in range(size):
            out.write(frames[i])
        print("camera_id_"+str(camera_id)+"_" + str(starting_frame_id) + " saved!")
        out.release()


    def appendSavedCrash(self,camera_id,starting_frame_id,from_no_of_times):




        last_frames = from_no_of_times*30
        new_frames_id = starting_frame_id -last_frames
        file_path = './saved_crash_vid/' +"(" + str(camera_id) + ") " + str(new_frames_id) + '.avi'
        cap = cv2.VideoCapture(file_path)

        new_frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            new_frames.append(frame)

        file_path = './saved_frames_vid/' + "(" + str(camera_id) + ") " + str(starting_frame_id) + '.avi'
        cap = cv2.VideoCapture(file_path)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            new_frames.append(frame)

        self.write(camera_id,new_frames,new_frames_id,frame_width,frame_height,True)


    def recordCrash(self,camera_id,starting_frame_id,crash_dic):
        crash_dic[camera_id] = 2

        new_frames = []
        from_no_of_times = 1
        while from_no_of_times >= 0:
            last_frames = from_no_of_times * 30
            new_frames_id = starting_frame_id - last_frames
            file_path = './saved_frames_vid/' + "(" + str(camera_id) + ") " + str(new_frames_id) + '.avi'
            cap = cv2.VideoCapture(file_path)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))

            while True:
                ret, frame = cap.read()
                if not ret:
                    if len(new_frames) == 0:
                        crash_dic[camera_id]-=1
                    break
                new_frames.append(frame)
            from_no_of_times -=1

        state = True
        increment = 1
        while state and crash_dic[camera_id] <5:
            last_frames = increment * 30
            new_frames_id = starting_frame_id + last_frames
            file_path = './saved_frames_vid/' + "(" + str(camera_id) + ") " + str(new_frames_id) + '.avi'
            cap = cv2.VideoCapture(file_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    state = False
                    break
                new_frames.append(frame)

            if state :
                crash_dic[camera_id] += 1

        self.write(camera_id, new_frames, starting_frame_id, frame_width, frame_height, True)

    def checkResult(self,camera_id,starting_frame_id,crash_dimentions,crash_dic):
        if len(crash_dimentions) == 0:
            return

        self.recordCrash(camera_id,starting_frame_id,crash_dic)




