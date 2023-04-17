# import cv2
# from cv2 import *
# def read_qr_code(filename):
#
#         img = cv2.imread(filename)
#         detect = cv2.QRCodeDetector()
#         value, points, straight_qrcode = detect.detectAndDecode(img)
#         return value
#
# print(read_qr_code(r'MyQRCode2.png'));
# with open('recieved/Failed.py', 'w')  as file:
#     file.write(str())
# file.close()

from qrtools import QR
myCode = QR(filename=r'MyQRCode2.png')
if myCode.decode():
  print (myCode.data)
  print (myCode.data_type)
  print (myCode.data_to_string())
