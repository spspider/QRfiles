import json
from collections import namedtuple
def customStudentDecoder(studentDict):
    return namedtuple('X', studentDict.keys())(*studentDict.values())

class write_file_and_deocde:
    def writefile(scanned_data):
        metadata_index = scanned_data.index("}b'",0,30)+1
        metadata_recieved = scanned_data[:metadata_index]
        string_recieved = scanned_data[metadata_index+2:len(scanned_data)-1]
        metadata_json = json.loads(metadata_recieved, object_hook=customStudentDecoder)
        print(metadata_json.filename)
        print(string_recieved)