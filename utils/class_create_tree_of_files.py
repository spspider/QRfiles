import os
import json

def insert_dash(string, index):
    return string[:index] + r"\\" + string[index + 1:]


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

class tree_of_files:
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
        Array_lineswithfiles.append("}")
        return Array_lineswithfiles

    def create_tree_of_files_json(dir_path):
        tree = {}
        for root, dirs, files in os.walk(dir_path):
            # remove the base directory from the path
            rel_path = root.replace(dir_path, '', 1).lstrip('/')
            # create a dictionary for each subdirectory
            subdir = tree.setdefault(rel_path, {})
            for filename in files:
                # add each file to the current subdirectory
                subdir[filename] = None
        return json.dumps(tree)
