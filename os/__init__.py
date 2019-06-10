import os
import sys
import pickle
import scipy.io
from datetime import datetime
import pydicom
import numpy as np
import numbers

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

def getDirsList(foldar_path,id_list=None):
    dir_list =[]
    for root, dirs, files in os.walk(foldar_path):
        for cur_dir in dirs:
            dir_list.append(os.path.join(root,cur_dir))
    # filter dir by id_list
    if id_list is None:
         return dir_list
    else:
        final_list = []
        id_str_list = ['_E'+str(id_num) for id_num in id_list]
        for one_id in id_str_list:
            final_list.append([x for x in dir_list if one_id in x][0])
        return final_list

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
    if os.path.isfile(file_name):
        file_name = file_name.split('.')[0] + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.pkl'
        print('File already existed, renamed to : ', file_name)
    with open(file_name,'wb') as f:
        pickle.dump(variable, f, protocol = pickle.HIGHEST_PROTOCOL)

def readMat(file_name):
    mat = scipy.io.loadmat(file_name)
    print ('this mat file have variables: ',mat.keys())
    return mat

def readDicomsToArray(dirPath):
    fileList = getFilePathList(dirPath)
    fileList.sort(key = lambda x: x.split('/')[-1])
    if len(fileList) == 0:
        print('file path name error')
        return -1
    refDicom = pydicom.read_file(fileList[0])
    refImage = refDicom.pixel_array
    dicomArray = np.zeros((refImage.shape[0],refImage.shape[1],len(fileList)))
    print('Dicom Files readed to array with shape : ' + str(dicomArray.shape))
    for i in range(len(fileList)):
        # print(fileList[i])
        dicomArray[:,:,i] = pydicom.read_file(fileList[i]).pixel_array
    return dicomArray
