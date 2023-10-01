import os
import codecs
from os.path import isfile, join


class shared_utilites:
    @staticmethod
    def createDirfromFile(filename):
        tofile = filename.replace("\\", "/")
        directory_created = ""
        if '/' in tofile:
            directory = tofile.rsplit('/', 1)[0]
            if not os.path.exists(directory):  # caller handles errors
                for each_directory in directory.split("/"):
                    directory_created += each_directory + "/"
                    if not os.path.exists(directory_created):
                        os.mkdir(directory_created)

    @staticmethod
    def write_file(filename, lines):
        directory_created = ""
        if '/' in filename:
            directory = filename.rsplit('/', 1)[0]
            if not os.path.exists(directory):  # caller handles errors
                for each_directory in directory.split("/"):
                    directory_created += each_directory + "/"
                    if not os.path.exists(directory_created):
                        os.mkdir(directory_created)
        f = open(filename, "w")
        f.close()
        f = codecs.open("temp_file", mode="a", encoding="utf-8")
        for line in lines:
            f.write(line)
        f.close()
        # convert
        with open("temp_file", 'r', encoding='utf-8') as inp, \
                open(filename, 'w', encoding='utf-8') as outp:
            for line in inp:
                outp.write(line)
        os.remove("temp_file")

    @staticmethod
    def create_folder(baseFolder,filename):
        directory_created =""
        if '/' in filename:
            directory = baseFolder+filename.rsplit('/', 1)[0]
            if not os.path.exists(directory):  # caller handles errors
                for each_directory in directory.split("/"):
                    directory_created += each_directory + "/"
                    os.mkdir(directory_created)  # make dir, read/write parts

    @staticmethod
    def load_splitted_files(folder_to_split):
        onlyfiles = [f for f in os.listdir(folder_to_split) if isfile(join(folder_to_split, f))]
        onlyfiles.sort()
        return onlyfiles