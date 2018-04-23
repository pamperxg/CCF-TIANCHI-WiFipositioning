-----------------基础特征---------------------------------------------------------------------------------------------
---原始构建的训练集,测试集train_binary,test_binary
-----训练集
drop table if exists train_binary;
create table if not exists train_binary as
with t1 as (select * from train_candidate a
left join 
(select index_id as index_id_s,user_id,mall_id,time_stamp,longitude,latitude,
w_bssid1,w_bssid2,w_bssid3,w_bssid4,w_bssid5,w_bssid6,w_bssid7,w_bssid8,w_bssid9,w_bssid10,
w_signal1,w_signal2,w_signal3,w_signal4,w_signal5,w_signal6,w_signal7,w_signal8,w_signal9,w_signal10 
from train2) b on a.index_id =b.index_id_s)
select index_id,shop_id,label,user_id,mall_id,time_stamp,longitude,latitude,
w_bssid1,w_bssid2,w_bssid3,w_bssid4,w_bssid5,w_bssid6,w_bssid7,w_bssid8,w_bssid9,w_bssid10,
w_signal1,w_signal2,w_signal3,w_signal4,w_signal5,w_signal6,w_signal7,w_signal8,w_signal9,w_signal10,
category_id,price,longitude_s,latitude_s from t1 c
left join (select category_id,price,longitude as longitude_s,latitude as latitude_s,shop_id as shop_id_s  from ant_tianchi_ccf_sl_shop_info) d on c.shop_id=d.shop_id_s;
----测试集
drop table if exists test_binary;
create table if not exists test_binary as
with t1 as (select * from test_candidate1  a left join 
(select row_id as row_id_s,user_id,mall_id,time_stamp,longitude,latitude,
w_bssid1,w_bssid2,w_bssid3,w_bssid4,w_bssid5,w_bssid6,w_bssid7,w_bssid8,w_bssid9,w_bssid10,
w_signal1,w_signal2,w_signal3,w_signal4,w_signal5,w_signal6,w_signal7,w_signal8,w_signal9,w_signal10 
from justfeng_binary_all_test_data_full) b 
on a.row_id = b.row_id_s)
select row_id,shop_id,user_id,mall_id,time_stamp,longitude,latitude,
w_bssid1,w_bssid2,w_bssid3,w_bssid4,w_bssid5,w_bssid6,w_bssid7,w_bssid8,w_bssid9,w_bssid10,
w_signal1,w_signal2,w_signal3,w_signal4,w_signal5,w_signal6,w_signal7,w_signal8,w_signal9,w_signal10, 
category_id,price,longitude_s,latitude_s
from t1 c left join 
(select category_id,price,longitude as longitude_s,latitude as latitude_s,shop_id as shop_id_s from ant_tianchi_ccf_sl_shop_info ) d on c.shop_id=d.shop_id_s;

--模型的输入只能为int，取出id类特征的后面的数字，信号强度为null(-999)的都为连接，把其设为正常的wifi值-60(id后面没有用上)
---处理训练集
drop table if exists train_binary_1;
create table if not exists train_binary_1 as
select t.*,
cast(splitid(w_bssid1) as bigint ) as wifi1,
cast(splitid(w_bssid2) as bigint ) as wifi2,
cast(splitid(w_bssid3) as bigint ) as wifi3,
cast(splitid(w_bssid4) as bigint ) as wifi4,
cast(splitid(w_bssid5) as bigint ) as wifi5,
cast(splitid(w_bssid6) as bigint ) as wifi6,
cast(splitid(w_bssid7) as bigint ) as wifi7,
cast(splitid(w_bssid8) as bigint ) as wifi8,
cast(splitid(w_bssid9) as bigint ) as wifi9,
cast(splitid(w_bssid10) as bigint ) as wifi10,
case when w_signal1=-999 then -60 else w_signal1 end as w_signal1_,
case when w_signal2=-999 then -60 else w_signal2 end as w_signal2_,
case when w_signal3=-999 then -60 else w_signal3 end as w_signal3_,
case when w_signal4=-999 then -60 else w_signal4 end as w_signal4_,
case when w_signal5=-999 then -60 else w_signal5 end as w_signal5_,
case when w_signal6=-999 then -60 else w_signal6 end as w_signal6_,
case when w_signal7=-999 then -60 else w_signal7 end as w_signal7_,
case when w_signal8=-999 then -60 else w_signal8 end as w_signal8_,
case when w_signal9=-999 then -60 else w_signal9 end as w_signal9_,
case when w_signal10=-999 then -60 else w_signal10 end as w_signal10_,
cast(splitid(mall_id) as bigint ) as mall,
cast(splitid(category_id) as bigint ) as category,
getdis(latitude,longitude,latitude_s,longitude_s) as distance
from train_binary t ;
---处理测试集
drop table if exists test_binary_1;
create table if not exists test_binary_1 as
select t.*,
cast(splitid(w_bssid1) as bigint ) as wifi1,
cast(splitid(w_bssid2) as bigint ) as wifi2,
cast(splitid(w_bssid3) as bigint ) as wifi3,
cast(splitid(w_bssid4) as bigint ) as wifi4,
cast(splitid(w_bssid5) as bigint ) as wifi5,
cast(splitid(w_bssid6) as bigint ) as wifi6,
cast(splitid(w_bssid7) as bigint ) as wifi7,
cast(splitid(w_bssid8) as bigint ) as wifi8,
cast(splitid(w_bssid9) as bigint ) as wifi9,
cast(splitid(w_bssid10) as bigint ) as wifi10,
case when w_signal1=-999 then -60 else w_signal1 end as w_signal1_,
case when w_signal2=-999 then -60 else w_signal2 end as w_signal2_,
case when w_signal3=-999 then -60 else w_signal3 end as w_signal3_,
case when w_signal4=-999 then -60 else w_signal4 end as w_signal4_,
case when w_signal5=-999 then -60 else w_signal5 end as w_signal5_,
case when w_signal6=-999 then -60 else w_signal6 end as w_signal6_,
case when w_signal7=-999 then -60 else w_signal7 end as w_signal7_,
case when w_signal8=-999 then -60 else w_signal8 end as w_signal8_,
case when w_signal9=-999 then -60 else w_signal9 end as w_signal9_,
case when w_signal10=-999 then -60 else w_signal10 end as w_signal10_,
cast(splitid(mall_id) as bigint ) as mall,
cast(splitid(category_id) as bigint ) as category,
getdis(latitude,longitude,latitude_s,longitude_s) as distance
from test_binary t ;

-------这里可以再用distance筛选一下候选集---------------------------------------------------------------------------------------------
---distance大于某个阈值进行筛选，可以增加正样本的比例，但是距离不确定是否还有异常值待去除


