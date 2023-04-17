# Importing library
import qrcode
fileName = "splitted/part0001"
# Data to encode
with open(fileName, mode='rb') as file: # b is important -> binary
    fileContent = file.read()

data = fileContent
img = qrcode.make(data)
img.save('MyQRCode2.png')