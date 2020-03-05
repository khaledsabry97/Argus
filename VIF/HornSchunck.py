from time import sleep, time

from scipy.ndimage.filters import convolve as filter2, gaussian_filter
import numpy as np
import cv2
#
windowAvg =np.array([[1 / 12, 1 / 6, 1 / 12],
                     [1/6,    0, 1/6],
                     [1/12, 1/6, 1/12]], float)

windowX = np.array([[-1, 1],
                    [-1, 1]]) * .25 #kernel for computing d/dx

# windowX = np.array([[-1, 0,1],
#                     [-1, 0,1],
#                     [-1,0,1]]) * .25 #kernel for computing d/dx
#

windowY = np.array([[-1, -1],
                    [ 1, 1]]) * .25 #kernel for computing d/dy
#
# windowY = np.array([[-1, -1,-1],
#                     [0, 0,0],
#                     [1,1,1]]) * .25 #kernel for computing d/dx

windowT = np.ones((2, 2)) * .25


def HornSchunck(frame1, frame2, alpha=0.101, NumOfIter=8):
    """
    frame1: frame at t=0
    frame2: frame at t=1
    alpha: regularization constant
    NumOfIter: number of iteration
    """
    #if the frame is integers then we need to convert it to floats
    frame1 = frame1.astype(np.float32)
    frame2 = frame2.astype(np.float32)

    # making the shape of horizontal and vertical change
	# Set initial value for the flow vectors
    H = np.zeros([frame1.shape[0], frame1.shape[1]])
    V = np.zeros([frame1.shape[0], frame1.shape[1]])

	# Estimate derivatives
    [fx, fy, ft] = derivatives(frame1, frame2)


	# Iteration to reduce error
    for i in range(NumOfIter):
        # avrageing the flow vectors
        # hAvg = filter2(H, windowAvg)
        # vAvg = filter2(V, windowAvg)
        hAvg = cv2.filter2D(H, -1, windowAvg)
        vAvg = cv2.filter2D(V, -1, windowAvg)
        # common part of update step
        top = fx*hAvg + fy*vAvg + ft
        down = alpha**2 + fx**2 + fy**2
        der = top/down

        # iterative step
        H = hAvg - fx * der
        V = vAvg - fy * der

    M = pow(pow(H, 2) + pow(V, 2), 0.5)

    #for i in range(U.shape[0]):
    #    for j in range(U.shape[1]):
     #       M[i, j] = pow(pow(U[i, j], 2) + pow(V[i, j], 2), 0.5)

    return H,V, M


def derivatives(frame1, frame2):
    t = time()
    fx = filter2(frame1, windowX) + filter2(frame2, windowX)
    # fx = cv2.filter2D(frame1, -1, windowX) + cv2.filter2D(frame2, -1, windowX)
    fy = filter2(frame1, windowY) + filter2(frame2, windowY)
    # fy = cv2.filter2D(frame1, -1, windowY) + cv2.filter2D(frame2, -1, windowY)
   # ft = im2 - im1
    ft = filter2(frame1, windowT) + filter2(frame2, -windowT)
    # ft = cv2.filter2D(frame1, -1, windowT) - cv2.filter2D(frame2, -1, windowT)
    # print(time() - t)
    return fx,fy,ft

def draw_vectors_hs(im1, im2, step = 10):
    print("drawing vectors")
    t = time()
    im1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    im1_gray = cv2.GaussianBlur(im1_gray,(5,5),0)
    im2_gray = cv2.GaussianBlur(im2_gray,(5,5),0)


    U, V, M = HornSchunck(im1_gray, im2_gray)

    print(time() - t)
    rows, cols = im2_gray.shape
    # print(rows, cols, range(0, rows, step))
    for i in range(0, rows, step):
        for j in range(0, cols, step):
            x = int(U[i, j]*2)
            y = int(V[i, j] *2)
            # if pow(x**2+y**2,0.5) > 20 or pow(x**2+y**2,0.5) < 10:
            #     continue
            cv2.arrowedLine(im2, (j, i), (j + x, i + y), (255, 0, 0))
            # cv2.circle(im2, (j, i), 1, (0, 0, 255), -1)
    return im2



if __name__ == "__main__":
    cap = cv2.VideoCapture("2.mkv")
    i =0
    while(i < 200):
        ret, frame = cap.read()  # get first frame
        i+=1
    ret,old = cap.read()
    while(True):
        ret, new = cap.read()
        ret, new = cap.read()
        if not ret:
            break


        # kernel = np.ones((3, 3), np.float32) / 9
        # new  = cv2.filter2D(new, -1, kernel)
        ret = draw_vectors_hs(old,new)
        old = new
        cv2.imshow("frame", ret)
        cv2.waitKey(1)

    cv2.destroyAllWindows()






























def ccw(A,B,C):
	return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])


def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

# buscamos si hay vectores de flujo optico que se intersectan, a fuerza bruta
def check_intersection(lines, frame):
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
cap = cv2.VideoCapture('normal2 .avi')
index = 0
frames = []
cv2.namedWindow('win',cv2.WINDOW_NORMAL)
while True:
    ret, frame = cap.read()

    if ret:

        frames.append(frame)

        # solo procesamos yolo una vez
        if index > 1:
            draw_vectors(frames[-2], frames[-1])


        cv2.imshow("win", frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

        index += 1

    else:
        break

cv2.destroyAllWindows()
'''


''' lukas kanade
cap = cv2.VideoCapture('normal7.mp4')
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
while not ret:
    print()
    ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

while(1):
    ret,frame = cap.read()
    if ret:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

        lines = []
        # draw the tracks
        for i, (new, old) in enumerate(zip(good_new,good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            lines.append((a, b, c, d))
            mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
            frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
            cv2.line(frame, (a, b), (c, d), (0, 0, 255), 1)
            # frame = cv2.circle(frame, (c, d), 5, (255,0 ,0), -1)

        check_intersection(lines, frame)


        img = cv2.add(frame,mask)

        cv2.imshow('frame',img)
        if cv2.waitKey() & 0xFF == ord('q'):
            break
    else:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()
'''