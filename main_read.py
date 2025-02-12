import time

import numpy as np
import cv2
from mss import mss
from utils.class_write_file_and_decode import write_file_and_deocde
from pyzbar.pyzbar import decode as qr_decode
sct = mss()
monitor = sct.monitors[1]
resolutionX = monitor['width']
resolutionY = monitor['height']
overwrite = True
bounding_box = {'top': 0, 'left': 0, 'width': resolutionX, 'height': resolutionY}
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return dim
def drawRectangle(imageRect):
    (x1_screen, y1_screen, width_screen, height_screen) = imageRect[:4]
    dimension1 = resolutionX / float(width_screen)
    x1 = int(x1_screen/dimension1)
    dimension2 = resolutionY / float(height_screen)
    y1 = int(y1_screen/dimension2)
    x2 = int(width_screen/dimension1 + x1)
    y2 = int(height_screen/dimension2 + y1)
    return cv2.rectangle(resize, (x1,y1), (x2, y2), (0, 0, 0), -1)
sct = mss()
imageRect = (1,1,1,1)




def readQR(image):
    try:
        qr = qr_decode(image)
        if qr:
            data = qr[0].data.decode("utf-8")
            return data
    except Exception:
        pass

for i in range(1, 0, -1):
    print(i)
    time.sleep(1)

while True:
    sct_img = sct.grab(bounding_box)

    frame_array = np.array(sct_img)
    screenName = 'screen'
    # dim = ResizeWithAspectRatio(frame_array, width=600)
    # resize = cv2.resize(frame_array, dim)
    # drawRectangle(imageRect)
    # cv2.imshow(screenName, resize)
    # imageRect = cv2.getWindowImageRect(screenName)
    try:
        write_file_and_deocde.decodeimag(frame_array,overwrite)
    except Exception:
        print(Exception)


    # if (cv2.waitKey(1) & 0xFF) == ord('q'):
    #     cv2.destroyAllWindows()
    #     break