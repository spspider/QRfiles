# Importing library
# import qrcode
# fileName = "splitted3/part0001"
# # Data to encode
# with open(fileName, mode='r') as file: # b is important -> binary
#     fileContent = file.read()
# # print(fileContent)
# data = fileContent
# img = qrcode.make(fileContent)
# img.save('MyQRCode3.png')
import os

filename = "output/file/file"
baseFolder = "folder123"
directory_created =""
if '/' in filename:
    directory = baseFolder+"/"+filename.rsplit('/', 1)[0]
    if not os.path.exists(directory):  # caller handles errors
        for each_directory in directory.split("/"):
            directory_created += each_directory + "/"
            os.mkdir(directory_created)  # make dir, read/write parts
