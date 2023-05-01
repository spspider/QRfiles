import json
from collections import namedtuple
import re
from pyzbar.pyzbar import decode as qr_decode
from class_shared_utilites import write_lines_to_files

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
    metadata_index = scanned_data.index("}b'", 0, 50) + 1
    metadata_recieved = scanned_data[:metadata_index]
    string_recieved = scanned_data[metadata_index + 2:len(scanned_data) - 1]
    metadata_json = json.loads(metadata_recieved, object_hook=customStudentDecoder)

    number_of_file = decodePart_number(metadata_json.filename)
    number_all_of_files = int(metadata_json.allfiles)
    print(number_of_file)
    print(number_all_of_files)
    filename = "recieved/"+('part%04d' % number_of_file)
    write_lines_to_files.write_file(filename, string_recieved)

class write_file_and_deocde:
    def decodeimag(img):
        scanned_data = readQR(img)
        writefile(scanned_data)

