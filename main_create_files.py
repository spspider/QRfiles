import os
import re
import shutil
import sys
import qrcode
import cv2
from os import listdir
from os.path import isfile, join
import json

from cv2_utils import cv2_utils
from class_write_file_and_decode import write_file_and_deocde
from class_create_tree_of_files import tree_of_files
from class_shared_utilites import shared_utilites


import numpy as np
from class_spilt import splitfile

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1500) #default: roughly a floppy

# import split
tree_of_files_json = r"output.json"
dir_path: str = r'ProgramToSend'
folder_to_split = "splitted3"

array_of_files = tree_of_files.create_tree_of_files(dir_path)
shared_utilites.write_file(tree_of_files_json, array_of_files)
#craatefilelist


def onlyfiles():
    onlyfiles = [f for f in listdir(folder_to_split) if isfile(join(folder_to_split, f))]
    onlyfiles.sort()
    return onlyfiles

def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1
class JsonHeader:
    f = ""
    a = 0
    p = 0,
class User():
  def __init__(self, input):
      self.__dict__.update(input)
def decodePart_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
def showQRcode(each_file,origianal_filename,onlyfiles):

    with open(folder_to_split + "\\" + each_file, mode='rb') as each_splitted_file: # b is important -> binary
        JsonHeader_json = JsonHeader()
        JsonHeader_json.p = decodePart_number(each_file) #part_file
        JsonHeader_json.a = len(onlyfiles) #allfiles
        JsonHeader_json.f = str(origianal_filename) #filename
        fileContent = str(json.dumps(JsonHeader_json.__dict__)) + str(each_splitted_file.read())

    print(fileContent)
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
def startSendFiles(filename_path, name_filename):
    #splitfile and send
    file = filename_path +"\\" + name_filename
    splitfile.split(file, folder_to_split, chunksize)
    for each_onlyfiles in onlyfiles():
        showQRcode(each_onlyfiles,file,onlyfiles())
        # input("Press Enter to continue..."+each_onlyfiles)



def create_sequence():
    json_file_list = listToString(array_of_files)
    user = json.loads(json_file_list, object_hook=User)
    for key, value in json.loads(json_file_list).items():
        for each_filename in value:
            startSendFiles(key,each_filename)

create_sequence()

    ######################################3

# for each_file in onlyfiles:
#     # input("Press Enter to continue...")
#     showQRcode(each_file,file)
sys.exit()
# print(onlyfiles)
# fileName = "splitted3/part0001"
# # Data to encode