----取出shop的历史wifi信息-------------------------------------------------------------------------------------------------------------
--提取特征：train1,justfeng_binary_all_train_data_full(train),
--dataset(train展开):justfeng_binary_all_dataset_full
--dataset1(train1展开):select * from justfeng_binary_all_dataset_full where index_id in (select index_id from train1)。
--训练集：train_binary,测试集：test_binary
---wifi1-10在候选集shop出现的次数出现比例，连接次数，当前强度与历史平均强度的差……
select * from train_binary ;
select * from test_binary ;
select * from justfeng_binary_all_dataset_full; 
---------------
-----每一个shop中每一个wifi历史出现次数,平均信号强度，在shop中出现次数的排名
---------------
--训练集shop历史特征-wifi历史出现次数,平均信号强度，在shop中出现次数的排名
drop table if exists shop_history_wifi_feats_train;
create table if not exists shop_history_wifi_feats_train as 
with t1 as (select * from justfeng_binary_all_dataset_full where index_id in (select index_id from train1)),
t2 as (select shop_id,w_bssid,count(*) as his_occur,avg(w_signal) as avg_sig from t1 group by shop_id,w_bssid) ---count(*)/count(distinct index_id)一样
select t2.*,row_number() over(partition by shop_id order by his_occur desc) num from t2;
select * from shop_history_wifi_feats_train;
--测试集shop历史特征-wifi历史出现次数,平均信号强度，在shop中出现次数的排名
drop table if exists shop_history_wifi_feats_test;
create table if not exists shop_history_wifi_feats_test as 
with t1 as (select shop_id,w_bssid,count(*) as his_occur,avg(w_signal) as avg_sig from justfeng_binary_all_dataset_full group by shop_id,w_bssid)
select t1.*,row_number() over(partition by shop_id order by his_occur desc) num from t1;
select * from shop_history_wifi_feats_test;
------------------
----每一个shop中的wifi的历史连接次数，连接次数rank
-----------------
--训练集wifi历史连接次数，连接次数rank
drop table if exists shop_history_wifi_conn_train;
create table if not exists shop_history_wifi_conn_train as
with t1 as (select *,case when w_flag='false' then 0 else 1 end as flag from justfeng_binary_all_dataset_full where index_id in (select index_id from train1)),
t2 as (select shop_id,w_bssid,sum(flag) as conn_times from t1 group by shop_id,w_bssid)
select t2.*,row_number() over(partition by shop_id order by conn_times desc) num from t2;
select * from shop_history_wifi_conn_train;
--测试集wifi历史连接次数，连接次数rank
drop table if exists shop_history_wifi_conn_test;
create table if not exists shop_history_wifi_conn_test as
with t1 as (select *,case when w_flag='false' then 0 else 1 end as flag from justfeng_binary_all_dataset_full),
t2 as (select shop_id,w_bssid,sum(flag) as conn_times from t1 group by shop_id,w_bssid)
select t2.*,row_number() over(partition by shop_id order by conn_times desc) num from t2;

--当前小时当前店铺的历史销量
drop table if exists shop_his_hour_sales_train;
create table if not exists shop_his_hour_sales_train as
with t1 as (select *,datepart(concat(time_stamp,':00'),'hh') as hour from justfeng_binary_all_dataset_full where index_id in (select index_id from train1))
select shop_id,hour,count(distinct index_id) as sale_hour from t1 group by shop_id,hour;
drop table if exists shop_his_hour_sales_test;
create table if not exists shop_his_hour_sales_test as
with t1 as (select *,datepart(concat(time_stamp,':00'),'hh') as hour from justfeng_binary_all_dataset_full)
select shop_id,hour,count(distinct index_id)*24/31 as sale_hour from t1 group by shop_id,hour;

--当前小时当前店铺wifi的出现数，连接数
--drop table if exists shop_his_hour_wifi_oc_train;
create table if not exists shop_his_hour_wifi_oc_train as
with t1 as(select *,datepart(concat(time_stamp,':00'),'hh') as hour,case when w_flag='false' then 0 else 1 end as flag from justfeng_binary_all_dataset_full where index_id in (select index_id from train1))
select shop_id,hour,count(w_bssid) as hour_occur,sum(flag) as hour_conn  from t1 group by shop_id,hour;
--drop table if exists shop_his_hour_wifi_oc_test;
create table if not exists shop_his_hour_wifi_oc_test as
with t1 as (select *,datepart(concat(time_stamp,':00'),'hh') as hour,case when w_flag='false' then 0 else 1 end as flag from justfeng_binary_all_dataset_full)
select shop_id,hour,count(w_bssid) as hour_occur,sum(flag) as hour_conn  from t1 group by shop_id,hour;

