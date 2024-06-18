import json
import os
from collections import namedtuple
import re
from pyzbar.pyzbar import decode as qr_decode
import cv2
import pyperclip

import pyautogui
import time

import numpy as np

from utils.class_shared_utilites import shared_utilites
from utils.class_join import class_join_join

recieve_folder = "recieved/"

def customStudentDecoder(studentDict):
    return namedtuple('X', studentDict.keys())(*studentDict.values())
def findQR_and_return_data_byQRSscanner(image):
    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # create QR code detector object
    detector = cv2.QRCodeDetector()
    # detect and decode QR codes in the image
    data, points, straight_qrcode = detector.detectAndDecode(gray)
    # if a QR code was detected, return the decoded data
    if data:
        return data
    else:
        return None
def findQR_and_return_data_byPyZbar(image):
    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect and decode QR codes in the image
    decoded_objects = qr_decode(gray)

    # if a QR code was detected, extract and return the data
    if decoded_objects:
        # extract data from the first decoded object in the list
        data = decoded_objects[0].data.decode('utf-8')
        return data
    else:
        return None
def decodePart_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
def readQR(image):
    # qr_data = findQR_and_return_data_byQRSscanner(image)
    try:
        qr_data = findQR_and_return_data_byPyZbar(image)
        if qr_data is not None:
            return qr_data
    except ValueError:
        print("problem with reading  data at file")
        pyautogui.keyDown('s')
        pyautogui.keyUp('s')



def check_if_all_files_exists(number_all_of_files, recieve_folder):
    parts = os.listdir(recieve_folder)
    parts.sort()
    if len(parts) == number_all_of_files:
        print("Count files match")
        return True
    else:
        return False
    pass

def list_of_parts(directory_files,filename):
    pattern = re.compile(f"{filename}part\d+$")
    # get a list of all files in the directory that match the pattern
    partfiles = [f for f in os.listdir(directory_files) if pattern.match(f)]
    # sort the list of files by their numeric part
    partfiles.sort(key=lambda f: int(f[len(filename) + 4:]))
    return partfiles
def check_if_all_files_exists_partfiles(number_all_of_files, directory_files, filename):
    # create a regular expression pattern to match the desired filenames
    # escape any special characters in the filename
    escaped_filename = re.escape(filename)
    pattern = re.compile(f"{escaped_filename}part\d+$")
    partfiles = [f for f in os.listdir(directory_files) if pattern.search(f)]
    # sort the list of files by their numeric part
    partfiles.sort(key=lambda f: int(f[len(filename) + 4:]))
    # check if all expected files exist
    all_files_exist = len(partfiles) == number_all_of_files and all(os.path.isfile(os.path.join(directory_files, f)) for f in partfiles)
    if all_files_exist:
        return True
    return False
        # print("All files exist.")


def delete_all_part_files(directory_files, filename):
    pattern = re.compile(f"{filename}part\d+$")
    # get a list of all files in the directory that match the pattern
    partfiles = [f for f in os.listdir(directory_files) if pattern.match(f)]
    # sort the list of files by their numeric part
    partfiles.sort(key=lambda f: int(f[len(filename) + 4:]))
    for f in os.listdir(directory_files):
        if pattern.match(f) and f != filename:
            os.remove(os.path.join(directory_files, f))
    pass

previous_file = ""
def pressAndWait(char,filename_part):
    global previous_file
    if previous_file != filename_part:
        pyautogui.press(char)
        previous_file = filename_part
        print(filename_part)
    else:
        # for i in range(2, 0, -1):
        #     print(i)
        time.sleep(0.25)
        # pyautogui.keyDown(char)
        # # time.sleep()
        # pyautogui.keyUp(char)

def writefile(scanned_data,overwrite):
    global previous_file
    metadata_index = -1
    try:
        metadata_index = scanned_data.index("\n&&&&&&&&&&&&777777777777\n") + 1
        metadata = scanned_data[metadata_index:]
    except ValueError:
        # print("Error: Metadata marker not found in scanned data")
        #detached
        print(scanned_data)
        pyperclip.copy(scanned_data)
        exit(1)
    metadata_recieved = scanned_data[:metadata_index] # full metadata

    string_recieved = scanned_data[metadata_index + 25:len(scanned_data)] # which data we are recieved
    metadata_json = json.loads(metadata_recieved, object_hook=customStudentDecoder)
    number_of_file = int(metadata_json.p)
    number_all_of_files = int(metadata_json.a)
    original_filename = str(metadata_json.f).replace('\\', '/').replace("¥¥", "/")
    ####################feature recieve with folder name
    filename_part = os.path.join(recieve_folder, original_filename + ('part%04d' % number_of_file))
    filename = os.path.join(recieve_folder, original_filename)
    if not os.path.exists(filename):
        shared_utilites.write_file(filename_part, string_recieved)
    else:
        # there should write some another output, like s - file exist, and we need to pass transmission
        pressAndWait('s', filename_part)
        print("File exist, skip",filename)
        return
    ##########################

    # directory_files = (recieve_folder + "/" + original_filename).rsplit('/', 1)[0]
    directory_files = os.path.dirname(os.path.join(recieve_folder, original_filename))
    filename = original_filename.rsplit('/', 1)[-1]
    if number_all_of_files == number_of_file: # latest file in sequence
        if check_if_all_files_exists_partfiles(number_all_of_files,directory_files,filename) != True:
            # end of transmittion of one file, if number of files less then actual number, then we need repeat transmittion.
            print("ERRRRRRRROOOORRR file not recieved", original_filename)
            pressAndWait('a', filename_part)
            return

    if check_if_all_files_exists_partfiles(number_all_of_files,directory_files,filename) == True:
        file = class_join_join.join_filename(directory_files,filename)
        # copy file to clipboard:
        with open(file, "r") as file:
            file_text = file.read()
        pyperclip.copy(file_text)

        # send End of transmittion:
    time.sleep(0.25)
    pressAndWait('q',filename_part)

class write_file_and_deocde:
    previous_number = 0
    def decodeimag(img,overwrite):
        scanned_data = readQR(img)
        if scanned_data is not None:
            writefile(scanned_data,overwrite=overwrite)

