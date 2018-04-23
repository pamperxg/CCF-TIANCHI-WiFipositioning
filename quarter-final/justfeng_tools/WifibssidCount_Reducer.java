package com.justfeng.bssidcnt;

import java.io.IOException;
import java.util.Iterator;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

public class WifibssidCount_Reducer extends ReducerBase {

	@Override
	public void setup(TaskContext context) throws IOException {
	}

	@Override
	public void reduce(Record key, Iterator<Record> values, TaskContext context)
			throws IOException {
		long count=0;
		while (values.hasNext()) {
			Record r=values.next();
			// TODO process value
			count+=(Long)r.get(0);
		}
		Record result_record =context.createOutputRecord();
		result_record.set("w_bssid",key.get(0));
		result_record.set("w_count",count);
		context.write(result_record);
	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
	}

}
