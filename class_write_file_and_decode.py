import json
import os
from collections import namedtuple
import re
from pyzbar.pyzbar import decode as qr_decode

import class_join
from class_shared_utilites import shared_utilites
from class_join import join
def customStudentDecoder(studentDict):
    return namedtuple('X', studentDict.keys())(*studentDict.values())

def decodePart_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
def readQR(image):
    qr = qr_decode(image)
    if qr:
        data = qr[0].data.decode("utf-8")
        return data

def writefile(scanned_data):
    metadata_index = scanned_data.index("}b'", 0, 120) + 1
    metadata_recieved = scanned_data[:metadata_index]
    string_recieved = scanned_data[metadata_index + 2:len(scanned_data) - 1]
    metadata_json = json.loads(metadata_recieved, object_hook=customStudentDecoder)

    number_of_file = int(metadata_json.p)
    number_all_of_files = int(metadata_json.a)
    original_filename = metadata_json.f
    filename = "recieved/"+('part%04d' % number_of_file)
    shared_utilites.write_file(filename, string_recieved)
    if number_of_file == number_all_of_files:
        #end of transportation
        class_join.join.join("recieved/",original_filename)
        #move_file
        shared_utilites.create_folder("folder/",original_filename)
        os.rename(filename,"folder/"+original_filename)
class write_file_and_deocde:
    def decodeimag(img):
        scanned_data = readQR(img)
        writefile(scanned_data)

