import json
from collections import namedtuple
import re
from pyzbar.pyzbar import decode as qr_decode


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


class write_file_and_deocde:
    def decodeimag(img):
        scanned_data = readQR(img)
        write_file_and_deocde.writefile(scanned_data)
    def writefile(scanned_data):
        metadata_index = scanned_data.index("}b'", 0, 30) + 1
        metadata_recieved = scanned_data[:metadata_index]
        string_recieved = scanned_data[metadata_index + 2:len(scanned_data) - 1]
        metadata_json = json.loads(metadata_recieved, object_hook=customStudentDecoder)
        print(decodePart_number(metadata_json.filename))