-----------------------------------------------------------------------训练集----------------------------------------------
----加入shop中wifi的历史信息，出现次数，平均强度，连接数，排名等
drop table if exists train_binary_a;
create table if not exists train_binary_a as 
select index_id,a.shop_id,label,user_id,mall_id,mall,time_stamp,
w_bssid1,wifi1,his_occur1/24 as his_occur1,w_signal1_,avg_sig1,rank1,(w_signal1_-avg_sig1)as diff_s_1,conn_times1/24 as conn_times1,conn_rank1,
w_bssid2,wifi2,his_occur2/24 as his_occur2,w_signal2_,avg_sig2,rank2,(w_signal2_-avg_sig2)as diff_s_2,conn_times2/24 as conn_times2,conn_rank2,
w_bssid3,wifi3,his_occur3/24 as his_occur3,w_signal3_,avg_sig3,rank3,(w_signal3_-avg_sig3)as diff_s_3,conn_times3/24 as conn_times3,conn_rank3,
w_bssid4,wifi4,his_occur4/24 as his_occur4,w_signal4_,avg_sig4,rank4,(w_signal4_-avg_sig4)as diff_s_4,conn_times4/24 as conn_times4,conn_rank4,
w_bssid5,wifi5,his_occur5/24 as his_occur5,w_signal5_,avg_sig5,rank5,(w_signal5_-avg_sig5)as diff_s_5,conn_times5/24 as conn_times5,conn_rank5,
w_bssid6,wifi6,his_occur6/24 as his_occur6,w_signal6_,avg_sig6,rank6,(w_signal6_-avg_sig6)as diff_s_6,conn_times6/24 as conn_times6,conn_rank6,
w_bssid7,wifi7,his_occur7/24 as his_occur7,w_signal7_,avg_sig7,rank7,(w_signal7_-avg_sig7)as diff_s_7,conn_times7/24 as conn_times7,conn_rank7,
w_bssid8,wifi8,his_occur8/24 as his_occur8,w_signal8_,avg_sig8,rank8,(w_signal8_-avg_sig8)as diff_s_8,conn_times8/24 as conn_times8,conn_rank8,
w_bssid9,wifi9,his_occur9/24 as his_occur9,w_signal9_,avg_sig9,rank9,(w_signal9_-avg_sig9)as diff_s_9,conn_times9/24 as conn_times9,conn_rank9,
w_bssid10,wifi10,his_occur10/24 as his_occur10,w_signal10_,avg_sig10,rank10,(w_signal10_-avg_sig10)as diff_s_10,conn_times10/24 as conn_times10,conn_rank10,
category_id,category,price,longitude,latitude,longitude_s,latitude_s,distance
from train_binary_1 a 
left join (select w_bssid,shop_id,his_occur as his_occur1,avg_sig as avg_sig1,num as rank1 from shop_history_wifi_feats_train) b on a.w_bssid1=b.w_bssid and a.shop_id=b.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur2,avg_sig as avg_sig2,num as rank2 from shop_history_wifi_feats_train) c on a.w_bssid2=c.w_bssid and a.shop_id=c.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur3,avg_sig as avg_sig3,num as rank3 from shop_history_wifi_feats_train) d on a.w_bssid3=d.w_bssid and a.shop_id=d.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur4,avg_sig as avg_sig4,num as rank4 from shop_history_wifi_feats_train) e on a.w_bssid4=e.w_bssid and a.shop_id=e.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur5,avg_sig as avg_sig5,num as rank5 from shop_history_wifi_feats_train) f on a.w_bssid5=f.w_bssid and a.shop_id=f.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur6,avg_sig as avg_sig6,num as rank6 from shop_history_wifi_feats_train) g on a.w_bssid6=g.w_bssid and a.shop_id=g.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur7,avg_sig as avg_sig7,num as rank7 from shop_history_wifi_feats_train) h on a.w_bssid7=h.w_bssid and a.shop_id=h.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur8,avg_sig as avg_sig8,num as rank8 from shop_history_wifi_feats_train) i on a.w_bssid8=i.w_bssid and a.shop_id=i.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur9,avg_sig as avg_sig9,num as rank9 from shop_history_wifi_feats_train) j on a.w_bssid9=j.w_bssid and a.shop_id=j.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur10,avg_sig as avg_sig10,num as rank10 from shop_history_wifi_feats_train) k on a.w_bssid10=k.w_bssid and a.shop_id=k.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times1,num as conn_rank1 from shop_history_wifi_conn_train ) l on a.w_bssid1=l.w_bssid and a.shop_id=l.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times2,num as conn_rank2 from shop_history_wifi_conn_train ) m on a.w_bssid2=m.w_bssid and a.shop_id=m.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times3,num as conn_rank3 from shop_history_wifi_conn_train ) n on a.w_bssid3=n.w_bssid and a.shop_id=n.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times4,num as conn_rank4 from shop_history_wifi_conn_train ) o on a.w_bssid4=o.w_bssid and a.shop_id=o.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times5,num as conn_rank5 from shop_history_wifi_conn_train ) p on a.w_bssid5=p.w_bssid and a.shop_id=p.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times6,num as conn_rank6 from shop_history_wifi_conn_train ) q on a.w_bssid6=q.w_bssid and a.shop_id=q.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times7,num as conn_rank7 from shop_history_wifi_conn_train ) r on a.w_bssid7=r.w_bssid and a.shop_id=r.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times8,num as conn_rank8 from shop_history_wifi_conn_train ) s on a.w_bssid8=s.w_bssid and a.shop_id=s.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times9,num as conn_rank9 from shop_history_wifi_conn_train ) t on a.w_bssid9=t.w_bssid and a.shop_id=t.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times10,num as conn_rank10 from shop_history_wifi_conn_train ) u on a.w_bssid10=u.w_bssid and a.shop_id=u.shop_id;

--关于缺失值的填充：
--0：wifi1, his_occur1, wifi2, his_occur2, wifi3, his_occur3, wifi4, his_occur4, wifi5, his_occur5, wifi6, his_occur6, 
-----wifi7, his_occur7, wifi8, his_occur8, wifi9, his_occur9, wifi10, his_occur10, longitude_s, latitude_s,
-----conn_times1,conn_times2,conn_times3,conn_times4,conn_times5,conn_times6,conn_times7,conn_times8,conn_times9,conn_times10
--999：rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9, rank10, category, price, distance, 
-------diff_s_1, diff_s_2, diff_s_3, diff_s_4, diff_s_5, diff_s_6, diff_s_7, diff_s_8, diff_s_9, diff_s_10,
-------conn_rank1,conn_rank2,conn_rank3,conn_rank4,conn_rank5,conn_rank6,conn_rank7,conn_rank8,conn_rank9,conn_rank10
--（-999）：avg_sig1, avg_sig2, avg_sig3, avg_sig4, avg_sig5, avg_sig6, avg_sig7, avg_sig8, avg_sig9, avg_sig10

