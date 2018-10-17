import os
import sys
import pickle
import scipy.io

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

def readPickle(file_name):
    if '.pkl' not in file_name:
        file_name = file_name +'.pkl'
    with open(file_name, "rb") as f:
        return pickle.load(file=f)

def writePickle(file_name,variable):
    if '.pkl' not in file_name:
        file_name = file_name + '.pkl'
    with open(file_name,'wb') as f:
        pickle.dump(variable, f, protocol = pickle.HIGHEST_PROTOCOL)

def readMat(file_name):
    mat = scipy.io.loadmat(file_name)
    print ('this mat file have variables: ',mat.keys())
    return mat
