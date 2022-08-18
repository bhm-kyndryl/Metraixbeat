#!/usr/bin/python

# import libs
import argparse
from encodings.utf_8 import encode
import subprocess
import datetime
import logging
import os
import random
import sys
import traceback
import json
import requests

from urllib.error import HTTPError



# import dependancies 
import values

# Functions

def GenerateEphemeralID():
    """ Generate specific format of random number for ELK internal purpose.

        Generating Ephemeral ID for current daemon execution
        or new LPAR id file creation (random string format 8-4-4-4-12).
    """
    
    # Generating Ephemeral ID
    # IMPROVEMENT / urandom can be converted into python style
    ShortRandom2 = subprocess.Popen("tr -dc a-z0-9 </dev/urandom |  head -c 4", shell=True, stdout=subprocess.PIPE).stdout
    ShortRandom2 = ShortRandom2.read().decode().replace("\n","")
    ShortRandom1 = subprocess.Popen("tr -dc a-z0-9 </dev/urandom |  head -c 4", shell=True, stdout=subprocess.PIPE).stdout
    ShortRandom1 = ShortRandom1.read().decode().replace("\n","")
    ShortRandom3 = subprocess.Popen("tr -dc a-z0-9 </dev/urandom |  head -c 4", shell=True, stdout=subprocess.PIPE).stdout
    ShortRandom3 = ShortRandom3.read().decode().replace("\n","")
    MediumRandom = subprocess.Popen("tr -dc a-z0-9 </dev/urandom |  head -c 8", shell=True, stdout=subprocess.PIPE).stdout
    MediumRandom = MediumRandom.read().decode().replace("\n","")
    LongRandom = subprocess.Popen("tr -dc a-z0-9 </dev/urandom |  head -c 12", shell=True, stdout=subprocess.PIPE).stdout
    LongRandom = LongRandom.read().decode().replace("\n","")

    # Formating string
    values.EphemeralID = MediumRandom + "-" + ShortRandom1 + "-" + ShortRandom2 + "-" + ShortRandom3 + "-" + LongRandom