-----加入当前小时店铺销量的信息，wifi信息,train_binary_wc为前一步产生的数据（填充缺失）
drop table if exists train_binary_wc;
create table if not exists train_binary_wc as
select index_id,a.shop_id,label,user_id,mall_id,mall,time_stamp,
w_bssid1,wifi1,his_occur1,w_signal1_,avg_sig1,rank1,diff_s_1,conn_times1,conn_rank1,(rank1-conn_rank1) as rank_diff1,(his_occur1-conn_times1) as occur_conn1,
w_bssid2,wifi2,his_occur2,w_signal2_,avg_sig2,rank2,diff_s_2,conn_times2,conn_rank2,(rank2-conn_rank2) as rank_diff2,(his_occur2-conn_times2) as occur_conn2,
w_bssid3,wifi3,his_occur3,w_signal3_,avg_sig3,rank3,diff_s_3,conn_times3,conn_rank3,(rank3-conn_rank3) as rank_diff3,(his_occur3-conn_times3) as occur_conn3,
w_bssid4,wifi4,his_occur4,w_signal4_,avg_sig4,rank4,diff_s_4,conn_times4,conn_rank4,(rank4-conn_rank4) as rank_diff4,(his_occur4-conn_times4) as occur_conn4,
w_bssid5,wifi5,his_occur5,w_signal5_,avg_sig5,rank5,diff_s_5,conn_times5,conn_rank5,(rank5-conn_rank5) as rank_diff5,(his_occur5-conn_times5) as occur_conn5,
w_bssid6,wifi6,his_occur6,w_signal6_,avg_sig6,rank6,diff_s_6,conn_times6,conn_rank6,(rank6-conn_rank6) as rank_diff6,(his_occur6-conn_times6) as occur_conn6,
w_bssid7,wifi7,his_occur7,w_signal7_,avg_sig7,rank7,diff_s_7,conn_times7,conn_rank7,(rank7-conn_rank7) as rank_diff7,(his_occur7-conn_times7) as occur_conn7,
w_bssid8,wifi8,his_occur8,w_signal8_,avg_sig8,rank8,diff_s_8,conn_times8,conn_rank8,(rank8-conn_rank8) as rank_diff8,(his_occur8-conn_times8) as occur_conn8,
w_bssid9,wifi9,his_occur9,w_signal9_,avg_sig9,rank9,diff_s_9,conn_times9,conn_rank9,(rank9-conn_rank9) as rank_diff9,(his_occur9-conn_times9) as occur_conn9,
w_bssid10,wifi10,his_occur10,w_signal10_,avg_sig10,rank10,diff_s_10,conn_times10,conn_rank10,(rank10-conn_rank10) as rank_diff10,(his_occur10-conn_times10) as occur_conn10,
category_id,category,price,longitude,latitude,longitude_s,latitude_s,(longitude-longitude_s) as longi_diff,(latitude-latitude_s) as lati_diff,distance,a.hour,
sale_hour/24 as sale_hour,hour_occur/24 as hour_occur,hour_conn/24 as hour_conn 
from (select t.*,datepart(concat(time_stamp,':00'),'hh') as hour from train_binary_a t) a
left join shop_his_hour_sales_train b on a.shop_id=b.shop_id and a.hour=b.hour
left join shop_his_hour_wifi_oc_train c on a.shop_id=c.shop_id and a.hour=c.hour;

----------------------------------------------------------测试集----------------------------------------------------------------------------------
----加入shop中wifi的历史信息，出现次数，平均强度，连接数，排名等
---连接次数的特征尝试按照时间长度做平滑，把测试集中构造出来的链接次数乘以24/31
drop table if exists test_binary_a;
create table if not exists test_binary_a as 
select row_id,a.shop_id,user_id,mall_id,mall,time_stamp,
w_bssid1,wifi1,his_occur1/31 as his_occur1,w_signal1_,avg_sig1,rank1,(w_signal1_-avg_sig1)as diff_s_1,conn_times1/31 as conn_times1,conn_rank1,
w_bssid2,wifi2,his_occur2/31 as his_occur2,w_signal2_,avg_sig2,rank2,(w_signal2_-avg_sig2)as diff_s_2,conn_times2/31 as conn_times2,conn_rank2,
w_bssid3,wifi3,his_occur3/31 as his_occur3,w_signal3_,avg_sig3,rank3,(w_signal3_-avg_sig3)as diff_s_3,conn_times3/31 as conn_times3,conn_rank3,
w_bssid4,wifi4,his_occur4/31 as his_occur4,w_signal4_,avg_sig4,rank4,(w_signal4_-avg_sig4)as diff_s_4,conn_times4/31 as conn_times4,conn_rank4,
w_bssid5,wifi5,his_occur5/31 as his_occur5,w_signal5_,avg_sig5,rank5,(w_signal5_-avg_sig5)as diff_s_5,conn_times5/31 as conn_times5,conn_rank5,
w_bssid6,wifi6,his_occur6/31 as his_occur6,w_signal6_,avg_sig6,rank6,(w_signal6_-avg_sig6)as diff_s_6,conn_times6/31 as conn_times6,conn_rank6,
w_bssid7,wifi7,his_occur7/31 as his_occur7,w_signal7_,avg_sig7,rank7,(w_signal7_-avg_sig7)as diff_s_7,conn_times7/31 as conn_times7,conn_rank7,
w_bssid8,wifi8,his_occur8/31 as his_occur8,w_signal8_,avg_sig8,rank8,(w_signal8_-avg_sig8)as diff_s_8,conn_times8/31 as conn_times8,conn_rank8,
w_bssid9,wifi9,his_occur9/31 as his_occur9,w_signal9_,avg_sig9,rank9,(w_signal9_-avg_sig9)as diff_s_9,conn_times9/31 as conn_times9,conn_rank9,
w_bssid10,wifi10,his_occur10/31 as his_occur10,w_signal10_,avg_sig10,rank10,(w_signal10_-avg_sig10)as diff_s_10,conn_times10/31 as conn_times10,conn_rank10,
category_id,category,price,longitude,latitude,longitude_s,latitude_s,distance
from test_binary_1 a 
left join (select w_bssid,shop_id,his_occur as his_occur1,avg_sig as avg_sig1,num as rank1 from shop_history_wifi_feats_test) b on a.w_bssid1=b.w_bssid and a.shop_id=b.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur2,avg_sig as avg_sig2,num as rank2 from shop_history_wifi_feats_test) c on a.w_bssid2=c.w_bssid and a.shop_id=c.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur3,avg_sig as avg_sig3,num as rank3 from shop_history_wifi_feats_test) d on a.w_bssid3=d.w_bssid and a.shop_id=d.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur4,avg_sig as avg_sig4,num as rank4 from shop_history_wifi_feats_test) e on a.w_bssid4=e.w_bssid and a.shop_id=e.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur5,avg_sig as avg_sig5,num as rank5 from shop_history_wifi_feats_test) f on a.w_bssid5=f.w_bssid and a.shop_id=f.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur6,avg_sig as avg_sig6,num as rank6 from shop_history_wifi_feats_test) g on a.w_bssid6=g.w_bssid and a.shop_id=g.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur7,avg_sig as avg_sig7,num as rank7 from shop_history_wifi_feats_test) h on a.w_bssid7=h.w_bssid and a.shop_id=h.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur8,avg_sig as avg_sig8,num as rank8 from shop_history_wifi_feats_test) i on a.w_bssid8=i.w_bssid and a.shop_id=i.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur9,avg_sig as avg_sig9,num as rank9 from shop_history_wifi_feats_test) j on a.w_bssid9=j.w_bssid and a.shop_id=j.shop_id
left join (select w_bssid,shop_id,his_occur as his_occur10,avg_sig as avg_sig10,num as rank10 from shop_history_wifi_feats_test) k on a.w_bssid10=k.w_bssid and a.shop_id=k.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times1,num as conn_rank1 from shop_history_wifi_conn_test ) l on a.w_bssid1=l.w_bssid and a.shop_id=l.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times2,num as conn_rank2 from shop_history_wifi_conn_test ) m on a.w_bssid2=m.w_bssid and a.shop_id=m.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times3,num as conn_rank3 from shop_history_wifi_conn_test ) n on a.w_bssid3=n.w_bssid and a.shop_id=n.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times4,num as conn_rank4 from shop_history_wifi_conn_test ) o on a.w_bssid4=o.w_bssid and a.shop_id=o.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times5,num as conn_rank5 from shop_history_wifi_conn_test ) p on a.w_bssid5=p.w_bssid and a.shop_id=p.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times6,num as conn_rank6 from shop_history_wifi_conn_test ) q on a.w_bssid6=q.w_bssid and a.shop_id=q.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times7,num as conn_rank7 from shop_history_wifi_conn_test ) r on a.w_bssid7=r.w_bssid and a.shop_id=r.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times8,num as conn_rank8 from shop_history_wifi_conn_test ) s on a.w_bssid8=s.w_bssid and a.shop_id=s.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times9,num as conn_rank9 from shop_history_wifi_conn_test ) t on a.w_bssid9=t.w_bssid and a.shop_id=t.shop_id
left join (select w_bssid,shop_id,conn_times as conn_times10,num as conn_rank10 from shop_history_wifi_conn_test ) u on a.w_bssid10=u.w_bssid and a.shop_id=u.shop_id;
------做除法运算后，int变成了double，把其变回bigint类型，不然预测的时候报错--让两个都变成double
/* drop table if exists test_binary_wc1;
create table if not exists test_binary_wc1 as 
select row_id,shop_id,user_id,mall_id,mall,time_stamp,
w_bssid1,wifi1,cast(his_occur1 as bigint ) as his_occur1,w_signal1_,avg_sig1,rank1,diff_s_1,cast(conn_times1 as bigint) as conn_times1,conn_rank1,
w_bssid2,wifi2,cast(his_occur2 as bigint ) as his_occur2,w_signal2_,avg_sig2,rank2,diff_s_2,cast(conn_times2 as bigint) as conn_times2,conn_rank2,
w_bssid3,wifi3,cast(his_occur3 as bigint ) as his_occur3,w_signal3_,avg_sig3,rank3,diff_s_3,cast(conn_times3 as bigint) as conn_times3,conn_rank3,
w_bssid4,wifi4,cast(his_occur4 as bigint ) as his_occur4,w_signal4_,avg_sig4,rank4,diff_s_4,cast(conn_times4 as bigint) as conn_times4,conn_rank4,
w_bssid5,wifi5,cast(his_occur5 as bigint ) as his_occur5,w_signal5_,avg_sig5,rank5,diff_s_5,cast(conn_times5 as bigint) as conn_times5,conn_rank5,
w_bssid6,wifi6,cast(his_occur6 as bigint ) as his_occur6,w_signal6_,avg_sig6,rank6,diff_s_6,cast(conn_times6 as bigint) as conn_times6,conn_rank6,
w_bssid7,wifi7,cast(his_occur7 as bigint ) as his_occur7,w_signal7_,avg_sig7,rank7,diff_s_7,cast(conn_times7 as bigint) as conn_times7,conn_rank7,
w_bssid8,wifi8,cast(his_occur8 as bigint ) as his_occur8,w_signal8_,avg_sig8,rank8,diff_s_8,cast(conn_times8 as bigint) as conn_times8,conn_rank8,
w_bssid9,wifi9,cast(his_occur9 as bigint ) as his_occur9,w_signal9_,avg_sig9,rank9,diff_s_9,cast(conn_times9 as bigint) as conn_times9,conn_rank9,
w_bssid10,wifi10,cast(his_occur10 as bigint ) as his_occur10,w_signal10_,avg_sig10,rank10,diff_s_10,cast(conn_times10 as bigint) as conn_times10,conn_rank10,
category_id,category,price,longitude,latitude,longitude_s,latitude_s,distance from test_binary_wc; */

