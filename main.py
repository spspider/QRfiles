# CHUNK_SIZE = 5
import os
# file_number = 1
filename = 'main.7z'
# if not os.path.exists(filename+"1"):
#     os.mkdir(filename+"1")
# with open(filename) as f:
#     chunk = f.read(CHUNK_SIZE)
#     while chunk:
#         with open('my_song_part_' + str(file_number)) as chunk_file:
#             chunk_file.write(chunk)
#         file_number += 1
#         chunk = f.read(CHUNK_SIZE)
import sys

################################3
# from pip._vendor.msgpack.fallback import xrange
#
# filePath = 'main.7z'
# yuv_string_bytes = bytes(open(filePath, 'rb').read())
#
# file_uv = open("uv_buffer", "wb+")
# file_y = open("y_buffer", "wb+")
# for i in xrange(0, len(yuv_string_bytes), 2):
#     uv = bytes(yuv_string_bytes[i])
#     y = bytes(yuv_string_bytes[i+1])
#     file_uv.write(uv)
#     file_y.write(y)
#
# file_y.close()
# file_uv.close()

# File to open and break apart
fileR = open(filename, "rb")
chunk = 0
how_many_bytes = 1024
byte = fileR.read(how_many_bytes)
directory = filename+"dir"
if not os.path.exists(directory):
    os.mkdir(directory)
while byte:
    # Open a temporary file and write a chunk of bytes
    fileN = str(directory)+"/chunk" + str(chunk) + ".f"
    fileT = open(fileN, "wb")
    fileT.write(byte)
    fileT.close()
    # Read next 1024 bytes
    byte = fileR.read(how_many_bytes)
    chunk += 1
# join file

