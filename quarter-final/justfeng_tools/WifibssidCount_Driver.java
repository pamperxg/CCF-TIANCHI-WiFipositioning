package com.justfeng.bssidcnt;

import com.aliyun.odps.OdpsException;
import com.aliyun.odps.data.TableInfo;
import com.aliyun.odps.mapred.JobClient;
import com.aliyun.odps.mapred.RunningJob;
import com.aliyun.odps.mapred.conf.JobConf;
import com.aliyun.odps.mapred.utils.InputUtils;
import com.aliyun.odps.mapred.utils.OutputUtils;
import com.aliyun.odps.mapred.utils.SchemaUtils;

public class WifibssidCount_Driver {

	public static void main(String[] args) throws OdpsException {
		JobConf job = new JobConf();

		// TODO: specify map output types
		job.setMapOutputKeySchema(SchemaUtils.fromString("w_bssid:string"));
		job.setMapOutputValueSchema(SchemaUtils.fromString("w_count:bigint"));

		// TODO: specify input and output tables
		 InputUtils.addTable(
		 TableInfo
		 .builder()
		 .tableName("FENG_TEST_MR")
		 .cols(new String[] { "user_id", "shop_id",
		 "time_stamp", "longitude","latitude", "wifi_infos" })
		 .build(), job);
		OutputUtils.addTable(TableInfo.builder().tableName("wbssid_count_out").build(),
				job);

		job.setMapperClass(com.justfeng.bssidcnt.WifibssidCount_Mapper.class);
		job.setReducerClass(com.justfeng.bssidcnt.WifibssidCount_Reducer.class);

		RunningJob rj = JobClient.runJob(job);
		rj.waitForCompletion();
	}

}
