import cv2
import os
# # read the QRCODE image
# img = cv2.imread("MyQRCode2.png")
# # initialize the cv2 QRCode detector
# detector = cv2.QRCodeDetector()
# data, bbox, straight_qrcode = detector.detectAndDecode(img)
# print(data)
#
#
import qrcode
data = "123"
img = qrcode.make(data)
img.save('MyQRCode2.png')

from pyzbar.pyzbar import decode as qr_decode
def decoder(image):
    gray_img = cv2.imread(image)
    qr = qr_decode(gray_img)[0]

    qrCodeData = qr.data.decode("utf-8")
    return qrCodeData
def readQR(image):
    gray_img = cv2.imread(image)
    qr = qr_decode(gray_img)
    if qr:
        data = qr[0].data.decode("utf-8")
        return data



print(readQR("MyQRCode2.png"))

