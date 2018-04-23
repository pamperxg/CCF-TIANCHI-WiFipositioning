--按latitude，longitude join产生结果（0.1442，0.1524）
prj_tc_231620_98573_kwpt3x.ant_tianchi_ccf_sl_predict_lati 
prj_tc_231620_98573_kwpt3x.ant_tianchi_ccf_sl_predict_logi 

--经纬度答案，lati填入logi（）
create table logilati as 
select * from ant_tianchi_ccf_sl_predict_logi a where a.shop_id is not null
union all 
select * from ant_tianchi_ccf_sl_predict_lati b where row_id in (select row_id from ant_tianchi_ccf_sl_predict_logi where shop_id is null);

--按wifi1join，产生结果(0.4197)
create table if not exists  tmp1 as 
select row_id,shop_id from (select row_id,w_bssid1 from justfeng_train_set where row_id is not null)t1 
left join (select shop_id,w_bssid1 as w_bssid1_ from justfeng_train_set where row_id is null) t2 on t1.w_bssid1=t2.w_bssid1_;
select * from tmp1;
drop table if exists ant_tianchi_ccf_sl_predict;
create table if not exists ant_tianchi_ccf_sl_predict as 
select row_id,shop_id from(
	select *,row_number() over (partition by row_id order by shop_id)num from tmp1 
)t where t.num=1;
drop table if exists tmp1;--


--构建wifi1+wifi2的列
drop table if exists train_wifi_12;
create table if not exists train_wifi_12 as
select shop_id,row_id,w_bssid1,w_bssid2,concat(w_bssid1,w_bssid2) as wifi12 from justfeng_train_set ;

select * from train_wifi_12 ;
drop table if exists train_wifi_12;

--按wifi12merge
drop table if exists tmp1;
create table if not exists  tmp1 as 
select row_id,shop_id from (select row_id,wifi12 from train_wifi_12  where row_id is not null)t1 
left join (select shop_id,wifi12 as wifi12_ from train_wifi_12  where row_id is null) t2 on t1.wifi12=t2.wifi12_;
/* select * from tmp1;
drop table if exists tmp1; */

drop table if exists tmp_wifi12_merge;
create table if not exists tmp_wifi12_merge as 
select row_id,shop_id from(
	select *,row_number() over (partition by row_id order by shop_id)num from tmp1 
)t where t.num=1;

--融合按wifi1merge和按wifi12merge的结果（0.5653）
drop table if exists ant_tianchi_ccf_sl_predict;
create table if not exists ant_tianchi_ccf_sl_predict as  
select * from tmp_wifi12_merge a where a.shop_id is not null
union all
select * from ant_tianchi_ccf_sl_predict_wifi1 where row_id in (select row_id from tmp_wifi12_merge where shop_id is null) ;


--wifi12，latilogi填入wifi12
create table  ant_tianchi_ccf_sl_predict_wifi12logilati as 
select * from ant_tianchi_ccf_sl_predict_wifi12 a where a.shop_id is not null
union all
select * from logilati where row_id in (select row_id from ant_tianchi_ccf_sl_predict_wifi12 where shop_id is null);

--构建wifi123列
drop table if exists train_wifi_123;
create table if not exists train_wifi_123 as
select shop_id,row_id,w_bssid1,w_bssid2,concat(w_bssid1,w_bssid2,w_bssid3) as wifi123 from justfeng_train_set ;
--得到按wifi123merge之后的表
drop table if exists tmp2;
create table if not exists  tmp2 as 
select row_id,shop_id from (select row_id,wifi123 from train_wifi_123  where row_id is not null)t1 
left join (select shop_id,wifi123 as wifi123_ from train_wifi_123  where row_id is null) t2 on t1.wifi123=t2.wifi123_;
drop table if exists tmp_wifi123_merge;
create table if not exists tmp_wifi123_merge as 
select row_id,shop_id from(
	select *,row_number() over (partition by row_id order by shop_id)num from tmp1 
)t where t.num=1;
drop table if exists ant_tianchi_ccf_sl_predict_wifi123;
--空值填入wifi12logilati结合的结果（0.5709）
create table if not exists ant_tianchi_ccf_sl_predict_wifi123 as  
select * from tmp_wifi123_merge a where a.shop_id is not null
union all
select * from ant_tianchi_ccf_sl_predict_wifi12 where row_id in (select row_id from tmp_wifi123_merge where shop_id is null) ;
create table  ant_tianchi_ccf_sl_predict_wifi123logilati as 
select * from ant_tianchi_ccf_sl_predict_wifi123 a where a.shop_id is not null
union all
select * from ant_tianchi_ccf_sl_predict_wifi12logilati where row_id in (select row_id from ant_tianchi_ccf_sl_predict_wifi123 where shop_id is null);


