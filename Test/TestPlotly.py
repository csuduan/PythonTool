import plotly
from plotly.graph_objs import *


data=[
    Scatter(
        x=['20170101', '20170102', '20170103', '20170104', '20170105'],
        y=[1, 3, 2, 3, 1],

    )
]

url=plotly.offline.plot(data,Layout(title="hello world"),filename='plot.html')
print(url)