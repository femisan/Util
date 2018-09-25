import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import pandas as pd

init_notebook_mode()

def plotOneLine(x,y,mode='lines+markers',legend_name='',title=''):
    d=[go.Scatter(x=x,y=y,mode=mode,name=legend_name)]
    fig=go.Figure(data=d,layout=go.Layout(title=title))
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
