### JSON format is matching with the Metricbeat version stored in ELKMonitoringVersion
	Should not be changed until metraixbeat is tested for different ELK versions
	"ELKMonitoringVersion": "7.5.2"


### JSON format is matching with the Metricbeat version stored in ECSVersion
	Should not be changed until metraixbeat is tested for different ECS versions
	"ECSVersion": "1.1.0"


### Set variable for ElasticSearch server Hostname running Metricbeat config
	Can add multiple servers for HA
		Exemple:
		"ELKServers": ["server00042.example.com", "server00052.example.com", "server00050.example.com", "server00053.example.com"]
		"ELKServers": ["server00042.example.com"]
	"ELKServers": ["ELKServers"]


### Set variable for ELK web username
	"ELKUsername": "elastic"


### Set variable for ELK web password
	"ELKPassword": "elastic"


### Set variable for ELK TCP port
	"ELKPort": "9200"


### Set variable for ELK HTTP protocol used
	"ELKWebProtocol": "http"


### Set variable for the ELK index name
	ex: 'metricbeat' will create metricbeat-aix-7.5.2. Rollover should make the rest
	"ELKMetricIndexName": "metricbeat"


### Set variable for the ELK index name 
	ex: 'filebeat' will create filebeat-aix-7.5.2 Rollover should make the rest
	"ELKLogIndexName": "filebeat"

### Adding DNS Suffix to hostname if not existing
		Exemple:
		"FQDN": ".example.com"
	"FQDN": ""


### DC site hosting the LPAR for easy reporting
	"HostingSite": "DataCenter 1"


### Application name hosted by the LPAR for easy reporting
	"LPARAppName": "Undefined Application"


### Maximum historical JSON messages (queued when ELK server was down) to proceed at each script Cycle
	Keep this value as it is will save CPU when reprocessing
	"ReprocessingValueAtOnce": "5"


### Time to wait before making sanity checks on Filebeat tail's processes (in seconds)
	"TailRefreshValue": "300"


### Time to wait between two executions of the Main Loop (in seconds)
	This is the main time of the daemon. Each loop will check if metricset need to be generated or not
	15 sec in a good average
	"CycleSleepTime": "15"


### Set the duration sample of the Disk IO metrics gathering process (in seconds)
	This will set the "iostat" command duration
	"DiskSampleRate": "1"


### If different than 0, set the limit of processes that must be taken into account while checking TOP processes CPU and MEME activity
	More the limit is high, more the daemon will use CPU
	"TopProcesses": "10"


### SAFETY - Time to wait before reloading a Tail process for which TargetFile has not been modified since 1 day (in minutes)
	Need some rework but it is safe to keep this value like this
	"TailReloadValue": "1440"


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


### Limit of time (in minutes) to wait before deleting historical queued JSON mesages
	Keeping too much historical JSON messages for reprocessing is CPU costly. Need to flush !
	"QueueingTimerLimit": "720"

	

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

