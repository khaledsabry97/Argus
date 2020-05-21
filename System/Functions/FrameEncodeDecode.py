import base64
import numpy as np

import cv2


def imgEncode(frame):
    return base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()

def imgDecode(frame_base_64):
    jpg_original = base64.b64decode(frame_base_64)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img



