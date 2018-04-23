package justfeng.wifitools;

public class wifidata {
	static int SIG_NULL = -999;
	String bssid;
	int signal;
	Boolean flag;

	public wifidata(String bssid, String signal, String flag) {
		super();
		this.bssid = bssid;
		if (signal.equals("null"))
			this.signal = -999;
		else
			this.signal = Integer.parseInt(signal);

		this.flag = Boolean.parseBoolean(flag);
	}

	public wifidata(String bssid, int signal, Boolean flag) {
		super();
		this.bssid = bssid;
		this.signal = signal;
		this.flag = flag;
	}

	public String getBssid() {
		return bssid;
	}

	public void setBssid(String bssid) {
		this.bssid = bssid;
	}

	public int getSignal() {
		return signal;
	}

	public void setSignal(int signal) {
		this.signal = signal;
	}

	public Boolean getFlag() {
		return flag;
	}

	public void setFlag(Boolean flag) {
		this.flag = flag;
	}

	@Override
	public String toString() {
		return "wifidata [bssid=" + bssid + ", signal=" + signal + ", flag="
				+ flag + "]";
	}
}