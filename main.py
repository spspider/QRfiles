import codecs
import os
import sys
import qrcode
import cv2


kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(2000) #default: roughly a floppy

# import split
file = "output.json"
dir_path: str = r'ProgramToSend'
folder_to_split = "splitted4"
# list to store files name
#convert to utf-8

from class_create_tree_of_files import tree_of_files
def write_file():

    f = open(file, "w")
    f.close()
    f = codecs.open("temp_file", "a", "utf-8")
    for line in tree_of_files.create_tree_of_files(dir_path):
        f.write(line)
    f.close()
    #convert
    with open("temp_file", 'r', encoding='utf-8') as inp, \
            open(file, 'w', encoding='utf-8') as outp:
        for line in inp:
            outp.write(line)
    os.remove("temp_file")

# os.system("split.py " + file + " splitted3 400")

def split(fromfile, todir, chunksize=chunksize):
    if not os.path.exists(todir):  # caller handles errors
        os.mkdir(todir)  # make dir, read/write parts
    else:
        for fname in os.listdir(todir):  # delete any existing files
            os.remove(os.path.join(todir, fname))
    partnum = 0
    input = open(fromfile, 'r', encoding='utf-8')  # use binary mode on Windows
    while 1:  # eof=empty string from read
        chunk = input.read(chunksize)  # get next part <= chunksize
        if not chunk: break
        partnum = partnum + 1
        filename = os.path.join(todir, ('part%04d' % partnum))
        fileobj = open(filename, 'w', encoding='utf-8')
        fileobj.write(chunk)
        fileobj.close()  # or simply open(  ).write(  )
    input.close()
    assert partnum <= 9999  # join sort fails if 5 digits
    return partnum
#split json file and send
write_file()
split(file, folder_to_split, chunksize)
# send
#craatefilelist

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(folder_to_split) if isfile(join(folder_to_split, f))]
onlyfiles.sort()

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
import json


class JsonHeader:
    filename = ""
    count = 0
    number_of_files = 0

def writefile(scanned_data):
    metadata_index = scanned_data.index("}b'",0,30)+1
    metadata_recieved = scanned_data[:metadata_index]
    string_recieved = scanned_data[metadata_index+2:len(scanned_data)-1]
    print(metadata_recieved)
    print(string_recieved)
def showQRcode(each_file):

    with open(folder_to_split + "\\" + each_file, mode='rb') as file: # b is important -> binary
        JsonHeader_json = JsonHeader()
        JsonHeader_json.filename = each_file
        fileContent = json.dumps(JsonHeader_json.__dict__) + str(file.read())
    img = qrcode.make(fileContent)
    #show image
    img.save('MyQRCode2.png')
    img = cv2.imread('MyQRCode2.png', cv2.IMREAD_ANYCOLOR)
    # imS = cv2.resize(img, (960, 540))
    resize = ResizeWithAspectRatio(img, width=600)
    cv2.imshow(each_file, resize)

    ########################################3

    #check if that file can be read
    from pyzbar.pyzbar import decode as qr_decode
    def readQR(image):
        qr = qr_decode(image)
        if qr:
            data = qr[0].data.decode("utf-8")
            return data
    scanned_data = readQR(img)
    writefile(scanned_data)

    cv2.waitKey()
    cv2.destroyAllWindows()
    ######################################3

for each_file in onlyfiles:
    # input("Press Enter to continue...")
    showQRcode(each_file)
    sys.exit()
# print(onlyfiles)
# fileName = "splitted3/part0001"
# # Data to encode