-----加入当前小时店铺销量的信息，同样按照时间长度做平滑*24/31，并转化为bigint类型,test_binary_wc1为前一步产生的数据（填充缺失，类型转换）
drop table if exists test_binary_wc;
create table if not exists test_binary_wc as
select  row_id,a.shop_id,user_id,mall_id,mall,time_stamp,
w_bssid1,wifi1,his_occur1,w_signal1_,avg_sig1,rank1,diff_s_1,conn_times1,conn_rank1,(rank1-conn_rank1) as rank_diff1,(his_occur1-conn_times1) as occur_conn1,
w_bssid2,wifi2,his_occur2,w_signal2_,avg_sig2,rank2,diff_s_2,conn_times2,conn_rank2,(rank2-conn_rank2) as rank_diff2,(his_occur2-conn_times2) as occur_conn2,
w_bssid3,wifi3,his_occur3,w_signal3_,avg_sig3,rank3,diff_s_3,conn_times3,conn_rank3,(rank3-conn_rank3) as rank_diff3,(his_occur3-conn_times3) as occur_conn3,
w_bssid4,wifi4,his_occur4,w_signal4_,avg_sig4,rank4,diff_s_4,conn_times4,conn_rank4,(rank4-conn_rank4) as rank_diff4,(his_occur4-conn_times4) as occur_conn4,
w_bssid5,wifi5,his_occur5,w_signal5_,avg_sig5,rank5,diff_s_5,conn_times5,conn_rank5,(rank5-conn_rank5) as rank_diff5,(his_occur5-conn_times5) as occur_conn5,
w_bssid6,wifi6,his_occur6,w_signal6_,avg_sig6,rank6,diff_s_6,conn_times6,conn_rank6,(rank6-conn_rank6) as rank_diff6,(his_occur6-conn_times6) as occur_conn6,
w_bssid7,wifi7,his_occur7,w_signal7_,avg_sig7,rank7,diff_s_7,conn_times7,conn_rank7,(rank7-conn_rank7) as rank_diff7,(his_occur7-conn_times7) as occur_conn7,
w_bssid8,wifi8,his_occur8,w_signal8_,avg_sig8,rank8,diff_s_8,conn_times8,conn_rank8,(rank8-conn_rank8) as rank_diff8,(his_occur8-conn_times8) as occur_conn8,
w_bssid9,wifi9,his_occur9,w_signal9_,avg_sig9,rank9,diff_s_9,conn_times9,conn_rank9,(rank9-conn_rank9) as rank_diff9,(his_occur9-conn_times9) as occur_conn9,
w_bssid10,wifi10,his_occur10,w_signal10_,avg_sig10,rank10,diff_s_10,conn_times10,conn_rank10,(rank10-conn_rank10) as rank_diff10,(his_occur10-conn_times10) as occur_conn10,
category_id,category,price,longitude,latitude,longitude_s,latitude_s,(longitude-longitude_s) as longi_diff,(latitude-latitude_s) as lati_diff,distance,a.hour,
sale_hour/31 as sale_hour,hour_occur/31 as hour_occur,hour_conn/31 as hour_conn
from (select t.*,datepart(concat(time_stamp,':00'),'hh') as hour from test_binary_a t) a
left join shop_his_hour_sales_train b on a.shop_id=b.shop_id and a.hour=b.hour
left join shop_his_hour_wifi_oc_train c on a.shop_id=c.shop_id and a.hour=c.hour;

