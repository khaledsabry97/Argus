import cv2

class Crashing:

    def __init__(self,vif):
        self.vif = vif

    def crash(self,frames,trackers):
        crash_dimentions = []

        # crash_dimentions.extend(self.predict(frames, trackers))
        for i in range(len(trackers)):
            for j in range(i + 1, len(trackers)):
                if i == j:
                    continue
                tracker_A = trackers[i]
                tracker_B = trackers[j]

                if self.checkDistance(tracker_A, tracker_B, 16) or\
                self.checkDistance( tracker_A, tracker_B,19) or\
                self.checkDistance(tracker_A,tracker_B,22) or\
                self.checkDistance( tracker_A, tracker_B, 25) or\
                self.checkDistance( tracker_A, tracker_B, 28):

                    crash_dimentions.extend(self.predict(frames, [tracker_B, tracker_A]))
        if len(crash_dimentions) > 0:
            xmin = 1000
            ymin = 1000
            xmax = 0
            ymax = 0
            for crash_dimension in crash_dimentions:
                xmin = min(xmin, crash_dimension[0])
                ymin = min(ymin, crash_dimension[1])
                xmax = max(xmax, crash_dimension[2])
                ymax = max(ymax, crash_dimension[3])
            crash_dimentions = [xmin,ymin,xmax,ymax]
        else:
            crash_dimentions = []


        return crash_dimentions

    def checkDistance(self, tracker_A, tracker_B, frame_no):
        if not tracker_A.isAboveSpeedLimit(frame_no - 10, frame_no) and not tracker_B.isAboveSpeedLimit(frame_no - 10,frame_no):
            return False

        xa, ya = tracker_A.estimationFutureCenter[frame_no]
        xb, yb = tracker_B.estimationFutureCenter[frame_no]
        r = pow(pow(xa - xb, 2) + pow(ya - yb, 2), 0.5)

        xa_actual, ya_actual = tracker_A.tracker.centers[frame_no]
        xb_actual, yb_actual = tracker_B.tracker.centers[frame_no]
        difference_trackerA_actual_to_estimate = pow(pow(xa_actual - xa, 2) + pow(ya_actual - ya, 2), 0.5)
        difference_trackerB_actual_to_estimate = pow(pow(xb_actual - xb, 2) + pow(yb_actual - yb, 2), 0.5)
        max_difference = max(difference_trackerA_actual_to_estimate, difference_trackerB_actual_to_estimate)

        if r == 0:
            return True

        if r < 40 and max_difference / r > 0.5:
            # print(r,difference_trackerA_actual_to_estimate,difference_trackerB_actual_to_estimate,max_difference/r)
            return True
        return False

    def predict(self,frames_RGB, trackers):
        gray_frames = []
        for frame in frames_RGB:
            gray_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        no_crash = 0
        crash = 0


        crash_dimentions = []
        for tracker in trackers:
            tracker_frames, width, height, xmin, xmax, ymin, ymax = tracker.getFramesOfTracking(gray_frames)
            crash_dimentions.append([xmin,ymin,xmax,ymax])

            if tracker_frames == None:
                continue

            if xmax - xmin < 50:  # 50
                continue
            if ymax - ymin <= 28:  # 35
                continue

            if (ymax - ymin) / (xmax - xmin) < 0.35:  # 0.35
                continue

            feature_vec = self.vif.process(tracker_frames)
            result = self.vif.clf.predict(feature_vec.reshape(1, 304))
            if result[0] == 0.0:
                no_crash += 1
            else:
                crash += 1
                tracker.saveTracking(frames_RGB)



        if crash == 0:
            crash_dimentions = []
        # print(crash, no_crash)
        return crash_dimentions

