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

from class_shared_utilites import shared_utilites

readsize = 2000
class join:
    def join(fromdir, tofile):
        shared_utilites.createDirfromFile(tofile)
        tofile = tofile.replace("\\","/")
        print(tofile)
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
        output.close(  )

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