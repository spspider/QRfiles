import os
import codecs
class shared_utilites:
    def write_file(filename, lines):
        if '/' in filename:
            direcory = filename.rsplit('/', 1)[0]
            if not os.path.exists(direcory):  # caller handles errors
                os.mkdir(direcory)  # make dir, read/write parts
        f = open(filename, "w")
        f.close()
        f = codecs.open("temp_file", "a", "utf-8")
        for line in lines:
            f.write(line)
        f.close()
        # convert
        with open("temp_file", 'r', encoding='utf-8') as inp, \
                open(filename, 'w', encoding='utf-8') as outp:
            for line in inp:
                outp.write(line)
        os.remove("temp_file")

    def create_folder(baseFolder,filename):
        directory_created =""
        if '/' in filename:
            directory = baseFolder+filename.rsplit('/', 1)[0]
            if not os.path.exists(directory):  # caller handles errors
                for each_directory in directory.split("/"):
                    directory_created += each_directory + "/"
                    os.mkdir(directory_created)  # make dir, read/write parts