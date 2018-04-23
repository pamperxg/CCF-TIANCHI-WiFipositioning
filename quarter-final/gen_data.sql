--justfeng_binary_all_dataset_full train展开表
--justfeng_binary_all_train_data_full  train表
--justfeng_binary_all_test_data_full test表
--19344308
--19316676
------------------构造训练集候选--------------------------

--将题目所给的train表数据集分为候选集合和训练集合，候选集合：train1除了八月后两周，训练集合：train2八月后两周
drop table if exists train1;
create table  if not exists train1 as
select * from (select *,datepart(concat(time_stamp,':00'),'mm') as month from justfeng_binary_all_train_data_full) a
where a.month=7 or (a.month=8 and a.day<18);
drop table if exists train2;
create table  if not exists train2 as
select * from (select *,datepart(concat(time_stamp,':00'),'mm') as month from justfeng_binary_all_train_data_full) a
where a.month=8 and a.day>=18;
--按wifi1匹配取出候选集合shop_id
drop table if exists s1_all;
create table s1_all as 
with t1 as (select * from justfeng_binary_all_dataset_full where index_id in (select index_id from train1)),--train1展开的表
t2 as (select * from t1 where w_bssid in (select w_bssid1 from train2))
select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t2 group by w_bssid,shop_id,w_signal ;
--按wifi2匹配取出候选集合shop_id
drop table if exists s2_all;
create table s2_all as 
with t1 as (select * from justfeng_binary_all_dataset_full where index_id in (select index_id from train1)),
t2 as (select * from t1 where w_bssid in (select w_bssid2 from train2))
select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t2 group by w_bssid,shop_id,w_signal;
--按wifi3匹配选出候选集合的shop_id
drop table if exists s3_all;
create table s3_all as 
with t1 as (select * from justfeng_binary_all_dataset_full where index_id in (select index_id from train1)),
t2 as (select * from t1 where w_bssid in (select w_bssid3 from train2))
select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t2 group by w_bssid,shop_id,w_signal;
--按wifi1构造候选,并降低正负样本比,训练集
drop table if exists tmp_shop_candidate1_all;
create table if not exists tmp_shop_candidate1_all as
select a.index_id,a.shop_id as shop_label,b.shop_id as shop_id,case when a.shop_id =b.shop_id then 1 else 0 end as label from train2 a
left join (select * from s1_all where num=1 and w_signal>-70) b on a.w_bssid1 =b.w_bssid;
select count(*) from tmp_shop_candidate1_all where label=1;--2509817
select count(distinct index_id) from tmp_shop_candidate1_all; --2799866
select count(*) from tmp_shop_candidate1_all;--17516544
--覆盖率：89.6,1:7
--按wifi2构造候选,训练集
drop table if exists tmp_shop_candidate2_all;
create table if not exists tmp_shop_candidate2_all as
select a.index_id,a.shop_id as shop_label,b.shop_id as shop_id,case when a.shop_id=b.shop_id then 1 else 0 end as label from train2 a 
left join (select * from s2_all where num=1 and w_signal>-60) b on a.w_bssid2 =b.w_bssid;
select count(*) from tmp_shop_candidate2_all where label=1;--1477048
select count(distinct index_id) from tmp_shop_candidate2_all; --2799866
select count(*) from tmp_shop_candidate2_all;--8507956
--覆盖率：52.7,1:5.78
--按wifi3构造候选，训练集
drop table if exists tmp_shop_candidate3_all;
create table if not exists tmp_shop_candidate3_all as
select a.index_id,a.shop_id as shop_label,b.shop_id as shop_id,case when a.shop_id=b.shop_id then 1 else 0 end as label from train2 a 
left join (select * from s3_all where num=1 and w_signal>-50) b on a.w_bssid3 =b.w_bssid;
select count(*) from tmp_shop_candidate3_all where label=1;--978806
select count(distinct index_id) from tmp_shop_candidate3_all; --2799866
select count(*) from tmp_shop_candidate3_all;--5007835
--覆盖率：35,1:5.1
--将wifi1、wifi2、wifi3构造的候选合并，得到训练集
drop table if exists train_candidate123;
create table if not exists train_candidate123 as
select index_id,shop_id,label from tmp_shop_candidate1_all 
union 
select index_id,shop_id,label from tmp_shop_candidate2_all
union
select index_id,shop_id,label from tmp_shop_candidate3_all;
select count(*) from train_candidate123 where label=1;--2570897
select count(distinct index_id) from train_candidate123; --2799866
select count(*) from train_candidate123;--20837995
--覆盖率：91.8,1:8
----构造的数据集中有null但有不仅仅一个null的去掉
drop table if exists train_candidate;
create table if not exists train_candidate as
select index_id,shop_id,label from
(select index_id,shop_id,label,row_number() over(partition by index_id order by shop_id desc) num from train_candidate123) a
where a.shop_id is not null or a.num = 1;
select count(*) from train_candidate where label=1;--2570897
select count(*) from train_candidate;--19344308
--1:7.5
-----------------------构造测试集候选--------------------------
--用整个train集中的数据构造test的候选集
--justfeng_binary_all_dataset_full
--justfeng_binary_all_test_data_full
drop table if exists test_candidate;
create table if not exists test_candidate as 
with t1 as (select * from justfeng_binary_all_dataset_full where w_bssid in (select w_bssid1 from justfeng_binary_all_test_data_full)),
t2 as (select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t1 group by w_bssid,shop_id,w_signal),
t3 as (select * from justfeng_binary_all_dataset_full where w_bssid in (select w_bssid2 from justfeng_binary_all_test_data_full)),
t4 as (select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t3 group by w_bssid,shop_id,w_signal),
t5 as (select * from justfeng_binary_all_dataset_full where w_bssid in (select w_bssid3 from justfeng_binary_all_test_data_full)),
t6 as (select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t5 group by w_bssid,shop_id,w_signal)
select row_id,shop_id from justfeng_binary_all_test_data_full a
left join 
(select * from t2 where num=1 and w_signal>-70) b on a.w_bssid1=b.w_bssid
union 
select row_id,shop_id from justfeng_binary_all_test_data_full a
left join 
(select * from t4 where num=1 and w_signal>-60) b on a.w_bssid2=b.w_bssid
union
select row_id,shop_id from justfeng_binary_all_test_data_full a
left join 
(select * from t6 where num=1 and w_signal>-50) b on a.w_bssid3=b.w_bssid;
-------选出来的候选集有重复，不知道为啥


