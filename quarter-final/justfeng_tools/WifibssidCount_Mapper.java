package com.justfeng.bssidcnt;

import java.io.IOException;
import java.util.Comparator;
import java.util.TreeSet;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

public class WifibssidCount_Mapper extends MapperBase {

	@Override
	public void setup(TaskContext context) throws IOException {
	}

	@Override
	public void map(long recordNum, Record record, TaskContext context)
			throws IOException {
		String wifi_infos = (String) record.get(5);

		Record bssid = context.createMapOutputKeyRecord();
		Record one = context.createMapOutputValueRecord();

		String[] wifi_infos_spilt = wifi_infos.split(";");
		// atleast exsist one wifi info
		String[] wifi_dat = wifi_infos_spilt[0].split("\\|");
		
		String key_bssid = wifi_dat[0];
		
		bssid.set(new Object[] { key_bssid });
		one.set(new Object[] { 1L });
		context.write(bssid, one);
		
		// delete same wifi info
		for (int i = 1; i < wifi_infos_spilt.length; i++) {
			if (!wifi_infos_spilt[i].equals(wifi_infos_spilt[i - 1])) {
				wifi_dat = wifi_infos_spilt[i].split("\\|");

				key_bssid = wifi_dat[0];

				bssid.set(new Object[] { key_bssid });
				one.set(new Object[] { 1L });
				
				context.write(bssid, one);
			}
		}
	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
	}

}
