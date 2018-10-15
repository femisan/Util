import os
import sys
def getFilePathList(foldar_path,file_type=None):
    """
    :param foldar_path: the foldar you want to traversal
    :param file_type:  extract file path list by file_type, if it's None, return all
    :return:     file list
    """
    file_list =[]
    for root, dirs, files in os.walk(foldar_path):
        for file in files:
            if file_type is None or file_type in file.lower():
                file_list.append(os.path.join(root,file))
    return file_list

class lazy(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val
