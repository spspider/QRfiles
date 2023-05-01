# Importing library
import qrcode
fileName = "splitted3/part0001"
# Data to encode
with open(fileName, mode='r') as file: # b is important -> binary
    fileContent = file.read()
# print(fileContent)
data = fileContent
img = qrcode.make(fileContent)
img.save('MyQRCode3.png')