--按照构造训练集候选的步骤
--按wifi1匹配取出候选集合shop_id
drop table if exists st1_all;
create table st1_all as 
with t1 as (select * from justfeng_binary_all_dataset_full where w_bssid in (select w_bssid1 from justfeng_binary_all_test_data_full))
select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t1 group by w_bssid,shop_id,w_signal ;
--按wifi2匹配取出候选集合shop_id
drop table if exists st2_all;
create table st2_all as 
with t1 as (select * from justfeng_binary_all_dataset_full where w_bssid in (select w_bssid2 from justfeng_binary_all_test_data_full))
select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t1 group by w_bssid,shop_id,w_signal;
--按wifi3匹配选出候选集合的shop_id
drop table if exists st3_all;
create table st3_all as 
with t1 as (select * from justfeng_binary_all_dataset_full where w_bssid in (select w_bssid3 from justfeng_binary_all_test_data_full))
select w_bssid,shop_id,w_signal,row_number() over (partition by w_bssid,shop_id order by w_signal desc) num from t1 group by w_bssid,shop_id,w_signal;
--按wifi1构造候选,并降低正负样本比,训练集
drop table if exists tmp_shop_candidatet1_all;
create table if not exists tmp_shop_candidatet1_all as
select a.row_id,b.shop_id from justfeng_binary_all_test_data_full a
left join (select * from st1_all where num=1 and w_signal>-70) b on a.w_bssid1 =b.w_bssid;

