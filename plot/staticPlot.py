
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact, widgets
# from IPython.display import display
import warnings

# def plotMatrixIn3D(Mat,name='Surface Plot', figsize =(11,9)):
#
#     X,Y = np.meshgrid( np.arange(Mat.shape[0]), np.arange(Mat.shape[1]) )
#     # fig = plt.figure()
#     fig, ax0  = plt.subplots(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
#     ax = fig.add_subplot(111, projection='3d')
#     surf = ax.plot_surface(X, Y, Mat, cmap='bwr', linewidth=0)
#     fig.colorbar(scurf)
#     ax.set_title(name)
#     fig.show()


def plotImagesWithInteractBar(images,axis=2,title='',cbarName='',climit=None,figsize=(4,4),updown=False):
    """
    :param image: images you want to plot 3-dimension
    :param axis:  axis number contains multi images
    """

    fig, ax = plt.subplots(figsize=figsize)
    def replot_it(index):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            slc = [slice(None)] * len(images.shape)
            slc[axis] = slice(index,index+1)
            one_image = np.squeeze(images[slc])
            plotImageWithTitle(np.squeeze(one_image),title,cbarName,climit,figsize,updown)
            ax.figure.canvas.draw()
    interact(replot_it,index=(0,images.shape[axis]-1))

def plotMatIn3D(Mat,x=None,y=None,title='Title',x_label='x',y_label='y',figsize =(11,9),view_angle=210):
    if x is None or y is None:
        x,y = np.meshgrid( np.arange(Mat.shape[0]), np.arange(Mat.shape[1]) )

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.view_init(azim=view_angle)
    ax.plot_wireframe(X=x,Y=y,Z=Mat)
    plt.show()

def plotCrossLine(data,title='',cbarName='',climit=None,xlabel='x',ylabel='y'):
    fig = plt.figure()

    plt.plot(np.arange(len(data)),data)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.show()
    # cbar=fig.colorbar(plt,fraction=0.046, pad=0.04)
    # cbar.set_label(cbarName, rotation=270, labelpad=8)
    # if climit is not None:
    #     cbar.set_clim(climit)
    # cbar.draw_all()

def plotSelectedRange(freqLine,selectList,rfBand,title='Excited Figure'):
    fig = plt.figure()
    pixLen=len(freqLine)
    plt.plot(np.arange(pixLen),freqLine)
    for freq in selectList:
        line = np.zeros(pixLen)
        line[:]=freq
        plt.plot(line)
    plt.ylim(freqLine[0], freqLine[-1])
    plt.ylabel('Offset Frequency (Hz)')
    plt.xlabel('Image Position')
    plt.title(title)
    plt.show()
#
#
# def plotSeperatedOddEvenImage(image):
#     imagePix = image.shape[0]
#     evenImage = np.zeros((imagePix,imagePix))
#     oddImage = np.zeros((imagePix,imagePix))
#     for i in range(image.shape[2]):
#         if np.mod(i,2) == 0:
#             evenImage = evenImage + image[:,:,i] *i
#         else:
#             oddImage = oddImage + image[:,:,i] *i
#     plotImageWithTitle(evenImage,'Even Lines')
#     plotImageWithTitle(evenImage,'Odd Lines')
#     return oddImage,evenImage


def plotImageWithTitle(image,title='',cbarName='',climit=None,figsize=(11,9),updown=False):
    # plt.figure()
    clip_image = image.copy()
    if climit is not None:
        clip_image[clip_image > climit[1]] = climit[1]
        clip_image[clip_image < climit[0]] = climit[0]
    fig0, ax0 = plt.subplots(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
    if updown:
        imgplot=plt.imshow(clip_image,origin='lower')
    else:
        imgplot=plt.imshow(clip_image)
    imgplot.set_cmap('nipy_spectral')
#     imgplot.set_cmap('gist_rainbow')
    plt.title(title)
    cbar=fig0.colorbar(imgplot,fraction=0.046, pad=0.04)
    cbar.set_label(cbarName, rotation=270, labelpad=8)
    if climit is not None:
        cbar.set_clim(climit)
    cbar.draw_all()
    plt.show()

def plotMRIImage(image,title=None,cbarName='',climit=None,color ='gray',figsize=(5,5),norm=False,updown=True):
    # plt.figure()
    clip_image = image.copy()
    if norm:
        clip_image /= np.max(np.abs(clip_image))
    if climit is not None:
        clip_image[clip_image > climit[1]] = climit[1]
        clip_image[clip_image < climit[0]] = climit[0]
    fig0, ax0 = plt.subplots(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
    if updown:
        imgplot=plt.imshow(clip_image,origin='lower')
    else:
        imgplot=plt.imshow(clip_image)
    imgplot.set_cmap(color)
#     imgplot.set_cmap('gist_rainbow')
    if title is not None:
        plt.title(title)
    cbar=fig0.colorbar(imgplot,fraction=0.046, pad=0.04)
    cbar.set_label(cbarName, rotation=270, labelpad=8)
    if climit is not None:
        cbar.set_clim(climit)
    cbar.draw_all()
    plt.show()


def plotVectorStreamLine(Vx,Vy,cbarName='',climit=None):

    strength = np.sqrt(Vx**2+Vy**2)
    if Vx.shape != Vy.shape:
        print ("please make sure you have input with same size")
        return -1
    horizontalSize=Vx.shape[1]
    verticalSize = Vx.shape[0]

#     circle3 = plt.Circle((0, 0), 0.2, color='black', fill=False)
    X,Y = np.meshgrid( np.arange(horizontalSize), np.arange(verticalSize) )

    fig0, ax0 = plt.subplots(num=None, figsize=(11,9), dpi=80, facecolor='w', edgecolor='k')

    strm = ax0.streamplot(X, Y, Vx, Vy, color=strength,density=[1,2],cmap=plt.cm.plasma)
#     ax0.streamplot(-X, Y, -Vx, Vy, color=strength,density=[1,2], cmap=plt.cm.plasma)
    # ax0.add_artist(circle3)
    cbar=fig0.colorbar(strm.lines,fraction=0.046, pad=0.04)
    cbar.set_label(cbarName, rotation=270, labelpad=8)
    if climit is not None:
        cbar.set_clim(climit)
    cbar.draw_all()
