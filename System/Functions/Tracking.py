import cv2


class Tracking:
    def __init__(self):
        pass

    def track(self,frames,trackers):

        for frame in frames:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # updating trackers
            for i, tracker in enumerate(trackers):
                tracker.update(frame_gray)
                tracker.futureFramePosition()

        return trackers