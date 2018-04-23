package justfeng.wifitools;

import java.io.IOException;
import java.util.Comparator;
import java.util.TreeSet;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

public class wifi_expand_Mapper extends MapperBase {

	@Override
	public void setup(TaskContext context) throws IOException {
	}

	@Override
	public void map(long recordNum, Record record, TaskContext context)
			throws IOException {
		TreeSet<wifidata> wifi_set = new TreeSet<wifidata>(
				new Comparator<wifidata>() {
					public int compare(wifidata w1, wifidata w2) {
						// TODO Auto-generated method stub
						int num = w2.getSignal() - w1.getSignal();
						return num == 0 ? 1 : num;
					}
				});
		String user_id = (String) record.get("user_id");
		String shop_id = (String) record.get("shop_id");
		String time_stamp = (String) record.get("time_stamp");
		double longitude = record.getDouble("longitude");
		double latitude = record.getDouble("latitude");
		long day = record.getBigint("day");
		String category_id = (String) record.get("category_id");
		double shop_longitude = record.getDouble("shop_longitude");
		double shop_latitude = record.getDouble("shop_latitude");
		long price = record.getBigint("price");
		String mall_id = (String) record.get("mall_id");
		long index_id = record.getBigint("index_id");
		int cnt = 0;
		for (int i = 0; i < 10; i++) {
			cnt++;
			if (!record.isNull("w_bssid" + cnt)
					&& !record.getString("w_bssid" + cnt).equals("null"))// bssid不存在就不添加了
			{
				String bssid = (String) record.get("w_bssid" + cnt);
				String sig = record.isNull(i * 3 + 6) ? "null" : record
						.getBigint("w_signal" + cnt).toString();
				String flag = (String) record.get("w_flag" + cnt);
				wifi_set.add(new wifidata(bssid, sig, flag));
			}
		}
		//for (wifidata w : wifi_set)
			//System.out.println(w);
		Record r = context.createOutputRecord();
		r.set("index_id", index_id);
		r.set("user_id", user_id);
		r.set("shop_id", shop_id);
		r.set("time_stamp", time_stamp);
		r.set("longitude", longitude);
		r.set("latitude", latitude);
		r.set("day", day);
		r.set("category_id", category_id);
		r.set("shop_longitude", shop_longitude);
		r.set("shop_latitude", shop_latitude);
		r.set("price", price);
		r.set("mall_id", mall_id);
		if (wifi_set.isEmpty())
			context.write(r);
		else
			for (wifidata w : wifi_set) {
				r.set("w_bssid", w.getBssid());
				if (w.getSignal() != wifidata.SIG_NULL)
					r.set("w_signal", w.getSignal());
				r.set("w_flag", w.getFlag().toString());
				context.write(r);
			}

	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
	}

}