--按wifi2构造候选,训练集
drop table if exists tmp_shop_candidatet2_all;
create table if not exists tmp_shop_candidatet2_all as
select a.row_id,b.shop_id from justfeng_binary_all_test_data_full a
left join (select * from st2_all where num=1 and w_signal>-60) b on a.w_bssid2 =b.w_bssid;
--按wifi3构造候选，训练集
drop table if exists tmp_shop_candidatet3_all;
create table if not exists tmp_shop_candidatet3_all as
select a.row_id,b.shop_id from justfeng_binary_all_test_data_full a
left join (select * from st3_all where num=1 and w_signal>-50) b on a.w_bssid3 =b.w_bssid;
--将wifi1、wifi2、wifi3构造的候选合并，得到训练集
drop table if exists test_candidate;
create table if not exists test_candidate as
select row_id,shop_id from tmp_shop_candidatet1_all 
union 
select row_id,shop_id from tmp_shop_candidatet2_all
union
select row_id,shop_id from tmp_shop_candidatet3_all;

-----去掉部分为null的记录
drop table if exists test_candidate1;
create table if not exists test_candidate1 as
select row_id,shop_id from
(select row_id,shop_id,row_number() over(partition by row_id order by shop_id desc) num from test_candidate ) a
where a.shop_id is not null or a.num = 1;
select count(*) from test_candidate ;--30775231,30868967,20551497
select count(*) from test_candidate1 ;--28329960，28605291,19316676
/* select count(*) from test_candidate; */
select * from test_candidate1 ;-------------19316676

-----------------------------得到训练集和测试集-------------------------------fe中有重写
--训练集,大约有0.5%为空
drop table if exists train_binary;
create table if not exists train_binary as
with t1 as (select * from train_candidate a
left join 
(select longitude,latitude,w_bssid1,w_bssid2,w_bssid3,w_signal1,w_signal2,w_signal3,index_id as index_id_s,mall_id from train2) b 
on a.index_id =b.index_id_s)
select index_id,mall_id,longitude,latitude,w_bssid1,w_bssid2,w_bssid3,w_signal1,w_signal2,w_signal3,mall_id,category_id,price,longitude_s,latitude_s,shop_id,label
from t1 c
left join (select category_id,price,longitude as longitude_s,latitude as latitude_s,shop_id as shop_id_s  from ant_tianchi_ccf_sl_shop_info) d on c.shop_id=d.shop_id_s;
/* --去掉部分为null的
drop table if exists train_binary_guo;
create table if not exists train_binary_guo as
select index_id,shop_id,label from
(select index_id,shop_id,label,row_number() over(partition by index_id order by shop_id desc) num from train_binary) a
where a.shop_id is not null or a.num = 1;
select count(*) from train_binary_guo where label=1;--2570897
select count(distinct index_id) from train_binary_guo;  
select count(*) from train_binary_guo;--19344308 */


--测试集,测试集中有0.2%shop_id为空
drop table if exists test_binary;
create table if not exists test_binary as
with t1 as (select * from test_candidate1  a 
left join 
(select row_id as row_id_s,mall_id,longitude,latitude,w_bssid1,w_bssid2,w_bssid3,w_signal1,w_signal2,w_signal3 from justfeng_binary_all_test_data_full) b 
on a.row_id = b.row_id_s)
select row_id,mall_id,longitude,latitude,w_bssid1,w_bssid2,w_bssid3,w_signal1,w_signal2,w_signal3,mall_id,category_id,price,longitude_s,latitude_s,shop_id
from t1 c left join 
(select category_id,price,longitude as longitude_s,latitude as latitude_s,shop_id as shop_id_s from ant_tianchi_ccf_sl_shop_info ) d on c.shop_id=d.shop_id_s;
/* --去掉部分为null的
drop table if exists test_binary_guo;
create table if not exists test_binary_guo as
select row_id,shop_id from
(select row_id,shop_id,row_number() over(partition by row_id order by shop_id desc) num from test_binary ) a
where a.shop_id is not null or a.num = 1;
select count(*) from test_binary_guo ;--30775231
select count(*) from test_binary ; */
select count(*) from train_binary ;--19344308
select count(*) from test_binary ;--19316676
select count(*) from train_candidate ;--19344308
select count(*) from test_candidate1 ;--19316676
select count(*) from train_binary_guo where shop_id is null;--104606
select count(*) from test_binary_guo where shop_id is null;--69285
