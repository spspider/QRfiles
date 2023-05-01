import codecs
import os
import sys
import qrcode
import cv2
from os import listdir
from os.path import isfile, join
import json

from cv2_utils import cv2_utils
from class_write_file_and_decode import write_file_and_deocde
from class_create_tree_of_files import tree_of_files


kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(2000) #default: roughly a floppy

# import split
file = "output.json"
dir_path: str = r'ProgramToSend'
folder_to_split = "splitted4"
# list to store files name
#convert to utf-8

def write_file():
    f = open(file, "w")
    f.close()
    f = codecs.open("temp_file", "a", "utf-8")
    for line in tree_of_files.create_tree_of_files(dir_path):
        f.write(line)
    f.close()
    #convert
    with open("temp_file", 'r', encoding='utf-8') as inp, \
            open(file, 'w', encoding='utf-8') as outp:
        for line in inp:
            outp.write(line)
    os.remove("temp_file")

# os.system("split.py " + file + " splitted3 400")


#split json file and send
write_file()
from class_spilt import splitfile
splitfile.split(file, folder_to_split, chunksize)
# send
#craatefilelist


onlyfiles = [f for f in listdir(folder_to_split) if isfile(join(folder_to_split, f))]
onlyfiles.sort()




class JsonHeader:
    filename = ""
    count = 0
    number_of_files = 0,



def showQRcode(each_file):

    with open(folder_to_split + "\\" + each_file, mode='rb') as file: # b is important -> binary
        JsonHeader_json = JsonHeader()
        JsonHeader_json.filename = each_file
        fileContent = json.dumps(JsonHeader_json.__dict__) + str(file.read())
    img = qrcode.make(fileContent)
    #show image
    img.save('MyQRCode2.png')
    img = cv2.imread('MyQRCode2.png', cv2.IMREAD_ANYCOLOR)
    # imS = cv2.resize(img, (960, 540))
    resize = cv2_utils.ResizeWithAspectRatio(img, width=600)
    cv2.imshow(each_file, resize)

    ########################################3

    #check if that file can be read
    from pyzbar.pyzbar import decode as qr_decode
    def readQR(image):
        qr = qr_decode(image)
        if qr:
            data = qr[0].data.decode("utf-8")
            return data
    scanned_data = readQR(img)
    write_file_and_deocde.writefile(scanned_data)

    cv2.waitKey()
    cv2.destroyAllWindows()
    ######################################3

for each_file in onlyfiles:
    # input("Press Enter to continue...")
    showQRcode(each_file)
    sys.exit()
# print(onlyfiles)
# fileName = "splitted3/part0001"
# # Data to encode
