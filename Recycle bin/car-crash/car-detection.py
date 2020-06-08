#esto usa yolo3, se debe haber descargado antes los pesos de la red entrenada con COCO
from PIL import Image

# import darknet as yolo
import numpy as np
import cv2
import dlib
import random
import HornSchunck as hs
from vif import ViF
import glob, os
import pickle
f = open('models/model-svm.sav', 'rb')

from yolo import YOLO

clf = pickle.load(open('models/model-svm1.sav', 'rb'))
total_frames = []
sub_sampling = 29
# net = yolo.load_net("yolov3.cfg",
#               "yolov3.weights", 0)
# meta = yolo.load_meta("coco.data")
counter_sub_video = 1
data = []


class Tracker:
    def __init__(self, frame, xmin, ymin, xmax, ymax, name, frame_index):
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
                    R = intersect(a1, a2, b1, b2)
                    rows, cols, ch = frame.shape

                    if R:
                        print("Intersection detected", a1, a2, b1, b2)
                        overlay = frame.copy()
                        cv2.rectangle(overlay, (int(self.get_position().left()), int(self.get_position().top())), (int(self.get_position().right()), int(self.get_position().bottom())), (0, 0, 255), -1)
                        cv2.rectangle(overlay, (int(tr.get_position().left()), int(tr.get_position().top())), (int(tr.get_position().right()), int(tr.get_position().bottom())), (0, 0, 255), -1)
                        opacity = 0.4
                        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)



#procesamo ViF por cada tracker
def vif(trackers,  frame_width, frame_height, frame):
    global sub_sampling
    print ("procesando ViF en cada tracker")
    global counter_sub_video
    for i, tracker in enumerate(trackers):
        print("procesando ViF en tracker " + str(tracker.name), tracker.get_position().right() - tracker.get_position().left(), tracker.get_position().bottom() - tracker.get_position().top())

        box = tracker.get_box_from_history(frame_width, frame_height)
        #por cada tracker, extreeremos los subframes

        if box[2] - box[0] < 100:
            print ("dimesiones del tracker muy pequenio, es ignorado")
            continue



        print ("tracker frame_index:", tracker.frame_index, "len history:", len(tracker.history))
        if len(tracker.history) < sub_sampling:
            print ("tracker con pocos frames en su historia, es ignorado")
        else:
            #fourcc = cv2.VideoWriter_fourcc(*'XVID')
            print ("el video se guardara como", str(counter_sub_video), (box[2] - box[0], box[3] - box[1]))
            #out = cv2.VideoWriter('dataset/Accidents/subvideos/' + str(counter_sub_video) + '.avi', fourcc, 30,
            #                      (box[2] - box[0], box[3] - box[1]))

            counter_sub_video += 1

            tracker_frames = []

            ''''
            # pitamos el aut que estamos procesando
            overlay = frame.copy()
            cv2.rectangle(overlay, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), -1)
            opacity = 0.4
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
            cv2.imshow("win", frame)
            cv2.waitKey(30)
            '''

            #for j in range(tracker.frame_index, tracker.frame_index + sub_sampling - 1):
            for j in range(tracker.frame_index, tracker.frame_index + len(tracker.history) ):

                img = total_frames[j]
                sub_image = img[box[1]:box[3], box[0]:box[2]]
                gray_image = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
                tracker_frames.append(gray_image)

                # procesamos el flujo optico, lo hacemos a partir de la segunda imagen
                #if j > tracker.frame_index:
                #    print ("Porcessing optic flow")
                #    u, v, m = hs.HornSchunck(tracker_frames[-2], tracker_frames[-1])
                #    print("optic flow vector magnitude", m)

                cv2.imshow("sub_image", sub_image)
                cv2.waitKey(0)
                #out.write(sub_image)


            print ("el tracker tiene " + str(len(tracker_frames)) + " frames")
            # procesing vif
            obj = ViF()
            feature_vec = obj.process(tracker_frames)
            data.append(feature_vec)

            # para evaluar vif en un modelo ya entrenado
            ###################################################################
            ###################################################################

            feature_vec = feature_vec.reshape(1, 304)
            print (feature_vec.shape)
            result = clf.predict(feature_vec)
            print ("RESULT SVM", result)
            font = cv2.FONT_HERSHEY_SIMPLEX
            print("RESULT ", result[0])
            if result[0] == 0.0:
                print(0)
                title = "normal"
            else:
                print(1)
                title = "car-crash"
                overlay = frame.copy()
                cv2.rectangle(overlay, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), -1)
                opacity = 0.4
                cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

            #cv2.putText(frame, title, (int(tracker.get_position().left()), int(tracker.get_position().top())), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("win", frame)
            cv2.waitKey(0)

            ###################################################################
            ###################################################################


