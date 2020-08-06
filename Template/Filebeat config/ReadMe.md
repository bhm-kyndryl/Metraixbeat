### Filebeat configuration file must be placed in the same directory than Parameters.conf file


# Here is an example of configuration file

	###"Config file name ( ".filebeat.conf" part of the name is mandatory) :
		syslog.filebeat.conf
		
	### TargetFile file:  	
		"/var/adm/syslog.debug"
		
	### Patterns to look for (with quotes and comma separated) : 
		"info", "warning", "error"
		
	### Multiline Separator to detect the end of the entrie in a file, if different than "\n"
		"" (not ready yet...)
		
	### Content of the file "/etc/metraixbeat/syslog.filebeat.conf" 
		(If Parameters.conf is inside "/etc/metraixbeat/" directory) :
		{
				"TargetFile": "/var/adm/syslog.debug",
				"Patterns": ["info", "warning", "error"],
				"MultilineSeparator": ""
		}

# TargetFile name may contain reference to date. The script will convert it
	We will ad new conversion if required by users...

	### Filebeat configuration file must be placed in the same directory than Parameters.conf file

### Here is an example of configuration file

	Config file name ( ".filebeat.conf" part of the name is mandatory) :
		syslog.filebeat.conf
		
	TargetFile file:  	
		"/var/adm/syslog.debug"
		
	Patterns to look for (with quotes and comma separated) : 
		"info", "warning", "error"
		
	Multiline Separator to detect the end of the entrie in a file, if different than "\n"
		"" (not ready yet...)
		
	Content of the file "/etc/metraixbeat/syslog.filebeat.conf" 
	(If Parameters.conf is inside "/etc/metraixbeat/" directory) :
	{
			"TargetFile": "/var/adm/syslog.debug",
			"Patterns": ["info", "warning", "error"],
			"MultilineSeparator": ""
	}

# TargetFile name may contain reference to date. The script will convert it
	We will ad new conversion if required by users...

###	Converting %yyyy to 4 digits years format

###	Converting %yy to 2 digits years format

###	Converting %MM to 2 digits month format

###	Converting %DD to 2 digits day format
  
###	Converting %hh to 2 digits hour format

###	Converting %mm to 2 digits minute format

###	Converting %ss to 2 digits second format

