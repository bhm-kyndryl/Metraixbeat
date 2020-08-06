# "Metraixbeat" daemon description:

### Command line to execute (as root)
	Usage:
	metraixbeat -c <Parameters.conf file path> -l <Logs directory path>
	
	My config:
	/opt/bin/python3.7 /opt/freeware/sbin/metraixbeat -c /etc/metraixbeat/Parameters.conf -l /var/adm/ras/metraixbeat/

<img
src=“./LPAR-Main-Dashboard.png”
raw=true
alt=“LPAR Main Dashboard”
style=“margin-right: 10px;”
/>

### Tried to make the same than "metricbeat" LINUX daemon 
	Working without modifications to ELK stack 
	Fit into already existing Metricbeat JSON structures ("metricbeat-*" index pattern)
	Possible to specify multiple Elastic servers for HA
	Queueing messages in case of Elastic servers failure
	Performance of the daemon is overall good without much impact on system but sample rate is much lower than LINUX metricbeat... 
	Please remember that I'm not DEV and I coded that script mainly for IBM Client project


### Need some help :-)
	I really think ELK and AIX can make something together, that's maybe because my boss ordered me so :-)
	Modern and efficient monitoring can be a good point to maintain our prefered OS at top level, help our diagnostics and give clear infrastructure view on AIX/VIOS
	I'm looking for bug reporters, testers and maybe developers to help me maintaining and make evoluate the code
	
	If you like AIX as much as I do, please join Metraixbeat IBM Github project !


### Fully based on Python3 
	Tested only with 3.7 but should work with other Python3 versions
	Only 2 dependencies to install from PIP before using it
		requests 	(pip install requests) for handling easily and properly TCP requests
		pingparsing 	(pip install pingparsing) to enable the "Ping Plotter" plugin


### Few minutes for tuning Parameter.conf file and the daemon is ready to go
	See Project wiki for all parameters that can be adjusted in "Parameters.conf" file


### Adding more AIX metrics for fine monitoring ! (See Project wiki  for full details)
	Added new metricset from "hpmstat"  command (smt mode usage, CPU cache reload and affinity, etc...)
	Added new metricset from "lparstat" command (monitoring hypervisor work on key metrics)
	Added metrics for hypervisor, memory and CPU (A lot...)
	Added tags for Host identification (frame serial, Datacenter, Application)

	
### Developped new Dashboards and detailed views for AIX to reflect all metricsets (see Project wiki )
	I've already created 11 Dashboards (for now) for LPAR which are available for download and then import into ELK
	(Overview/CPU/MEMORY/FC/Network/Disk/Filesystems/Processes/HPM/Hypervisor/Ping Plotter)
	You will find screenshots of them in Project wiki
	I will create Infrastructure Dashboard in the next two months	
  
  
### Tried to add filebeat "basic" functionality inside this metraixbeat daemon
	Tailing a file and catch events depending of specified patterns
	Each Target File and matching patterns can be configured inside a simple JSON file (see Project wiki )
	Target File sanity is checked in many way (by inode, size, name, etc ...)
	TODO: Need to handle mutliline separator for huge log stack like JAVA. For now, working good with log file content ending with "\n"
  
  
### Added functionality to send the result of SH script directly into ELK
	Each executed script and sample rate can be configured inside a simple JSON file (see Project wiki )
  
  
### Things that are not tunable for now and/or need rework
	Bug in buckets
		Visual builder is not taking into account "min_doc_count" value and the result is that we can see some gaps in graphs when zoom in is too high (less than 1H).
		I think this is mainly because my sample rates are lower than metrixbeat. Those empty bucket should be replace by previous non-empty bucket value but it is not... 
		I will create a ticket to ELK team for that.	
	ELK Version
		This development is based on ELK 7.5.2. It should work with other higher versions (until JSON messages are not modified for metricsets...)
		Didn't tested it on other version as I need time for that and i dont need it now.
	Index names
		You can configure a part of the metricbeat and filebeat index but naming convention hardly coded
		"ex: 'metricbeat' will create metricbeat-aix-7.5.2" (ELK 7.5.2 is this current Metraixbeat version) and rollover should do the rest
	system.socket.summary
		This metricset requires a lot of CPU to be generated. I keep it schedule but with low sample rate because very usefull
	system.socket metricset can be generated but take a lot of CPU resources
		This metricset requires too much CPU to be generated. I disable it by scheduling a looooong schedule in "Parameters.conf" file... Need rework !
