def handleTimerEvent():
	target_address = "10.0.9.92"
	address = system.net.getIpAddress()
	client = system.net.httpClient()
	body = {"address":address}
	url = "http://"+ target_address + ":8088/system/eventstream/Training/observe"
	client.post(url = url, data = body)