def start_process(path):
    global total_frames
    print("reading video " + path)
    total_frames = []

    cap = cv2.VideoCapture(path)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(str(frame_count) + " frames y " + str(fps) + " as framerate")

    index = 0

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('video2.avi', fourcc, 30, (1280, 720))

    detections = 0
    trackers = []

    '''
    Para el flujo optico

    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    while not ret:
        print()
        ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    color = np.random.randint(0,255,(100,3))
    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)

    Para el flujo optico FIN
    '''
    yolo = YOLO()
    while True:
        ret, frame = cap.read()

        if ret:
            new_frame = frame.copy()
            total_frames.append(new_frame)

            # las veces que se eejcua ViF
            if index > 0 and (index % sub_sampling == 0 or index == frame_count - 1):
                print ("FRAME " + str(index) + " VIF")
                vif(trackers, frame_width, frame_height, frame)

            # las veces que se ejecuta yolo
            if index % sub_sampling == 0 or index == 0 :
                print ("FRAME " + str(index) + " YOLO")
                trackers = []

                cv2.imwrite("tmp/img.jpg", frame)
                image = Image.fromarray(frame)
                detections = yolo.detect_image(image)  # [x,y,w,h]
                # detections = yolo.detect(net, meta, "/home/vicente/projects/violence/car-crash/tmp/img.jpg")
                print (detections)
                for det in detections:
                    label = 'car'
                    #accuracy = det[1]
                    box = det

                    width = box[2]
                    height = box[3]
                    xmin = box[0] - width / 2
                    ymin = box[1] - height / 2

                    if label == 'car':
                        cv2.rectangle(frame, (xmin, ymin), (xmin + width, ymin + height), (0, 0, 255))

                        # solo agregamos al tracker si esta dentro de los limites del frame, no no hacemos esto
                        # el tracker no funciona bien

                        if xmin + width < frame_width and ymin + height < frame_height:
                            tr = Tracker(frame, (xmin, ymin, xmin + width, ymin + height), random.randrange(100), index)
                            trackers.append(tr)
                        else:
                            if xmin + width < frame_width and ymin + height >= frame_height:
                                tr = Tracker(frame, (xmin, ymin, xmin + width, frame_height - 1), random.randrange(100),
                                             index)
                            elif xmin + width >= frame_width and ymin + height < frame_height:
                                tr = Tracker(frame, (xmin, ymin, frame_width - 1, ymin + height), random.randrange(100),
                                             index)
                            else:
                                tr = Tracker(frame, (xmin, ymin, frame_width - 1, frame_height - 1),
                                             random.randrange(100), index)
                            trackers.append(tr)

            else:
                print ("FRAME " + str(index) + " UPDATE TRACKER")
                # out.write(frame)
                # procesamos el flujo optico con lucas kanade
                '''
                gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, gray_image, p0, None, **lk_params)

                # Select good points
                good_new = p1[st == 1]
                good_old = p0[st == 1]

                lines = []
                # select de optic flow vector
                for i, (new, old) in enumerate(zip(good_new, good_old)):
                    a, b = new.ravel()
                    c, d = old.ravel()
                    lines.append((a, b, c, d))
                    mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
                    frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
                    cv2.line(frame, (a, b), (c, d), (0, 0, 255), 1)
                '''

                # update trackers
                for i, tracker in enumerate(trackers):
                    tr_pos = tracker.update(frame)
                    if tr_pos.left() > 0 and tr_pos.top() > 0 and tr_pos.right() < frame_width and tr_pos.bottom() < frame_height:
                        cv2.rectangle(frame, (int(tr_pos.left()), int(tr_pos.top())),
                                      (int(tr_pos.right()), int(tr_pos.bottom())), (0, 0, 255))
                        tracker.add_history(tr_pos)

                        # al parecer no funcioa bien, suelen haber intersecciones entre los vvectores de un mismo auto, ademas falta corregir cuales son lostracker que intersetan
                        # check_intersection(lines, frame, trackers)

            cv2.imshow("win", frame)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break

            index += 1

        else:
            break

    cv2.destroyAllWindows()