--提交答案
drop table if exists ant_tianchi_ccf_sl_predict ;
alter table ant_tianchi_ccf_sl_predict_wifi123logilati rename to ant_tianchi_ccf_sl_predict;

alter table ant_tianchi_ccf_sl_predict1 rename to ant_tianchi_ccf_sl_predict_rule;


--对于模型预测出来的文件,生成结果文件
alter table ant_tianchi_ccf_sl_predict rename to ant_tianchi_ccf_sl_predict8110;

drop table if exists ant_tianchi_ccf_sl_predict;
create table if not exists  ant_tianchi_ccf_sl_predict as 
with t1 as (select row_id,shop_id,prediction_score from g_xgb_pred_3 where row_id not in (select row_id from g_xgb_pred_3 where prediction_result=1)),
t2 as (select row_id,shop_id,row_number() over(partition by row_id order by prediction_score) num from t1),
t3 as (select row_id,shop_id,prediction_score from g_xgb_pred_3 where prediction_result = 1),
t4 as (select row_id,shop_id,row_number() over(partition by row_id order by prediction_score desc)num from t3)
select row_id,shop_id from t2 where num=1
union all
select row_id,shop_id from t4 where num=1;

--------------------------------------------------------XGBOOST------------------------------------------------------------------------
drop table if exists g_xgb_pred_3;
DROP OFFLINEMODEL IF EXISTS g_xgboost_5;

-- train
PAI -name xgboost -project algo_public
-Deta="0.03"
-Dobjective="binary:logistic"
-DitemDelimiter=","
-Dseed="2017"
-Dnum_round="1000"
-DlabelColName="label"
-DinputTableName="train_binary_af"
-DenableSparse="false"
-Dmax_depth="9"
-Dsubsample="0.7"
-Dcolsample_bytree="0.7"
-DmodelName="g_xgboost_5"
-Dgamma="10"
-Dlambda="20" 
-DfeatureColNames="co_div_r1,oc_div_r1,avg_sig1,oc_div_cr1,conn_times1,co_div_cr1,score1,rank1,his_occur1,score4,score3,conn_rank1,occur_conn1,score2,diff_s_1,oc_div_r2,oc_div_cr2,his_occur2,rank2,occur_conn2,oc_div_r3,co_div_r2,rank_diff1,his_occur3,avg_sig2,diff_s_2,occur_conn3,oc_div_cr3,conn_times2,his_occur4,co_div_cr2,oc_div_r4,occur_conn4,rank3,oc_div_cr4,his_occur5,occur_conn5,diff_s_3,o_c_div_rd1,rank4,oc_div_r5,conn_rank2,occur_conn6,his_occur6,diff_s_4,oc_div_cr5,co_div_r3,rank5,oc_div_r6,conn_times3,o_c_div_rd2,o_c_div_rd3,co_div_cr3,diff_s_5,occur_conn7,o_c_div_rd4,his_occur7,oc_div_cr6,rank6,diff_s_6,oc_div_r7,o_c_div_rd5,co_div_r4,occur_conn8,diff_s_7,avg_sig3,oc_div_cr7,his_occur8,rank7,conn_rank3,oc_div_r8,diff_s_8,co_div_cr4,o_c_div_rd6,conn_times4,rank8,diff_s_9,oc_div_cr8,occur_conn9,his_occur9,oc_div_r9,rank9,diff_s_10,co_div_r5,o_c_div_rd7,conn_rank4,oc_div_cr9,co_div_cr5,avg_sig4,rank10,conn_times5,oc_div_r10,sqr_dis,rank_diff2,distance,occur_conn10,his_occur10,oc_div_cr10,o_c_div_rd8,co_div_r6,conn_rank5,hour_conn,rank_diff3,co_div_cr6,sale_hour,rank_diff4,avg_sig10,conn_times6,hour_occur,avg_sig5,rank_diff5,conn_rank6,co_div_r7,o_c_div_rd9,avg_sig9,rank_diff6,co_div_cr7,avg_sig6,avg_sig7,avg_sig8,lati_diff,longi_diff,rank_diff7,rank_diff8,conn_rank7,rank_diff9,rank_diff10,co_div_r8,conn_times7,co_div_cr8,conn_rank8,o_c_div_rd10,conn_rank9,co_div_r9,conn_rank10,co_div_cr9,conn_times8,co_div_r10,co_div_cr10,conn_times9,conn_times10"
-Dmin_child_weight="2";
--Dscale_pos_weight="6"
--DkvDelimiter=":"
--Dbase_score="0.11"

