import codecs
import os
import sys
import qrcode
import cv2
from os import listdir
from os.path import isfile, join
import json

import class_write_file_and_decode
from cv2_utils import cv2_utils
from class_write_file_and_decode import write_file_and_deocde
from class_create_tree_of_files import tree_of_files
from class_shared_utilites import write_lines_to_files

import numpy as np
from class_spilt import splitfile

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(2000) #default: roughly a floppy

# import split
file = "output.json"
dir_path: str = r'ProgramToSend'
folder_to_split = "splitted3"
# list to store files name
#convert to utf-8



# os.system("split.py " + file + " splitted3 400")


#split json file and send
write_lines_to_files.write_file(file, tree_of_files.create_tree_of_files(dir_path))
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
        JsonHeader_json.allfiles = len(onlyfiles)
        fileContent = json.dumps(JsonHeader_json.__dict__) + str(file.read())

    img = qrcode.make(fileContent)
    #show image
    frame_array = np.array(img)
    ########################################
    img.save('MyQRCode2.png')
    img = cv2.imread('MyQRCode2.png', cv2.IMREAD_ANYCOLOR)
    # imS = cv2.resize(img, (960, 540))
    resize = cv2_utils.ResizeWithAspectRatio(img, width=600)
    cv2.imshow(each_file, resize)
    #check if that file can be read
    write_file_and_deocde.decodeimag(img)

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
