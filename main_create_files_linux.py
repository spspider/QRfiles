import os
import re
import sys
import json
import cyrtranslit
import qrcode as qrcode

from utils.class_create_tree_of_files_linux import tree_of_files
from utils.class_shared_utilites_linux import shared_utilites

import numpy as np
from utils.class_spilt import splitfile

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1500)  # default: roughly a floppy

# import split
tree_of_files_json = r"output.json"
dir_path: str = r'FilesToSend'
folder_to_split = "splitted3"

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


def showQRcode(each_file, origianal_filename, onlyfiles):
    with open(os.path.join(folder_to_split, each_file), encoding="utf-8",
              mode='r') as each_splitted_file:  # b is important -> binary
        JsonHeader_json = JsonHeader()
        JsonHeader_json.p = decodePart_number(each_file)  # part_file
        JsonHeader_json.a = len(onlyfiles)  # allfiles
        JsonHeader_json.f = str(origianal_filename).replace("\\", "/")  # filename
        fileContent = str(json.dumps(JsonHeader_json.__dict__)) + "\n&&&&&&&&&&&&777777777777\n" + str(
            each_splitted_file.read())
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=2,
        )

        qr = qrcode.QRCode(version=None, box_size=10, border=4)
        qr.add_data(fileContent, optimize=0)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save("test.png")

        # show image
def trasnlit_each_file(splitted_file):
    file1 = open(splitted_file, encoding='utf-8', mode='r')
    Lines = file1.readlines()
    count = 0
    # Strips the newline character
    Array_Of_Lines = []
    for line in Lines:
        count += 1
        line_traslitted = cyrtranslit.to_latin(line.strip())
        Array_Of_Lines.append(line_traslitted.join("\n"))
    shared_utilites.write_file(splitted_file, Array_Of_Lines)


def startSendFiles(file):
    # splitfile and send
    # delete in splitted folder
    if os.path.isdir(folder_to_split):
        for eachFile in shared_utilites.load_splitted_files(folder_to_split):
            os.remove(folder_to_split + "/" + eachFile)

    splitfile.split(file, folder_to_split, chunksize)
    get_splitted_files = shared_utilites.load_splitted_files(folder_to_split)
    for each_onlyfiles in get_splitted_files:
        # trasnlit_each_file(folder_to_split+"/"+each_onlyfiles)
        showQRcode(each_onlyfiles, file, get_splitted_files)
        # input("Press Enter to continue..."+each_onlyfiles)


def list_all_files(root_dir):
    file_list = []
    for current_dir, dirs, files in os.walk(root_dir):
        # loop through all files in the current directory
        for file in files:
            # add the file to the list
            file_list.append(os.path.join(current_dir, file))
    return file_list


def create_sequence():
    list_of_files = list_all_files(dir_path)

    for each_file in list_of_files:
        startSendFiles(each_file)


create_sequence()