def LoadDaemonConfig():
    """This function will get all the required parameters from config file and load them into vars   
    
    TODO: Describe the fcuntion, all vars and its content
    """   
    
    # Checking if Configuration file exists
    if os.path.exists(values.ConfigFilePath):
        # Executing with Try/Catch to handle any error in file
        try:
            with open(values.ConfigFilePath, 'r') as ConfigFile:
                # Loading JSOn file content
                JSONValues = json.load(ConfigFile)

                # Set variables for ELK server.
                values.ELKMonitoringVersion = JSONValues["ELKMonitoringVersion"]
                values.ECSVersion = JSONValues["ECSVersion"]
                values.ElasticServers = JSONValues["ElasticServers"]
                values.FilebeatServers = JSONValues["FilebeatServers"]
                values.LogstashServers = JSONValues["LogstashServers"]
                
                # Checking if Filebeat output is empty
                if len(values.FilebeatServers) == 0:
                    # Then defaulting to Metricbeat output
                    values.FilebeatServers = values.ElasticServers
                # Checking if Logstash output is empty
                if len(values.LogstashServers) == 0:
                    # Then defaulting to Metricbeat output
                    values.LogstashServers = values.ElasticServers
                
                values.ELKUsername = JSONValues["ELKUsername"]
                values.ELKPassword = JSONValues["ELKPassword"]
                values.ELKCertificate = JSONValues["ELKCertificate"]
                # Handling if ELKCertificate is empty
                if(len(values.ELKCertificate) == 0):
                    values.ELKCertificate = "True"
                values.ElasticPort = JSONValues["ElasticPort"]
                values.FilebeatPort = JSONValues["FilebeatPort"]
                values.LogstashPort = JSONValues["LogstashPort"]
                values.ELKWebProtocol = JSONValues["ELKWebProtocol"]
                # Duplicating *Servers to *ServersAvailable making all ELK servers failed by default
                values.ElasticServersAvailable = values.ElasticServers[:]
                values.ElasticServersFailed = []
                values.FilebeatServersAvailable = values.FilebeatServers[:]
                FilebeatServersFailed = []
                values.LogstashServersAvailable = values.LogstashServers[:]
                values.LogstashServersFailed = []
                values.ElasticIndexName = JSONValues["ElasticIndexName"]
                values.FilebeatIndexName = JSONValues["FilebeatIndexName"]
                
                # Setting NMON sequence counter to 0
                NMONSeq = 0

                # Script functional variables
                # Time to wait before refreshing tail's processes status (in seconds)
                values.TailRefreshValue = int(JSONValues["TailRefreshValue"])
                # Time to wait between two execution of the Main Loop (in seconds)
                values.CycleSleepTime = int(JSONValues["CycleSleepTime"])
                # How much time to run metric commands and get averaged results
                values.DiskSampleRate = int(JSONValues["DiskSampleRate"])
                # If different than 0, set the limit of processes that must be taken into account while checking TOP processes CPU activity
                values.TopProcesses = int(JSONValues["TopProcesses"])
                # Adding FQDN to the hostname if not existing, andd necessary...
                values.FQDN = JSONValues["FQDN"]
                # How much messages are sent within one connection to server
                values.BulkMaxSize = int(JSONValues["BulkMaxSize"])

                # Topic timers variables (in seconds)
                # Time to wait before sending new metric values to ELK server
                values.SystemProcessWaitValue = int(JSONValues["SystemProcessWaitValue"])
                values.SystemFilesystemAndFstatWaitValue = int(JSONValues["SystemFilesystemAndFstatWaitValue"])
                values.SystemDiskIOWaitValue = int(JSONValues["SystemDiskIOWaitValue"])
                values.SystemProcessSummaryWaitValue = int(JSONValues["SystemProcessSummaryWaitValue"])
                values.SystemLoadWaitValue = int(JSONValues["SystemLoadWaitValue"])
                values.SystemFcWaitValue = int(JSONValues["SystemFcWaitValue"])
                values.SystemSocketSummaryWaitValue = int(JSONValues["SystemSocketSummaryWaitValue"])
                values.SystemSocketWaitValue = int(JSONValues["SystemSocketWaitValue"])
                values.SystemMemoryWaitValue = int(JSONValues["SystemMemoryWaitValue"])
                values.SystemNetworkWaitValue = int(JSONValues["SystemNetworkWaitValue"])
                values.SystemCoreAndCpuWaitValue = int(JSONValues["SystemCoreAndCpuWaitValue"])
                
                print(f'function load config  value  {values.SystemCoreAndCpuWaitValue}')
                # Loading PingPlotter targets and configuration values
                values.PingPlotterTargets = JSONValues["PingPlotterTargets"]
                values.PingPlotterWaitValue = int(JSONValues["PingPlotterWaitValue"])
                values.PingSamples = int(JSONValues["PingSamples"])
                values.PingTimeout = JSONValues["PingTimeout"]
                
                # Checking other JSON values linked to custom plugins
                values.IfSystemHPMStatEnable = JSONValues["IfSystemHPMStatEnable"]
                values.IfSystemHypervisorEnable = JSONValues["IfSystemHypervisorEnable"]
                values.SystemHPMStatWaitValue = int(JSONValues["SystemHPMStatWaitValue"])
                values.SystemHypervisorWaitValue = int(JSONValues["SystemHypervisorWaitValue"])
                values.ErrptLogWaitValue = int(JSONValues["ErrptLogWaitValue"])

                
                # Loading Tags
                values.Tags = JSONValues["tags"]
                
                # Generating tagz var for rollup purpose
                values.Tagz = ""
                for Tag in values.Tags:  
                    values.Tagz += Tag + ','
                values.Tagz = values.Tagz[:-1]
                
                # Loading Labels
                values.Labels = JSONValues["labels"]
                
                # Loading some parameter that can restrict the number of devices checked for some cases
                # Network Adapters
                values.EntRestricted = JSONValues["EntRestricted"]
                # Fiber Channel Adapters
                values.FcsRestricted = JSONValues["FcsRestricted"]
                # HDISK devices
                values.HdiskRestricted = JSONValues["HdiskRestricted"]
                
                # Checking if Proxy bypass is required
                values.BypassProxy = JSONValues["bypassproxy"]
                
                # Disabling proxy if requested
                if values.BypassProxy == 'yes':
                    os.environ['no_proxy'] = '*'
                
        except:
            # problem encountered while loading JSON daemon configuration file, exiting
            logging.info("            ==> Error while loading " + values.ConfigFilePath + " daemon config file !")
            logging.info("                Please check the Configuration file JSON parameters, format and validity")
            logging.info(str(traceback.print_exc()))
            traceback.print_exc()
            os._exit(2)
    else:
        # Daemon configuration file does not exist, exiting
        logging.info("            ==> Error while loading " + values.ConfigFilePath + " daemon config file !")
        logging.info("                Config file does not exist")
        logging.info(str(traceback.print_exc()))
        traceback.print_exc()
        os._exit(2)

    # Log
    # Log
    logging.info(" - Loading Daemon configuration... Done !")

    # Debug
    # print('\nDEBUG\n')
    # print('<!> DEBUG ', ELKMonitoringVersion, 'ELKMonitoringVersion')
    # print('<!> DEBUG ', ECSVersion, 'ECSVersion')
    # print('<!> DEBUG ', BaseDir, 'BaseDir')
    # print('<!> DEBUG ', Metricbeat_LogStash_HostName, 'Metricbeat_LogStash_HostName')
    # print('<!> DEBUG ', Filebeat_LogStash_HostName, 'Filebeat_LogStash_HostName')
    # print('<!> DEBUG ', Metricbeat_LogStash_PORT, 'Metricbeat_LogStash_PORT')
    # print('<!> DEBUG ', Filebeat_LogStash_PORT, 'Filebeat_LogStash_PORT')
    # print('<!> DEBUG ', FQDN, 'FQDN')
    # print('<!> DEBUG ', TailRefreshValue, 'TailRefreshValue')
    # print('<!> DEBUG ', CycleSleepTime, 'CycleSleepTime')
    # print('<!> DEBUG ', DiskSampleRate, 'DiskSampleRate')
    # print('<!> DEBUG ', TopProcesses, 'TopProcesses')
    # print('<!> DEBUG ', SystemProcessWaitValue, 'SystemProcessWaitValue')
    # print('<!> DEBUG ', SystemFilesystemAndFstatWaitValue, 'SystemFilesystemAndFstatWaitValue')
    # print('<!> DEBUG ', SystemDiskIOWaitValue, 'SystemDiskIOWaitValue')
    # print('<!> DEBUG ', SystemProcessSummaryWaitValue, 'SystemProcessSummaryWaitValue')
    # print('<!> DEBUG ', SystemLoadWaitValue, 'SystemLoadWaitValue')
    # print('<!> DEBUG ', SystemFcWaitValue, 'SystemFcWaitValue')
    # print('<!> DEBUG ', SystemMemoryWaitValue, 'SystemMemoryWaitValue')
    # print('<!> DEBUG ', SystemNetworkWaitValue, 'SystemNetworkWaitValue')
    # print('<!> DEBUG ', SystemCoreAndCpuWaitValue, 'SystemCoreAndCpuWaitValue')
    # print('\nFINDEBUG\n')
    pass

