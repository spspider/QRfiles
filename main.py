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
dir_path = r'ProgramToSend'
folder_to_split = "splitted4"
# list to store files name
#convert to utf-8

def insert_dash(string, index):
    return string[:index] + r"\\" + string[index+1:]
def find_all_loc(vars, key):
    pos = []
    start = 0
    end = len(vars)
    while True:
        loc = vars.find(key, start, end)
        if loc == -1:
            break
        else:
            pos.append(loc)
            start = loc + len(key)
    return pos
# creating Json Object with direcoriesdef create_tree_of_files(dir_path):
def create_tree_of_files(dir_path):
    Array_lineswithfiles = []
    Array_lineswithfiles.append("{")
    for (dir_path, dir_names, file_names) in os.walk(dir_path):
        pos = find_all_loc(dir_path, "\\")
        num_pos = 0
        for xpos in pos:
            dir_path = insert_dash(dir_path,xpos+num_pos)
            num_pos += 1
        Array_lineswithfiles.append("\""+dir_path+"\":")
        filelist = ''
        if len(file_names) == 0:
            filelist += "[]"
        else:
            filelist += '['
            for x in file_names:
                filelist += "\"" + str(x) + "\"" + ", "
            filelist = filelist[:-2]
            filelist += ']'
        filelist += ", "

        # filelist = filelist[:-2]
        Array_lineswithfiles.append(str(filelist))
    Array_lineswithfiles[len(Array_lineswithfiles) - 1] = Array_lineswithfiles[len(Array_lineswithfiles) - 1][:-2]
    print()
    Array_lineswithfiles.append("}")
    return Array_lineswithfiles

def write_file():

    f = open(file, "w")
    f.close()
    f = codecs.open("temp_file", "a", "utf-8")
    for line in create_tree_of_files(dir_path):
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
            data = qr[0].data
            return data
    print(readQR(img))
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
