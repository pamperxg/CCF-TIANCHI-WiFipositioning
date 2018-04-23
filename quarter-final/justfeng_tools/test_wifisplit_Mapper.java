package justfeng.wifitools;

import java.io.IOException;
import java.util.Comparator;
import java.util.TreeSet;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

public class test_wifisplit_Mapper extends MapperBase {

	@Override
	public void setup(TaskContext context) throws IOException {
	}

	@Override
	public void map(long recordNum, Record record, TaskContext context)
			throws IOException {
		String row_id = (String) record.get("row_id");
		String user_id = (String) record.get("user_id");
		String mall_id = (String) record.get("mall_id");		
		String time_stamp = (String) record.get("time_stamp");
		double longitude = record.getDouble("longitude");
		double latitude = record.getDouble("latitude");
		String wifi_infos = (String) record.get("wifi_infos");
		String[] wifi_infos_spilt = wifi_infos.split(";");
		TreeSet<wifidata> wifi_set = new TreeSet<wifidata>(
				new Comparator<wifidata>() {
					public int compare(wifidata w1, wifidata w2) {
						int num = w2.getSignal() - w1.getSignal();
						return num == 0 ? 1 : num;
					}
				});
		// atleast exsist one wifi info
		String[] wifi_dat = wifi_infos_spilt[0].split("\\|");
		wifi_set.add(new wifidata(wifi_dat[0], wifi_dat[1], wifi_dat[2]));
		// delete same wifi info
		for (int i = 1; i < wifi_infos_spilt.length; i++) {
			if (!wifi_infos_spilt[i].equals(wifi_infos_spilt[i - 1])) {
				wifi_dat = wifi_infos_spilt[i].split("\\|");
				wifi_set.add(new wifidata(wifi_dat[0], wifi_dat[1], wifi_dat[2]));
			}
		}

		Record result_record = context.createOutputRecord();
		result_record.set("row_id", row_id);
		result_record.set("user_id", user_id);
		result_record.set("mall_id", mall_id);		
		result_record.set("time_stamp", time_stamp);
		result_record.set("longitude", longitude);
		result_record.set("latitude", latitude);
		int cnt = 1;
		for (wifidata w : wifi_set) {
			result_record.set("w_bssid" + cnt, w.getBssid());
			if (w.getSignal() != wifidata.SIG_NULL)
				result_record.set("w_signal" + cnt, w.getSignal());
			result_record.set("w_flag" + cnt, w.getFlag().toString());
			cnt++;
		}
		context.write(result_record);
	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
	}

}
