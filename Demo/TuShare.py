import tushare as ts
import pandas as pd

print(ts.__version__)
code='600848'

pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

df=ts.get_k_data(code,start='2016-01-11',end='2017-06-20', ktype='5')
#df=ts.get_tick_data('000756','2015-03-27')
# df = ts.get_k_data(code, start='2016-01-01',end='2017-06-01',ktype='60')
#df=ts.get_czce_daily('20170615')

#df.to_csv(f'D:\\tmp\\{code}-m60.csv')
print(df)