-- predict
PAI -name prediction -project algo_public
-DdetailColName="prediction_detail"
-DappendColNames="row_id,shop_id"
-DmodelName="g_xgboost_5"
-DitemDelimiter=","
-DresultColName="prediction_result"
-Dlifecycle="28"
-DoutputTableName="g_xgb_pred_5"
-DscoreColName="prediction_score"
-DkvDelimiter=":"
-DfeatureColNames="co_div_r1,oc_div_r1,avg_sig1,oc_div_cr1,conn_times1,co_div_cr1,score1,rank1,his_occur1,score4,score3,conn_rank1,occur_conn1,score2,diff_s_1,oc_div_r2,oc_div_cr2,his_occur2,rank2,occur_conn2,oc_div_r3,co_div_r2,rank_diff1,his_occur3,avg_sig2,diff_s_2,occur_conn3,oc_div_cr3,conn_times2,his_occur4,co_div_cr2,oc_div_r4,occur_conn4,rank3,oc_div_cr4,his_occur5,occur_conn5,diff_s_3,o_c_div_rd1,rank4,oc_div_r5,conn_rank2,occur_conn6,his_occur6,diff_s_4,oc_div_cr5,co_div_r3,rank5,oc_div_r6,conn_times3,o_c_div_rd2,o_c_div_rd3,co_div_cr3,diff_s_5,occur_conn7,o_c_div_rd4,his_occur7,oc_div_cr6,rank6,diff_s_6,oc_div_r7,o_c_div_rd5,co_div_r4,occur_conn8,diff_s_7,avg_sig3,oc_div_cr7,his_occur8,rank7,conn_rank3,oc_div_r8,diff_s_8,co_div_cr4,o_c_div_rd6,conn_times4,rank8,diff_s_9,oc_div_cr8,occur_conn9,his_occur9,oc_div_r9,rank9,diff_s_10,co_div_r5,o_c_div_rd7,conn_rank4,oc_div_cr9,co_div_cr5,avg_sig4,rank10,conn_times5,oc_div_r10,sqr_dis,rank_diff2,distance,occur_conn10,his_occur10,oc_div_cr10,o_c_div_rd8,co_div_r6,conn_rank5,hour_conn,rank_diff3,co_div_cr6,sale_hour,rank_diff4,avg_sig10,conn_times6,hour_occur,avg_sig5,rank_diff5,conn_rank6,co_div_r7,o_c_div_rd9,avg_sig9,rank_diff6,co_div_cr7,avg_sig6,avg_sig7,avg_sig8,lati_diff,longi_diff,rank_diff7,rank_diff8,conn_rank7,rank_diff9,rank_diff10,co_div_r8,conn_times7,co_div_cr8,conn_rank8,o_c_div_rd10,conn_rank9,co_div_r9,conn_rank10,co_div_cr9,conn_times8,co_div_r10,co_div_cr10,conn_times9,conn_times10"
-DinputTableName="test_binary_af"
-DenableSparse="false";

---生成提交结果 0.81+
alter table ant_tianchi_ccf_sl_predict rename to ant_tianchi_ccf_sl_predict_zuo;
drop table if exists ant_tianchi_ccf_sl_predict;
create table if not exists  ant_tianchi_ccf_sl_predict as 
with t1 as (select row_id,shop_id,prediction_score from g_xgb_pred_3 where row_id not in (select row_id from g_xgb_pred_3 where prediction_result=1)),
t2 as (select row_id,shop_id,row_number() over(partition by row_id order by prediction_score) num from t1),
t3 as (select row_id,shop_id,prediction_score from g_xgb_pred_3 where prediction_result = 1),
t4 as (select row_id,shop_id,row_number() over(partition by row_id order by prediction_score desc)num from t3)
select row_id,shop_id from t2 where num=1
union all
select row_id,shop_id from t4 where num=1;

--case when prediction_result=0 then 1.0-prediction_score else prediction_score end as probability from wepon_xgb_pred;

select count(*) from g_xgb_pred_3 where prediction_result=1;
select count(distinct row_id) from g_xgb_pred_3;
