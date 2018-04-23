import pandas as pd
import numpy as np
import os
from com_util import *
import gc
from collections import defaultdict
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

def get_negtive_sample(train1,train2):
#     print ('train2 shape:'+str(train2.shape))
    test1 = merge_wifi_data(train1,train2,'wifi1','wifi1')
    test2 = merge_wifi_data(train1,train2,'wifi2','wifi2')
    test3 = merge_wifi_data(train1,train2,'wifi3','wifi3')



    t1 = test1[['index','shop_id']]
    t2 = test2[['index','shop_id']]
    t3 = test3[['index','shop_id']]


    t0 = pd.concat([t1,t2,t3],axis=0)
    t0 = t0.loc[~t0['shop_id'].isnull()]
    t0.drop_duplicates(inplace=True)
    t1 = t0.drop_duplicates(subset='index')
#     print ('t1 shape:'+str(t1.shape))
#     print('t0.shape: ',t0.shape)
#     del test1,test2
#     gc.collect()
    return t0

def merge_wifi_data(data,test,column1,column2):
    data = data[['shop_id']+[column1]]
    data.drop_duplicates(inplace=True)

    test = test[['index']+[column2]]
    data =data.rename(columns = {column1:'wifi'})
    test = test.rename(columns = {column2:'wifi'})


    test = test.merge(data,on='wifi',how='left')
    return test

def get_label(result,test):
    if 'shop_id' in test.columns:
        t1 = test.copy()
        t1.rename(columns={'shop_id':'label'},inplace=True)
        result = result.merge(t1,on='index',how='left')
        result['label'] = (result['shop_id']==result['label']).astype(int)
    else:
        result = result.merge(test,on=['index'],how='left')
#     print(result.columns)
    return result

