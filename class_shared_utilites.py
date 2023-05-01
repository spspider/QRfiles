import os
import codecs
class write_lines_to_files:
    def write_file(file, lines):
        direcory = file.rsplit('/', 1)[0]
        print(direcory)
        if not os.path.exists(direcory):  # caller handles errors
            os.mkdir(direcory)  # make dir, read/write parts
        f = open(file, "w")
        f.close()
        f = codecs.open("temp_file", "a", "utf-8")
        for line in lines:
            f.write(line)
        f.close()
        # convert
        with open("temp_file", 'r', encoding='utf-8') as inp, \
                open(file, 'w', encoding='utf-8') as outp:
            for line in inp:
                outp.write(line)
        os.remove("temp_file")