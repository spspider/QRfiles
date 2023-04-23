import numpy as np
import cv2
from mss import mss
from PIL import Image
resolutionX = 1920
resolutionY = 1080
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
while True:
    sct_img = sct.grab(bounding_box)

    frame_array = np.array(sct_img)
    # frame_array = np.flip(frame_array[:, :, :3], 2)
    screenName = 'screen'
    dim = ResizeWithAspectRatio(frame_array, width=600)
    resize = cv2.resize(frame_array, dim)
    drawRectangle(imageRect)
    cv2.imshow(screenName, resize)
    imageRect = cv2.getWindowImageRect(screenName)
    #
    # print(dim)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(frame_array)

    if data:
        print(data)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break