def get_shop_feature(result,train1,dataset1):
    #一个商店有多少wifi
    t0 = dataset1.groupby('shop_id')['wifi'].agg('nunique').reset_index().rename(columns={'wifi':'wifi_nums_of_shop'})
    result = result.merge(t0,on='shop_id',how='left')
    #商店出现次数
    t0 = dataset1.sort_values(by='connect',ascending=False).drop_duplicates(subset='index')
    t0 = dataset1.groupby('shop_id')['connect'].agg('count').reset_index().rename(columns={'connect':'shop_num'})
    result = result.merge(t0,on='shop_id',how='left')
    #商店连接wifi次数
    t0 = dataset1.groupby('shop_id')['connect'].agg('sum').reset_index().rename(columns={'connect':'shop_connect_num'})
    result = result.merge(t0,on='shop_id',how='left')
    #商店连接wifi比例
    result['shop_connect_rt'] = result['shop_connect_num']/result['shop_num']
    #商店1-10平均信号强度
    t0 = train1.groupby('shop_id')['signal1'].agg(np.nanmean).reset_index().rename(columns={'signal1':'shop_mean_signal1'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal2'].agg(np.nanmean).reset_index().rename(columns={'signal2':'shop_mean_signal2'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal3'].agg(np.nanmean).reset_index().rename(columns={'signal3':'shop_mean_signal3'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal4'].agg(np.nanmean).reset_index().rename(columns={'signal4':'shop_mean_signal4'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal5'].agg(np.nanmean).reset_index().rename(columns={'signal5':'shop_mean_signal5'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal6'].agg(np.nanmean).reset_index().rename(columns={'signal6':'shop_mean_signal6'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal7'].agg(np.nanmean).reset_index().rename(columns={'signal7':'shop_mean_signal7'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal8'].agg(np.nanmean).reset_index().rename(columns={'signal8':'shop_mean_signal8'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal9'].agg(np.nanmean).reset_index().rename(columns={'signal9':'shop_mean_signal9'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train1.groupby('shop_id')['signal10'].agg(np.nanmean).reset_index().rename(columns={'signal10':'shop_mean_signal10'})
    result = result.merge(t0,on='shop_id',how='left')
    
    return result
    

def get_wifi_feature(result,train1,dataset1,dataset):
    #wifi包含店铺数
    t0 = dataset1.groupby('wifi')['shop_id'].agg('nunique').reset_index().rename(columns={'shop_id':'shop_num_of_wifi'})
    t0['wifi1'] = t0['wifi']
    t0['wifi2'] = t0['wifi']
    t0['wifi3'] = t0['wifi']
    t0['wifi4'] = t0['wifi']
    t0['wifi5'] = t0['wifi']
    t0['wifi6'] = t0['wifi']
    t0['wifi7'] = t0['wifi']
    t0['wifi8'] = t0['wifi']
    t0['wifi9'] = t0['wifi']
    t0['wifi10'] = t0['wifi']

    result = result.merge(t0[['wifi1','shop_num_of_wifi']],on='wifi1',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi1'},inplace=True)
    
    
    result = result.merge(t0[['wifi2','shop_num_of_wifi']],on='wifi2',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi2'},inplace=True)
    
    result = result.merge(t0[['wifi3','shop_num_of_wifi']],on='wifi3',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi3'},inplace=True)
    
    result = result.merge(t0[['wifi4','shop_num_of_wifi']],on='wifi4',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi4'},inplace=True)
    
    result = result.merge(t0[['wifi5','shop_num_of_wifi']],on='wifi5',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi5'},inplace=True)
    
    result = result.merge(t0[['wifi6','shop_num_of_wifi']],on='wifi6',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi6'},inplace=True)
    
    result = result.merge(t0[['wifi7','shop_num_of_wifi']],on='wifi7',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi7'},inplace=True)
    
    result = result.merge(t0[['wifi8','shop_num_of_wifi']],on='wifi8',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi8'},inplace=True)
    
    result = result.merge(t0[['wifi9','shop_num_of_wifi']],on='wifi9',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi9'},inplace=True)
    
    result = result.merge(t0[['wifi10','shop_num_of_wifi']],on='wifi10',how='left')
    result.rename(columns={'shop_num_of_wifi':'shop_num_of_wifi10'},inplace=True)
    
    #wifi出现次数
    t0 = dataset1.drop_duplicates(subset='index')
    t0 = dataset1.groupby('wifi')['connect'].agg('count').reset_index().rename(columns={'connect':'wifi_num'})
    
    t0['wifi1'] = t0['wifi']
    t0['wifi2'] = t0['wifi']
    t0['wifi3'] = t0['wifi']
    t0['wifi4'] = t0['wifi']
    t0['wifi5'] = t0['wifi']
    t0['wifi6'] = t0['wifi']
    t0['wifi7'] = t0['wifi']
    t0['wifi8'] = t0['wifi']
    t0['wifi9'] = t0['wifi']
    t0['wifi10'] = t0['wifi']
    
    result = result.merge(t0[['wifi1','wifi_num']],on='wifi1',how='left')
    result.rename(columns={'wifi_num':'wifi_num1'},inplace=True)
    
    result = result.merge(t0[['wifi2','wifi_num']],on='wifi2',how='left')
    result.rename(columns={'wifi_num':'wifi_num2'},inplace=True)
    
    result = result.merge(t0[['wifi3','wifi_num']],on='wifi3',how='left')
    result.rename(columns={'wifi_num':'wifi_num3'},inplace=True)
    
    result = result.merge(t0[['wifi4','wifi_num']],on='wifi4',how='left')
    result.rename(columns={'wifi_num':'wifi_num4'},inplace=True)
    
    result = result.merge(t0[['wifi5','wifi_num']],on='wifi5',how='left')
    result.rename(columns={'wifi_num':'wifi_num5'},inplace=True)
    
    result = result.merge(t0[['wifi6','wifi_num']],on='wifi6',how='left')
    result.rename(columns={'wifi_num':'wifi_num6'},inplace=True)
    
    result = result.merge(t0[['wifi7','wifi_num']],on='wifi7',how='left')
    result.rename(columns={'wifi_num':'wifi_num7'},inplace=True)
    
    result = result.merge(t0[['wifi8','wifi_num']],on='wifi8',how='left')
    result.rename(columns={'wifi_num':'wifi_num8'},inplace=True)
    
    result = result.merge(t0[['wifi9','wifi_num']],on='wifi9',how='left')
    result.rename(columns={'wifi_num':'wifi_num9'},inplace=True)
    
    result = result.merge(t0[['wifi10','wifi_num']],on='wifi10',how='left')
    result.rename(columns={'wifi_num':'wifi_num10'},inplace=True)
    #wifi被连接次数
    t0 = dataset1.groupby('wifi')['connect'].agg('sum').reset_index().rename(columns={'connect':'wifi_connect_num'})
    
    t0['wifi1'] = t0['wifi']
    t0['wifi2'] = t0['wifi']
    t0['wifi3'] = t0['wifi']
    t0['wifi4'] = t0['wifi']
    t0['wifi5'] = t0['wifi']
    t0['wifi6'] = t0['wifi']
    t0['wifi7'] = t0['wifi']
    t0['wifi8'] = t0['wifi']
    t0['wifi9'] = t0['wifi']
    t0['wifi10'] = t0['wifi']
    
    result = result.merge(t0[['wifi1','wifi_connect_num']],on='wifi1',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num1'},inplace=True)
    
    result = result.merge(t0[['wifi2','wifi_connect_num']],on='wifi2',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num2'},inplace=True)
    
    result = result.merge(t0[['wifi3','wifi_connect_num']],on='wifi3',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num3'},inplace=True)
    
    result = result.merge(t0[['wifi4','wifi_connect_num']],on='wifi4',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num4'},inplace=True)
    
    result = result.merge(t0[['wifi5','wifi_connect_num']],on='wifi5',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num5'},inplace=True)
    
    result = result.merge(t0[['wifi6','wifi_connect_num']],on='wifi6',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num6'},inplace=True)
    
    result = result.merge(t0[['wifi7','wifi_connect_num']],on='wifi7',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num7'},inplace=True)
    
    result = result.merge(t0[['wifi8','wifi_connect_num']],on='wifi8',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num8'},inplace=True)
    
    result = result.merge(t0[['wifi9','wifi_connect_num']],on='wifi9',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num9'},inplace=True)
    
    result = result.merge(t0[['wifi10','wifi_connect_num']],on='wifi10',how='left')
    result.rename(columns={'wifi_connect_num':'wifi_connect_num10'},inplace=True)
    
    
    #wifi连接比例
    result['wifi_connect_rt1'] = result['wifi_connect_num1']/result['wifi_num1']
    result['wifi_connect_rt2'] = result['wifi_connect_num2']/result['wifi_num2']
    result['wifi_connect_rt3'] = result['wifi_connect_num3']/result['wifi_num3']
    result['wifi_connect_rt4'] = result['wifi_connect_num4']/result['wifi_num4']
    result['wifi_connect_rt5'] = result['wifi_connect_num5']/result['wifi_num5']
    result['wifi_connect_rt6'] = result['wifi_connect_num6']/result['wifi_num6']
    result['wifi_connect_rt7'] = result['wifi_connect_num7']/result['wifi_num7']
    result['wifi_connect_rt8'] = result['wifi_connect_num8']/result['wifi_num8']
    result['wifi_connect_rt9'] = result['wifi_connect_num9']/result['wifi_num9']
    result['wifi_connect_rt10'] = result['wifi_connect_num10']/result['wifi_num10']
    
    
    #wifi是否第一次出现
    t0 = dataset.copy()
    t1 = t0.groupby('wifi')['day'].agg('min').reset_index().rename(columns={'day':'wifi_first_apperance'})
    t0 = t0.merge(t1,on=['wifi'],how='left')
    t0['wifi_first_apperance'] = (t0['wifi_first_apperance']==t0['day']).astype(int)
    t0 = t0[['wifi','day','wifi_first_apperance']].drop_duplicates()
    t0['wifi1'] = t0['wifi']
    t0['wifi2'] = t0['wifi']
    t0['wifi3'] = t0['wifi']
    t0['wifi4'] = t0['wifi']
    t0['wifi5'] = t0['wifi']
    t0['wifi6'] = t0['wifi']
    t0['wifi7'] = t0['wifi']
    t0['wifi8'] = t0['wifi']
    t0['wifi9'] = t0['wifi']
    t0['wifi10'] = t0['wifi']
    
    result = result.merge(t0[['wifi1','day','wifi_first_apperance']],on=['wifi1','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance1'},inplace=True)

    result = result.merge(t0[['wifi2','day','wifi_first_apperance']],on=['wifi2','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance2'},inplace=True)

    result = result.merge(t0[['wifi3','day','wifi_first_apperance']],on=['wifi3','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance3'},inplace=True)

    result = result.merge(t0[['wifi4','day','wifi_first_apperance']],on=['wifi4','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance4'},inplace=True)

    result = result.merge(t0[['wifi5','day','wifi_first_apperance']],on=['wifi5','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance5'},inplace=True)

    result = result.merge(t0[['wifi6','day','wifi_first_apperance']],on=['wifi6','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance6'},inplace=True)

    result = result.merge(t0[['wifi7','day','wifi_first_apperance']],on=['wifi7','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance7'},inplace=True)

    result = result.merge(t0[['wifi8','day','wifi_first_apperance']],on=['wifi8','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance8'},inplace=True)

    result = result.merge(t0[['wifi9','day','wifi_first_apperance']],on=['wifi9','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance9'},inplace=True)

    result = result.merge(t0[['wifi10','day','wifi_first_apperance']],on=['wifi10','day'],how='left')
    result.rename(columns={'wifi_first_apperance':'wifi_first_apperance10'},inplace=True)
    
    
    #wifi是不是移动热点
    t0 = dataset.copy()
    t0['hotspot']=0
    t0 = merge_min(t0,['wifi'],'longitude','min_longitude')
    t0 = merge_min(t0,['wifi'],'latitude','min_latitude')
    t0 = merge_max(t0,['wifi'],'latitude','max_latitude')
    t0 = merge_max(t0,['wifi'],'longitude','max_longitude')
    judge = (t0['max_latitude']-t0['max_latitude']>0.015)|(t0['max_longitude']-t0['min_longitude']>0.015)
    t0.loc[judge,'hotspot']=1
    t0 = t0[['wifi','hotspot']].drop_duplicates()
#     print(t0['hotspot'].value_counts())
    
    t0['wifi1'] = t0['wifi']
    t0['wifi2'] = t0['wifi']
    t0['wifi3'] = t0['wifi']
    t0['wifi4'] = t0['wifi']
    t0['wifi5'] = t0['wifi']
    t0['wifi6'] = t0['wifi']
    t0['wifi7'] = t0['wifi']
    t0['wifi8'] = t0['wifi']
    t0['wifi9'] = t0['wifi']
    t0['wifi10'] = t0['wifi']
    
    result = result.merge(t0[['wifi1','hotspot']],on='wifi1',how='left')
    result.rename(columns={'hotspot':'hotspot1'},inplace=True)
    
    result = result.merge(t0[['wifi2','hotspot']],on='wifi2',how='left')
    result.rename(columns={'hotspot':'hotspot2'},inplace=True)
    
    result = result.merge(t0[['wifi3','hotspot']],on='wifi3',how='left')
    result.rename(columns={'hotspot':'hotspot3'},inplace=True)
    
    result = result.merge(t0[['wifi4','hotspot']],on='wifi4',how='left')
    result.rename(columns={'hotspot':'hotspot4'},inplace=True)
    
    result = result.merge(t0[['wifi5','hotspot']],on='wifi5',how='left')
    result.rename(columns={'hotspot':'hotspot5'},inplace=True)
    
    result = result.merge(t0[['wifi6','hotspot']],on='wifi6',how='left')
    result.rename(columns={'hotspot':'hotspot6'},inplace=True)
    
    result = result.merge(t0[['wifi7','hotspot']],on='wifi7',how='left')
    result.rename(columns={'hotspot':'hotspot7'},inplace=True)
    
    result = result.merge(t0[['wifi8','hotspot']],on='wifi8',how='left')
    result.rename(columns={'hotspot':'hotspot8'},inplace=True)
    
    result = result.merge(t0[['wifi9','hotspot']],on='wifi9',how='left')
    result.rename(columns={'hotspot':'hotspot9'},inplace=True)
    
    result = result.merge(t0[['wifi10','hotspot']],on='wifi10',how='left')
    result.rename(columns={'hotspot':'hotspot10'},inplace=True)
    
    
    #wifi 1-10 的平均强度
    t0 = train1.groupby('wifi1')['signal1'].agg(np.nanmean).reset_index().rename(columns={'signal1':'wifi_mean_signal1'}).drop_duplicates()
    result = result.merge(t0,on='wifi1',how='left')
    
    t0 = train1.groupby('wifi2')['signal2'].agg(np.nanmean).reset_index().rename(columns={'signal2':'wifi_mean_signal2'}).drop_duplicates()
    result = result.merge(t0,on='wifi2',how='left')
    
    t0 = train1.groupby('wifi3')['signal3'].agg(np.nanmean).reset_index().rename(columns={'signal3':'wifi_mean_signal3'}).drop_duplicates()
    result = result.merge(t0,on='wifi3',how='left')
    
    t0 = train1.groupby('wifi4')['signal4'].agg(np.nanmean).reset_index().rename(columns={'signal4':'wifi_mean_signal4'}).drop_duplicates()
    result = result.merge(t0,on='wifi4',how='left')
    
    t0 = train1.groupby('wifi5')['signal5'].agg(np.nanmean).reset_index().rename(columns={'signal5':'wifi_mean_signal5'}).drop_duplicates()
    result = result.merge(t0,on='wifi5',how='left')
    
    t0 = train1.groupby('wifi6')['signal6'].agg(np.nanmean).reset_index().rename(columns={'signal6':'wifi_mean_signal6'}).drop_duplicates()
    result = result.merge(t0,on='wifi6',how='left')
    
    t0 = train1.groupby('wifi7')['signal7'].agg(np.nanmean).reset_index().rename(columns={'signal7':'wifi_mean_signal7'}).drop_duplicates()
    result = result.merge(t0,on='wifi7',how='left')
    
    t0 = train1.groupby('wifi8')['signal8'].agg(np.nanmean).reset_index().rename(columns={'signal8':'wifi_mean_signal8'}).drop_duplicates()
    result = result.merge(t0,on='wifi8',how='left')
    
    t0 = train1.groupby('wifi9')['signal9'].agg(np.nanmean).reset_index().rename(columns={'signal9':'wifi_mean_signal9'}).drop_duplicates()
    result = result.merge(t0,on='wifi9',how='left')
    
    t0 = train1.groupby('wifi10')['signal10'].agg(np.nanmean).reset_index().rename(columns={'signal10':'wifi_mean_signal10'}).drop_duplicates()
    result = result.merge(t0,on='wifi10',how='left')
    
    return result
    
    

def get_shop_wifi_feature(result,train,dataset1,dataset):
    #shop_wifi出现次数，权值，比例
    t1 = train.groupby(['shop_id','wifi1'])['index'].agg('count').reset_index().rename(columns={'wifi1':'wifi','index':'c1'})
    t2 = train.groupby(['shop_id','wifi2'])['index'].agg('count').reset_index().rename(columns={'wifi2':'wifi','index':'c2'})
    t3 = train.groupby(['shop_id','wifi3'])['index'].agg('count').reset_index().rename(columns={'wifi3':'wifi','index':'c3'})
    t4 = train.groupby(['shop_id','wifi4'])['index'].agg('count').reset_index().rename(columns={'wifi4':'wifi','index':'c4'})
    t5 = train.groupby(['shop_id','wifi5'])['index'].agg('count').reset_index().rename(columns={'wifi5':'wifi','index':'c5'})
    t6 = train.groupby(['shop_id','wifi6'])['index'].agg('count').reset_index().rename(columns={'wifi6':'wifi','index':'c6'})
    t7 = train.groupby(['shop_id','wifi7'])['index'].agg('count').reset_index().rename(columns={'wifi7':'wifi','index':'c7'})
    t8 = train.groupby(['shop_id','wifi8'])['index'].agg('count').reset_index().rename(columns={'wifi8':'wifi','index':'c8'})
    t9 = train.groupby(['shop_id','wifi9'])['index'].agg('count').reset_index().rename(columns={'wifi9':'wifi','index':'c9'})
    t10 = train.groupby(['shop_id','wifi10'])['index'].agg('count').reset_index().rename(columns={'wifi10':'wifi','index':'c10'})
    
    t1 = t1.merge(t2,on=['shop_id','wifi'],how='outer')
    t1 = t1.merge(t3,on=['shop_id','wifi'],how='outer')
    t1 = t1.merge(t4,on=['shop_id','wifi'],how='outer')
    t1 = t1.merge(t5,on=['shop_id','wifi'],how='outer')
    t1 = t1.merge(t6,on=['shop_id','wifi'],how='outer')
    t1 = t1.merge(t7,on=['shop_id','wifi'],how='outer')
    t1 = t1.merge(t8,on=['shop_id','wifi'],how='outer')
    t1 = t1.merge(t9,on=['shop_id','wifi'],how='outer')
    t1 = t1.merge(t10,on=['shop_id','wifi'],how='outer')
    
#     print('t1 shape: ',t1.shape)
    
    t1 = t1.fillna(0)
    
    t1['score'] = 20*t1['c1']+16*t1['c2']+10*t1['c3']+8*t1['c4']+5*t1['c5']+3*t1['c6'] +2*t1['c7']+t1['c8']+t1['c9']+t1['c10']
    t1['wifi1'] = t1['wifi']
    t1['wifi2'] = t1['wifi']
    t1['wifi3'] = t1['wifi']
    t1['wifi4'] = t1['wifi']
    t1['wifi5'] = t1['wifi']
    t1['wifi6'] = t1['wifi']
    t1['wifi7'] = t1['wifi']
    t1['wifi8'] = t1['wifi']
    t1['wifi9'] = t1['wifi']
    t1['wifi10'] = t1['wifi']
#     print (sum(t1['score'])/3)
    
    result = result.merge(t1[['shop_id','wifi1','score']],on=['shop_id','wifi1'],how='left')
    result.rename(columns={'score':'score1'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi2','score']],on=['shop_id','wifi2'],how='left')
    result.rename(columns={'score':'score2'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi3','score']],on=['shop_id','wifi3'],how='left')
    result.rename(columns={'score':'score3'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi4','score']],on=['shop_id','wifi4'],how='left')
    result.rename(columns={'score':'score4'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi5','score']],on=['shop_id','wifi5'],how='left')
    result.rename(columns={'score':'score5'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi6','score']],on=['shop_id','wifi6'],how='left')
    result.rename(columns={'score':'score6'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi7','score']],on=['shop_id','wifi7'],how='left')
    result.rename(columns={'score':'score7'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi8','score']],on=['shop_id','wifi8'],how='left')
    result.rename(columns={'score':'score8'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi9','score']],on=['shop_id','wifi9'],how='left')
    result.rename(columns={'score':'score9'},inplace=True)
    
    result = result.merge(t1[['shop_id','wifi10','score']],on=['shop_id','wifi10'],how='left')
    result.rename(columns={'score':'score10'},inplace=True)
    
    result =result.fillna(0)
    
#     result = result.loc[~((result['score1']==0)&(result['score2']==0)&(result['score3']==0)&(result['score4']==0)&(result['score5']==0)&(result['score6']==0)),:]
    
    result = merge_sum(result,['index'],'score1','all_score1')
    result = merge_sum(result,['index'],'score2','all_score2')
    result = merge_sum(result,['index'],'score3','all_score3')
    result = merge_sum(result,['index'],'score4','all_score4')
    result = merge_sum(result,['index'],'score5','all_score5')
    result = merge_sum(result,['index'],'score6','all_score6')
    result = merge_sum(result,['index'],'score7','all_score7')
    result = merge_sum(result,['index'],'score8','all_score8')
    result = merge_sum(result,['index'],'score9','all_score9')
    result = merge_sum(result,['index'],'score10','all_score10')
    
    
    result['score1_rt'] = result['score1']/result['all_score1']
    result['score2_rt'] = result['score2']/result['all_score2']
    result['score3_rt'] = result['score3']/result['all_score3']
    result['score4_rt'] = result['score4']/result['all_score4']
    result['score5_rt'] = result['score5']/result['all_score5']
    result['score6_rt'] = result['score6']/result['all_score6']
    result['score7_rt'] = result['score7']/result['all_score7']
    result['score8_rt'] = result['score8']/result['all_score8']
    result['score9_rt'] = result['score9']/result['all_score9']
    result['score10_rt'] = result['score10']/result['all_score10']
    
    #shop_wifi出现次数
    t0 = dataset1.groupby(['shop_id','wifi'])['connect'].agg('count').reset_index().rename(columns={'connect':'shop_wifi_num'})
    
    t0['wifi1'] = t0['wifi']
    t0['wifi2'] = t0['wifi']
    t0['wifi3'] = t0['wifi']
    t0['wifi4'] = t0['wifi']
    t0['wifi5'] = t0['wifi']
    t0['wifi6'] = t0['wifi']
    t0['wifi7'] = t0['wifi']
    t0['wifi8'] = t0['wifi']
    t0['wifi9'] = t0['wifi']
    t0['wifi10'] = t0['wifi']
    
    result = result.merge(t0[['shop_id','wifi1','shop_wifi_num']],on=['shop_id','wifi1'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num1'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi2','shop_wifi_num']],on=['shop_id','wifi2'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num2'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi3','shop_wifi_num']],on=['shop_id','wifi3'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num3'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi4','shop_wifi_num']],on=['shop_id','wifi4'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num4'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi5','shop_wifi_num']],on=['shop_id','wifi5'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num5'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi6','shop_wifi_num']],on=['shop_id','wifi6'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num6'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi7','shop_wifi_num']],on=['shop_id','wifi7'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num7'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi8','shop_wifi_num']],on=['shop_id','wifi8'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num8'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi9','shop_wifi_num']],on=['shop_id','wifi9'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num9'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi10','shop_wifi_num']],on=['shop_id','wifi10'],how='left')
    result.rename(columns={'shop_wifi_num':'shop_wifi_num10'},inplace=True)
    
    #shop_wifi连接次数
    t0 = dataset1.groupby(['shop_id','wifi'])['connect'].agg('sum').reset_index().rename(columns={'connect':'shop_wifi_conn_num'})
    
    t0['wifi1'] = t0['wifi']
    t0['wifi2'] = t0['wifi']
    t0['wifi3'] = t0['wifi']
    t0['wifi4'] = t0['wifi']
    t0['wifi5'] = t0['wifi']
    t0['wifi6'] = t0['wifi']
    t0['wifi7'] = t0['wifi']
    t0['wifi8'] = t0['wifi']
    t0['wifi9'] = t0['wifi']
    t0['wifi10'] = t0['wifi']
    
    result = result.merge(t0[['shop_id','wifi1','shop_wifi_conn_num']],on=['shop_id','wifi1'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num1'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi2','shop_wifi_conn_num']],on=['shop_id','wifi2'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num2'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi3','shop_wifi_conn_num']],on=['shop_id','wifi3'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num3'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi4','shop_wifi_conn_num']],on=['shop_id','wifi4'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num4'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi5','shop_wifi_conn_num']],on=['shop_id','wifi5'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num5'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi6','shop_wifi_conn_num']],on=['shop_id','wifi6'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num6'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi7','shop_wifi_conn_num']],on=['shop_id','wifi7'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num7'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi8','shop_wifi_conn_num']],on=['shop_id','wifi8'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num8'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi9','shop_wifi_conn_num']],on=['shop_id','wifi9'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num9'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi10','shop_wifi_conn_num']],on=['shop_id','wifi10'],how='left')
    result.rename(columns={'shop_wifi_conn_num':'shop_wifi_conn_num10'},inplace=True)
    
    #shop_wifi连接比例
    result['shop_wifi_conn1_rt'] = result['shop_wifi_conn_num1']/result['shop_wifi_num1']
    result['shop_wifi_conn2_rt'] = result['shop_wifi_conn_num2']/result['shop_wifi_num2']
    result['shop_wifi_conn3_rt'] = result['shop_wifi_conn_num3']/result['shop_wifi_num3']
    result['shop_wifi_conn4_rt'] = result['shop_wifi_conn_num4']/result['shop_wifi_num4']
    result['shop_wifi_conn5_rt'] = result['shop_wifi_conn_num5']/result['shop_wifi_num5']
    result['shop_wifi_conn6_rt'] = result['shop_wifi_conn_num6']/result['shop_wifi_num6']
    result['shop_wifi_conn7_rt'] = result['shop_wifi_conn_num7']/result['shop_wifi_num7']
    result['shop_wifi_conn8_rt'] = result['shop_wifi_conn_num8']/result['shop_wifi_num8']
    result['shop_wifi_conn9_rt'] = result['shop_wifi_conn_num9']/result['shop_wifi_num9']
    result['shop_wifi_conn10_rt'] = result['shop_wifi_conn_num10']/result['shop_wifi_num10']
    
    #shop_wifi平均信号强度
    t0 = dataset1.groupby(['shop_id','wifi'])['signal'].agg('mean').reset_index().rename(columns={'signal':'shop_wifi_mean_signal'})
    
    t0['wifi1'] = t0['wifi']
    t0['wifi2'] = t0['wifi']
    t0['wifi3'] = t0['wifi']
    t0['wifi4'] = t0['wifi']
    t0['wifi5'] = t0['wifi']
    t0['wifi6'] = t0['wifi']
    t0['wifi7'] = t0['wifi']
    t0['wifi8'] = t0['wifi']
    t0['wifi9'] = t0['wifi']
    t0['wifi10'] = t0['wifi']
    
    result = result.merge(t0[['shop_id','wifi1','shop_wifi_mean_signal']],on=['shop_id','wifi1'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal1'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi2','shop_wifi_mean_signal']],on=['shop_id','wifi2'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal2'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi3','shop_wifi_mean_signal']],on=['shop_id','wifi3'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal3'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi4','shop_wifi_mean_signal']],on=['shop_id','wifi4'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal4'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi5','shop_wifi_mean_signal']],on=['shop_id','wifi5'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal5'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi6','shop_wifi_mean_signal']],on=['shop_id','wifi6'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal6'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi7','shop_wifi_mean_signal']],on=['shop_id','wifi7'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal7'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi8','shop_wifi_mean_signal']],on=['shop_id','wifi8'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal8'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi9','shop_wifi_mean_signal']],on=['shop_id','wifi9'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal9'},inplace=True)
    
    result = result.merge(t0[['shop_id','wifi10','shop_wifi_mean_signal']],on=['shop_id','wifi10'],how='left')
    result.rename(columns={'shop_wifi_mean_signal':'shop_wifi_mean_signal10'},inplace=True)
    
    #shop_wifi连接次数/wifi连接次数
    result['shop_wifi_conn_rt1'] = result['shop_wifi_conn_num1']/result['wifi_connect_num1']
    result['shop_wifi_conn_rt2'] = result['shop_wifi_conn_num2']/result['wifi_connect_num2']
    result['shop_wifi_conn_rt3'] = result['shop_wifi_conn_num3']/result['wifi_connect_num3']
    result['shop_wifi_conn_rt4'] = result['shop_wifi_conn_num4']/result['wifi_connect_num4']
    result['shop_wifi_conn_rt5'] = result['shop_wifi_conn_num5']/result['wifi_connect_num5']
    result['shop_wifi_conn_rt6'] = result['shop_wifi_conn_num6']/result['wifi_connect_num6']
    result['shop_wifi_conn_rt7'] = result['shop_wifi_conn_num7']/result['wifi_connect_num7']
    result['shop_wifi_conn_rt8'] = result['shop_wifi_conn_num8']/result['wifi_connect_num8']
    result['shop_wifi_conn_rt9'] = result['shop_wifi_conn_num9']/result['wifi_connect_num9']
    result['shop_wifi_conn_rt10'] = result['shop_wifi_conn_num10']/result['wifi_connect_num10']
    return result

def ka_add_groupby_features_1_vs_n(df, group_columns_list, agg_dict, only_new_feature=True):

    df_new = df.copy()
    grouped = df_new.groupby(group_columns_list)

    the_stats = grouped.agg(agg_dict)
    the_stats.columns = the_stats.columns.droplevel(0)
    the_stats.reset_index(inplace=True)
    if only_new_feature:
        df_new = the_stats
    else:
        df_new = pd.merge(left=df_new, right=the_stats, on=group_columns_list, how='left')

    return df_new

def get_jwd_feature(result,train,dataset1,dataset):
    result['longitude'] = result['longitude']*1000000%100000
    result['latitude'] = result['latitude']*1000000%100000
    train['longitude'] = train['longitude']*1000000%100000
    train['latitude'] = train['latitude']*1000000%100000
#     result['shop_longitude'] = result['shop_longitude']*1000000%100000
#     result['shop_latitude'] = result['shop_latitude']*1000000%100000
    train['shop_longitude'] = train['shop_longitude']*1000000%100000
    train['shop_latitude'] = train['shop_latitude']*1000000%100000
    
#     result = result.drop(['shop_longitude','shop_latitude'],axis=1)
    t0 = train[['shop_id','shop_longitude','shop_latitude']].drop_duplicates()
    result = result.merge(t0,on = 'shop_id',how='left')
    
    
    train['distance'] = np.sqrt(((train['longitude'] - train['shop_longitude'])/100)**2 + ((train['latitude'] - train['shop_latitude'])/100)**2)
    result['distance'] = np.sqrt(((result['longitude'] - result['shop_longitude'])/100)**2 + ((result['latitude'] - result['shop_latitude'])/100)**2)
    
    #样本到商店的平均，Std距离
    t0 = train.groupby('shop_id')['distance'].agg(np.nanmean).reset_index().rename(columns={'distance':'mean_distance'})
    result = result.merge(t0,on='shop_id',how='left')
    
    t0 = train.groupby('shop_id')['distance'].agg(np.nanstd).reset_index().rename(columns={'distance':'std_distance'})
    result = result.merge(t0,on='shop_id',how='left')
    
    #商店最大，最小，平均，中值经纬度,面积
    train = merge_min(train,['shop_id'],'longitude','shop_min_longitude')
    train = merge_max(train,['shop_id'],'longitude','shop_max_longitude')
    train = merge_mean(train,['shop_id'],'longitude','shop_mean_longitude')
    train = merge_median(train,['shop_id'],'longitude','shop_median_longitude')
    train = merge_min(train,['shop_id'],'latitude','shop_min_latitude')
    train = merge_max(train,['shop_id'],'latitude','shop_max_latitude')
    train = merge_mean(train,['shop_id'],'latitude','shop_mean_latitude')
    train = merge_median(train,['shop_id'],'latitude','shop_median_latitude')
    
    train['area'] = ((train['shop_max_longitude']-train['shop_min_longitude'])/100) * ((train['shop_max_latitude']-train['shop_min_latitude'])/100)
    t0 = train[['shop_id','shop_min_longitude','shop_max_longitude','shop_min_latitude','shop_max_latitude','shop_mean_latitude','shop_median_latitude','shop_mean_longitude','shop_median_longitude','area']].drop_duplicates()
    result = result.merge(t0,on='shop_id',how='left')
    
#     #wifi最大，最小，平均，中值经纬度,面积
#     dataset1['longitude'] = dataset1['longitude']*1000000%100000
#     dataset1['latitude'] = dataset1['latitude']*1000000%100000

#     agg_dict = {'latitude':{'wifi_max_latitude':'max'}, 
#             'longitude':{'wifi_max_longitude':'max'}}
#     t0 = ka_add_groupby_features_1_vs_n(dataset1, ['wifi'], agg_dict)
#     print('t0:',t0.columns)
#     t0 = t0.drop_duplicates()
    
#     t0['wifi1'] = t0['wifi']
#     t0['wifi2'] = t0['wifi']
#     t0['wifi3'] = t0['wifi']
#     t0['wifi4'] = t0['wifi']
#     t0['wifi5'] = t0['wifi']
#     t0['wifi6'] = t0['wifi']
#     t0['wifi7'] = t0['wifi']
#     t0['wifi8'] = t0['wifi']
#     t0['wifi9'] = t0['wifi']
#     t0['wifi10'] = t0['wifi']
    
#     result = result.merge(t0[['wifi1','wifi_max_longitude','wifi_max_latitude']],on=['wifi1'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude1','wifi_max_latitude':'wifi_max_latitude1'},inplace=True)
    
#     result = result.merge(t0[['wifi2','wifi_max_longitude','wifi_max_latitude']],on=['wifi2'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude2','wifi_max_latitude':'wifi_max_latitude2'},inplace=True)
    
#     result = result.merge(t0[['wifi3','wifi_max_longitude','wifi_max_latitude']],on=['wifi3'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude3','wifi_max_latitude':'wifi_max_latitude3'},inplace=True)
    
#     result = result.merge(t0[['wifi4','wifi_max_longitude','wifi_max_latitude']],on=['wifi4'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude4','wifi_max_latitude':'wifi_max_latitude4'},inplace=True)
    
#     result = result.merge(t0[['wifi5','wifi_max_longitude','wifi_max_latitude']],on=['wifi5'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude5','wifi_max_latitude':'wifi_max_latitude5'},inplace=True)
    
#     result = result.merge(t0[['wifi6','wifi_max_longitude','wifi_max_latitude']],on=['wifi6'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude6','wifi_max_latitude':'wifi_max_latitude6'},inplace=True)
    
#     result = result.merge(t0[['wifi7','wifi_max_longitude','wifi_max_latitude']],on=['wifi7'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude7','wifi_max_latitude':'wifi_max_latitude7'},inplace=True)
    
#     result = result.merge(t0[['wifi8','wifi_max_longitude','wifi_max_latitude']],on=['wifi8'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude8','wifi_max_latitude':'wifi_max_latitude8'},inplace=True)
    
#     result = result.merge(t0[['wifi9','wifi_max_longitude','wifi_max_latitude']],on=['wifi9'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude9','wifi_max_latitude':'wifi_max_latitude9'},inplace=True)
    
#     result = result.merge(t0[['wifi10','wifi_max_longitude','wifi_max_latitude']],on=['wifi10'],how='left')
#     result.rename(columns={'wifi_max_longitude':'wifi_max_longitude10','wifi_max_latitude':'wifi_max_latitude10'},inplace=True)
    
    
#     agg_dict = {'latitude':{'wifi_min_latitude':'min'}, 
#             'longitude':{'wifi_min_longitude':'min'}}
#     t0 = ka_add_groupby_features_1_vs_n(dataset1, ['wifi'], agg_dict)
#     t0['wifi1'] = t0['wifi']
#     t0['wifi2'] = t0['wifi']
#     t0['wifi3'] = t0['wifi']
#     t0['wifi4'] = t0['wifi']
#     t0['wifi5'] = t0['wifi']
#     t0['wifi6'] = t0['wifi']
#     t0['wifi7'] = t0['wifi']
#     t0['wifi8'] = t0['wifi']
#     t0['wifi9'] = t0['wifi']
#     t0['wifi10'] = t0['wifi']
    
#     result = result.merge(t0[['wifi1','wifi_min_longitude','wifi_min_latitude']],on=['wifi1'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude1','wifi_min_latitude':'wifi_min_latitude1'},inplace=True)
    
#     result = result.merge(t0[['wifi2','wifi_min_longitude','wifi_min_latitude']],on=['wifi2'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude2','wifi_min_latitude':'wifi_min_latitude2'},inplace=True)
    
#     result = result.merge(t0[['wifi3','wifi_min_longitude','wifi_min_latitude']],on=['wifi3'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude3','wifi_min_latitude':'wifi_min_latitude3'},inplace=True)
    
#     result = result.merge(t0[['wifi4','wifi_min_longitude','wifi_min_latitude']],on=['wifi4'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude4','wifi_min_latitude':'wifi_min_latitude4'},inplace=True)
    
#     result = result.merge(t0[['wifi5','wifi_min_longitude','wifi_min_latitude']],on=['wifi5'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude5','wifi_min_latitude':'wifi_min_latitude5'},inplace=True)
    
#     result = result.merge(t0[['wifi6','wifi_min_longitude','wifi_min_latitude']],on=['wifi6'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude6','wifi_min_latitude':'wifi_min_latitude6'},inplace=True)
    
#     result = result.merge(t0[['wifi7','wifi_min_longitude','wifi_min_latitude']],on=['wifi7'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude7','wifi_min_latitude':'wifi_min_latitude7'},inplace=True)
    
#     result = result.merge(t0[['wifi8','wifi_min_longitude','wifi_min_latitude']],on=['wifi8'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude8','wifi_min_latitude':'wifi_min_latitude8'},inplace=True)
    
#     result = result.merge(t0[['wifi9','wifi_min_longitude','wifi_min_latitude']],on=['wifi9'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude9','wifi_min_latitude':'wifi_min_latitude9'},inplace=True)
    
#     result = result.merge(t0[['wifi10','wifi_min_longitude','wifi_min_latitude']],on=['wifi10'],how='left')
#     result.rename(columns={'wifi_min_longitude':'wifi_min_longitude10','wifi_min_latitude':'wifi_min_latitude10'},inplace=True)
    
    
    
#     result['area1'] = ((result['wifi_max_longitude1']-result['wifi_min_longitude1'])/100) * ((result['wifi_max_latitude1']-result['wifi_min_latitude1'])/100)
#     result['area2'] = ((result['wifi_max_longitude2']-result['wifi_min_longitude2'])/100) * ((result['wifi_max_latitude2']-result['wifi_min_latitude2'])/100)
#     result['area3'] = ((result['wifi_max_longitude3']-result['wifi_min_longitude3'])/100) * ((result['wifi_max_latitude3']-result['wifi_min_latitude3'])/100)
#     result['area4'] = ((result['wifi_max_longitude4']-result['wifi_min_longitude4'])/100) * ((result['wifi_max_latitude4']-result['wifi_min_latitude4'])/100)
#     result['area5'] = ((result['wifi_max_longitude5']-result['wifi_min_longitude5'])/100) * ((result['wifi_max_latitude5']-result['wifi_min_latitude5'])/100)
#     result['area6'] = ((result['wifi_max_longitude6']-result['wifi_min_longitude6'])/100) * ((result['wifi_max_latitude6']-result['wifi_min_latitude6'])/100)
#     result['area7'] = ((result['wifi_max_longitude7']-result['wifi_min_longitude7'])/100) * ((result['wifi_max_latitude7']-result['wifi_min_latitude7'])/100)
#     result['area8'] = ((result['wifi_max_longitude8']-result['wifi_min_longitude8'])/100) * ((result['wifi_max_latitude8']-result['wifi_min_latitude8'])/100)
#     result['area9'] = ((result['wifi_max_longitude9']-result['wifi_min_longitude9'])/100) * ((result['wifi_max_latitude9']-result['wifi_min_latitude9'])/100)
#     result['area10'] = ((result['wifi_max_longitude10']-result['wifi_min_longitude10'])/100) * ((result['wifi_max_latitude10']-result['wifi_min_latitude10'])/100)
    
    
    
    return result

def get_feature_set(train1,train2,dataset1,dataset):
    #1.构造负样本
    result = get_negtive_sample(train1,train2)
#     print('1',result.shape)
#     2.构造label
    result = get_label(result,train2)
#     print('2',result.shape)
    #2.得到shop有关特征
    result = get_shop_feature(result,train1,dataset1)
#     print('3',result.shape)
    #3.得到wifi有关特征
    result = get_wifi_feature(result,train1,dataset1,dataset)
#     print('4',result.shape)
    #4.得到shop_wifi有关特征
    result = get_shop_wifi_feature(result,train1,dataset1,dataset)
#     print('5',result.shape)
    #5.经纬度有关特征
    result = get_jwd_feature(result,train1,dataset1,dataset)
    
    #6得到时间有关特征
    result = get_time_feature(result,train1,dataset1,dataset)

    
    return result

if __name__ == '__main__':
    df_train = pd.read_csv('train.csv')
    df_test = pd.read_csv('test.csv')
    feats = ['wifi1','wifi2','wifi3','wifi4','wifi5','wifi6','wifi7','wifi8','wifi9','wifi10']
    df_train[feats] = df_train[feats].fillna('0000')
    df_test[feats] = df_test[feats].fillna('0000')
    
    df_train1 = df_train.loc[(df_train['day']<25)&(df_train['day'])>=1,:]
    df_train2 = df_train.loc[(df_train['day']<32)&(df_train['day']>=25),:]
    df_train2 = df_train2.drop(['shop_longitude', 'shop_latitude'],axis=1)
    
    df_dataset = pd.read_csv('dataset.csv')
    df_dataset1 = df_dataset.loc[(df_dataset['day']<25)&(df_dataset['day']>=1),:]

    df_valid_dataset = df_dataset.copy()
    df_dataset2 = pd.read_csv('dataset2.csv')
    df_dataset = pd.concat([df_dataset,df_dataset2],axis=0)
    del df_dataset2
    gc.collect()
    
    mall_list = list(set(df_train['mall_id']))
    answer = pd.DataFrame()
    

    for mall in ['m_690','m_615']:
        print(mall)
        train1 = df_train1.loc[df_train1.mall_id==mall,:]
        print('train shape:',train2.shape)
        train2 = df_train2.loc[df_train2.mall_id==mall,:]
        train = df_train.loc[df_train.mall_id==mall,:]
        test = df_test.loc[df_test.mall_id==mall,:]
        
        dataset1 = df_dataset1.loc[df_dataset1.mall_id==mall,:]
        dataset = df_dataset.loc[df_dataset.mall_id==mall,:]
        valid_dataset = df_valid_dataset.loc[df_valid_dataset.mall_id==mall,:]
        
        
        train_feature = get_feature_set(train1,train2,dataset1,valid_dataset)
        test_feature = get_feature_set(train,test,valid_dataset,dataset)


        feats = ['wifi1','wifi2','wifi3','wifi4','wifi5','wifi6','wifi7','wifi8','wifi9','wifi10']
        for c in feats:
            train_feature[c] = train_feature[c].apply(lambda x:x[2:])
            train_feature[c] = train_feature[c].astype(str)
            test_feature[c] = test_feature[c].apply(lambda x:x[2:])
            test_feature[c] = test_feature[c].astype(str)

        
        lbl = LabelEncoder()

        for c in feats:
            lbl.fit(list(train_feature[c])+list(test_feature[c]))
            train_feature[c]= lbl.transform(train_feature[c])
            test_feature[c] = lbl.transform(list(test_feature[c]))

        train_feature[['wifi1','wifi2','wifi3','wifi4','wifi5','wifi6','wifi7','wifi8','wifi9','wifi10']] = train_feature[['wifi1','wifi2','wifi3','wifi4','wifi5','wifi6','wifi7','wifi8','wifi9','wifi10']].replace('00',np.nan)
        test_feature[['wifi1','wifi2','wifi3','wifi4','wifi5','wifi6','wifi7','wifi8','wifi9','wifi10']] = test_feature[['wifi1','wifi2','wifi3','wifi4','wifi5','wifi6','wifi7','wifi8','wifi9','wifi10']].replace('00',np.nan)
        print('train_feature shape:',train_feature.shape)
        import lightgbm as lgb
        y_train = train_feature['label']
        feats = ['wifi1','wifi2','wifi_nums_of_shop','shop_num','shop_connect_num','shop_connect_rt',
         'shop_mean_signal1','shop_mean_signal2','shop_mean_signal3','shop_mean_signal4','shop_mean_signal5','shop_mean_signal6', 'shop_mean_signal7','shop_mean_signal8','shop_mean_signal9','shop_mean_signal10',
         'shop_num_of_wifi1','shop_num_of_wifi2','shop_num_of_wifi3','shop_num_of_wifi4','shop_num_of_wifi5','shop_num_of_wifi6','shop_num_of_wifi7','shop_num_of_wifi8','shop_num_of_wifi9','shop_num_of_wifi10',
          'wifi_num1' , 'wifi_num2','wifi_num3','wifi_num4','wifi_num5','wifi_num6','wifi_num7','wifi_num8','wifi_num9','wifi_num10',
         'wifi_first_apperance1','wifi_first_apperance2','wifi_first_apperance3','wifi_first_apperance4','wifi_first_apperance5','wifi_first_apperance6',
          'wifi_first_apperance7','wifi_first_apperance8','wifi_first_apperance9','wifi_first_apperance10',
         'hotspot1','hotspot2','hotspot3','hotspot4','hotspot5','hotspot6','hotspot7','hotspot8','hotspot9','hotspot10',
         'wifi_mean_signal1','wifi_mean_signal2','wifi_mean_signal3','wifi_mean_signal4','wifi_mean_signal5','wifi_mean_signal6','wifi_mean_signal7','wifi_mean_signal8','wifi_mean_signal9','wifi_mean_signal10',
         'score1','score2','score3','score4','score5','score6','score7','score8','score9','score10',
         'score1_rt','score2_rt','score3_rt','score4_rt','score5_rt','score6_rt','score7_rt','score8_rt','score9_rt','score10_rt',
         'shop_wifi_num1','shop_wifi_num2','shop_wifi_num3','shop_wifi_num4','shop_wifi_num5','shop_wifi_num6', 'shop_wifi_num7','shop_wifi_num10','shop_wifi_num8','shop_wifi_num9',
         'shop_wifi_conn_num1','shop_wifi_conn_num2','shop_wifi_conn_num3', 'shop_wifi_conn_num4','shop_wifi_conn_num5','shop_wifi_conn_num6','shop_wifi_conn_num7','shop_wifi_conn_num8','shop_wifi_conn_num9','shop_wifi_conn_num10',
         'shop_wifi_conn1_rt','shop_wifi_conn2_rt','shop_wifi_conn3_rt','shop_wifi_conn4_rt','shop_wifi_conn5_rt','shop_wifi_conn6_rt','shop_wifi_conn7_rt','shop_wifi_conn8_rt','shop_wifi_conn9_rt','shop_wifi_conn10_rt',
         'shop_wifi_mean_signal1','shop_wifi_mean_signal2','shop_wifi_mean_signal3','shop_wifi_mean_signal4','shop_wifi_mean_signal5','shop_wifi_mean_signal6','shop_wifi_mean_signal7','shop_wifi_mean_signal8','shop_wifi_mean_signal9','shop_wifi_mean_signal10',
         'shop_wifi_conn_rt1','shop_wifi_conn_rt2','shop_wifi_conn_rt3','shop_wifi_conn_rt4','shop_wifi_conn_rt5','shop_wifi_conn_rt6','shop_wifi_conn_rt7','shop_wifi_conn_rt8','shop_wifi_conn_rt9','shop_wifi_conn_rt10',
         'signal1','signal2','signal3','signal4','signal5','signal6','signal7','signal8','signal9','signal10'
        ]


        X_train = train_feature[feats]
        X_train = X_train.fillna(0)
        index = test_feature['index']
        row_id = test_feature['row_id']
        shop_id = test_feature['shop_id']
        X_test = test_feature[feats]
        X_test = X_test.fillna(0)
#         print(X_train.columns)
        lgb_train = lgb.Dataset(X_train, y_train)
        # lgb_valid = lgb.Dataset(X_test,reference=lgb_train)

        params = {'max_depth':6,'num_leaves':64,'learning_rate':0.03,'num_threads':40,'objective':'binary','bagging_fraction':0.7,'bagging_freq':1,'min_sum_hessian_in_leaf':70}

        params['is_unbalance']='true'

        params['metric'] = 'binary_error'

        params['data_random_seed'] = 2017

        watchlist = [lgb_train]
        lgbm = lgb.train(params,
                        lgb_train,
                        num_boost_round=2000,valid_set=watchlist)

        predict = lgbm.predict(X_test,lgbm.best_iteration)
        
        
        result = pd.DataFrame()
        result['predict'] = predict
        result = pd.concat([row_id,result,shop_id],axis=1)
        result.sort_values(by=['row_id','predict'],ascending=False,inplace=True)
        result.drop_duplicates(subset='row_id',inplace=True)
        test = test.merge(result)
        answer = pd.concat([answer,test])

result = answer[['row_id','shop_id']]
test = df_test.merge(result,on='row_id',how='left')

result = test[['row_id','shop_id']]

result.to_csv('result.csv',index=None)
