import pandas as pd
import numpy as np
#出现在了训练集中的店铺同样出现在了测试集中，匹配一下可以得到80准确率
train_wifi_top3 = pd.read_csv('../input/train_wifi_top3.csv')
test_wifi_top3 = pd.read_csv('../input/test_wifi_top3.csv')

train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/AB-evaluation_public.csv')

train_wifi_top3['wifi1'] = train_wifi_top3['wifi1']+train_wifi_top3['wifi2']
test_wifi_top3['wifi1'] = test_wifi_top3['wifi1']+test_wifi_top3['wifi2']

train = train[['shop_id','mall_id']]
test = test[['row_id','mall_id']]

train = pd.concat([train,train_wifi_top3],axis=1)
test = pd.concat([test,test_wifi_top3],axis=1)

train.drop(['wifi2','wifi3'],axis=1,inplace=True)
test.drop(['wifi2','wifi3'],axis=1,inplace=True)

mall_id_list = train['mall_id'].unique()
l = []
for mall_id in mall_id_list:
#     print(mall_id)
    train_ = train[train.mall_id == mall_id]
    test_ = test[test.mall_id == mall_id]
    wifi_list = train_.merge(test_,on='wifi1',how='inner').wifi1.unique()
    s = []
    for i in wifi_list: 
        s.append(train_[train_.wifi1==i])
    df = pd.concat(s)
    df1 = df.drop_duplicates(subset=['shop_id','wifi1'])
    tes = test_.merge(df1,on='wifi1',how='left')
    tes = tes.drop_duplicates('row_id')
    l.append(tes[['row_id','shop_id']])
result = pd.concat(l)
test = test.merge(result,on='row_id',how='left')
res = test[['row_id','shop_id']]
res.to_csv('result.csv',index=None)

