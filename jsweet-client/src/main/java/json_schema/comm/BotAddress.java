package json_schema.comm;

public class BotAddress extends def.js.Object {

	public void setHostName(String hostname) {
		$set("host", hostname);
	}

	public void setPort(String port) {
		$set("port", port);
	}
}