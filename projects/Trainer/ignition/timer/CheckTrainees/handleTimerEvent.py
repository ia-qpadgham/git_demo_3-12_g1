def handleTimerEvent():
	gateways = system.tag.readBlocking(["[default]TraineeGateways"])[0].value
	trainee_data = {}
	trainee_list = []
	for address, timestamp in gateways.items():
		last_check = system.date.parse(timestamp, "MMM dd, yyyy, hh:mm:ss aa")
		seconds = system.date.secondsBetween(last_check, system.date.now())
		
		if seconds < 15:
			trainee_list.append(address)
	
	sys_props_endpoint = "/data/api/v1/resources/singleton/ignition/system-properties"
	historian_endpoint = "/data/api/v1/resources/find/com.inductiveautomation.historian/historian-provider/CoreHistorian"
	device_endpoint = "/data/api/v1/resources/find/com.inductiveautomation.opcua/device/Simulator"
	
	client = system.net.httpClient(timeout=3000)
	header = {"X-Ignition-API-Token":"reportKey:q-U4pEIfW4jL9XmWSgQRUMY6-QBszKSsWV-aw2zrF8U"}
	for address in trainee_list:
		new_data = {}
		
		sys_props_url = "http://" + address + ":8088" + sys_props_endpoint
		sys_props_result = client.get(sys_props_url, headers = header).json
		new_data["sys_props"] = sys_props_result
		
		try:
			historian_url = "http://" + address + ":8088" + historian_endpoint
			historian_result = client.get(historian_url, headers = header).json
			new_data["historian"] = historian_result
		except:
			pass
		
		try:
			device_url = "http://" + address + ":8088" + device_endpoint
			device_result = client.get(device_url, headers = header).json
			new_data["device"] = device_result
		except:
			pass
		
		
		trainee_data[address] = new_data
	system.tag.writeBlocking(["[default]TraineeData"], [trainee_data])