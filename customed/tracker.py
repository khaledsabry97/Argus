import dlib
import cv2
import glob, os

class Tracker:
    def __init__(self, frame, coor, name, frame_index):
        # (xmin, ymin, xmax, ymax)
        xmin = coor[0]
        ymin = coor[1]
        xmax = coor[2]
        ymax = coor[3]
        self.tracker = dlib.correlation_tracker()
        self.tracker.start_track(frame, dlib.rectangle(xmin, ymin, xmax, ymax))
        self.name = name
        self.frame_index = frame_index
        self.history = [dlib.rectangle(xmin, ymin, xmax, ymax)]
        self.flow_vectors = []

    def update(self, frame):
        self.tracker.update(frame)
        return self.tracker.get_position()

    def get_position(self):
        return self.tracker.get_position()

    def add_history(self, pos):
        self.history.append(pos)

    # retorna los bounding box mas miniimos y maximos segun el recorrido de cada tracker
    def get_box_from_history(self, frame_width, frame_height):
        #print("propcsing get_box_from_history...")
        #print(self.history)
        xmin = self.history[0].left()
        ymin = self.history[0].top()
        xmax = self.history[0].right()
        ymax = self.history[0].bottom()
        for pos in self.history:
            if pos.left() < xmin:
                xmin = pos.left()
            if pos.right() > xmax:
                xmax = pos.right()
            if pos.top() < ymin:
                ymin = pos.top()
            if pos.bottom() > ymax:
                ymax = pos.bottom()

        if xmin < 0:
            xmin = 0
        if ymin < 0:
            ymin = 0
        if xmax > frame_width:
            xmax = frame_width - 1
        if ymax > frame_height:
            ymax = frame_height - 1

        #print(int(xmin), int(ymin), int(xmax), int(ymax))

        return (int(xmin), int(ymin), int(xmax), int(ymax))

    def add_vector(self, line):
        self.flow_vectors.append(line)

    def clean_flow_vector(self):
        self.flow_vectors = []

    def is_inside(self, line):
        pos = self.get_position()
        # si la primera coordenada esta dentro
        if line[0] > pos.left() and line[1] > pos.top() and line[0] < pos.right() and line[1] < pos.bottom():
            return True
        # si la segunda coordenada esta dentro
        elif line[2] > pos.left() and line[3] > pos.top() and line[2] < pos.right() and line[3] < pos.bottom():
            return True
        else:
            return False

    def intersect_with(self, tr, frame):
        total_flow_vector = self.flow_vectors + tr.flow_vectors
        for i in range(len(total_flow_vector)):
            for j in range(len(total_flow_vector)):

                print("checking intersect betweeen flow vector in trackers", self.flow_vectors, tr.flow_vectors)

                a1 = (total_flow_vector[i][0], total_flow_vector[i][1])
                a2 = (total_flow_vector[i][2], total_flow_vector[i][3])
                b1 = (total_flow_vector[j][0], total_flow_vector[j][1])
                b2 = (total_flow_vector[j][2], total_flow_vector[j][3])

                if i != j:
                    R = self.intersect(a1, a2, b1, b2)
                    rows, cols, ch = frame.shape

                    if R:
                        print("Intersection detected", a1, a2, b1, b2)
                        overlay = frame.copy()
                        cv2.rectangle(overlay, (int(self.get_position().left()), int(self.get_position().top())), (int(self.get_position().right()), int(self.get_position().bottom())), (0, 0, 255), -1)
                        cv2.rectangle(overlay, (int(tr.get_position().left()), int(tr.get_position().top())), (int(tr.get_position().right()), int(tr.get_position().bottom())), (0, 0, 255), -1)
                        opacity = 0.4
                        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)


    def intersect(self, A, B, C, D):
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def ccw(self, A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
