# Importing library
import re

from os import listdir
from os.path import isfile, join
import json

tree_of_files_json = r"output.json"
dir_path: str = r'ProgramToSend'
folder_to_split = "splitted3"

def onlyfiles():
    onlyfiles = [f for f in listdir(folder_to_split) if isfile(join(folder_to_split, f))]
    onlyfiles.sort()
    return onlyfiles
def decodePart_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
class JsonHeader:
    f = "",
    a = "",
    p = ""
import qrcode
origianal_filename = "file"
onlyfiles_list = onlyfiles()
for each_file in onlyfiles_list:

# Data to encode
    with open(folder_to_split + "\\" + each_file, mode='r') as file: # b is important -> binary
        fileContent = file.read()
        JsonHeader_json = JsonHeader()
        JsonHeader_json.p = decodePart_number(each_file)  # part_file
        JsonHeader_json.a = len(onlyfiles_list)  # allfiles
        JsonHeader_json.f = str(origianal_filename)  # filename
        metadata='{"p": 2, "a": 5, "f": "ProgramToSend\\m_IoTManager\\CaptivePortalAdvanced.ino"}'
        # print(fileContent)
        data = metadata+str(fileContent)
        print(data)
        img = qrcode.make(fileContent)
        img.save('MyQRCode3.png')
import os

# filename = "output/file/file"
# baseFolder = "folder123"
# directory_created =""
# if '/' in filename:
#     directory = baseFolder+"/"+filename.rsplit('/', 1)[0]
#     if not os.path.exists(directory):  # caller handles errors
#         for each_directory in directory.split("/"):
#             directory_created += each_directory + "/"
#             os.mkdir(directory_created)  # make dir, read/write parts
