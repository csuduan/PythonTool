import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#创建series
# s1=pd.Series([1,2,np.nan]);
# s2=pd.Series(data=[1,2,3],index=['a','b','c']);
#
# datas=pd.date_range('20130101',periods=6)
# df1=pd.DataFrame(np.random.randn(6,4),index=datas,columns=list('ABCD'))
# data = {'state':['Ohino','Ohino','Ohino','Nevada','Nevada'],
#         'year':[2003,2001,2002,2001,2002],
#         'pop':[1.5,1.7,3.6,2.4,2.9]}
# index=[4,3,2,1,0]
# df2=pd.DataFrame(data,index=index)
#df1.head()
#df1.tail(2)

#df2.plot()

#ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
#ts = ts.cumsum()
#df3 = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
#df3 = df3.cumsum()
#plt.figure();
#df3.plot();



# df3=df2.sort_values(by='year')

data = [[1,2,3],[4,5,6]]
index = [1,4]
columns=['a','b','c']
df = pd.DataFrame(data=data, index=index, columns=columns)
print(df)

df.plot()

print("end")