---填充缺失，类型转换后的数据集
--train_binary_wc,test_binary_wc1
---加入rank差值，连接次数差值，经纬度差值，当前小时销量
--train_binary_wct,test_binary_wct
---再次填充缺失值，sale_hour
--train_binary_wct1,test_binary_wct1

----之前得到的特征集：
----train_binary_wct1,test_binary_wct1
--对于之前计算得差值特征取绝对值，longi_diff*10000,lati_diff*10000,rank_diff,diff_s，然而取绝对值效果变差
--计算score特征，his_occur_score,conn_score,rank_score,conn_rank_score(score可以再做差值，但是之前已经做过次数差和rank差)，没用,这些score没用上
(20*his_occur1+16*his_occur2+10*his_occur3+8*his_occur4+5*his_occur5+3*his_occur6+2*his_occur7+his_occur8+his_occur9+his_occur10) as his_occur_score,
(20*conn_times1+16*conn_times2+10*conn_times3+8*conn_times4+5*conn_times5+3*conn_times6+2*conn_times7+conn_times8+conn_times9+conn_times10) as conn_score,
(20*rank1+16*rank2+10*rank3+8*rank4+5*rank5+3*rank6+2*rank7+rank8+rank9+rank10) as rank_score,
(20*conn_rank1+16*conn_rank2+10*conn_rank3+8*conn_rank4+5*conn_rank5+3*conn_rank6+2*conn_rank7+conn_rank8+conn_rank9+conn_rank10) as conn_rank_score

--原始的特征是否和比率特征能混用待检验，加入比率和一些新的特征
drop table if exists train_binary_wcts;
create table if not exists train_binary_wcts as 
select index_id,shop_id,label,time_stamp,
his_occur1,avg_sig1,rank1,diff_s_1,conn_times1,conn_rank1,rank_diff1,occur_conn1,getratio(conn_times1,his_occur1) as conn_ratio1,(his_occur1/rank1) as oc_div_r1,(his_occur1/conn_rank1) as oc_div_cr1,getratio(occur_conn1,rank_diff1) as o_c_div_rd1,(conn_times1/conn_rank1) as co_div_cr1,(conn_times1/rank1) as co_div_r1,
his_occur2,avg_sig2,rank2,diff_s_2,conn_times2,conn_rank2,rank_diff2,occur_conn2,getratio(conn_times2,his_occur2) as conn_ratio2,(his_occur2/rank2) as oc_div_r2,(his_occur2/conn_rank2) as oc_div_cr2,getratio(occur_conn2,rank_diff2) as o_c_div_rd2,(conn_times2/conn_rank2) as co_div_cr2,(conn_times2/rank2) as co_div_r2,
his_occur3,avg_sig3,rank3,diff_s_3,conn_times3,conn_rank3,rank_diff3,occur_conn3,getratio(conn_times3,his_occur3) as conn_ratio3,(his_occur3/rank3) as oc_div_r3,(his_occur3/conn_rank3) as oc_div_cr3,getratio(occur_conn3,rank_diff3) as o_c_div_rd3,(conn_times3/conn_rank3) as co_div_cr3,(conn_times3/rank3) as co_div_r3,
his_occur4,avg_sig4,rank4,diff_s_4,conn_times4,conn_rank4,rank_diff4,occur_conn4,getratio(conn_times4,his_occur4) as conn_ratio4,(his_occur4/rank4) as oc_div_r4,(his_occur4/conn_rank4) as oc_div_cr4,getratio(occur_conn4,rank_diff4) as o_c_div_rd4,(conn_times4/conn_rank4) as co_div_cr4,(conn_times4/rank4) as co_div_r4,
his_occur5,avg_sig5,rank5,diff_s_5,conn_times5,conn_rank5,rank_diff5,occur_conn5,getratio(conn_times5,his_occur5) as conn_ratio5,(his_occur5/rank5) as oc_div_r5,(his_occur5/conn_rank5) as oc_div_cr5,getratio(occur_conn5,rank_diff5) as o_c_div_rd5,(conn_times5/conn_rank5) as co_div_cr5,(conn_times5/rank5) as co_div_r5,
his_occur6,avg_sig6,rank6,diff_s_6,conn_times6,conn_rank6,rank_diff6,occur_conn6,getratio(conn_times6,his_occur6) as conn_ratio6,(his_occur6/rank6) as oc_div_r6,(his_occur6/conn_rank6) as oc_div_cr6,getratio(occur_conn6,rank_diff6) as o_c_div_rd6,(conn_times6/conn_rank6) as co_div_cr6,(conn_times6/rank6) as co_div_r6,
his_occur7,avg_sig7,rank7,diff_s_7,conn_times7,conn_rank7,rank_diff7,occur_conn7,getratio(conn_times7,his_occur7) as conn_ratio7,(his_occur7/rank7) as oc_div_r7,(his_occur7/conn_rank7) as oc_div_cr7,getratio(occur_conn7,rank_diff7) as o_c_div_rd7,(conn_times7/conn_rank7) as co_div_cr7,(conn_times7/rank7) as co_div_r7,
his_occur8,avg_sig8,rank8,diff_s_8,conn_times8,conn_rank8,rank_diff8,occur_conn8,getratio(conn_times8,his_occur8) as conn_ratio8,(his_occur8/rank8) as oc_div_r8,(his_occur8/conn_rank8) as oc_div_cr8,getratio(occur_conn8,rank_diff8) as o_c_div_rd8,(conn_times8/conn_rank8) as co_div_cr8,(conn_times8/rank8) as co_div_r8,
his_occur9,avg_sig9,rank9,diff_s_9,conn_times9,conn_rank9,rank_diff9,occur_conn9,getratio(conn_times9,his_occur9) as conn_ratio9,(his_occur9/rank9) as oc_div_r9,(his_occur9/conn_rank9) as oc_div_cr9,getratio(occur_conn9,rank_diff9) as o_c_div_rd9,(conn_times9/conn_rank9) as co_div_cr9,(conn_times9/rank9) as co_div_r9,
his_occur10,avg_sig10,rank10,diff_s_10,conn_times10,conn_rank10,rank_diff10,occur_conn10,getratio(conn_times10,his_occur10) as conn_ratio10,(his_occur10/rank10) as oc_div_r10,(his_occur10/conn_rank10) as oc_div_cr10,getratio(occur_conn10,rank_diff10) as o_c_div_rd10,(conn_times10/conn_rank10) as co_div_cr10,(conn_times10/rank10) as co_div_r10,
longi_diff*10000 as longi_diff,lati_diff*10000 as lati_diff,sqrt(longi_diff*10000*longi_diff*10000+lati_diff*10000*lati_diff*10000) as sqr_dis,distance,sale_hour
from train_binary_wct1;

