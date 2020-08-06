### Custom script configuration file must be placed in the same directory than Parameters.conf file

	The goal is to be able to send any values to ELK.
	The OS script executed must be SH and returns two column per line

	By default, the first column will be the name and the second will be the value.


# Here is an example of configuration file

	### Config file name ( ".custom.conf" part of the name is mandatory) :
		who.custom.conf
		
	### OS script executed :  	
		"/etc/metraixbeat/who.sh"
		
	### Time to wait between two script executions
		60
		
	### Content of the file "/etc/metraixbeat/who.custom.conf" :
		{
			"OSScript": "/etc/metraixbeat/who.sh",
			"Refresh": 60
		}
	
	### Executed "/etc/metraixbeat/who.sh" script content:
		who | awk '{print $1 " " $2}'

	### This will return two metrics per line in ELK
		system.custom.[ScriptName].name	
			ex: system.custom.who.name
		system.custom.[ScriptName].value	
			ex: system.custom.who.value