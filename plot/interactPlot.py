import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import pandas as pd
import numpy as np

init_notebook_mode(connected=True)


def convertMeshPoint(x,y,z):
    g=(x,y,z)
    points = np.vstack(map(np.ravel, g))
    return points

def plotSurface(Mat,x=None,y=None):
    if x is None or y is None:
        x,y = np.meshgrid( np.arange(Mat.shape[0]), np.arange(Mat.shape[1]) )

    x,y,z = convertMeshPoint(x,y,Mat)
    trace1 = go.Mesh3d(x=x,
                   y=y,
                   z=z,
                   opacity=0.5,
                   color='#66CCFF'
                  )

    layout = go.Layout(
                        scene = dict(
                        xaxis = dict(
                            nticks=4, range = [-100,100],),
                        yaxis = dict(
                            nticks=4, range = [-50,100],),
                        zaxis = dict(
                            nticks=4, range = [-100,100],),),
                        width=700,
                        margin=dict(
                        r=20, l=10,
                        b=10, t=10)
                      )
    fig = go.Figure(data=[trace1], layout=layout)
    iplot(fig)

def plotOneLine(x,y,mode='lines+markers',legend_name='',title=''):
    d=[go.Scatter(x=x,y=y,mode=mode,name=legend_name)]
    fig=go.Figure(data=d,layout=go.Layout(title=title))
    iplot(fig,show_link=False)

def plotImage(img,title='',scale=1.0):
    row,col = img.shape
    d = [go.Heatmap(z=img,x=np.arange(col),y=np.arange(row))]
    height= 600 * scale
    width = height * (col/row)
    layout = go.Layout(
    title=title,
    autosize=True,
    width=width,
    height=height,
    margin=go.layout.Margin(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
#     paper_bgcolor='#7f7f7f',
#     plot_bgcolor='#c7c7c7'
    )
    fig=go.Figure(data=d,layout=layout)
    iplot(fig,show_link=False)


def plotDataFrameColumn(data_frame,mode_dict={},title=''):
    # the chage_mode_dict is a dict to change style of column eg. {'col1':'lines+markers','col2':'lines'}
    assert(isinstance(data_frame, pd.core.frame.DataFrame) == True),"Input should be Pands DataFrame"
    d=[]
    for key,series in data_frame.iteritems():
        mode = mode_dict.get(key,'lines+markers')
        d.append(go.Scatter(x=series.index,y=series.values,name=key,mode=mode))
    fig=go.Figure(data=d,layout=go.Layout(title=title))
    iplot(fig,show_link=False)
