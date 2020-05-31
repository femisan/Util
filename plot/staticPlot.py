
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact, widgets
# from IPython.display import display
import warnings

# def plotMatrixIn3D(Mat,name='Surface Plot', figsize =(5,5)):
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

def plotMatIn3D(Mat,x=None,y=None,title='Title',x_label='x',y_label='y',figsize =(5,5),view_angle=210):
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


def plotImageWithTitle(image,title='',cbarName='',climit=None,figsize=(5,5),updown=False,axis=None):
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
    if axis is not None and axis is False:
        plt.axis('off')
    cbar=fig0.colorbar(imgplot,fraction=0.046, pad=0.04)
    cbar.set_label(cbarName, rotation=270, labelpad=8)
    if climit is not None:
        cbar.set_clim(climit)
    cbar.draw_all()
    plt.show()

def plotMRIImage(image,title=None,cbarName='',climit=None,color ='gray',figsize=(5,5),norm=False,updown=True,axis=None):
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
    if axis is not None and axis is False:
        plt.axis('off')
    cbar=fig0.colorbar(imgplot,fraction=0.046, pad=0.04)
    cbar.set_label(cbarName, rotation=270, labelpad=8)
    if climit is not None:
        cbar.set_clim(climit)
    cbar.draw_all()
    plt.show()

def plotMRIImageWithFieldMap(Image,fieldmap,title='',cbarName='',climit=None,figsize=(5,5),updown=False,alpha=0.5,axis=None):
    # plt.figure()
    fig0, ax0 = plt.subplots(num=None, figsize=figsize, dpi=80, facecolor='w', edgecolor='k')
    if updown:
        imgplot = plt.imshow(Image, 'gray', interpolation='none',origin='lower')
        imgplot = plt.imshow(fieldmap, 'nipy_spectral', interpolation='none',origin='lower',alpha=alpha)
#         imgplot=plt.imshow(image,origin='lower')
    else:
        imgplot = plt.imshow(Image, 'gray', interpolation='none')
        imgplot = plt.imshow(fieldmap, 'nipy_spectral', interpolation='none',alpha=alpha)
    imgplot.set_cmap('jet')
#     imgplot.set_cmap('gist_rainbow')
    plt.title(title)
    if axis is not None and axis is False:
        plt.axis('off')
    cbar=fig0.colorbar(imgplot,fraction=0.046, pad=0.04)
    cbar.set_label(cbarName, rotation=270, labelpad=8)
    if climit is not None:
        cbar.set_clim(climit)
    cbar.draw_all()

def plotVectorStreamLine(Vx,Vy,cbarName='',climit=None):

    strength = np.sqrt(Vx**2+Vy**2)
    if Vx.shape != Vy.shape:
        print ("please make sure you have input with same size")
        return -1
    horizontalSize=Vx.shape[1]
    verticalSize = Vx.shape[0]

#     circle3 = plt.Circle((0, 0), 0.2, color='black', fill=False)
    X,Y = np.meshgrid( np.arange(horizontalSize), np.arange(verticalSize) )

    fig0, ax0 = plt.subplots(num=None, figsize=(5,5), dpi=80, facecolor='w', edgecolor='k')

    strm = ax0.streamplot(X, Y, Vx, Vy, color=strength,density=[1,2],cmap=plt.cm.plasma)
#     ax0.streamplot(-X, Y, -Vx, Vy, color=strength,density=[1,2], cmap=plt.cm.plasma)
    # ax0.add_artist(circle3)
    cbar=fig0.colorbar(strm.lines,fraction=0.046, pad=0.04)
    cbar.set_label(cbarName, rotation=270, labelpad=8)
    if climit is not None:
        cbar.set_clim(climit)
    cbar.draw_all()


##plotSelectedRange(sliceFreqMap[:, 120], offsetFrequency[:,120],RFFREQLST,rfBandWidth, 'Excition Profile around SPIOs boundry')
# this function is in Dropbox/ViewLine/CreateMRIImage.ipy

# def plotSelectedRange(sliceSelection,deltaB, selectList, rfBand, title='Excited Figure'):
#     fig, ax = plt.subplots()
# #     fig = plt.figure()
#     xs = np.arange(IMAGEPIX)
#     xmin,xmax= 50,200
#     zerobias = sliceSelection[xmin]
#
#     plt.plot(xs, sliceSelection-zerobias, ':',color='k')
#     plt.plot(xs, deltaB,'--',color='k')
#     plt.plot(xs, sliceSelection-zerobias+ deltaB,'-',color='k')
#
#     trueField = sliceSelection + deltaB
#
#     excitedSlicePosition =[]
#     for i,freq in enumerate(selectList):
#         line = np.zeros(IMAGEPIX)
#         line[:] = freq
#         if i%2==0:
#             color = 'b'
#         else:
#             color = 'r'
#         plt.plot(line - rfBand/2 - zerobias,'-',color=color,alpha=0.5)
#
#         print(i)
#         # only plot even lines
#         if i%2==0:
#             excite = np.argwhere((trueField<=freq+rfBand/2) &(trueField >= freq - rfBand/2)).flatten()
#             #  excite will obtained data like [116 145 146 147 148  168 169]
#             # using ediff1d and minus 1 to find the edge of index
#             splitIndex = np.array(np.nonzero(np.ediff1d(excite) - 1)).flatten()
#             # print(excite)
#             if (size(splitIndex)>0):
#                 splitIndex = splitIndex + 1
#                 excitedSlicePosition = excitedSlicePosition+ np.split(excite,splitIndex)
#             else:
#                 excitedSlicePosition = excitedSlicePosition+ [excite]
#
#     # print(excitedSlicePosition)
#     for ix  in excitedSlicePosition:
#         if size(ix)> 0:
#             if size(ix) == 1:
#                 # set edge to 1 will disappear the narrow line
#                 edge = 1
#             else:
#                 edge = 0.5
#             ix = np.append(ix,ix[-1]+1)
#             print(ix)
#             iy = np.take(trueField, ix)
#             a = min(ix)
#             b = max(ix)
#             iy = iy - zerobias
#             verts = [(a, 0), *zip(ix, iy), (b, 0)]
#
#             poly = Polygon(verts, facecolor = '0.8', edgecolor= str(edge))
#             ax.add_patch(poly)
#
#
#     plt.xlim(xmin,xmax)
#     plt.ylim(0,30000-zerobias)
#     plt.ylabel('Frequency (Hz)')
#     plt.xlabel('Image Position')
#     plt.title(title)
#     plt.show()