drop table if exists test_binary_wcts;
create table if not exists test_binary_wcts as 
select row_id,shop_id,time_stamp,
his_occur1,avg_sig1,rank1,diff_s_1,conn_times1,conn_rank1,rank_diff1,occur_conn1,getratio(conn_times1,his_occur1) as conn_ratio1,(his_occur1/rank1) as oc_div_r1,(his_occur1/conn_rank1) as oc_div_cr1,getratio(occur_conn1,rank_diff1) as o_c_div_rd1,(conn_times1/conn_rank1) as co_div_cr1,(conn_times1/rank1) as co_div_r1,
his_occur2,avg_sig2,rank2,diff_s_2,conn_times2,conn_rank2,rank_diff2,occur_conn2,getratio(conn_times2,his_occur2) as conn_ratio2,(his_occur2/rank2) as oc_div_r2,(his_occur2/conn_rank2) as oc_div_cr2,getratio(occur_conn2,rank_diff2) as o_c_div_rd2,(conn_times2/conn_rank2) as co_div_cr2,(conn_times2/rank2) as co_div_r2,
his_occur3,avg_sig3,rank3,diff_s_3,conn_times3,conn_rank3,rank_diff3,occur_conn3,getratio(conn_times3,his_occur3) as conn_ratio3,(his_occur3/rank3) as oc_div_r3,(his_occur3/conn_rank3) as oc_div_cr3,getratio(occur_conn3,rank_diff3) as o_c_div_rd3,(conn_times3/conn_rank3) as co_div_cr3,(conn_times3/rank3) as co_div_r3,
his_occur4,avg_sig4,rank4,diff_s_4,conn_times4,conn_rank4,rank_diff4,occur_conn4,getratio(conn_times4,his_occur4) as conn_ratio4,(his_occur4/rank4) as oc_div_r4,(his_occur4/conn_rank4) as oc_div_cr4,getratio(occur_conn4,rank_diff4) as o_c_div_rd4,(conn_times4/conn_rank4) as co_div_cr4,(conn_times4/rank4) as co_div_r4,
his_occur5,avg_sig5,rank5,diff_s_5,conn_times5,conn_rank5,rank_diff5,occur_conn5,getratio(conn_times5,his_occur5) as conn_ratio5,(his_occur5/rank5) as oc_div_r5,(his_occur5/conn_rank5) as oc_div_cr5,getratio(occur_conn5,rank_diff5) as o_c_div_rd5,(conn_times5/conn_rank5) as co_div_cr5,(conn_times5/rank5) as co_div_r5,
his_occur6,avg_sig6,rank6,diff_s_6,conn_times6,conn_rank6,rank_diff6,occur_conn6,getratio(conn_times6,his_occur6) as conn_ratio6,(his_occur6/rank6) as oc_div_r6,(his_occur6/conn_rank6) as oc_div_cr6,getratio(occur_conn6,rank_diff6) as o_c_div_rd6,(conn_times6/conn_rank6) as co_div_cr6,(conn_times6/rank6) as co_div_r6,
his_occur7,avg_sig7,rank7,diff_s_7,conn_times7,conn_rank7,rank_diff7,occur_conn7,getratio(conn_times7,his_occur7) as conn_ratio7,(his_occur7/rank7) as oc_div_r7,(his_occur7/conn_rank7) as oc_div_cr7,getratio(occur_conn7,rank_diff7) as o_c_div_rd7,(conn_times7/conn_rank7) as co_div_cr7,(conn_times7/rank7) as co_div_r7,
his_occur8,avg_sig8,rank8,diff_s_8,conn_times8,conn_rank8,rank_diff8,occur_conn8,getratio(conn_times8,his_occur8) as conn_ratio8,(his_occur8/rank8) as oc_div_r8,(his_occur8/conn_rank8) as oc_div_cr8,getratio(occur_conn8,rank_diff8) as o_c_div_rd8,(conn_times8/conn_rank8) as co_div_cr8,(conn_times8/rank8) as co_div_r8,
his_occur9,avg_sig9,rank9,diff_s_9,conn_times9,conn_rank9,rank_diff9,occur_conn9,getratio(conn_times9,his_occur9) as conn_ratio9,(his_occur9/rank9) as oc_div_r9,(his_occur9/conn_rank9) as oc_div_cr9,getratio(occur_conn9,rank_diff9) as o_c_div_rd9,(conn_times9/conn_rank9) as co_div_cr9,(conn_times9/rank9) as co_div_r9,
his_occur10,avg_sig10,rank10,diff_s_10,conn_times10,conn_rank10,rank_diff10,occur_conn10,getratio(conn_times10,his_occur10) as conn_ratio10,(his_occur10/rank10) as oc_div_r10,(his_occur10/conn_rank10) as oc_div_cr10,getratio(occur_conn10,rank_diff10) as o_c_div_rd10,(conn_times10/conn_rank10) as co_div_cr10,(conn_times10/rank10) as co_div_r10,
longi_diff*10000 as longi_diff,lati_diff*10000 as lati_diff,sqrt(longi_diff*10000*longi_diff*10000+lati_diff*10000*lati_diff*10000) as sqr_dis,distance,sale_hour
from test_binary_wct1;

