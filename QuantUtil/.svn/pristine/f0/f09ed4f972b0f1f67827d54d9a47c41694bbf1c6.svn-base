import tushare as ts
import pandas as pd
import pymssql
import sqlalchemy
import time
import requests
from bs4 import BeautifulSoup

#SHIBOR爬虫

engine =sqlalchemy.create_engine('mssql+pymssql://wind:wind@192.168.1.10:1433/wind')
date=time.strftime('%Y%m%d',time.localtime(time.time()))
date='20180518'
tms=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


def main():
    url = 'http://www.shibor.org/shibor/ShiborTendaysShow.do'  # 网址
    r = requests.get(url)
    print(r.status_code, r.encoding)
    html = r.content

    soup = BeautifulSoup(html, 'lxml')

    table=soup.find_all(id='result')[1]

    datas=[]
    for tr in table.find_all('tr'):
        tds=tr.find_all('td')

        dt=tds[0].contents[0].replace('-','')
        datas.append([dt, 'SHIBORON.IR',tds[1].contents[0]])
        datas.append([dt, 'SHIBOR1W.IR', tds[2].contents[0]])
        datas.append([dt, 'SHIBOR2W.IR', tds[3].contents[0]])
        datas.append([dt, 'SHIBOR1M.IR', tds[4].contents[0]])
        datas.append([dt, 'SHIBOR3M.IR', tds[5].contents[0]])
        datas.append([dt, 'SHIBOR6M.IR', tds[6].contents[0]])
        datas.append([dt, 'SHIBOR9M.IR', tds[7].contents[0]])
        datas.append([dt, 'SHIBOR1Y.IR', tds[8].contents[0]])

    df=pd.DataFrame(datas,columns=['TRADE_DT','S_INFO_WINDCODE','B_INFO_RATE'])
    df['OBJECT_ID'] = 0
    df['OPDATE'] = tms
    df['OPMODE'] = 0

    df = df[df['TRADE_DT'] == date]


    print(df)
    if len(df) > 0:
        df.to_sql('SHIBORPRICES', engine, index=False, if_exists='append')


if __name__ == '__main__':
    engine.connect().execute(f'delete from shiborprices where trade_dt=\'{date}\'')
    main()