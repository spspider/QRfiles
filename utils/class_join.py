#!/usr/bin/python
##########################################################
# join all part files in a dir created by split.py.
# This is roughly like a 'cat fromdir/* > tofile' command
# on unix, but is a bit more portable and configurable,
# and exports the join operation as a reusable function.
# Relies on sort order of file names: must be same length.
# Could extend split/join to popup Tkinter file selectors.
##########################################################

import os, sys
import re
from utils.class_shared_utilites import shared_utilites

readsize = 1500
class class_join_join:
    def join(fromdir, tofile):
        shared_utilites.createDirfromFile(tofile)
        tofile = tofile.replace("\\","/")
        output = open(tofile,encoding="utf-8", mode='w')
        parts  = os.listdir(fromdir)
        parts.sort(  )
        for filename in parts:
            filepath = os.path.join(fromdir, filename)
            fileobj  = open(filepath,encoding="utf-8", mode='r')
            while 1:
                filebytes = fileobj.read(readsize)
                if not filebytes: break
                output.write(filebytes)
            fileobj.close(  )
            # os.unlink(fromdir+filename)
        output.close(  )

    def join_filename(directory, filename):
        # extract the basename and extension from the filename
        pattern = re.compile(f"{filename}part\d+$")
        # get a list of all files in the directory that match the pattern
        partfiles = [f for f in os.listdir(directory) if pattern.match(f)]
        # sort the list of files by their numeric part
        partfiles.sort(key=lambda f: int(f[len(filename) + 4:]))

        # create the output file and concatentate the part files into it
        output_filename = os.path.join(directory, filename)
        with open(output_filename, 'w', encoding='utf-8') as output:
            for partfile in partfiles:
                partfile_path = os.path.join(directory, partfile)
                with open(partfile_path, 'r', encoding='utf-8') as part:
                    output.write(part.read())
                os.remove(partfile_path)
        for f in partfiles:
            if f != filename:
                try:
                    os.remove(os.path.join(directory, f))
                except FileNotFoundError:
                    pass
        return output_filename
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: class_join.py [from-dir-name to-file-name]')
    else:
        if len(sys.argv) != 3:
            interactive = 1
            fromdir = input('Directory containing part files? ')
            tofile  = input('Name of file to be recreated? ')
        else:
            interactive = 0
            fromdir, tofile = sys.argv[1:]
        absfrom, absto = map(os.path.abspath, [fromdir, tofile])
        print('Joining', absfrom, 'to make', absto)

        try:
            join(fromdir, tofile)
        except:
            print('Error joining files:')
            # print(sys.exc_type, sys.exc_value)
        else:
           print('Join complete: see', absto)
        if interactive: input('Press Enter key') # pause if clicked