def ccw(A,B,C):
	return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])


def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


# buscamos si hay vectores de flujo optico que se intersectan, a fuerza bruta
def check_intersection(lines, frame, trackers):
    print ("asignando vector a cada tracker")
    print ("en total " + str(len(lines)) + " vectores y " + str(len(trackers)) + " trackers")
    print ("vectores", lines)
    # asiganmos los vectores de flujo a cada tracker segun su posicion
    for tr in trackers:
        tr.clean_flow_vector()
        i = 0
        while True:
            if i >= len(lines):
                break
            if tr.is_inside(lines[i]):
                tr.add_vector(lines[i])
                lines.pop(i)
            i = i + 1

        print (str(len(tr.flow_vectors)) + " asignados al tracker")
        print (tr.flow_vectors)

    # buscamos que tracker se interceptan
    for i in range(len(trackers)):
        for j in range(len(trackers)):
            if i != j:
                tr_a = trackers[i].get_position()
                tr_b = trackers[j].get_position()

                if tr_a.left() > tr_b.right() or tr_b.left() > tr_a.right():
                    print("no overlapping")
                elif tr_a.top() < tr_b.bottom() or tr_b.top() > tr_a.bottom():
                    print("no overlapping")
                else:
                    if trackers[i].intersect_with(trackers[j], frame):
                        print ("POSIBLE CAR CRASH")




    '''
    print("vericando intersecciones entre " + str(len(lines)))
    print(lines)
    for i in range(0, len(lines)):
        for j in range(0, len(lines)):
            #L1 = line([lines[i][0], lines[i][1]], [lines[i][2], lines[i][3]])
            #L2 = line([lines[j][0], lines[j][1]], [lines[j][2], lines[j][3]])
            #print([lines[i][0], lines[i][1]], [lines[i][2], lines[i][3]], [lines[j][0], lines[j][1]], [lines[j][2], lines[j][3]])

            a1 = (lines[i][0], lines[i][1])
            a2 = (lines[i][2], lines[i][3])
            b1 = (lines[j][0], lines[j][1])
            b2 = (lines[j][2], lines[j][3])

            if i != j:
                # R = intersection(L1, L2)
                R = intersect(a1, a2, b1, b2)
                rows, cols, ch = frame.shape

                if R:
                    print("Intersection detected", a1, a2, b1,b2)
                    overlay = frame.copy()
                    cv2.rectangle(overlay, (0, 0), (cols - 1, rows - 1), (0, 0, 255), -1)
                    opacity = 0.4
                    cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
                    
    '''




'''
detections = yolo.detect(net, meta, "/home/vicente/projects/violence/car-crash/car3.jpeg")
img = cv2.imread("/home/vicente/projects/violence/car-crash/car3.jpeg")

print(detections)
print len(detections)

for det in detections:
    label = det[0]
    accuracy = det[1]
    box = det[2]

    width = int(box[2])
    height = int(box[3])
    xmin = int(box[0]) - width/2
    ymin = int(box[1]) - height/2

    cv2.rectangle(img, (xmin, ymin), (xmin + width, ymin + height), (0, 0, 255))

cv2.imshow("win", img)
cv2.waitKey(0)
'''


#goog: 10, 6,

start_process("choque10.mp4")



#for file in glob.glob("dataset/Accidents/*.mp4"):
#    start_process(file, net, meta)

#np.savetxt("data.csv", data, delimiter=",")




