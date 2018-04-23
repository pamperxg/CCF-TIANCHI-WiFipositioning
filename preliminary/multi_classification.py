import pandas as pd
import numpy as np
from sklearn import  preprocessing
import xgboost as xgb
# import lightgbm as lgb
from sklearn.model_selection import train_test_split
import time

df=pd.read_csv('input/ccf_first_round_user_shop_behavior.csv')
shop=pd.read_csv('input/ccf_first_round_shop_info.csv')
test=pd.read_csv('input/AB-evaluation_public.csv')
df=pd.merge(df,shop[['shop_id','mall_id']],how='left',on='shop_id')
df['time_stamp']=pd.to_datetime(df['time_stamp'])
train=pd.concat([df,test])
mall_list=list(set(list(shop.mall_id)))
result=pd.DataFrame()

print('begin:',time.strftime("%H:%M:%S",time.localtime()))
#感谢麦芽的香气
for mall in mall_list:
    print(mall)
    train1=train[train.mall_id==mall].reset_index(drop=True)       
    l=[]
    wifi_dict = {}
    for index,row in train1.iterrows():
        wifi_list = [wifi.split('|') for wifi in row['wifi_infos'].split(';')]
        for i in wifi_list:
            row[i[0]]=int(i[1])
            if i[0] not in wifi_dict:
                wifi_dict[i[0]]=1
            else:
                wifi_dict[i[0]]+=1
        l.append(row)
    
    df1=df[df.mall_id==mall].reset_index(drop=True)
    wifi_dict1 = {}
    for index,row in df1.iterrows():
        wifi_list = [wifi.split('|') for wifi in row['wifi_infos'].split(';')]
        for i in wifi_list:
            if i[0] not in wifi_dict1:
                wifi_dict1[i[0]]=1
            else:
                wifi_dict1[i[0]]+=1    
    test1=test[test.mall_id==mall].reset_index(drop=True)
    wifi_dict2 = {}
    for index,row in test1.iterrows():
        wifi_list = [wifi.split('|') for wifi in row['wifi_infos'].split(';')]
        for i in wifi_list:
            if i[0] not in wifi_dict2:
                wifi_dict2[i[0]]=1
            else:
                wifi_dict2[i[0]]+=1                
    tr_wifi = pd.DataFrame(pd.Series(wifi_dict1)).reset_index()
    tr_wifi.columns=['id','times']
    te_wifi = pd.DataFrame(pd.Series(wifi_dict2)).reset_index()
    te_wifi.columns=['id','times']
    com_wifi = tr_wifi.merge(te_wifi,on='id',how='inner')
#     com_wifi['times'] = com_wifi['times_x']+com_wifi['times_y']
#     com_wifi.drop(['times_x','times_y'],axis=1,inplace=True)
    list1 = com_wifi.id.values
    
    
    delete_wifi=[]
    for i in wifi_dict:
        if (wifi_dict[i]<20) or (i not in list1):
            delete_wifi.append(i)
    
            
    m=[]
    for row in l:
        new={}
        for n in row.keys():
            if n not in delete_wifi:
                new[n]=row[n]
        m.append(new)
    train1=pd.DataFrame(m)
    df_train=train1[train1.shop_id.notnull()]
    df_test=train1[train1.shop_id.isnull()]
    lbl = preprocessing.LabelEncoder()
    lbl.fit(list(df_train['shop_id'].values))
    df_train['label'] = lbl.transform(list(df_train['shop_id'].values))    
    num_class=df_train['label'].max()+1    
    params = {
            'objective': 'multi:softmax',
            'eta': 0.1,
            'max_depth': 9,
            'eval_metric': 'merror',
            'seed': 1024,
            'missing': -999,
            'min_child_weight':1.1,
            'lambda': 10,
            'subsample': 0.7,
            'colsample_bytree': 0.7,
            'colsample_bylevel': 0.7,
#             'eta': 0.03,
            'tree_method': 'exact',
            'num_class':num_class,
            'silent' : 1
            }
    feature=[x for x in train1.columns if x not in ['row_id','user_id','label','shop_id','time_stamp','mall_id','wifi_infos']]
    
#     X_train, X_test, y_train, y_test = train_test_split(df_train[feature],df_train['label'],test_size=0.1, random_state=66)
    xgbtrain = xgb.DMatrix(df_train[feature], df_train['label'])
