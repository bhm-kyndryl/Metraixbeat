### Filebeat configuration file must be placed in the same directory than Parameters.conf file


# Here is an example of configuration file

{
        "TargetFile": "/var/adm/syslog.err",
        "Patterns": ["."],
        "MultilineSeparator": "",
        "Output": "Filebeat"
}


	### Config file name ( ".filebeat.conf" part of the name is mandatory) :
		syslog.filebeat.conf
		
	### TargetFile file:  	
		"/var/adm/syslog.debug"
		
		If you need to use dynamic date/time naming, please use Python Format Code List
		You can find a list of them at the bottom of the following page
		
		"https://www.programiz.com/python-programming/datetime/strftime"

		Exemple:
		For Target file like this
			logws.%Y-%m-%d.log
		It will be interpreted as
			logws.2021-01-08.log
			
	### Patter that need to be matched
		These are Python REGEX. You can use "https://pythex.org/" to test your REGEX before applying it.
		
		With the given REGEX, you just have to escape the "\" and you are good to go !
		
		Exemple:
		For matching "test" into the following string
			"It is my test string"
			
		You can use by example the following REGEX to match " test " 
			.* test \w*$
			
		Then, escape "\" characters and add it into config file
			"Patterns": ".* test \\w*$"
		
	### Multiline Separator to detect the end of the entrie in a file, if different than "\n"
	    If traditional log file ending with "\n", then let this field empty ("")
	
		You can specify a Python REGEX to determine the begining of a new log line and then handle some big log stack like JAVA or CATALINA by example
		The best way to acheive this is to use the following website
		
		"https://pythex.org/"
		
		With the given REGEX, you just have to escape the "\" and you are good to go !
		
		Exemple:
		For line in logfile begining with 
			####<Jan 8, 2021 2:48:35 PM UTC>
			
		You will have a matching REGEX on pythex.org like
			####<\w* \w*, \w* \w*:\w*:\w* \w* \w*>
			
		Then, escape "\" characters and add it into config file
			"MultilineSeparator": "####<\\w* \\w*, \\w* \\w*:\\w*:\\w* \\w* \\w*>"
			
	### Output need to be specified to go to different destinations
	    This parameter can be "Metricbeat", "Filebeat" or "Logstash", and will ouput according to Parameters.conf configuration
		


	
