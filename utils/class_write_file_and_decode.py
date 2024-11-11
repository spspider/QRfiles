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
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = cv2.QRCodeDetector()
    data, points, straight_qrcode = detector.detectAndDecode(gray)
    if data:
        return data
    else:
        return None


def findQR_and_return_data_byPyZbar(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded_objects = qr_decode(gray)
    if decoded_objects:
        data = decoded_objects[0].data.decode('utf-8')
        return data
    else:
        return None


def decodePart_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())


def readQR(image):
    try:
        qr_data = findQR_and_return_data_byPyZbar(image)
        if qr_data is not None:
            return qr_data
    except ValueError:
        print("Problem with reading data at file")
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


def list_of_parts(directory_files, filename):
    pattern = re.compile(f"{filename}part\d+$")
    partfiles = [f for f in os.listdir(directory_files) if pattern.match(f)]
    partfiles.sort(key=lambda f: int(f[len(filename) + 4:]))
    return partfiles


def check_if_all_files_exists_partfiles(number_all_of_files, directory_files, filename):
    escaped_filename = re.escape(filename)
    pattern = re.compile(f"{escaped_filename}part\d+$")
    partfiles = [f for f in os.listdir(directory_files) if pattern.search(f)]
    partfiles.sort(key=lambda f: int(f[len(filename) + 4:]))
    all_files_exist = len(partfiles) == number_all_of_files and all(
        os.path.isfile(os.path.join(directory_files, f)) for f in partfiles)
    if all_files_exist:
        return True
    return False


def delete_all_part_files(directory_files, filename):
    pattern = re.compile(f"{filename}part\d+$")
    partfiles = [f for f in os.listdir(directory_files) if pattern.match(f)]
    partfiles.sort(key=lambda f: int(f[len(filename) + 4:]))
    for f in partfiles:
        os.remove(os.path.join(directory_files, f))
    pass


previous_file = ""


def pressAndWait(char, filename_part):
    global previous_file
    if previous_file != filename_part:
        pyautogui.press(char)
        previous_file = filename_part
        print(filename_part)
    else:
        pass
        time.sleep(0.1)


def writefile(scanned_data, overwrite):
    global previous_file
    metadata_index = -1
    try:
        metadata_index = scanned_data.index("\n&&&&&&&&&&&&777777777777\n") + 1
        metadata = scanned_data[metadata_index:]
    except ValueError:
        print(scanned_data)
        pyperclip.copy(scanned_data)
        exit(1)

    metadata_recieved = scanned_data[:metadata_index]  # full metadata
    string_recieved = scanned_data[metadata_index + 25:len(scanned_data)]  # received data
    metadata_json = json.loads(metadata_recieved, object_hook=customStudentDecoder)

    number_of_file = int(metadata_json.p)
    number_all_of_files = int(metadata_json.a)
    original_filename = str(metadata_json.f).replace('\\', '/').replace("¥¥", "/")

    filename_part = os.path.join(recieve_folder, original_filename + ('part%04d' % number_of_file))
    filename = os.path.join(recieve_folder, original_filename)

    if overwrite or not os.path.exists(filename_part):
        shared_utilites.write_file(filename_part, string_recieved)
    else:
        pressAndWait('s', filename_part)
        print("File exists, skip", filename_part)
        return

    directory_files = os.path.dirname(os.path.join(recieve_folder, original_filename))
    filename = original_filename.rsplit('/', 1)[-1]

    if number_all_of_files == number_of_file:
        if not check_if_all_files_exists_partfiles(number_all_of_files, directory_files, filename):
            print("ERRRRRRRROOOORRR file not received", original_filename)
            pressAndWait('a', filename_part)
            return

    if check_if_all_files_exists_partfiles(number_all_of_files, directory_files, filename):
        file = class_join_join.join_filename(directory_files, filename)
        with open(file, "r") as file:
            file_text = file.read()
        pyperclip.copy(file_text)
        delete_all_part_files(directory_files, filename)  # Delete all part files upon successful transfer

    # time.sleep(0.1)
    pressAndWait('q', filename_part)


class write_file_and_deocde:
    previous_number = 0

    def decodeimag(img, overwrite):
        scanned_data = readQR(img)
        if scanned_data is not None:
            writefile(scanned_data, overwrite=overwrite)
