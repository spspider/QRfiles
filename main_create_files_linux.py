import os
import re
import sys
import cv2
import json
import cyrtranslit
import qrcode as qrcode

from utils.cv2_utils import cv2_utils
from utils.class_create_tree_of_files_linux import tree_of_files
from utils.class_shared_utilites_linux import shared_utilites


import numpy as np
from utils.class_spilt import splitfile

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



def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1
class JsonHeader:
    f = "",
    a = "",
    p = ""
class User():
  def __init__(self, input):
      self.__dict__.update(input)
def decodePart_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
def showQRcode(each_file,origianal_filename,onlyfiles):
    with open(folder_to_split + "\\" + each_file,encoding="utf-8", mode='r') as each_splitted_file: # b is important -> binary
        JsonHeader_json = JsonHeader()
        JsonHeader_json.p = decodePart_number(each_file) #part_file
        JsonHeader_json.a = len(onlyfiles) #allfiles
        JsonHeader_json.f = str(origianal_filename).replace("\\","/") #filename
        fileContent = str(json.dumps(JsonHeader_json.__dict__)) + "\n&&&&&&&&&&&&777777777777\n"+ str(each_splitted_file.read())
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=2,
        )
        qr.add_data(fileContent, optimize=0)
        qr.make()
        text = qr.make_ascii()
        print(text)
        #show image
#         frame_array = np.array(img)
#         ########################################
#         img.save('MyQRCode2.png')
#         img = cv2.imread('MyQRCode2.png', cv2.IMREAD_ANYCOLOR)
#         # imS = cv2.resize(img, (960, 540))
#         resize = cv2_utils.ResizeWithAspectRatio(img, width=600)
#         cv2.imshow(each_file, resize)
#         #check if that file can be read
#         # Disabling write and decode function, to test it
#         # write_file_and_deocde.decodeimag(img)
#         while True:
#             key = cv2.waitKey()
#             if key == ord('q'):
#                 cv2.destroyAllWindows()
#                 break  # exit the loop
def trasnlit_each_file(splitted_file):
    file1 = open(splitted_file,encoding = 'utf-8', mode = 'r')
    Lines = file1.readlines()
    count = 0
    # Strips the newline character
    Array_Of_Lines = []
    for line in Lines:
        count += 1
        line_traslitted = cyrtranslit.to_latin(line.strip())
        Array_Of_Lines.append(line_traslitted.join("\n"))
    shared_utilites.write_file(splitted_file, Array_Of_Lines)


def startSendFiles(filename_path, name_filename):
    #splitfile and send
    file = filename_path +"\\" + name_filename

    #delete in splitted folder
    if os.path.isdir(folder_to_split):
        for eachFile in shared_utilites.load_splitted_files(folder_to_split):
            os.remove(folder_to_split+"/"+eachFile)

    splitfile.split(file, folder_to_split, chunksize)
    get_splitted_files = shared_utilites.load_splitted_files(folder_to_split)
    for each_onlyfiles in get_splitted_files:
        # trasnlit_each_file(folder_to_split+"/"+each_onlyfiles)
        showQRcode(each_onlyfiles, file, get_splitted_files)
        # input("Press Enter to continue..."+each_onlyfiles)


def create_sequence():
    json_file_list = listToString(array_of_files)
    # user = json.loads(json_file_list, object_hook=User)
    for folder_to_file, value in json.loads(json_file_list).items():
        for each_filename in value:
            startSendFiles(folder_to_file,each_filename)

create_sequence()

    ######################################3

sys.exit()