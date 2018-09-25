import os
import sys
def getFilePathList(foldar_path,file_type=None):
    file_list =[]
    for root, dirs, files in os.walk(foldar_path):
        for file in files:
            if file_type is None or file_type in file.lower():
                file_list.append(os.path.join(root,file))
    return file_list
