from numpy.linalg import inv
import numpy as np
import cv2


class EstimateTranslation:

    def __init__(self):
        self.WINDOW_SIZE = 25

    def estimateAllTranslation(self, startXs, startYs, img1, img2):
        I = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        I = cv2.GaussianBlur(I, (5, 5), 0.2)
        Iy, Ix = np.gradient(I.astype(float))  # first order derivatives

        # reshape and initialization
        startXs_flat = startXs.flatten()
        startYs_flat = startYs.flatten()
        newXs = np.full(startXs_flat.shape, -1, dtype=float)
        newYs = np.full(startYs_flat.shape, -1, dtype=float)

        for i in range(np.size(startXs)):
            if startXs_flat[i] != -1:
                newXs[i], newYs[i] = self.estimateFeatureTranslation(startXs_flat[i], startYs_flat[i], Ix, Iy, img1, img2)
        newXs = np.reshape(newXs, startXs.shape)
        newYs = np.reshape(newYs, startYs.shape)
        return newXs, newYs

    def estimateFeatureTranslation(self, startX, startY, Ix, Iy, img1, img2):
        X = startX
        Y = startY
        mesh_x, mesh_y = np.meshgrid(np.arange(self.WINDOW_SIZE), np.arange(self.WINDOW_SIZE))
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        mesh_x_flat_fix = mesh_x.flatten() + X - np.floor(self.WINDOW_SIZE / 2)
        mesh_y_flat_fix = mesh_y.flatten() + Y - np.floor(self.WINDOW_SIZE / 2)
        coor_fix = np.vstack((mesh_x_flat_fix, mesh_y_flat_fix))
        I1_value = self.interp2(img1_gray, coor_fix[[0], :], coor_fix[[1], :])
        Ix_value = self.interp2(Ix, coor_fix[[0], :], coor_fix[[1], :])
        Iy_value = self.interp2(Iy, coor_fix[[0], :], coor_fix[[1], :])
        I = np.vstack((Ix_value, Iy_value))
        A = I.dot(I.T)

        for _ in range(15):
            mesh_x_flat = mesh_x.flatten() + X - np.floor(self.WINDOW_SIZE / 2)
            mesh_y_flat = mesh_y.flatten() + Y - np.floor(self.WINDOW_SIZE / 2)
            coor = np.vstack((mesh_x_flat, mesh_y_flat))
            I2_value = self.interp2(img2_gray, coor[[0], :], coor[[1], :])
            Ip = (I2_value - I1_value).reshape((-1, 1))
            b = -I.dot(Ip)
            solution = inv(A).dot(b)
            X += solution[0, 0]
            Y += solution[1, 0]

        return X, Y


    def interp2(self, v, xq, yq):
        if len(xq.shape) == 2 or len(yq.shape) == 2:
            dim_input = 2
            q_h = xq.shape[0]
            q_w = xq.shape[1]
            xq = xq.flatten()
            yq = yq.flatten()

        h = v.shape[0]
        w = v.shape[1]
        if xq.shape != yq.shape:
            raise 'query coordinates Xq Yq should have same shape'

        x_floor = np.floor(xq).astype(np.int32)
        y_floor = np.floor(yq).astype(np.int32)
        x_ceil = np.ceil(xq).astype(np.int32)
        y_ceil = np.ceil(yq).astype(np.int32)

        x_floor[x_floor < 0] = 0
        y_floor[y_floor < 0] = 0
        x_ceil[x_ceil < 0] = 0
        y_ceil[y_ceil < 0] = 0

        x_floor[x_floor >= w - 1] = w - 1
        y_floor[y_floor >= h - 1] = h - 1
        x_ceil[x_ceil >= w - 1] = w - 1
        y_ceil[y_ceil >= h - 1] = h - 1

        v1 = v[y_floor, x_floor]
        v2 = v[y_floor, x_ceil]
        v3 = v[y_ceil, x_floor]
        v4 = v[y_ceil, x_ceil]

        lh = yq - y_floor
        lw = xq - x_floor
        hh = 1 - lh
        hw = 1 - lw

        w1 = hh * hw
        w2 = hh * lw
        w3 = lh * hw
        w4 = lh * lw

        interp_val = v1 * w1 + w2 * v2 + w3 * v3 + w4 * v4

        if dim_input == 2:
            return interp_val.reshape(q_h, q_w)
        return interp_val