#     xgbtrain = xgb.DMatrix(X_train,y_train)
#     xgbtrain1 = xgb.DMatrix(X_test,y_test)
    xgbtest = xgb.DMatrix(df_test[feature])
    watchlist = [ (xgbtrain,'train'), (xgbtrain, 'test') ]
    num_rounds=400
    model = xgb.train(params, xgbtrain, num_rounds, watchlist, early_stopping_rounds=50)
    df_test['label']=model.predict(xgbtest)
    df_test['shop_id']=df_test['label'].apply(lambda x:lbl.inverse_transform(int(x)))
    r=df_test[['row_id','shop_id']]
    result=pd.concat([result,r])
    result['row_id']=result['row_id'].astype('int')

print('end:',time.strftime("%H:%M:%S",time.localtime()))
result.to_csv('sub.csv',index=False)


#开始乱写版本
import numpy as np
import pandas as pd
import do_feature
import gc
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
import re
import time
# from utils import *
# from sklearn.metrics import accuracy_score
# from com_util import *

user = pd.read_csv('input/ccf_first_round_user_shop_behavior.csv')
shop = pd.read_csv('input/ccf_first_round_shop_info.csv')
train = pd.read_csv('input/train.csv')
test = pd.read_csv('input/AB-evaluation_public.csv')

wifi = pd.read_csv('input/train_wifi.csv')
train_wifi_top6 = pd.read_csv('input/train_wifi_top6.csv')
test_wifi_top6 = pd.read_csv('input/test_wifi_top6.csv')

train = pd.concat([train,train_wifi_top6],axis=1)
train.drop('wifi_infos',axis=1,inplace=True)

test = pd.concat([test,test_wifi_top6],axis=1)
test.drop(['wifi_infos'],axis=1,inplace=True)

train_wifi_s_top6 = pd.read_csv('input/train_wifi_s_top6.csv')
train_wifi_s_top6.columns = ['wifi_s_1','wifi_s_2','wifi_s_3','wifi_s_4','wifi_s_5','wifi_s_6']
train = pd.concat([train,train_wifi_s_top6],axis=1)
test_wifi_s_top6 = pd.read_csv('input/test_wifi_s_top6.csv')
test_wifi_s_top6.columns = ['wifi_s_1','wifi_s_2','wifi_s_3','wifi_s_4','wifi_s_5','wifi_s_6']
test = pd.concat([test,test_wifi_s_top6],axis=1)

# train_conn3 = pd.read_csv('input/train_conn3.csv')
# test_conn3 = pd.read_csv('input/test_conn3.csv')
# train = pd.concat([train,train_conn3],axis=1)
# test = pd.concat([test,test_conn3],axis=1)


print(train.columns)
print(test.columns)

def do_wifi_s_1(t):
    if t>-30:
        return 0
    elif (t<=-30) and (t>=-70):
        return 1
    else:
        return 2

def do_wifi_s_2(t):
    if t>-40:
        return 0
    elif (t<=-40) and (t>=-80):
        return 1
    else:
        return 2

def get_wifi_1(s):
    if s in wifi_list_1:
        return int(s.split('_')[1])
    else:
        return 0
def get_wifi_2(s):
    if s in wifi_list_2:
        return int(s.split('_')[1])
    else:
        return 0
def get_wifi_3(s):
    if s in wifi_list_3:
        return int(s.split('_')[1])
    else:
        return 0
def get_wifi_4(s):
    if s in wifi_list_4:
        return int(s.split('_')[1])
    else:
        return 0
def get_wifi_5(s):
    if s in wifi_list_5:
        return int(s.split('_')[1])
    else:
        return 0
def get_wifi_12(s):
    if s in wifi_list_12:
        return int(re.sub("\D", "", s))
    else:
        return 0
def get_wifi_123(s):
    if s in wifi_list_123:
        return float(re.sub("\D", "", s))
    else:
        return 0

# def get_user(s):
#     if s in user_list:
#         return np.int(s.split('_')[1])
#     else:
#         return 0
# def is_hot_user(s):
#     if s in user_list:
#         return 1
#     else:
#         return 0
    

