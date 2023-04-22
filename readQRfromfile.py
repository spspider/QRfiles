import cv2
# read the QRCODE image
img = cv2.imread("MyQRCode2.png")
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
data, bbox, straight_qrcode = detector.detectAndDecode(img)
print(data)
#
#
