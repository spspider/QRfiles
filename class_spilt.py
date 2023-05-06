#!/usr/bin/python
#########################################################
# split a file into a set of portions; class_join.py puts them
# back together; this is a customizable version of the
# standard unix split command-line utility; because it
# is written in Python, it also works on Windows and can
# be easily tweaked; because it exports a function, it
# can also be imported and reused in other applications;
#########################################################
#https://www.oreilly.com/library/view/programming-python-second/0596000855/ch04s02.html
import sys, os

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1500)  # default: roughly a floppy
class splitfile:
    def split(fromfile, todir, chunksize=chunksize):
        if not os.path.exists(todir):  # caller handles errors
            os.mkdir(todir)  # make dir, read/write parts
        else:
            for fname in os.listdir(todir):  # delete any existing files
                os.remove(os.path.join(todir, fname))
        try:
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
        except UnicodeDecodeError:
            return


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: split.py [file-to-split target-dir [chunksize]]')
    else:
        if len(sys.argv) < 3:
            interactive = 1
            fromfile = input('File to be split? ')  # input if clicked
            todir = input('Directory to store part files? ')
        else:
            interactive = 0
            fromfile, todir = sys.argv[1:3]  # args in cmdline
            if len(sys.argv) == 4: chunksize = int(sys.argv[3])
        absfrom, absto = map(os.path.abspath, [fromfile, todir])
        print('Splitting', absfrom, 'to', absto, 'by', chunksize)

        try:
            parts = splitfile.split(fromfile, todir, chunksize)
        except:
            print('Error during split:')
            # print(sys.exc_type, sys.exc_value)
        else:
            print('Split finished:', parts, 'parts are in', absto)
        if interactive: input('Press Enter key')  # pause if clicked