----------------------------------------------------------加入新的特征
create table if not exists train_binary_wcts1 as 
select index_id,shop_id,label,time_stamp,datepart(concat(time_stamp,':00'),'hh') as hour,
his_occur1,conn_times1,avg_sig1,rank1,diff_s_1,conn_rank1,rank_diff1,occur_conn1,oc_div_r1,oc_div_cr1,o_c_div_rd1,co_div_cr1,co_div_r1,
his_occur2,conn_times2,avg_sig2,rank2,diff_s_2,conn_rank2,rank_diff2,occur_conn2,oc_div_r2,oc_div_cr2,o_c_div_rd2,co_div_cr2,co_div_r2,
his_occur3,conn_times3,avg_sig3,rank3,diff_s_3,conn_rank3,rank_diff3,occur_conn3,oc_div_r3,oc_div_cr3,o_c_div_rd3,co_div_cr3,co_div_r3,
his_occur4,conn_times4,avg_sig4,rank4,diff_s_4,conn_rank4,rank_diff4,occur_conn4,oc_div_r4,oc_div_cr4,o_c_div_rd4,co_div_cr4,co_div_r4,
his_occur5,conn_times5,avg_sig5,rank5,diff_s_5,conn_rank5,rank_diff5,occur_conn5,oc_div_r5,oc_div_cr5,o_c_div_rd5,co_div_cr5,co_div_r5,
his_occur6,conn_times6,avg_sig6,rank6,diff_s_6,conn_rank6,rank_diff6,occur_conn6,oc_div_r6,oc_div_cr6,o_c_div_rd6,co_div_cr6,co_div_r6,
his_occur7,conn_times7,avg_sig7,rank7,diff_s_7,conn_rank7,rank_diff7,occur_conn7,oc_div_r7,oc_div_cr7,o_c_div_rd7,co_div_cr7,co_div_r7,
his_occur8,conn_times8,avg_sig8,rank8,diff_s_8,conn_rank8,rank_diff8,occur_conn8,oc_div_r8,oc_div_cr8,o_c_div_rd8,co_div_cr8,co_div_r8,
his_occur9,conn_times9,avg_sig9,rank9,diff_s_9,conn_rank9,rank_diff9,occur_conn9,oc_div_r9,oc_div_cr9,o_c_div_rd9,co_div_cr9,co_div_r9,
his_occur10,conn_times10,avg_sig10,rank10,diff_s_10,conn_rank10,rank_diff10,occur_conn10,oc_div_r10,oc_div_cr10,o_c_div_rd10,co_div_cr10,co_div_r10,
longi_diff,lati_diff,sqr_dis,distance,sale_hour,
(co_div_r1+co_div_r2+co_div_r3+co_div_r4+co_div_r5+co_div_r6+co_div_r7+co_div_r8+co_div_r9+co_div_r10) as score1,
(oc_div_r1+oc_div_r2+oc_div_r3+oc_div_r4+oc_div_r5+oc_div_r6+oc_div_r7+oc_div_r8+oc_div_r9+oc_div_r10) as score2,
(oc_div_cr1+oc_div_cr2+oc_div_cr3+oc_div_cr4+oc_div_cr5+oc_div_cr6+oc_div_cr7+oc_div_cr8+oc_div_cr9+oc_div_cr10) as score3,
(co_div_cr1+co_div_cr2+co_div_cr3+co_div_cr4+co_div_cr5+co_div_cr6+co_div_cr7+co_div_cr8+co_div_cr9+co_div_cr10) as score4
from train_binary_wcts;

create table if not exists test_binary_wcts1 as 
select row_id,shop_id,time_stamp,datepart(concat(time_stamp,':00'),'hh') as hour,
his_occur1,conn_times1,avg_sig1,rank1,diff_s_1,conn_rank1,rank_diff1,occur_conn1,oc_div_r1,oc_div_cr1,o_c_div_rd1,co_div_cr1,co_div_r1,
his_occur2,conn_times2,avg_sig2,rank2,diff_s_2,conn_rank2,rank_diff2,occur_conn2,oc_div_r2,oc_div_cr2,o_c_div_rd2,co_div_cr2,co_div_r2,
his_occur3,conn_times3,avg_sig3,rank3,diff_s_3,conn_rank3,rank_diff3,occur_conn3,oc_div_r3,oc_div_cr3,o_c_div_rd3,co_div_cr3,co_div_r3,
his_occur4,conn_times4,avg_sig4,rank4,diff_s_4,conn_rank4,rank_diff4,occur_conn4,oc_div_r4,oc_div_cr4,o_c_div_rd4,co_div_cr4,co_div_r4,
his_occur5,conn_times5,avg_sig5,rank5,diff_s_5,conn_rank5,rank_diff5,occur_conn5,oc_div_r5,oc_div_cr5,o_c_div_rd5,co_div_cr5,co_div_r5,
his_occur6,conn_times6,avg_sig6,rank6,diff_s_6,conn_rank6,rank_diff6,occur_conn6,oc_div_r6,oc_div_cr6,o_c_div_rd6,co_div_cr6,co_div_r6,
his_occur7,conn_times7,avg_sig7,rank7,diff_s_7,conn_rank7,rank_diff7,occur_conn7,oc_div_r7,oc_div_cr7,o_c_div_rd7,co_div_cr7,co_div_r7,
his_occur8,conn_times8,avg_sig8,rank8,diff_s_8,conn_rank8,rank_diff8,occur_conn8,oc_div_r8,oc_div_cr8,o_c_div_rd8,co_div_cr8,co_div_r8,
his_occur9,conn_times9,avg_sig9,rank9,diff_s_9,conn_rank9,rank_diff9,occur_conn9,oc_div_r9,oc_div_cr9,o_c_div_rd9,co_div_cr9,co_div_r9,
his_occur10,conn_times10,avg_sig10,rank10,diff_s_10,conn_rank10,rank_diff10,occur_conn10,oc_div_r10,oc_div_cr10,o_c_div_rd10,co_div_cr10,co_div_r10,
longi_diff,lati_diff,sqr_dis,distance,sale_hour,
(co_div_r1+co_div_r2+co_div_r3+co_div_r4+co_div_r5+co_div_r6+co_div_r7+co_div_r8+co_div_r9+co_div_r10) as score1,
(oc_div_r1+oc_div_r2+oc_div_r3+oc_div_r4+oc_div_r5+oc_div_r6+oc_div_r7+oc_div_r8+oc_div_r9+oc_div_r10) as score2,
(oc_div_cr1+oc_div_cr2+oc_div_cr3+oc_div_cr4+oc_div_cr5+oc_div_cr6+oc_div_cr7+oc_div_cr8+oc_div_cr9+oc_div_cr10) as score3,
(co_div_cr1+co_div_cr2+co_div_cr3+co_div_cr4+co_div_cr5+co_div_cr6+co_div_cr7+co_div_cr8+co_div_cr9+co_div_cr10) as score4
from test_binary_wcts;

select * from train_binary_wcts1;

create table if not exists train_binary_af1 as 
select a.*, hour_occur/24 as hour_occur,hour_conn/24 as hour_conn from train_binary_wcts1 a
left join shop_his_hour_wifi_oc_train c on a.shop_id=c.shop_id and a.hour=c.hour;

create table if not exists test_binary_af1 as
select a.*,hour_occur/31 as hour_occur,hour_conn/31 as hour_conn from test_binary_wcts1 a 
left join shop_his_hour_wifi_oc_test c on a.shop_id=c.shop_id and a.hour=c.hour;
--再用pai平台进行缺失值填充，填0，hour_conn,hour_occur