def LoadPluginConfig():
    """This function will get all the required information from Plugin config files and load them into vars   
    All files analyzed need to be in the same folder than main Parameters.conf file and have specific naming convention
    
    Please refer to README.md
    
    TODO: Describe the function, all vars and its content
    """
    # Log
    logging.info(" - Loading Filebeat plugin's config files...")

    
    # Defining config path from ConfigFilePath
    ConfigPathtmp = values.ConfigFilePath.split('/').pop()
    values.ConfigPath = values.ConfigFilePath.replace(ConfigPathtmp,'')

    # Loading filebeat plugin configs
    for f_name in os.listdir(values.ConfigPath):
        if f_name.endswith('filebeat.conf'):
            # Log
            logging.info("           " + f_name + ":")

            # Generating full path name for current file
            FullPathFileName = values.ConfigPath + f_name

            # Loading JSON file content
            # We load JSON content into try/catch to avoid failure if JSON formatting is not good.
            try:
                with open(FullPathFileName, 'r') as ConfigFile:
                    JSONValues = json.load(ConfigFile)

                    # Log
                    logging.info("            * Target file                 = " + JSONValues["TargetFile"])
                    logging.info("            * Patterns                    = " + str(JSONValues["Patterns"]))
                    logging.info("            * Multiline sparator REGEX    = " + JSONValues["MultilineSeparator"])
                    logging.info("            * Output                      = " + JSONValues["Output"])
                    
                    # Generating EGREP string from list of patterns
                    PatternMatch = ""
                    for Pattern in JSONValues["Patterns"]:
                        PatternMatch = PatternMatch + Pattern + "|"
                    PatternMatch = PatternMatch[:-1]
                    
                    # Converting date format, if any, in target file                   
                    CurrentTargetFile = ConvertFileName(JSONValues["TargetFile"])

                    # Checking if file exists
                    try:                        
                        # Looking for corresponding file
                        OSCommand = "ls -lart " + CurrentTargetFile + " | tail -n 1 | awk '{print $NF}'"
                        CheckTargetFile = subprocess.Popen(OSCommand, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
                        CheckTargetFile = CheckTargetFile.read().decode().split()
                        
                        # Checking if file exists
                        if os.path.exists(str(CheckTargetFile[0])):
                            # If yes
                            CurrentTargetFile = str(CheckTargetFile[0])
                            
                            # Storing the last line of the Target file to start tail on
                            with open(CurrentTargetFile, "r") as LastLine:
                                TargetFileLastLine = len(LastLine.readlines()) + 1
                                
                            # Storing the inode and size of the Target file to start tail on
                            TargetFileInode = os.stat(CurrentTargetFile).st_ino
                            TargetFileSize = os.stat(CurrentTargetFile).st_size
                        else:
                            # If no
                            # File does not exists, rising a warning but loading config with 0 default values
                            LastLine = 0
                            TargetFileInode = 0
                            TargetFileSize = 0
                            TargetFileLastLine = 0
                            
                            # Log
                            logging.info("            ==> Warning while loading " + f_name + " config file !")
                            logging.info("                File does not exists yet, daemon will retry later...")
                            
                            # Initializing state value to start tail from line 1 when file will be available
                            values.TargetFileCurrentPosArray[f_name] = 0
                            
                    except:
                        # File does not exists, rising a warning but loading config with 0 default values
                        LastLine = 0
                        TargetFileInode = 0
                        TargetFileSize = 0
                        TargetFileLastLine = 0
                        
                        # Log
                        logging.info("            ==> Warning while loading " + f_name + " config file !")
                        logging.info("                File does not exists yet, daemon will retry later...")
                        
                        # Initializing state value to start tail from line 1 when file will be available
                        values.TargetFileCurrentPosArray[f_name] = 0

                    # Storing results into FilebeatConfigsArray dictionnary
                    # ConfigString = CurrentTargetFile + ',' + JSONValues["TargetFile"] + ',' + PatternMatch + ',' + str(TargetFileLastLine) + ',' + str(TargetFileInode) + ',' + str(TargetFileSize) + ',' + str(JSONValues["MultilineSeparator"] + ',' + str(JSONValues["Output"]))
                    values.FilebeatConfigsArray[f_name] = CurrentTargetFile + ',' + JSONValues["TargetFile"] + ',' + PatternMatch + ',' + str(TargetFileLastLine) + ',' + str(TargetFileInode) + ',' + str(TargetFileSize) + ',' + str(JSONValues["MultilineSeparator"] + ',' + str(JSONValues["Output"]))
            except:
                # If error, bypassing this plugin
                # Log
                logging.info("            ==> Error while loading " + f_name + " config file !")
                logging.info("                Please check JSON format and validity")
                logging.info(str(traceback.print_exc()))
                traceback.print_exc()
            # pass

    # All filebeat plugins loaded
    # Log
    logging.info("            ==> All Filebeat plugin's config files loaded !")

    # Log
    logging.info(" - Loading Custom Metric plugin's config files...")

    # Loading custom exec plugin configs
    for f_name in os.listdir(values.ConfigPath):
        if f_name.endswith('custom.conf'):
            # Log
            logging.info("           " + f_name + ":")

            # Generating full path name for current file
            FullPathFileName = values.ConfigPath + f_name

            # Loading JSON file content
            # We load JSON content into try/catch to avoid failure if JSON formatting is not good.
            try:
                with open(FullPathFileName, 'r') as ConfigFile:
                    JSONValues = json.load(ConfigFile)

                    # Log
                    logging.info("            * OS Script               = " + JSONValues["OSScript"])
                    logging.info("            * Refresh value in sec    = " + str(JSONValues["Refresh"]))
                    logging.info("            * Output                  = " + JSONValues["Output"])


                    # Storing results into FilebeatConfigsArray dictionnary
                    # ConfigString = JSONValues["OSScript"] + ',' + str(JSONValues["Refresh"]) + ',' + JSONValues["Output"]
                    values.CustomMetricsConfigsArray[f_name] = JSONValues["OSScript"] + ',' + str(JSONValues["Refresh"]) + ',' + JSONValues["Output"]
            except:
                # If error, bypassing this plugin
                # Log
                logging.info("            ==> Error while loading " + f_name + " config file !")
                logging.info("                Please check that target file is existing, JSON format and validity")
                logging.info(str(traceback.print_exc()))
                traceback.print_exc()
                os._exit(2)

            # Debug
            # print('\nDEBUG\n')
            # print('<!> DEBUG ', 'CustomMetricsConfigsArray[f_name]', CustomMetricsConfigsArray[f_name])
            # print('<!> DEBUG ', 'f_name ', f_name)
            # print('<!> DEBUG ', 'OSScript ', JSONValues["OSScript"])
            # print('<!> DEBUG ', 'Refresh ', str(JSONValues["Refresh"]))
            # print('\nFINDEBUG\n')
    # All Custom Metric plugins loaded
    # Log
    logging.info("            ==> All Custom Metric plugin's config files loaded !")
    
    # Loading PingPlotter plugin configs
    # Log
    logging.info("            Ping check:")
    for ping_dest in values.PingPlotterTargets.split(','):
        # Log
        logging.info("            * " + ping_dest)
    # Log
    logging.info("            ==> All Ping Check destinations are loaded !")
    pass

def CheckServers():
    """ This function check the state of the Metricbeat Elasticsearch server.

        It also handles the retransmit queues for Metricbeat and Filebeat items.
        On each script loop execution, it will resend some queued messages up to a given number.
        
    Please refer to README.md
    
    TODO: Describe the function, all vars and its content
    """
       
    # Checking for unavailable Elastic servers
    if len(values.ElasticServersFailed) != 0:
                        
        # Choosing randomly one Elastic server in the failed pool
        ElasticServer = random.choice(values.ElasticServersFailed)
        
        # If ElasticServer server is unavailable, we send a get request
        try:
            # Defining URL and credentials for web request
            values.ELKCreds = (values.ELKUsername, values.ELKPassword)
            ElasticServerURL = values.ELKWebProtocol + '://' + ElasticServer + ':' + values.ElasticPort + '/'
            
            # Connect and send encoded JSON message     
            values.ElasticServerCnx = requests.session()
            ELKAnswer = values.ElasticServerCnx.get(ElasticServerURL, auth=values.ELKCreds, timeout=5, verify=values.ELKCertificate)

            # If the response was successful, no Exception will be raised
            ELKAnswer.raise_for_status()

        except HTTPError as http_err:
            # ELK server is still unavailable
            # Log
            logging.info("WARNING  ==> " + ElasticServer +  " is unavailable for Metricbeat messages")
            
            # Creating the error stack file and filling error stack informations
            # with open(CrashDumpCheckLog, 'a') as f:
                # f.write('\n\n')
                # f.write(str(datetime.datetime.now()))
                # f.write(':\n')
                # f.write(str(http_err))
                # f.write(traceback.format_exc())
                # f.write('\n')

            # Print and log error stack for debug purpose
            # logging.info('WARNING  ==> Please check ' + CrashDumpCheckLog + ' for more informations on HTTP errors')
            # traceback.print_exc()

        except Exception as err:
            # ELK server is still unavailable
            # Log
            logging.info("WARNING  ==> " + ElasticServer +  " is unavailable for Metricbeat messages")
            
            # Creating the error stack file and filling error stack informations
            # with open(CrashDumpCheckLog, 'a') as f:
                # f.write('\n\n')
                # f.write(str(datetime.datetime.now()))
                # f.write(':\n')
                # f.write(str(err))
                # f.write(traceback.format_exc())
                # f.write('\n')

            # Print and log error stack for debug purpose
            # logging.info('WARNING  ==> Please check ' + CrashDumpCheckLog + ' for more informations on HTTP errors')
            # traceback.print_exc()
        
        else:
            # ELK server is available, let's add it into the Available pool 
            # Into a try/catch because some background processes can modify these value
            try:
                values.ElasticServersFailed.remove(ElasticServer)
                values.ElasticServersAvailable.append(ElasticServer)
                logging.info("INFO     ==> " + ElasticServer +  " is Online ! Processing Metricbeat messages on this server")
            except:
                # Nothing to do
                pass

    # Checking for unavailable Filebeat servers
    if len(values.FilebeatServersFailed) != 0:
             
        # Choosing randomly one Filebeat server in the failed pool
        FilebeatServer = random.choice(values.FilebeatServersFailed)
        
        # If FilebeatServer server is unavailable, we send a get request
        try:
            # Defining URL and credentials for web request
            values.ELKCreds = (values.ELKUsername, values.ELKPassword)
            FilebeatServerURL = values.ELKWebProtocol + '://' + FilebeatServer + ':' + values.FilebeatPort + '/'
            
            # Connect and send encoded JSON message     
            values.FilebeatServerCnx = requests.session()
            ELKAnswer = values.FilebeatServerCnx.get(FilebeatServerURL, auth=values.ELKCreds, timeout=5, verify=values.ELKCertificate)

            # If the response was successful, no Exception will be raised
            ELKAnswer.raise_for_status()

        except HTTPError as http_err:
            # ELK server is still unavailable
            # Log
            logging.info("WARNING  ==> " + FilebeatServer +  " is unavailable for Filebeat messages")
            
            # Creating the error stack file and filling error stack informations
            # with open(CrashDumpCheckLog, 'a') as f:
                # f.write('\n\n')
                # f.write(str(datetime.datetime.now()))
                # f.write(':\n')
                # f.write(str(http_err))
                # f.write(traceback.format_exc())
                # f.write('\n')

            # Print and log error stack for debug purpose
            # logging.info('WARNING  ==> Please check ' + CrashDumpCheckLog + ' for more informations on HTTP errors')
            # traceback.print_exc()

        except Exception as err:
            # ELK server is still unavailable
            # Log
            logging.info("WARNING  ==> " + FilebeatServer +  " is unavailable for Filebeat messages")
            
            # Creating the error stack file and filling error stack informations
            # with open(CrashDumpCheckLog, 'a') as f:
                # f.write('\n\n')
                # f.write(str(datetime.datetime.now()))
                # f.write(':\n')
                # f.write(str(err))
                # f.write(traceback.format_exc())
                # f.write('\n')

            # Print and log error stack for debug purpose
            # logging.info('WARNING  ==> Please check ' + CrashDumpCheckLog + ' for more informations on HTTP errors')
            # traceback.print_exc()
        
        else:
            # ELK server is available, let's add it into the Available pool 
            # Into a try/catch because some background processes can modify these value
            try:
                values.FilebeatServersFailed.remove(FilebeatServer)
                values.FilebeatServersAvailable.append(FilebeatServer)
                logging.info("INFO     ==> " + FilebeatServer +  " is Online ! Processing Filebeat messages on this server")
            except:
                # Nothing to do
                pass

    # Checking for unavailable Logstash servers
    if len(values.LogstashServersFailed) != 0:
                        
        # Choosing randomly one Logstash server in the failed pool
        LogstashServer = random.choice(values.LogstashServersFailed)
        
        # If LogstashServer server is unavailable, we send a get request
        try:
            # Defining URL and credentials for web request
            values.ELKCreds = (values.ELKUsername, values.ELKPassword)
            LogstashServerURL = values.ELKWebProtocol + '://' + LogstashServer + ':' + values.LogstashPort + '/'
            
            # Connect and send encoded JSON message
            values.LogstashServerCnx = requests.session()

            ELKAnswer = values.LogstashServerCnx.get(LogstashServerURL, auth=values.ELKCreds, timeout=5, verify=values.ELKCertificate)
            
            # If the response was successful, no Exception will be raised
            ELKAnswer.raise_for_status()

        except HTTPError as http_err:
            # ELK server is still unavailable
            # Log
            logging.info("WARNING  ==> " + LogstashServer +  " is unavailable for Logstash messages")
            
            # Creating the error stack file and filling error stack informations
            # with open(CrashDumpCheckLog, 'a') as f:
                # f.write('\n\n')
                # f.write(str(datetime.datetime.now()))
                # f.write(':\n')
                # f.write(str(http_err))
                # f.write(traceback.format_exc())
                # f.write('\n')

            # Print and log error stack for debug purpose
            # logging.info('WARNING  ==> Please check ' + CrashDumpCheckLog + ' for more informations on HTTP errors')
            # traceback.print_exc()

        except Exception as err:
            # ELK server is still unavailable
            # Log
            logging.info("WARNING  ==> " + LogstashServer +  " is unavailable for Logstash messages")
            
            # Creating the error stack file and filling error stack informations
            # with open(CrashDumpCheckLog, 'a') as f:
                # f.write('\n\n')
                # f.write(str(datetime.datetime.now()))
                # f.write(':\n')
                # f.write(str(err))
                # f.write(traceback.format_exc())
                # f.write('\n')

            # Print and log error stack for debug purpose
            # logging.info('WARNING  ==> Please check ' + CrashDumpCheckLog + ' for more informations on HTTP errors')
            # traceback.print_exc()
        
        else:
            # ELK server is available, let's add it into the Available pool 
            # Into a try/catch because some background processes can modify these value
            try:
                values.LogstashServersFailed.remove(LogstashServer)
                values.LogstashServersAvailable.append(LogstashServer)
                logging.info("INFO     ==> " + LogstashServer +  " is Online ! Processing Logstash messages on this server")
            except:
                # Nothing to do
                pass
 
    # Checking if queued messages need to be sent in SendQueueArray and if one Elastic servers are available
    if (len(values.SendQueueArray) > 0 and values.MetricbeatQueueFlushed == False and len(values.ElasticServersAvailable) > 0):
        # If one Elastic server is available, we flush the current queue as messages are too old
        SendJSON('Flush', 'Metricbeat')
        # Logstring = 'INFO ==> Sending order to flush ' + str(len(SendQueueArray)) + ' JSON Metricbeat messages'
        # logging.info(Logstring)
        
    if (len(values.FilebeatSendQueueArray) > 0 and values.FilebeatQueueFlushed == False and len(values.FilebeatServersAvailable) > 0):
        # If one Filebeat server is available, we flush the current queue as messages are too old
        SendJSON('Flush', 'Filebeat')
        # Logstring = 'INFO ==> Sending order to flush ' + str(len(FilebeatSendQueueArray)) + ' JSON Filebeat messages'
        # logging.info(Logstring)
        
    if (len(values.LogstashSendQueueArray) > 0 and values.LogstashQueueFlushed == False and len(values.LogstashServersAvailable) > 0):
        # If one Logstash server is available, we flush the current queue as messages are too old
        SendJSON('Flush', 'Logstash')
        # Logstring = 'INFO ==> Sending order to flush ' + str(len(LogstashSendQueueArray)) + ' JSON Logstash messages'
        # logging.info(Logstring)
        
    # Logging messages about queue states
    if (len(values.SendQueueArray) > values.BulkMaxSize or len(values.ElasticServersAvailable) == 0):
        LogString = "WARNING  ==>  " + str(len(values.SendQueueArray)) + " Metricbeat historical JSON messages queued"
        logging.info(LogString)
    if (len(values.FilebeatSendQueueArray) > values.BulkMaxSize or len(values.FilebeatServersAvailable) == 0):
        LogString = "WARNING  ==>  " + str(len(values.FilebeatSendQueueArray)) + " Filebeat historical JSON messages queued"
        logging.info(LogString)
    if (len(values.LogstashSendQueueArray) > values.BulkMaxSize or len(values.LogstashServersAvailable) == 0):
        LogString = "WARNING  ==>  " + str(len(values.LogstashSendQueueArray)) + " Logstash historical JSON messages queued"
        logging.info(LogString)

    # Finally, reseting Queue Flush states
    values.MetricbeatQueueFlushed = False
    values.FilebeatQueueFlushed = False
    values.LogstashQueueFlushed = False

def ConvertFileName(FileName):
    """This function convert date time for easy use and tracking while making tail on log files
    
    TODO: Describe the function, all vars and its content
    """
    
    # Depending of the config file, TargetFile name may contain reference to date. Let's convert it !
    # We will ad new conversion if required by users...

    FileNameC = str(FileName.replace('%a', datetime.datetime.now().strftime("%a")))
    FileNameC = FileNameC.replace('%A', datetime.datetime.now().strftime("%A"))
    FileNameC = FileNameC.replace('%w', datetime.datetime.now().strftime("%w"))
    FileNameC = FileNameC.replace('%d', datetime.datetime.now().strftime("%d"))
    FileNameC = FileNameC.replace('%-d', datetime.datetime.now().strftime("%-d"))
    FileNameC = FileNameC.replace('%b', datetime.datetime.now().strftime("%b"))
    FileNameC = FileNameC.replace('%B', datetime.datetime.now().strftime("%B"))
    FileNameC = FileNameC.replace('%m', datetime.datetime.now().strftime("%m"))
    FileNameC = FileNameC.replace('%-m', datetime.datetime.now().strftime("%-m"))
    FileNameC = FileNameC.replace('%y', datetime.datetime.now().strftime("%y"))
    FileNameC = FileNameC.replace('%-y', datetime.datetime.now().strftime("%-y"))
    FileNameC = FileNameC.replace('%Y', datetime.datetime.now().strftime("%Y"))
    FileNameC = FileNameC.replace('%YY', datetime.datetime.now().strftime("%YY"))
    FileNameC = FileNameC.replace('%H', datetime.datetime.now().strftime("%H"))
    FileNameC = FileNameC.replace('%-H', datetime.datetime.now().strftime("%-H"))
    FileNameC = FileNameC.replace('%I', datetime.datetime.now().strftime("%I"))
    FileNameC = FileNameC.replace('%-I', datetime.datetime.now().strftime("%-I"))
    FileNameC = FileNameC.replace('%p', datetime.datetime.now().strftime("%p"))
    FileNameC = FileNameC.replace('%M', datetime.datetime.now().strftime("%M"))
    FileNameC = FileNameC.replace('%-M', datetime.datetime.now().strftime("%-M"))
    FileNameC = FileNameC.replace('%S', datetime.datetime.now().strftime("%S"))
    FileNameC = FileNameC.replace('%-S', datetime.datetime.now().strftime("%-S"))
    FileNameC = FileNameC.replace('%f', datetime.datetime.now().strftime("%f"))
    FileNameC = FileNameC.replace('%z', datetime.datetime.now().strftime("%z"))
    FileNameC = FileNameC.replace('%j', datetime.datetime.now().strftime("%j"))
    FileNameC = FileNameC.replace('%-j', datetime.datetime.now().strftime("%-j"))
    FileNameC = FileNameC.replace('%U', datetime.datetime.now().strftime("%U"))
    FileNameC = FileNameC.replace('%W', datetime.datetime.now().strftime("%W"))
    FileNameC = FileNameC.replace('%c', datetime.datetime.now().strftime("%c"))
    FileNameC = FileNameC.replace('%x', datetime.datetime.now().strftime("%x"))
    FileNameC = FileNameC.replace('%X', datetime.datetime.now().strftime("%X"))
    FileNameC = FileNameC.replace('%%', datetime.datetime.now().strftime("%%"))
    
    
    # Returning converted string
    # print('\nconverted: ', FileNameC,'\n')
    return FileNameC

def CompareTimer(TimedTopic, MetricsWaitValue, CustomMetric = ''):
    """ This function compare the last execution time and the specific timer for an element.
        If Timer is reached, the function return True and will trigger the underlying function.

        - TimedTopic is the metric on which the timer needed to be checked
        - MetricsWaitValue is the number of seconds to wait before work for metric is triggered
    """
    
    # Get current timestamp
    CurrentTimer = datetime.datetime.now()
    #MetricsWaitValue = int(MetricsWaitValue)
    # Try/Catch to avoid errors on non defined dictionary entrie / First execution
    try:
        # Dictionary entrie is not empty
        # Get last execution date/time
        LastTopicExecTime = values.ExecutionTimers[TimedTopic]

        # Comparing current and last execution date/time to get actual delay
        TimerLatency = CurrentTimer - LastTopicExecTime

        # Converting TimerLatency in seconds
        TimerLatency = TimerLatency.total_seconds()
    except:
        # Dictionary entrie is empty
        # We set TimerLatency very high (3600) to force the work for this first execution
        TimerLatency = 3600

    # Comparing last execution value with current timestamp
    # and take decision to schedule the work or not
    if TimerLatency > MetricsWaitValue:
        values.ExecutionTimers[TimedTopic] = datetime.datetime.now()
        # Log
        LogString = "==> " + TimedTopic + " " + CustomMetric + " : New execution triggered ! (" + str(round(TimerLatency,2)) + " sec elapsed for " + str(MetricsWaitValue) + " seconds wait time)."
        logging.info(LogString)
        # print('YES ExecutionTimers[TimedTopic] and TimerLatency and MetricsWaitValue: ' + str(ExecutionTimers[TimedTopic]) + ' ' + str(round(TimerLatency,2)) + ' ' + str(MetricsWaitValue))
        return str(TimerLatency).replace('.', '')
    else:
        RemainingTime = MetricsWaitValue - TimerLatency
        # Log
        LogString = "  ! (" + str(round(RemainingTime,2)) + "/" + str(MetricsWaitValue) + " sec) " + TimedTopic + CustomMetric + " has NOT reached timer value."
        logging.info(LogString)
        # print('NO ExecutionTimers[TimedTopic] and TimerLatency and MetricsWaitValue: ' + str(ExecutionTimers[TimedTopic]) + ' ' + str(round(TimerLatency,2)) + ' ' + str(MetricsWaitValue))
        return values.devnull

def conf_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
    
def logs_path(path):
    if os.path.isdir(path):
        values.LogFilePath=path
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def shutdown():
    logging.info('Shutting down')
    sys.exit(1)

def signal_handler(signum, frame):
    shutdown()
    
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='this agent metricbeat from the servers AIX AIX 5.3, 6.1, 7.1 and 7.2.', 
        prog='metraixbeat'
    )
    parser.add_argument('-c', '--configFile', type=conf_path, help=' parameters.conf file path')
    parser.add_argument('-l', '--logFilePath', type=logs_path, help='Logs directory path')
    return parser.parse_args()
