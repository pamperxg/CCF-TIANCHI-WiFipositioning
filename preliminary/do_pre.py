import pandas as pd
import numpy as np
import gc
import time
import warnings 
warnings.filterwarnings('ignore')

print('begin:',time.strftime("%H:%M:%S",time.localtime()))

fileFrom='input/ccf_first_round_user_shop_behavior.csv'
fileTo='train_wifi.csv'
dataFrom=''
dataTo=''

df=pd.read_csv(dataFrom+fileFrom)

wifiDict={
    'index':[],
    'bssid':[],
    'strength':[],
    'connect':[]
}

for index,row in df.iterrows():
    for wifi in row.wifi_infos.split(';'):
        info=wifi.split('|')
        wifiDict['index'].append(index)
        wifiDict['bssid'].append(info[0])
        wifiDict['strength'].append(info[1])
        wifiDict['connect'].append(info[2])
print('done')
del df
gc.collect()
df=pd.DataFrame(wifiDict)
df.to_csv(dataTo+fileTo,index=None)
print('end:',time.strftime("%H:%M:%S",time.localtime()))

def get_wifitop10(wifi,n):
    df=wifi.copy()
    s=[]
    for i in range(n):
        columns=['wifi1','wifi2','wifi3','wifi4','wifi5','wifi6','wifi7','wifi8','wifi9','wifi10']
        df1 = df[df['index']==i].sort_values(by='strength',axis=0,ascending=True).reset_index()
        df1.drop('level_0',axis=1,inplace=True)
        if df1.shape[0] >= 10:
            df1 = df1.loc[:9]['bssid']
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0] == 9:
            df1 = df1.loc[:8]['bssid']
            df1 = df1.append(pd.Series(['NaN']))
            df1.index=columns
        elif df1.shape[0] == 8:
            df1 = df1.loc[:7]['bssid']
            df1 = df1.append(pd.Series(['NaN','NaN']))
            df1.index=columns
        elif df1.shape[0] == 7:
            df1 = df1.loc[:6]['bssid']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN']))
            df1.index=columns
        elif df1.shape[0] == 6:
            df1 = df1.loc[:5]['bssid']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN']))
            df1.index=columns
        elif df1.shape[0]==5:
            df1 = df1.loc[:4]['bssid']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN','NaN']))
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0]==4:
            df1 = df1.loc[:3]['bssid']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN','NaN','NaN']))
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0]==3:
            df1 = df1.loc[:2]['bssid']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN','NaN','NaN','NaN']))
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0]==2:
            df1 = df1.loc[:1]['bssid']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN']))
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0]==1:
            a = df1.loc[0]['bssid']
            df1 = pd.Series([a,'NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN'])
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
    df_wifi = pd.concat(s)
    wifi_top10 = df_wifi.reset_index()
    wifi = wifi_top10.drop('index',axis=1)
    return wifi
	
def get_wifi_signal(wifi,n):
    df=wifi.copy()
    s=[]
    for i in range(n):
        if i%10000==0:
            print('i:',i)
        columns=['signal1','signal2','signal3','signal4','signal5','signal6','signal7','signal8','signal9','signal10']
        df1 = df[df['index']==i].sort_values(by='strength',axis=0,ascending=True).reset_index()
        df1.drop('level_0',axis=1,inplace=True)
        if df1.shape[0] >= 10:
            df1 = df1.loc[:9]['strength']
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0] == 9:
            df1 = df1.loc[:8]['strength']
            df1 = df1.append(pd.Series(['NaN']))
            df1.index=columns
        elif df1.shape[0] == 8:
            df1 = df1.loc[:7]['strength']
            df1 = df1.append(pd.Series(['NaN','NaN']))
            df1.index=columns
        elif df1.shape[0] == 7:
            df1 = df1.loc[:6]['strength']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN']))
            df1.index=columns
        elif df1.shape[0] == 6:
            df1 = df1.loc[:5]['strength']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN']))
            df1.index=columns
        elif df1.shape[0]==5:
            df1 = df1.loc[:4]['strength']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN','NaN']))
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0]==4:
            df1 = df1.loc[:3]['strength']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN','NaN','NaN']))
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0]==3:
            df1 = df1.loc[:2]['strength']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN','NaN','NaN','NaN']))
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0]==2:
            df1 = df1.loc[:1]['strength']
            df1 = df1.append(pd.Series(['NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN']))
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
        elif df1.shape[0]==1:
            a = df1.loc[0]['strength']
            df1 = pd.Series([a,'NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN'])
            df1.index=columns
            s.append(pd.DataFrame(df1).T)
    df_wifi = pd.concat(s)
    wifi_top10 = df_wifi.reset_index()
    wifi = wifi_top10.drop('index',axis=1)
    return wifi

print('start:',time.strftime("%H:%M:%S",time.localtime()))
n=train.shape[0]
wifi = get_wifitop10(df,n)
wifi_s = get_wifi_signal(df,n)
print('end:',time.strftime("%H:%M:%S",time.localtime()))
wifi.to_csv('wifi_top10.csv',index=None)