# def is_hot_wifi1(s):
#     if s in wifi_list_1:
#         return 1
#     else:
#         return 0
# def is_hot_wifi2(s):
#     if s in wifi_list_2:
#         return 1
#     else:
#         return 0
# def is_hot_wifi3(s):
#     if s in wifi_list_3:
#         return 1
#     else:
#         return 0
# def is_hot_wifi12(s):
#     if s in wifi_list_12:
#         return 1
#     else:
#         return 0
# def is_hot_wifi123(s):
#     if s in wifi_list_123:
#         return 1
#     else:
#         return 0

# mall_id_list = ['m_1950','m_7800']
mall_id_list = train['mall_id'].unique()
# mall_id = 'm_7800'
l=[]

print('begin:',time.strftime("%H:%M:%S",time.localtime()))

for mall_id in mall_id_list:
    print(mall_id)
    train_m = train[train.mall_id == mall_id].reset_index()
    test_m = test[test.mall_id == mall_id].reset_index()
    test_a = test_m[['row_id']]
    print(train.shape)
    print(test.shape)
    print(train_m.shape)
    print(test_m.shape)

    test_m.drop(['index','mall_id'],axis=1,inplace=True)
    train_m.drop(['index','mall_id','category_id','price'],axis=1,inplace=True)

    c1 = train_m.drop('shop_id',axis=1)
    c2 = test_m.drop('row_id',axis=1)
    all_df = pd.concat([c1,c2])
    print(all_df.shape)

    del c1,c2
    gc.collect()

    #wifi相关特征
    train_m['wifi12'] = train_m['wifi1']+train_m['wifi2']
    test_m['wifi12'] = test_m['wifi1']+test_m['wifi2']
    all_df['wifi12'] = all_df['wifi1']+all_df['wifi2']

    train_m['wifi123'] = train_m['wifi1']+train_m['wifi2']+train_m['wifi3']
    test_m['wifi123'] = test_m['wifi1']+test_m['wifi2']+test_m['wifi3']
    all_df['wifi123'] = all_df['wifi1']+all_df['wifi2']+all_df['wifi3']

    wifi_list_1 = train_m.merge(test_m,on='wifi1',how='inner').wifi1.unique()
    wifi_list_2 = train_m.merge(test_m,on='wifi2',how='inner').wifi2.unique()
    wifi_list_3 = train_m.merge(test_m,on='wifi3',how='inner').wifi3.unique()
    wifi_list_4 = train_m.merge(test_m,on='wifi4',how='inner').wifi4.unique()
    wifi_list_5 = train_m.merge(test_m,on='wifi5',how='inner').wifi5.unique()
    wifi_list_12 = train_m.merge(test_m,on='wifi12',how='inner').wifi12.unique()
    wifi_list_123 = train_m.merge(test_m,on='wifi123',how='inner').wifi123.unique()

    # all_df['is_hot_wifi1'] = all_df.wifi1.apply(is_hot_wifi1)#冗余特征？
    # all_df['is_hot_wifi2'] = all_df.wifi2.apply(is_hot_wifi2)
    # all_df['is_hot_wifi3'] = all_df.wifi3.apply(is_hot_wifi3)
    # all_df['is_hot_wifi12'] = all_df.wifi12.apply(is_hot_wifi12)
    # all_df['is_hot_wifi123'] = all_df.wifi123.apply(is_hot_wifi123)

    all_df['wifi1'] = all_df.wifi1.apply(get_wifi_1)
    all_df['wifi2'] = all_df.wifi2.apply(get_wifi_2)
    all_df['wifi3'] = all_df.wifi3.apply(get_wifi_3)
    all_df['wifi4'] = all_df.wifi4.apply(get_wifi_4)
    all_df['wifi5'] = all_df.wifi5.apply(get_wifi_5)
    all_df['wifi12'] = all_df.wifi12.apply(get_wifi_12)
    all_df['wifi123'] = all_df.wifi123.apply(get_wifi_123)
    enc = LabelEncoder()
    all_df['wifi1'] = enc.fit_transform(all_df['wifi1'].values.reshape(-1,1))
    all_df['wifi2'] = enc.fit_transform(all_df['wifi2'].values.reshape(-1,1))
    all_df['wifi3'] = enc.fit_transform(all_df['wifi3'].values.reshape(-1,1))
    all_df['wifi4'] = enc.fit_transform(all_df['wifi4'].values.reshape(-1,1))
    all_df['wifi5'] = enc.fit_transform(all_df['wifi5'].values.reshape(-1,1))
    all_df['wifi12'] = enc.fit_transform(all_df['wifi12'].values.reshape(-1,1))    
    all_df['wifi123'] = enc.fit_transform(all_df['wifi123'].values.reshape(-1,1))


    #经纬度处理
    # all_df['longitude'] = all_df.longitude.apply(lambda x:int(str('% .2f' % (int(str(x*10000).split('.')[0])/100)).split('.')[1]))#取中间两位
    # all_df['latitude'] = all_df.latitude.apply(lambda x:int(str('% .2f' % (int(str(x*10000).split('.')[0])/100)).split('.')[1]))

    # all_df['longitude'] = all_df.longitude.apply(lambda x:int(str('% .2f' % (int(str(x*10000).split('.')[0])/100)).split('.')[1]))
    # all_df['latitude'] = all_df.latitude.apply(lambda x:int(str('% .2f' % (int(str(x*10000).split('.')[0])/100)).split('.')[1]))

    #wifi_s
