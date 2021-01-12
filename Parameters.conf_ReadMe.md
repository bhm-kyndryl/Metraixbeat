### JSON format is matching with the Metricbeat version stored in ELKMonitoringVersion
	Should not be changed until metraixbeat is tested for different ELK versions
	"ELKMonitoringVersion": "7.10.1"


### JSON format is matching with the Metricbeat version stored in ECSVersion
	Should not be changed until metraixbeat is tested for different ECS versions
	"ECSVersion": "1.5.0"


### Set variable for ElasticSearch server Hostname running Metricbeat config
	Can add multiple servers for HA
		Exemple:
		"ElasticServers": ["server00042.example.com", "server00052.example.com", "server00050.example.com", "server00053.example.com"]
		"ElasticServers": ["server00042.example.com"]
	"ElasticServers": ["ELKServers"]

### Set variable for ELK TCP port
	"ElasticPort": "9200"
	
	
### You will have the same configuration items for filebeat and logstash


### Set variable for ELK username
	"ELKUsername": "elastic"


### Set variable for ELK password
	"ELKPassword": "elastic"


### Set variable for ELK HTTP protocol used
	"ELKWebProtocol": "http"
	or
	"ELKWebProtocol": "https"


### Set variable for SSL certificate (ROOT CA) path to file (.pem was working for me) only if HTTPS is used. Can be concatenation of ROOT CA and INTERMEDIATE
	"ELKCertificate": ""


### Set variable for the Metrics index name
	ex: 'metricbeat' will create metricbeat-7.10.1. Write alias should make the rest if configured
	"ElasticIndexName": "metricbeat"


### Set variable for the Logs index name
	ex: 'filebeat' will create filebeat-7.10.1. Write alias should make the rest if configured
	"FilebeatIndexName": "filebeat"


### Adding DNS Suffix to hostname if not existing
		Exemple:
		"FQDN": ".example.com"
	"FQDN": ""


### Tags for easy keywork adding
		Exemple:
		"tags": ["DataCenter 1","Application name"]
	"tags": [""]
	

### Labels for easy labeling (Power hosting frame SN is automatically added in label list)
		Exemple:
		"labels": ["key1:value1","key2:value2","key3:value3"],
	"labels": [""]
	
	
### Maximum number of JSON messages to queue before sending JSON Bulk message. 
	"BulkMaxSize": "10"


### Time to wait before making sanity checks on Filebeat tail's processes (in seconds)
	"TailRefreshValue": "300"


### Time to wait between two executions of the Main Loop (in seconds)
	This is the main time of the daemon. Each loop will check if metricset need to be generated or not
	15 sec in a good average
	"CycleSleepTime": "15"


### Set the duration sample of the Disk IO metrics gathering process (in seconds)
	This will set the "iostat" command duration
	"DiskSampleRate": "1"


### If different than 0, set the limit of processes that must be taken into account while checking TOP processes CPU and MEM activity
	More the limit is high, more the daemon will use CPU
	"TopProcesses": "10"
	

### List of servers to be checked with PingPlotter plugin
		Exemple:
		"PingPlotterTargets": "google.com,10.10.128.1,8.8.8.8"
		"PingPlotterTargets": "8.8.8.8"
	"PingPlotterTargets": ""


### Number of ping requests to send to each PingPlotter targets at each check
	"PingSamples": "5"


### Amout of time to wait before exiting ping test if no answer received
	Number of seconds, followed by "s"
	"PingTimeout": "1s"


### Enable System.Hypervisor custom metricset for Hypervisor values
	"yes" or "no"
	"IfSystemHypervisorEnable": "yes"


### Enable System.HPMStat custom metricset for HPM monitoring values
	"yes" or "no"
	"IfSystemHPMStatEnable": "yes"


### Limit the number of monitored network adapters to the given list. Sort and separate them by comma
	Exemple for all interfaces: 		"EntRestricted": "all"
	Exemple for all ent interfaces: 		"EntRestricted": "ent16,ent17,ent18"
	Exemple for all en  interfaces: 		"EntRestricted": "en16,en17,en18"
	"EntRestricted": "all"


### Limit the number of monitored fiber channel adapters to the given list. Sort and separate them by comma
	Exemple for all interfaces: 		"FcsRestricted": "all"
	Exemple for all interfaces: 		"FcsRestricted": "fcs16,fcs17,fcs18"
	"FcsRestricted": "all"


### Limit the number of monitored HDISK devices to the given list. Sort and separate them by comma
	Exemple for all interfaces: 		"HdiskRestricted": "all"
	Exemple for all interfaces: 		"HdiskRestricted": "hdisk16,hdisk17,hdisk18"
	"HdiskRestricted": "all"
	

### Topic timers variables (in seconds). Time to wait before sending new metric values to ELK server
	For now, default value are good for my case but up to you to play with all metricset depending of your needs
	Some metricset take more CPU than others so make carefull testing to reach your balance point :-)
	
	"SystemSocketWaitValue": "1000000000",	
	"PingPlotterWaitValue": "300"
	"SystemHypervisorWaitValue": "300"
	"SystemProcessWaitValue": "300"
	"SystemSocketSummaryWaitValue": "300"
	"SystemFilesystemAndFstatWaitValue": "240"
	"SystemDiskIOWaitValue": "180"
	"SystemProcessSummaryWaitValue": "120"
	"SystemHPMStatWaitValue": "60"
	"SystemLoadWaitValue": "60"
	"SystemMemoryWaitValue": "30"
	"SystemFcWaitValue": "20"
	"SystemNetworkWaitValue": "20"
	"SystemCoreAndCpuWaitValue": "15"

