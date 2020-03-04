from scipy.ndimage.filters import convolve as filter2
import numpy as np
import cv2
#
HSKERN =np.array([[1/12, 1/6, 1/12],
                  [1/6,    0, 1/6],
                  [1/12, 1/6, 1/12]],float)

kernelX = np.array([[-1, 1],
                     [-1, 1]]) * .25 #kernel for computing d/dx

kernelY = np.array([[-1,-1],
                     [ 1, 1]]) * .25 #kernel for computing d/dy

kernelT = np.ones((2,2))*.25


def HornSchunck(im1, im2, alpha=0.001, Niter=8, verbose=False):
    """
    im1: image at t=0
    im2: image at t=1
    alpha: regularization constant
    Niter: number of iteration
    """
    im1 = im1.astype(np.float32)
    im2 = im2.astype(np.float32)

	#set up initial velocities
    uInitial = np.zeros([im1.shape[0],im1.shape[1]])
    vInitial = np.zeros([im1.shape[0],im1.shape[1]])

	# Set initial value for the flow vectors
    U = uInitial
    V = vInitial

	# Estimate derivatives
    [fx, fy, ft] = computeDerivatives(im1, im2)

    #if verbose:
    #    from .plots import plotderiv
    #    plotderiv(fx,fy,ft)

#    print(fx[100,100],fy[100,100],ft[100,100])

	# Iteration to reduce error
    for _ in range(Niter):
#%% Compute local averages of the flow vectors
        uAvg = filter2(U, HSKERN)
        vAvg = filter2(V, HSKERN)
#%% common part of update step
        der = (fx*uAvg + fy*vAvg + ft) / (alpha**2 + fx**2 + fy**2)
#%% iterative step
        U = uAvg - fx * der
        V = vAvg - fy * der

    M = pow(pow(U, 2) + pow(V, 2), 0.5)

    #for i in range(U.shape[0]):
    #    for j in range(U.shape[1]):
     #       M[i, j] = pow(pow(U[i, j], 2) + pow(V[i, j], 2), 0.5)

    return U,V, M


def computeDerivatives(im1, im2):

    fx = filter2(im1,kernelX) + filter2(im2,kernelX)
    fy = filter2(im1,kernelY) + filter2(im2,kernelY)

   # ft = im2 - im1
    ft = filter2(im1,kernelT) + filter2(im2,-kernelT)

    return fx,fy,ft

def draw_vectors_hs(im1, im2, step = 16):
    print("drawing vectors")
    im1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    U, V, M = HornSchunck(im1_gray, im2_gray)

    rows, cols = im2_gray.shape

    print(rows, cols, range(0, rows, step))
    for i in range(0, rows, step):
        for j in range(0, cols, step):
            x = int(U[i, j]*2)
            y = int(V[i, j] *2)
            cv2.line(im2, (j, i), (j + x, i + y), (255, 0, 0))
            cv2.circle(im2, (j, i), 1, (255, 0, 0), -1)

def draw_vectors_lk(im1, im2):
    # params for ShiTomasi corner detection
    feature_params = dict(maxCorners=100,
                          qualityLevel=0.3,
                          minDistance=7,
                          blockSize=7)

    # Parameters for lucas kanade optical flow
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Create some random colors
    color = np.random.randint(0, 255, (100, 3))

    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)


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