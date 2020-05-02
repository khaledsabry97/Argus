from VIF.vif import VIF

vif = VIF()


def checkDistance(frames,tracker_A,tracker_B,frame_no):
    xa, ya = tracker_A.estimationFutureCenter[frame_no]
    xb, yb = tracker_B.estimationFutureCenter[frame_no]
    r = pow(pow(xa - xb, 2) + pow(ya - yb, 2), 0.5)
    print(r)
    if r < 40:
        return True
    return False


def process(trackers,frames):
    new_trackers = []
    for tracker in trackers:
        if tracker.isAboveSpeedLimit():
            new_trackers.append(tracker)
    for i in range(len(new_trackers)):
        for j in range(i+1,len((new_trackers))):
            if i == j:
                continue
            tracker_A = trackers[i]
            tracker_B = trackers[j]

            if checkDistance(frames,tracker_A,tracker_B,15) or checkDistance(frames,tracker_A,tracker_B,25):
                print("accident has occured!")
                vif.predict(frames, [tracker_B,tracker_A])


