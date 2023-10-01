import json
import os
from collections import namedtuple
import re
from pyzbar.pyzbar import decode as qr_decode
import cv2
import numpy as np

from utils.class_shared_utilites import shared_utilites
from utils.class_join import class_join_join


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
    qr_data = findQR_and_return_data_byPyZbar(image)
    if qr_data is not None:
        return qr_data
recieve_folder = "recieved/"


def check_if_all_files_exists(number_all_of_files, recieve_folder, final_file_location):
    parts = os.listdir(recieve_folder)
    parts.sort()
    if len(parts) == number_all_of_files:
        print("Count files match")
        return True
    else:
        return False
    pass


def writefile(scanned_data):
    # print(scanned_data)
    metadata_index = scanned_data.index("\n&&&&&&&&&&&&777777777777\n") + 1
    metadata_recieved = scanned_data[:metadata_index] # full metadata
    string_recieved = scanned_data[metadata_index + 25:len(scanned_data)] # which data we are recieved
    metadata_json = json.loads(metadata_recieved, object_hook=customStudentDecoder)
    number_of_file = int(metadata_json.p)
    number_all_of_files = int(metadata_json.a)
    original_filename = str(metadata_json.f).replace("\\", "/").replace("¥¥", "/")

    filename = recieve_folder + ('part%04d' % number_of_file)
    shared_utilites.write_file(filename, string_recieved)

    # if number_of_file == number_all_of_files:

        # end of transportation
    final_file_location = "recieved_files\\" + original_filename
    if check_if_all_files_exists(number_all_of_files, recieve_folder, final_file_location) == True:
        if os.path.isfile(final_file_location):
            os.remove(final_file_location)
        class_join_join.join(recieve_folder, final_file_location)
        if os.path.isdir(recieve_folder):
            for eachFile in shared_utilites.load_splitted_files(recieve_folder):
                os.remove(recieve_folder + "/" + eachFile)
        # move_file


        # shared_utilites.create_folder("folder/","folder/"+original_filename)

        # os.rename(filename,"folder/"+original_filename)
class write_file_and_deocde:
    previous_number = 0
    def decodeimag(img):
        scanned_data = readQR(img)
        if scanned_data is not None:
            writefile(scanned_data)