#     all_df['wifi_s_1_'] = all_df.wifi_s_1.apply(do_wifi_s_1)
#     all_df['wifi_s_2_'] = all_df.wifi_s_2.apply(do_wifi_s_2)

    #time_stamp
    all_df = do_feature.get_time_feature(all_df)
    all_df.loc[all_df.day==28,'is_weekend']=1
    all_df.drop(['time_stamp','day','is_last_day','hour','day_of_week','wifi6','wifi_s_6','user_id'],axis=1,inplace=True)

    
    all_df.loc[all_df.wifi1==0,'wifi_s_1']=0
    all_df.loc[all_df.wifi2==0,'wifi_s_2']=0
    all_df.loc[all_df.wifi3==0,'wifi_s_3']=0
    all_df.loc[all_df.wifi4==0,'wifi_s_4']=0
    all_df.loc[all_df.wifi5==0,'wifi_s_5']=0
    #user_id
    # user_list = train_m.merge(test_m,on='user_id',how='inner').user_id.unique()
    # all_df['user_id'] = all_df.user_id.apply(get_user)
    # all_df['user_id'] = enc.fit_transform(all_df['user_id'].values.reshape(-1,1))
    # all_df['is_hot_user'] = all_df.user_id.apply(is_hot_user)

    #分回训练集和测试集
    train_l = all_df.loc[:train_m.shape[0]-1,:]
    test_l = all_df.loc[train_m.shape[0]:,:]
    train_l = pd.concat([train_l,train_m[['shop_id']]],axis=1)
    train_l['label'] = enc.fit_transform(train_l['shop_id'].values.reshape(-1,1))

    print(all_df.shape)
    print(train_l.shape)
    print(test_l.shape)
    del train_m,test_m
    gc.collect()

    #测试集和训练集划分
    train_x = train_l.drop(['shop_id','label'],axis=1)
    train_y = train_l[['label']]
#     X_train, X_test, y_train, y_test = train_test_split(train_x,train_y,test_size=0.3, random_state=66)

    #训练模型
    train_matrix = xgb.DMatrix(train_x,label=train_y)
#     test_matrix = xgb.DMatrix(X_test,label=y_test)
    n = train_l.shop_id.nunique()
    params = {'booster': 'gbtree',
              'objective': 'multi:softmax',
    #           'objective': 'multi:softprob',
              'eval_metric': 'merror',
              'gamma': 1,
              'min_child_weight': 1.5,
              'max_depth': 5,
              'lambda': 10,
              'subsample': 0.7,
              'colsample_bytree': 0.7,
              'colsample_bylevel': 0.7,
              'eta': 0.03,
              'tree_method': 'exact',
              'seed': 2017,
    #           'nthread': 12,
              "num_class":n
              }
    num_round = 800
    early_stopping_rounds = 50
#     watchlist = [(train_matrix, 'train'),
#                  (test_matrix, 'eval')
#                  ]

    model = xgb.train(params, train_matrix, num_boost_round=num_round)
    print(model.best_iteration)
    test_d = xgb.DMatrix(test_l)
    predict = model.predict(test_d,ntree_limit=model.best_iteration)

    s = []
    for i in predict:
        s.append(train_l[train_l.label == i].shop_id.unique()[0])

    test_a['shop_id'] = s
    l.append(test_a)

print('end:',time.strftime("%H:%M:%S",time.localtime()))    

result = pd.concat(l)
result.to_csv('result.csv',index=None)
