import os
import re
import sys
import cv2
import json
import cyrtranslit
import qrcode as qrcode

from utils.cv2_utils import cv2_utils
from utils.class_shared_utilites import shared_utilites
from utils.class_write_file_and_decode import write_file_and_deocde

import numpy as np
from utils.class_spilt import splitfile

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1500) #default: roughly a floppy

# import split
tree_of_files_json = r"output.json"
dir_path: str = r'FilesToSend'
folder_to_split = "splitted3"
skip_that_file = False
reset_index = False
#craatefilelist



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
def showQRcode(each_file, original_filename, onlyfiles):
    global skip_that_file, reset_index
    with open(os.path.join(folder_to_split, each_file), encoding="utf-8", mode='r') as each_splitted_file: # b is important -> binary
        JsonHeader_json = JsonHeader()
        JsonHeader_json.p = decodePart_number(each_file) #part_file
        JsonHeader_json.a = len(onlyfiles) #allfiles
        JsonHeader_json.f = str(original_filename) #.replace("\\","/") #filename
        fileContent = str(json.dumps(JsonHeader_json.__dict__)) + "\n&&&&&&&&&&&&777777777777\n"+ each_splitted_file.read()
        # print(fileContent)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=2,
        )
        qr.add_data(fileContent, optimize=0)
        img = qr.make_image(fill_color="black", back_color="white")
        #show image
        frame_array = np.array(img)
        ########################################
        img.save('MyQRCode2.png')
        img = cv2.imread('MyQRCode2.png', cv2.IMREAD_ANYCOLOR)
        # imS = cv2.resize(img, (960, 540))
        resize = cv2_utils.ResizeWithAspectRatio(img, width=600)
        cv2.imshow(each_file, resize)
        #check if that file can be read
        # Disabling write and decode function, to test it
        # write_file_and_deocde.decodeimag(frame_array)

        while True:
            key = cv2.waitKey()
            if key == ord('q'):
                cv2.destroyAllWindows()
                if JsonHeader_json.a == JsonHeader_json.p:
                    os.remove(original_filename)
                break  # exit the loop
            if key == ord('a'):
                #again transmittion
                cv2.destroyAllWindows()
                reset_index = True
                break  # exit the loop
            if key == ord('s'):
                # skip this file
                skip_that_file = True
                cv2.destroyAllWindows()

                break  # exit the loop

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

def startShowQRCode(get_splitted_files,file):
    global skip_that_file, reset_index
    for each_onlyfiles in get_splitted_files:
        # trasnlit_each_file(folder_to_split+"/"+each_onlyfiles)
        showQRcode(each_onlyfiles, file, get_splitted_files)  # Just an example function call
        # Check if we need to reset the loop
        if reset_index:
            reset_index = False
            startShowQRCode(get_splitted_files, file)
            break
        if skip_that_file:
            skip_that_file = False
            break
def startSendFiles(file):
        global skip_that_file, reset_index
        # splitfile and send
        # delete in splitted folder
        for file_name in folder_to_split:
            file_path = os.path.join(folder_to_split, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)


        splitfile.split(file, folder_to_split, chunksize)
        get_splitted_files = shared_utilites.load_splitted_files(folder_to_split)

        startShowQRCode(get_splitted_files, file)


def list_all_files(root_dir):
    file_list = []
    for current_dir, dirs, files in os.walk(root_dir):
        # loop through all files in the current directory
        for file in files:
            # add the file to the list
            file_list.append(os.path.join(current_dir, file))
    return file_list


def create_sequence():
    global skip_that_file
    skip_that_file = False

    list_of_files = list_all_files(dir_path)
    # list_of_files = list_all_files(r'recieved')
    for each_file in list_of_files:
        startSendFiles(each_file)
        print(each_file)



create_sequence()

    ######################################3

sys.exit()
