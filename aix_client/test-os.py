#!/opt/bin/python3

# Python header
__author__ = "Benjamin Herson-Macarel"
#__copyright__ = ""
__credits__ = ["Who", "wants", "to", "be", "added", "???"]
__license__ = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"
__version__ = "1.21.12"
__maintainer__ = "Benjamin Herson-Macarel"
__email__ = "benjamin.herson-macarel-isc.france@ibm.com"
__status__ = "Stable"

# Imports
import os
import sys
import getopt
import time
import subprocess
import threading
import datetime
import socket
import ssl
import math
import json
import select
import re
import random
import signal
import traceback
import shutil
import logging

# The following are python packages from other developers. Dependencies need to be installed as a prerequisite
# requests for handling HTTP requets in efficient and simple way
import requests
from requests.exceptions import HTTPError
# Parsing ping results and get output in JSON (efficient and no time to waste developing the same...)
import pingparsing

# Classes

# Functions
def LoadDaemonConfig():
    """This function will get all the required parameters from config file and load them into vars   
    
    TODO: Describe the fcuntion, all vars and its content
    """
    # Switching vars to global
    global BaseDir
    global LogFilePath
    global ConfigFilePath
    global ELKMonitoringVersion
    global ECSVersion
    global ElasticServers
    global FilebeatServers
    global LogstashServers
    global ElasticPort
    global FilebeatPort
    global LogstashPort
    global ELKUsername
    global ELKPassword
    global ELKWebProtocol
    global ELKCertificate
    global ElasticIndexName
    global FilebeatIndexName
    global ElasticServersAvailable
    global FilebeatServersAvailable
    global LogstashServersAvailable
    global ElasticServersFailed
    global FilebeatServersFailed
    global LogstashServersFailed
    global FQDN
    global TailRefreshValue
    global CycleSleepTime
    global DiskSampleRate
    global TopProcesses
    global SystemProcessWaitValue
    global SystemFilesystemAndFstatWaitValue
    global SystemDiskIOWaitValue
    global SystemProcessSummaryWaitValue
    global SystemLoadWaitValue
    global SystemFcWaitValue
    global SystemSocketSummaryWaitValue
    global SystemSocketWaitValue
    global SystemMemoryWaitValue
    global SystemNetworkWaitValue
    global SystemCoreAndCpuWaitValue
    global IfSystemHPMStatEnable
    global IfSystemHypervisorEnable
    global SystemHPMStatWaitValue
    global SystemHypervisorWaitValue
    global ErrptLogWaitValue
    global PingPlotterTargets
    global PingPlotterWaitValue
    global PingSamples
    global PingTimeout
    global EntRestricted
    global FcsRestricted
    global HdiskRestricted
    global Tags
    global Tagz
    global Labels
    global BulkMaxSize
    global NMONSeq
    
    # Checking if Configuration file exists
    if os.path.exists(ConfigFilePath):
        # Executing with Try/Catch to handle any error in file
        try:
            with open(ConfigFilePath, 'r') as ConfigFile:
                # Loading JSOn file content
                JSONValues = json.load(ConfigFile)

                # Set variables for ELK server.
                ELKMonitoringVersion = JSONValues["ELKMonitoringVersion"]
                ECSVersion = JSONValues["ECSVersion"]
                ElasticServers = JSONValues["ElasticServers"]
                FilebeatServers = JSONValues["FilebeatServers"]
                LogstashServers = JSONValues["LogstashServers"]
                
                # Checking if Filebeat output is empty
                if len(FilebeatServers) == 0:
                    # Then defaulting to Metricbeat output
                    FilebeatServers = ElasticServers
                # Checking if Logstash output is empty
                if len(LogstashServers) == 0:
                    # Then defaulting to Metricbeat output
                    LogstashServers = ElasticServers
                
                ELKUsername = JSONValues["ELKUsername"]
                ELKPassword = JSONValues["ELKPassword"]
                ELKCertificate = JSONValues["ELKCertificate"]
                # Handling if ELKCertificate is empty
                if(len(ELKCertificate) == 0):
                    ELKCertificate = "True"
                ElasticPort = JSONValues["ElasticPort"]
                FilebeatPort = JSONValues["FilebeatPort"]
                LogstashPort = JSONValues["LogstashPort"]
                ELKWebProtocol = JSONValues["ELKWebProtocol"]
                # Duplicating *Servers to *ServersAvailable making all ELK servers failed by default
                ElasticServersAvailable = ElasticServers[:]
                ElasticServersFailed = []
                FilebeatServersAvailable = FilebeatServers[:]
                FilebeatServersFailed = []
                LogstashServersAvailable = LogstashServers[:]
                LogstashServersFailed = []
                ElasticIndexName = JSONValues["ElasticIndexName"]
                FilebeatIndexName = JSONValues["FilebeatIndexName"]
                
                # Setting NMON sequence counter to 0
                NMONSeq = 0

                # Script functional variables
                # Time to wait before refreshing tail's processes status (in seconds)
                TailRefreshValue = int(JSONValues["TailRefreshValue"])
                # Time to wait between two execution of the Main Loop (in seconds)
                CycleSleepTime = int(JSONValues["CycleSleepTime"])
                # How much time to run metric commands and get averaged results
                DiskSampleRate = int(JSONValues["DiskSampleRate"])
                # If different than 0, set the limit of processes that must be taken into account while checking TOP processes CPU activity
                TopProcesses = int(JSONValues["TopProcesses"])
                # Adding FQDN to the hostname if not existing, andd necessary...
                FQDN = JSONValues["FQDN"]
                # How much messages are sent within one connection to server
                BulkMaxSize = int(JSONValues["BulkMaxSize"])

                # Topic timers variables (in seconds)
                # Time to wait before sending new metric values to ELK server
                SystemProcessWaitValue = int(JSONValues["SystemProcessWaitValue"])
                SystemFilesystemAndFstatWaitValue = int(JSONValues["SystemFilesystemAndFstatWaitValue"])
                SystemDiskIOWaitValue = int(JSONValues["SystemDiskIOWaitValue"])
                SystemProcessSummaryWaitValue = int(JSONValues["SystemProcessSummaryWaitValue"])
                SystemLoadWaitValue = int(JSONValues["SystemLoadWaitValue"])
                SystemFcWaitValue = int(JSONValues["SystemFcWaitValue"])
                SystemSocketSummaryWaitValue = int(JSONValues["SystemSocketSummaryWaitValue"])
                SystemSocketWaitValue = int(JSONValues["SystemSocketWaitValue"])
                SystemMemoryWaitValue = int(JSONValues["SystemMemoryWaitValue"])
                SystemNetworkWaitValue = int(JSONValues["SystemNetworkWaitValue"])
                SystemCoreAndCpuWaitValue = int(JSONValues["SystemCoreAndCpuWaitValue"])
                
                # Loading PingPlotter targets and configuration values
                PingPlotterTargets = JSONValues["PingPlotterTargets"]
                PingPlotterWaitValue = int(JSONValues["PingPlotterWaitValue"])
                PingSamples = int(JSONValues["PingSamples"])
                PingTimeout = JSONValues["PingTimeout"]
                
                # Checking other JSON values linked to custom plugins
                IfSystemHPMStatEnable = JSONValues["IfSystemHPMStatEnable"]
                IfSystemHypervisorEnable = JSONValues["IfSystemHypervisorEnable"]
                SystemHPMStatWaitValue = int(JSONValues["SystemHPMStatWaitValue"])
                SystemHypervisorWaitValue = int(JSONValues["SystemHypervisorWaitValue"])
                ErrptLogWaitValue = int(JSONValues["ErrptLogWaitValue"])

                
                # Loading Tags
                Tags = JSONValues["tags"]
                
                # Generating tagz var for rollup purpose
                Tagz = ""
                for Tag in Tags:  
                    Tagz += Tag + ','
                Tagz = Tagz[:-1]
                
                # Loading Labels
                Labels = JSONValues["labels"]
                
                # Loading some parameter that can restrict the number of devices checked for some cases
                # Network Adapters
                EntRestricted = JSONValues["EntRestricted"]
                # Fiber Channel Adapters
                FcsRestricted = JSONValues["FcsRestricted"]
                # HDISK devices
                HdiskRestricted = JSONValues["HdiskRestricted"]
                
                # Checking if Proxy bypass is required
                BypassProxy = JSONValues["bypassproxy"]
                
                # Disabling proxy if requested
                if BypassProxy == 'yes':
                    os.environ['no_proxy'] = '*'
                
        except:
            # problem encountered while loading JSON daemon configuration file, exiting
            logging.info("            ==> Error while loading " + ConfigFilePath + " daemon config file !")
            logging.info("                Please check the Configuration file JSON parameters, format and validity")
            logging.info(str(traceback.print_exc()))
            traceback.print_exc()
            os._exit(2)
    else:
        # Daemon configuration file does not exist, exiting
        logging.info("            ==> Error while loading " + ConfigFilePath + " daemon config file !")
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

    # Using global FilebeatConfigsArray and CustomMetricsConfigsArray dictionary for follow up purpose
    global FilebeatConfigsArray
    global CustomMetricsConfigsArray
    global PingPlotterArray
    global TargetFileCurrentPosArray

    # Switching vars to global
    global ConfigFilePath
    
    # Defining config path from ConfigFilePath
    ConfigPathtmp = ConfigFilePath.split('/').pop()
    ConfigPath = ConfigFilePath.replace(ConfigPathtmp,'')

    # Loading filebeat plugin configs
    for f_name in os.listdir(ConfigPath):
        if f_name.endswith('filebeat.conf'):
            # Log
            logging.info("           " + f_name + ":")

            # Generating full path name for current file
            FullPathFileName = ConfigPath + f_name

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
                            TargetFileCurrentPosArray[f_name] = 0
                            
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
                        TargetFileCurrentPosArray[f_name] = 0

                    # Storing results into FilebeatConfigsArray dictionnary
                    ConfigString = CurrentTargetFile + ',' + JSONValues["TargetFile"] + ',' + PatternMatch + ',' + str(TargetFileLastLine) + ',' + str(TargetFileInode) + ',' + str(TargetFileSize) + ',' + str(JSONValues["MultilineSeparator"] + ',' + str(JSONValues["Output"]))
                    FilebeatConfigsArray[f_name] = ConfigString
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
    for f_name in os.listdir(ConfigPath):
        if f_name.endswith('custom.conf'):
            # Log
            logging.info("           " + f_name + ":")

            # Generating full path name for current file
            FullPathFileName = ConfigPath + f_name

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
                    ConfigString = JSONValues["OSScript"] + ',' + str(JSONValues["Refresh"]) + ',' + JSONValues["Output"]
                    CustomMetricsConfigsArray[f_name] = ConfigString
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
    for ping_dest in PingPlotterTargets.split(','):
        # Log
        logging.info("            * " + ping_dest)
    # Log
    logging.info("            ==> All Ping Check destinations are loaded !")
    pass

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
    global EphemeralID
    EphemeralID = MediumRandom + "-" + ShortRandom1 + "-" + ShortRandom2 + "-" + ShortRandom3 + "-" + LongRandom

def GetLPARInformations():
    """ Get necessary LPAR informations.
        All those values are used to format JSON messages sent to ELK.

        FQDN:
        Adding DNS suffix on hostname which doesn't have one.

        LPARArch and AIXVersion:
        Get LPAR AIX version and Power architecture (Power8/7/6+).

        NetworkCards:
        List of network cards is taken from "ifconfig -a" OS command.

        FcCards:
        List of Fiber Channel cards which are correctly connected and linked.

        IDs:
        LPARRndID is fixed across reboot. Defined one time if ID file does not exist.
        AgentID is fixed across reboot. Defined one time if ID file does not exist.
        EphemeralID is generated on each daemon execution and generated by 'GenerateEphemeralID' method.

        NumProc:
        Define the number of CPU threads available on LPAR.
    """

    # Switching vars to global
    global BaseDir
    global LPARName
    global LPARSMTMode
    global LPARArch
    global LPARHost
    global AIXVersion
    global LPARRndID
    global AgentID
    global NetworkCards
    global FcCards
    # FcCards list need to be formated before being used
    FcCards = []
    global NumProc
    global NumProcString
    global IfVIOS
    global Tags
    global Tagz
    global Labels

    # Checking if LPAR name contains DNS suffix. Adding if not
    # Checking first if var FQDN is not null
    if FQDN != "":
        if not FQDN in LPARName:
            LPARName = LPARName + FQDN

    # Log
    logging.info(" - Checking LPAR hostname... Done !")

    # Get LPAR hardware architecture
    CmdLine = "prtconf | egrep \"Processor Type|Serial Number\" | awk '{print $NF}'"
    LPARPrtConf =  subprocess.Popen(CmdLine, shell=True, stdout=subprocess.PIPE).stdout
    LPARPrtConf = LPARPrtConf.read().decode().split('\n')
    LPARArch = LPARPrtConf[1]
    LPARHost = LPARPrtConf[0]
    
    
    # Disabled for now as hosting frame has been moved to labels
    # Tags.append(LPARHost)
    # Tagz = Tagz + ',' + LPARHost
    
    # Adding hosting frame to Labels list
    LabelHostStr = 'powersn:' + str(LPARHost)
    Labels.append(LabelHostStr)
    
    # Log
    logging.info(" - Checking LPAR Architecture... Done !")
    
    # Get LPAR AIX OS Version
    AIXVersion =  subprocess.Popen("oslevel -s", shell=True, stdout=subprocess.PIPE).stdout
    AIXVersion =  AIXVersion.read().decode().replace("\n","")
    
    # Checking if LPAR or VIOS
    if os.path.exists("/usr/ios/cli/ioscli"):
        IfVIOS = True
    else:
        IfVIOS = False

    # Log
    logging.info(" - Checking LPAR AIX version ... Done !")
    
    # Get current SMT mode  
    LPARSMTModeCmdLine = "smtctl | grep has | awk '{print $3}' | head -1"    
    LPARSMTMode =  subprocess.Popen(LPARSMTModeCmdLine, shell=True, stdout=subprocess.PIPE).stdout
    LPARSMTMode =  LPARSMTMode.read().decode().replace("\n","")
    
    # Defining config path from ConfigFilePath
    ConfigPathtmp = ConfigFilePath.split('/').pop()
    ConfigPath = ConfigFilePath.replace(ConfigPathtmp,'')

    
    # Defining LPAR ID file name
    RandomIDFile = ConfigPath + 'Host.ID'

    # If LPAR ID file exists, let's get content as defined scripts vars
    if os.path.exists(RandomIDFile):
        # Get LPAR Unique ID
        # IMPROVEMENT / Can be converted into python style
        LPARRndIDCmd = "cat " + RandomIDFile + " | grep LPARRndID | awk '{print $2}'"
        LPARRndID = subprocess.Popen(LPARRndIDCmd, shell=True, stdout=subprocess.PIPE).stdout
        LPARRndID = LPARRndID.read().decode().replace('\r','')
        LPARRndID = LPARRndID.replace('\n','')
        # Get LPAR ephemeral ID
        # IMPROVEMENT / Can be converted into python style
        AgentIDCmd = "cat " + RandomIDFile + " | grep AgentID | awk '{print $2}'"
        AgentID = subprocess.Popen(AgentIDCmd, shell=True, stdout=subprocess.PIPE).stdout
        AgentID = AgentID.read().decode().replace('\r','')
        AgentID = AgentID.replace('\n','')

    # If not, let's create it, fill it and define scripts vars
    else:
        # Generating LPAR ID in specific format
        # IMPROVEMENT / Can be converted into python style
        LPARRndID = subprocess.Popen("cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 32 | head -n 1", shell=True, stdout=subprocess.PIPE).stdout
        LPARRndID = LPARRndID.read().decode().replace("\n","")

        # Generating unique formated ID for uniqueAgent ID value
        # as it is same format than ephemeral ID
        GenerateEphemeralID()
        AgentID = EphemeralID

        # Creating the LPAR ID file
        OpenedFile = open(RandomIDFile,"w+")

        # Filling it with data
        OpenedFile.write("LPARRndID ")
        OpenedFile.write(LPARRndID)
        OpenedFile.write("\r\n")
        OpenedFile.write("AgentID ")
        OpenedFile.write(AgentID)
        OpenedFile.write("\r\n")

        # Close the LPAR ID file
        OpenedFile.close()

    # Generating unique and ephemeral ID for current script execution
    GenerateEphemeralID()

    # Log
    logging.info(" - Checking LPAR Metricbeat unique ID... Done !")

    # Defining the name of network adapters
    if EntRestricted == 'all':
        # No restriction, taking all network adapters
        NetworkCards = subprocess.Popen("ifconfig -a | grep ': ' | awk -F ':' '{print $1}' | grep -v 'lo0'", shell=True, stdout=subprocess.PIPE).stdout
        NetworkCards = NetworkCards.read().decode().split('\n')
        if IfVIOS:
            # Detecting SEA adapters
            NetworkCardsSEA = subprocess.Popen("lsdev -Cc adapter | grep 'Shared Ethernet Adapter' | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout
            NetworkCardsSEA = NetworkCardsSEA.read().decode().split('\n')
            # Adding SEA to the list of monitored adapters
            NetworkCards = NetworkCards + NetworkCardsSEA
    else:
        # Restriction are specified. Setting Network card list to the given list
        NetworkCards = []
        NetworkCards = EntRestricted.split(',')
    
    # Log
    logging.info(" - Checking LPAR Network interface list ... Done !")

    # Defining the name of FC adapters
    if FcsRestricted == 'all':
        FCCardsTemp = subprocess.Popen("lsdev -Cc adapter | grep fcs | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout
        FCCardsTemp = FCCardsTemp.read().decode().split('\n')
    else:
        # Restriction are specified. Setting Network card list to the given list
        FCCardsTemp = []
        FCCardsTemp = FcsRestricted.split(',')

    # Log
    logging.info(" - Checking LPAR FC interface list ... Done !")

    # Checking FC link status and exclude unlinked cards
    for CurrLine in FCCardsTemp:
        if(len(CurrLine) != 0):
            FCCardFcStatCmd = "fcstat " + CurrLine
            FCCardFcStatState = subprocess.Popen(FCCardFcStatCmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            stdout, stderr = FCCardFcStatState.communicate()
            # If link is ok, adding the FC card into definitive array
            if(FCCardFcStatState.returncode == 0):
                FcCards.append(CurrLine)

    # Log
    logging.info(" - Checking LPAR FC link status... Done !")

    # Defining number of CPU threads
    NumProc = subprocess.Popen("bindprocessor -q | awk '{print $NF}'", shell=True, stdout=subprocess.PIPE).stdout
    NumProc = NumProc.read().decode().split()
    NumProc = int(NumProc[0]) + 1
    NumProcString = str(NumProc)

    # Log
    logging.info(" - Checking LPAR CPU configuration... Done !")
    
    # Generate fix JSON values for LPAR
    GenerateStaticJSON()

def CompareTimer(TimedTopic, MetricsWaitValue, CustomMetric = ''):
    """ This function compare the last execution time and the specific timer for an element.
        If Timer is reached, the function return True and will trigger the underlying function.

        - TimedTopic is the metric on which the timer needed to be checked
        - MetricsWaitValue is the number of seconds to wait before work for metric is triggered
    """

    # Using global ExecutionTimers dictionary for follow up purpose
    global ExecutionTimers
    global devnull

    # Get current timestamp
    CurrentTimer = datetime.datetime.now()

    # Try/Catch to avoid errors on non defined dictionary entrie / First execution
    try:
        # Dictionary entrie is not empty
        # Get last execution date/time
        LastTopicExecTime = ExecutionTimers[TimedTopic]

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
        ExecutionTimers[TimedTopic] = datetime.datetime.now()
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
        return devnull

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

def GenerateStaticJSON():
    """This function generate a static JSON message containing the pieces that will remain unchange until daemon restart
    
    Please refer to README.md
    
    TODO: Describe the function, all vars and its content
    """
    
    global StaticJSON
    global StaticJSONFilebeat
    
    # Define tags for metricbeat
    JSONTags=(''
    '\"tags\": ' + str(Tags).replace('\'','"') + ','
    '\"rollup\":{\"tagz\": \"' + str(Tagz) + '\",\"hostname\":\"' + LPARName + '\"},')
    
    # Define rollup tags for filebeat (adding extra tagz and hostname field with rolled-up naming convention for easy use in dashboard)
    JSONTagsFilebeat=(''
    '\"tags\": ' + str(Tags).replace('\'','"') + ','
    '\"rollup\":{\"tagz\":{\"terms\":{\"value\": \"' + str(Tagz) + '\"}},\"hostname\":{\"terms\":{\"value\": \"' + LPARName + '\"}}},')
    
    # Define Agent JSON for metricbeat
    JSONAgent = (''
    '\"agent\":{'
    '\"version\":\"' + ELKMonitoringVersion + '\",'
    '\"type\":\"metricbeat\",'
    '\"ephemeral_id\":\"' + EphemeralID + '\",'
    '\"hostname\":\"' + LPARName + '\",'
    '\"id\":\"' + AgentID + '\"'
    '},')
    
    # Define Agent JSON for filebeat
    JSONAgentFilebeat = (''
    '\"agent\":{'
    '\"version\":\"' + ELKMonitoringVersion + '\",'
    '\"type\":\"filebeat\",'
    '\"ephemeral_id\":\"' + EphemeralID + '\",'
    '\"hostname\":\"' + LPARName + '\",'
    '\"id\":\"' + AgentID + '\"'
    '},')
    
    # Checking if LPAR is a VIOS
    if IfVIOS:
        OSFamily = 'VIOS'
    else:
        OSFamily = 'AIX'
        
    # Define Host JSON for metricbeat
    JSONHost = (''
    '\"host\":{'
    '\"name\":\"' + LPARName + '\",'
    '\"hostname\":\"' + LPARName + '\",'
    '\"architecture\":\"' + LPARArch + '\",'
    '\"id\":\"' + LPARRndID + '\",'
    '\"containerized\":false,'
    '\"os\":{'
    '\"platform\":\"AIX\",'
    '\"version\":\"' + AIXVersion + '\",'
    '\"family\":\"' + OSFamily + '\",'
    '\"name\":\"AIX\",'
    '\"kernel\":\"' + AIXVersion + '\",'
    '\"codename\":\"AIX\"'
    '}},')

    # Define ECS JSON
    JSONEcs = (''
    '\"ecs\":{'
    '\"version\":\"' + ECSVersion + '\"'
    '},')
    
    # Generating labels JSON with key/value pairs
    LabelString = '\"labels\":{'
    for Label in Labels:
        if len(Label) != 0:
            LabelString += '\"' + Label.replace(':','\":\"') + '\",'
        
    LabelString = LabelString[:-1]
    LabelString += '}'
	
    StaticJSON = JSONTags + JSONAgent + JSONHost + JSONEcs + LabelString
    StaticJSONFilebeat = JSONTagsFilebeat + JSONAgentFilebeat + JSONHost + JSONEcs + LabelString
    
    # print(StaticJSON)

    pass

def GenerateDynamicJson(EventDataset, ServiceType, MetricSet, ComparisonTimer):
    """This function generate a static JSON message containing the pieces that will change for each message
    
    Please refer to README.md
    
    TODO: Describe the function, all vars and its content
    """
    JSONServiceType = (''
    '\"service\":{'
    '\"type\":\"' + ServiceType + '\"'
    '},')

    JSONEventDataset = (''
    '\"event\":{'
    '\"module\":\"' + ServiceType + '\",'
    '\"duration\":' + ComparisonTimer + ','
    '\"dataset\":\"' + EventDataset + '\"'
    '},')

    JSONMetricSet = (''
    '\"metricset\":{'
    '\"name\":\"' + MetricSet + '\",'
    '\"period\":1'
    '}')
    
    DynamicJSON = JSONServiceType + JSONEventDataset + JSONMetricSet

    return DynamicJSON

def CheckServers():
    """ This function check the state of the Metricbeat Elasticsearch server.

        It also handles the retransmit queues for Metricbeat and Filebeat items.
        On each script loop execution, it will resend some queued messages up to a given number.
        
    Please refer to README.md
    
    TODO: Describe the function, all vars and its content
    """

    # Setting global vars
    global SendQueueArray
    global FilebeatSendQueueArray
    global LogstashSendQueueArray
    global ELKUsername
    global ELKPassword
    global ElasticServers
    global FilebeatServers
    global LogstashServers
    global ElasticPort
    global FilebeatPort
    global LogstashPort
    global ELKCertificate
    global ElasticServersAvailable
    global ElasticServersFailed
    global FilebeatServersAvailable
    global FilebeatServersFailed
    global LogstashServersAvailable
    global LogstashServersFailed
    global ElasticIndexName
    global FilebeatIndexName
    global ELKUsername
    global ELKPassword
    global ElasticServerCnx
    global FilebeatServerCnx
    global LogstashServerCnx
    global AllElasticServersFailedDate
    global AllFilebeatServersFailedDate
    global AllLogstashServersFailedDate
    global MetricbeatQueueFlushed
    global FilebeatQueueFlushed
    global LogstashQueueFlushed
    global BulkMaxSize
    
    # Checking for unavailable Elastic servers
    if len(ElasticServersFailed) != 0:
                        
        # Choosing randomly one Elastic server in the failed pool
        ElasticServer = random.choice(ElasticServersFailed)
        
        # If ElasticServer server is unavailable, we send a get request
        try:
            # Defining URL and credentials for web request
            ELKCreds = (ELKUsername, ELKPassword)
            ElasticServerURL = ELKWebProtocol + '://' + ElasticServer + ':' + ElasticPort + '/'
            
            # Connect and send encoded JSON message     
            ElasticServerCnx = requests.session()
            ELKAnswer = ElasticServerCnx.get(ElasticServerURL, auth=ELKCreds, timeout=5, verify=ELKCertificate)

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
                ElasticServersFailed.remove(ElasticServer)
                ElasticServersAvailable.append(ElasticServer)
                logging.info("INFO     ==> " + ElasticServer +  " is Online ! Processing Metricbeat messages on this server")
            except:
                # Nothing to do
                pass

    # Checking for unavailable Filebeat servers
    if len(FilebeatServersFailed) != 0:
             
        # Choosing randomly one Filebeat server in the failed pool
        FilebeatServer = random.choice(FilebeatServersFailed)
        
        # If FilebeatServer server is unavailable, we send a get request
        try:
            # Defining URL and credentials for web request
            ELKCreds = (ELKUsername, ELKPassword)
            FilebeatServerURL = ELKWebProtocol + '://' + FilebeatServer + ':' + FilebeatPort + '/'
            
            # Connect and send encoded JSON message     
            FilebeatServerCnx = requests.session()
            ELKAnswer = FilebeatServerCnx.get(FilebeatServerURL, auth=ELKCreds, timeout=5, verify=ELKCertificate)

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
                FilebeatServersFailed.remove(FilebeatServer)
                FilebeatServersAvailable.append(FilebeatServer)
                logging.info("INFO     ==> " + FilebeatServer +  " is Online ! Processing Filebeat messages on this server")
            except:
                # Nothing to do
                pass

    # Checking for unavailable Logstash servers
    if len(LogstashServersFailed) != 0:
                        
        # Choosing randomly one Logstash server in the failed pool
        LogstashServer = random.choice(LogstashServersFailed)
        
        # If LogstashServer server is unavailable, we send a get request
        try:
            # Defining URL and credentials for web request
            ELKCreds = (ELKUsername, ELKPassword)
            LogstashServerURL = ELKWebProtocol + '://' + LogstashServer + ':' + LogstashPort + '/'
            
            # Connect and send encoded JSON message
            LogstashServerCnx = requests.session()

            ELKAnswer = LogstashServerCnx.get(LogstashServerURL, auth=ELKCreds, timeout=5, verify=ELKCertificate)
            
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
                LogstashServersFailed.remove(LogstashServer)
                LogstashServersAvailable.append(LogstashServer)
                logging.info("INFO     ==> " + LogstashServer +  " is Online ! Processing Logstash messages on this server")
            except:
                # Nothing to do
                pass
 
    # Checking if queued messages need to be sent in SendQueueArray and if one Elastic servers are available
    if (len(SendQueueArray) > 0 and MetricbeatQueueFlushed == False and len(ElasticServersAvailable) > 0):
        # If one Elastic server is available, we flush the current queue as messages are too old
        SendJSON('Flush', 'Metricbeat')
        # Logstring = 'INFO ==> Sending order to flush ' + str(len(SendQueueArray)) + ' JSON Metricbeat messages'
        # logging.info(Logstring)
        
    if (len(FilebeatSendQueueArray) > 0 and FilebeatQueueFlushed == False and len(FilebeatServersAvailable) > 0):
        # If one Filebeat server is available, we flush the current queue as messages are too old
        SendJSON('Flush', 'Filebeat')
        # Logstring = 'INFO ==> Sending order to flush ' + str(len(FilebeatSendQueueArray)) + ' JSON Filebeat messages'
        # logging.info(Logstring)
        
    if (len(LogstashSendQueueArray) > 0 and LogstashQueueFlushed == False and len(LogstashServersAvailable) > 0):
        # If one Logstash server is available, we flush the current queue as messages are too old
        SendJSON('Flush', 'Logstash')
        # Logstring = 'INFO ==> Sending order to flush ' + str(len(LogstashSendQueueArray)) + ' JSON Logstash messages'
        # logging.info(Logstring)
        
    # Logging messages about queue states
    if (len(SendQueueArray) > BulkMaxSize or len(ElasticServersAvailable) == 0):
        LogString = "WARNING  ==>  " + str(len(SendQueueArray)) + " Metricbeat historical JSON messages queued"
        logging.info(LogString)
    if (len(FilebeatSendQueueArray) > BulkMaxSize or len(FilebeatServersAvailable) == 0):
        LogString = "WARNING  ==>  " + str(len(FilebeatSendQueueArray)) + " Filebeat historical JSON messages queued"
        logging.info(LogString)
    if (len(LogstashSendQueueArray) > BulkMaxSize or len(LogstashServersAvailable) == 0):
        LogString = "WARNING  ==>  " + str(len(LogstashSendQueueArray)) + " Logstash historical JSON messages queued"
        logging.info(LogString)
        
    # Finally, reseting Queue Flush states
    MetricbeatQueueFlushed = False
    FilebeatQueueFlushed = False
    LogstashQueueFlushed = False

def SendToMetricbeat(BulkJSON, BulkSize):
    """ This function send a JSON message to the Metricbeat Logstash server.
        If Logstash is not available, the JSON message is queued for further reprocessing.
        
        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    # Setting global vars
    global SendQueueArray
    global FilebeatSendQueueArray
    global LogstashSendQueueArray
    global ELKCreds
    global ElasticServers
    global FilebeatServers
    global LogstashServers
    global ElasticServersAvailable
    global ElasticServersFailed
    global FilebeatServersAvailable
    global FilebeatServersFailed
    global LogstashServersAvailable
    global LogstashServersFailed
    global ElasticPort
    global FilebeatPort
    global LogstashPort
    global ELKCertificate
    global ELKWebProtocol
    global ElasticIndexName
    global FilebeatIndexName
    global ElasticServerCnx
    global FilebeatServerCnx
    global LogstashServerCnx
    global BulkMaxSize
    global MetricbeatQueueFlushed
    global FilebeatQueueFlushed
    global LogstashQueueFlushed


    # Choosing one availale Elastic server in the pool, if Message bucket is fill enough
    ElasticServer = random.choice(ElasticServersAvailable)
    # print('Elastic server choosen: ', ElasticServer)
    # print('Available list: ', ElasticServersAvailable)

    # Send Data to Elastic server with a Try/Catch
    try:
        # Define ELK url depending of index and choosen Elastic server
        CurrentIndex = ElasticIndexName + '-' + ELKMonitoringVersion
        ElasticServerURL = ELKWebProtocol + '://' + ElasticServer + ':' + ElasticPort + '/' + CurrentIndex + '/_bulk'
        
        # Defining credential for web request
        ELKCreds = (ELKUsername, ELKPassword)

        # Connect and send encoded data
        ELKAnswer = ElasticServerCnx.post(ElasticServerURL, data = BulkJSON.encode("utf8"), headers={"Content-Type" : "application/x-ndjson; charset=utf-8"}, auth=ELKCreds, timeout=5, verify=ELKCertificate)

        # If the response was successful, no Exception will be raised
        ELKAnswer.raise_for_status()

        # print('DEBUG: ELK Answer: ', str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Removing those successfully sent messages from queue
        del SendQueueArray[0:BulkSize]
            

    except HTTPError as http_err:
        # We received HTTP exception
        # Elastic server has fall down, queing message and setting Elastic server as unavailable
        try:
            ElasticServersAvailable.remove(ElasticServer)
            ElasticServersFailed.append(ElasticServer)
        except:
            # Nothing to do, server already removed
            # traceback.print_exc()
            pass
            
        # Log
        logging.info("WARNING  ==> " + ElasticServer +  " became unvailable, queueing Metricbeat JSON messages")
        # print(str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Creating the error stack file and filling error stack informations
        with open(CrashDumpSendLog, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(http_err))
            f.write(traceback.format_exc())
            # f.write('\nJSON message:\n')
            # f.write(JSONToSend)
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('WARNING  ==> Please check ' + CrashDumpSendLog + ' for more informations on HTTP errors')
        # traceback.print_exc()
        
    except Exception as err:
        # We received another type of exception
        # Elastic server has fall down, queing message and setting Elastic server as unavailable
        # Making that into a try/catch because some background threads can act on that also and clea the content
        try:
            ElasticServersAvailable.remove(ElasticServer)
            ElasticServersFailed.append(ElasticServer)
        except:
            # Nothing to do, server already removed
            # traceback.print_exc()
            pass
        
        # Log
        logging.info("WARNING  ==> " + ElasticServer +  " became unvailable, queueing Metricbeat JSON messages")
        # print(str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Creating the error stack file and filling error stack informations
        with open(CrashDumpSendLog, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(err))
            f.write(traceback.format_exc())
            # f.write('\nJSON message:\n')
            # f.write(JSONToSend)
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('WARNING  ==> Please check ' + CrashDumpSendLog + ' for more informations on HTTP errors')
        # traceback.print_exc()
        pass
 
def SendToFilebeat(BulkJSON, BulkSize):
    """ This function send a JSON message to the Metricbeat Logstash server.
        If Logstash is not available, the JSON message is queued for further reprocessing.
        
        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    # Setting global vars
    global SendQueueArray
    global FilebeatSendQueueArray
    global LogstashSendQueueArray
    global ELKCreds
    global ElasticServers
    global FilebeatServers
    global LogstashServers
    global ElasticServersAvailable
    global ElasticServersFailed
    global FilebeatServersAvailable
    global FilebeatServersFailed
    global LogstashServersAvailable
    global LogstashServersFailed
    global ElasticPort
    global FilebeatPort
    global LogstashPort
    global ELKCertificate
    global ELKWebProtocol
    global ElasticIndexName
    global FilebeatIndexName
    global ElasticServerCnx
    global FilebeatServerCnx
    global LogstashServerCnx
    global BulkMaxSize
    global MetricbeatQueueFlushed
    global FilebeatQueueFlushed
    global LogstashQueueFlushed


    # Choosing one availale Filebeat server in the pool, if Message bucket is fill enough
    FilebeatServer = random.choice(FilebeatServersAvailable)
    # print('Filebeat server choosen: ', FilebeatServer)
    # print('Available list: ', FilebeatServersAvailable)

    # Send Data to Filebeat server with a Try/Catch
    try:
        # Define ELK url depending of index and choosen Filebeat server
        CurrentIndex = FilebeatIndexName + '-' + ELKMonitoringVersion
        FilebeatServerURL = ELKWebProtocol + '://' + FilebeatServer + ':' + FilebeatPort + '/' + CurrentIndex + '/_bulk'
        
        # Defining credential for web request
        ELKCreds = (ELKUsername, ELKPassword)

        # Connect and send encoded data
        ELKAnswer = FilebeatServerCnx.post(FilebeatServerURL, data = BulkJSON.encode("utf8"), headers={"Content-Type" : "application/x-ndjson; charset=utf-8"}, auth=ELKCreds, timeout=5, verify=ELKCertificate)

        # If the response was successful, no Exception will be raised
        ELKAnswer.raise_for_status()

        # print('DEBUG: ELK Answer: ', str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Removing those successfully sent messages from queue
        del FilebeatSendQueueArray[0:BulkSize]
        

    except HTTPError as http_err:
        # We received HTTP exception
        # Filebeat server has fall down, queing message and setting Filebeat server as unavailable
        try:
            FilebeatServersAvailable.remove(FilebeatServer)
            FilebeatServersFailed.append(FilebeatServer)
        except:
            # Nothing to do, server already removed
            # traceback.print_exc()
            pass
            
        # Log
        logging.info("WARNING  ==> " + FilebeatServer +  " became unvailable, queueing Filebeat JSON messages")
        # print(str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Creating the error stack file and filling error stack informations
        with open(CrashDumpSendLog, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(http_err))
            f.write(traceback.format_exc())
            # f.write('\nJSON message:\n')
            # f.write(JSONToSend)
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('WARNING  ==> Please check ' + CrashDumpSendLog + ' for more informations on HTTP errors')
        # traceback.print_exc()
        
    except Exception as err:
        # We received another type of exception
        # Filebeat server has fall down, queing message and setting Filebeat server as unavailable
        # Making that into a try/catch because some background threads can act on that also and clea the content
        try:
            FilebeatServersAvailable.remove(FilebeatServer)
            FilebeatServersFailed.append(FilebeatServer)
        except:
            # Nothing to do, server already removed
            # traceback.print_exc()
            pass
        
        # Log
        logging.info("WARNING  ==> " + FilebeatServer +  " became unvailable, queueing Filebeat JSON messages")
        
        # print(str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Creating the error stack file and filling error stack informations
        with open(CrashDumpSendLog, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(err))
            f.write(traceback.format_exc())
            # f.write('\nJSON message:\n')
            # f.write(JSONToSend)
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('WARNING  ==> Please check ' + CrashDumpSendLog + ' for more informations on HTTP errors')
        # traceback.print_exc()
        pass

def SendToLogstash(BulkJSON, BulkSize):
    """ This function send a JSON message to the Metricbeat Logstash server.
        If Logstash is not available, the JSON message is queued for further reprocessing.
        
        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    # Setting global vars
    global SendQueueArray
    global FilebeatSendQueueArray
    global LogstashSendQueueArray
    global ELKCreds
    global ElasticServers
    global FilebeatServers
    global LogstashServers
    global ElasticServersAvailable
    global ElasticServersFailed
    global FilebeatServersAvailable
    global FilebeatServersFailed
    global LogstashServersAvailable
    global LogstashServersFailed
    global ElasticPort
    global FilebeatPort
    global LogstashPort
    global ELKCertificate
    global ELKWebProtocol
    global ElasticIndexName
    global FilebeatIndexName
    global ElasticServerCnx
    global FilebeatServerCnx
    global LogstashServerCnx
    global BulkMaxSize
    global MetricbeatQueueFlushed
    global FilebeatQueueFlushed
    global LogstashQueueFlushed


    # Choosing one availale Logstash server in the pool, if Message bucket is fill enough
    LogstashServer = random.choice(LogstashServersAvailable)
    # print('Logstash server choosen: ', LogstashServer)
    # print('Available list: ', LogstashServersAvailable)

    # Send Data to Logstash server with a Try/Catch
    try:
        # Define ELK url depending of index and choosen Logstash server
        LogstashServerURL = ELKWebProtocol + '://' + LogstashServer + ':' + LogstashPort + '/_bulk'
        
        # Defining credential for web request
        ELKCreds = (ELKUsername, ELKPassword)

        # Connect and send encoded data
        ELKAnswer = LogstashServerCnx.post(LogstashServerURL, data = BulkJSON.encode("utf8"), headers={"Content-Type" : "application/x-ndjson; charset=utf-8"}, auth=ELKCreds, timeout=5, verify=ELKCertificate)

        # If the response was successful, no Exception will be raised
        ELKAnswer.raise_for_status()

        # print('DEBUG: ELK Answer: ', str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Removing those successfully sent messages from queue
        del LogstashSendQueueArray[0:BulkSize]

    except HTTPError as http_err:
        # We received HTTP exception
        # Logstash server has fall down, queing message and setting Logstash server as unavailable
        try:
            LogstashServersAvailable.remove(LogstashServer)
            LogstashServersFailed.append(LogstashServer)
        except:
            # Nothing to do, server already removed
            # traceback.print_exc()
            pass
            
        # Log
        logging.info("WARNING  ==> " + LogstashServer +  " became unvailable, queueing Logstash JSON messages")
        # print(str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Creating the error stack file and filling error stack informations
        with open(CrashDumpSendLog, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(http_err))
            f.write(traceback.format_exc())
            # f.write('\nJSON message:\n')
            # f.write(JSONToSend)
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('WARNING  ==> Please check ' + CrashDumpSendLog + ' for more informations on HTTP errors')
        # traceback.print_exc()
        
    except Exception as err:
        # We received another type of exception
        # Logstash server has fall down, queing message and setting Logstash server as unavailable
        # Making that into a try/catch because some background threads can act on that also and clea the content
        try:
            LogstashServersAvailable.remove(LogstashServer)
            LogstashServersFailed.append(LogstashServer)
        except:
            # Nothing to do, server already removed
            # traceback.print_exc()
            pass
        
        # Log
        logging.info("WARNING  ==> " + LogstashServer +  " became unvailable, queueing Logstash JSON messages")
        
        # print(str(ELKAnswer))
        # print(str(ELKAnswer.text))
        
        # Creating the error stack file and filling error stack informations
        with open(CrashDumpSendLog, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(err))
            f.write(traceback.format_exc())
            # f.write('\nJSON message:\n')
            # f.write(JSONToSend)
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('WARNING  ==> Please check ' + CrashDumpSendLog + ' for more informations on HTTP errors')
        # traceback.print_exc()
        pass
 
def SendJSON(JSONToSend, MesssageOutput = 'Metricbeat'):
    """ This function send a JSON message to the Metricbeat Logstash server.
        If Logstash is not available, the JSON message is queued for further reprocessing.
        
        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    # Setting global vars
    global SendQueueArray
    global FilebeatSendQueueArray
    global LogstashSendQueueArray
    global ELKCreds
    global ElasticServers
    global FilebeatServers
    global LogstashServers
    global ElasticServersAvailable
    global ElasticServersFailed
    global FilebeatServersAvailable
    global FilebeatServersFailed
    global LogstashServersAvailable
    global LogstashServersFailed
    global ElasticPort
    global FilebeatPort
    global LogstashPort
    global ELKCertificate
    global ELKWebProtocol
    global ElasticIndexName
    global FilebeatIndexName
    global ElasticServerCnx
    global FilebeatServerCnx
    global LogstashServerCnx
    global BulkMaxSize
    global MetricbeatQueueFlushed
    global FilebeatQueueFlushed
    global LogstashQueueFlushed
      
    ### Metricbeat Pool
    if MesssageOutput == 'Metricbeat':

        # Checking if JSON message need to be queued or sent
        if (ElasticServersAvailable and len(SendQueueArray) >= BulkMaxSize and JSONToSend != 'Flush'):

            # Checking if history messages are in the queue
            if len(SendQueueArray) == BulkMaxSize:
                # No historical message present
                if BulkMaxSize <= 1:
                    # If BulkMaxSize is 0 or 1, we sent the JSON message directly
                    BulkJSON = '\n{ "index":{} }\n' + JSONToSend + '\n'
                        
                else:
                    # Creating Bulk JSON message
                    separator = '\n{ "index":{} }\n'
                    BulkJSON = '{ "index":{} }\n' + str(separator.join(SendQueueArray[0:BulkMaxSize])) + '\n'
                    BulkSize = BulkMaxSize
                    
                    # Queuing the current message from function call, waiting for next loop execution
                    SendQueueArray.append(JSONToSend)
                    
            else:
                # Historical messages are queued, let's send them one by one to the current message
                # Creating Bulk JSON message
                BulkJSON = '{ "index":{} }\n' + str(SendQueueArray[0]) + '\n{ "index":{} }\n' + JSONToSend + '\n' 
                BulkSize = 1
            
            # Recording that queue has been flushed, or tried to
            MetricbeatQueueFlushed = True
            SendToMetricbeat(BulkJSON, BulkSize)

        else:
            # Checking if flush order has been sent
            if JSONToSend == 'Flush':
                # Creating Bulk JSON message and flushing the queue content
                if BulkMaxSize <= 1:
                    # If BulkMaxSize is 0 or 1, we sent the message directly
                    BulkJSON = '\n{ "index":{} }\n' + SendQueueArray[0] + '\n'
                    
                    # Log
                    # LogString = "INFO  ==>  " + str(len(SendQueueArray)) + " JSON Metricbeat messages has been FORCE flushed"
                    # logging.info(LogString)
                    
                    # Recording that queue has been flushed, or tried to
                    MetricbeatQueueFlushed = True
                    SendToMetricbeat(BulkJSON, 1)

                else:
                    # Checking for the correct size of the flush
                    if len(SendQueueArray) > BulkMaxSize:
                        BulkSize = BulkMaxSize
                    else:
                        BulkSize = len(SendQueueArray)
                    
                    separator = '\n{ "index":{} }\n'
                    BulkJSON = '{ "index":{} }\n' + str(separator.join(SendQueueArray[0:len(SendQueueArray)])) + '\n'
                    
                    # Log
                    # LogString = "INFO  ==>  " + str(len(SendQueueArray)) + " JSON Metricbeat messages has been flushed"
                    # logging.info(LogString)
                    
                    # Recording that queue has been flushed, or tried to
                    MetricbeatQueueFlushed = True
                    SendToMetricbeat(BulkJSON, BulkSize)
                    
                    
   
            else:                
                # No Elastic server available or Bulk max size not reached, waiting for next loop
                SendQueueArray.append(JSONToSend)
            
    ### Filebeat Pool
    if MesssageOutput == 'Filebeat':

        # Checking if JSON message need to be queued or sent
        if (FilebeatServersAvailable and len(FilebeatSendQueueArray) >= BulkMaxSize and JSONToSend != 'Flush'):

            # Checking if history messages are in the queue
            if len(FilebeatSendQueueArray) == BulkMaxSize:
                # No historical message present
                if BulkMaxSize <= 1:
                    # If BulkMaxSize is 0 or 1, we sent the JSON message directly
                    BulkJSON = '\n{ "index":{} }\n' + JSONToSend + '\n'
                        
                else:
                    # Creating Bulk JSON message
                    separator = '\n{ "index":{} }\n'
                    BulkJSON = '{ "index":{} }\n' + str(separator.join(FilebeatSendQueueArray[0:BulkMaxSize])) + '\n'
                    BulkSize = BulkMaxSize
                    
                    # Queuing the current message from function call, waiting for next loop execution
                    FilebeatSendQueueArray.append(JSONToSend)
                    
            else:
                # Historical messages are queued, let's send them one by one to the current message
                # Creating Bulk JSON message
                BulkJSON = '{ "index":{} }\n' + str(FilebeatSendQueueArray[0]) + '\n{ "index":{} }\n' + JSONToSend + '\n' 
                BulkSize = 1
            
            # Recording that queue has been flushed, or tried to
            FilebeatQueueFlushed = True
            SendToFilebeat(BulkJSON, BulkSize)

        else:
            # Checking if flush order has been sent
            if JSONToSend == 'Flush':
                # Creating Bulk JSON message and flushing the queue content
                if BulkMaxSize <= 1:
                    # If BulkMaxSize is 0 or 1, we sent the message directly
                    BulkJSON = '\n{ "index":{} }\n' + FilebeatSendQueueArray[0] + '\n'
                    
                    # Log
                    # LogString = "INFO  ==>  " + str(len(FilebeatSendQueueArray)) + " JSON Filebeat messages has been FORCE flushed"
                    logging.info(LogString)
                    
                    # Recording that queue has been flushed, or tried to
                    FilebeatQueueFlushed = True
                    SendToFilebeat(BulkJSON, 1)

                else:
                    # Checking for the correct size of the flush
                    if len(FilebeatSendQueueArray) > BulkMaxSize:
                        BulkSize = BulkMaxSize
                    else:
                        BulkSize = len(FilebeatSendQueueArray)
                        
                    separator = '\n{ "index":{} }\n'
                    BulkJSON = '{ "index":{} }\n' + str(separator.join(FilebeatSendQueueArray[0:BulkSize])) + '\n'
                    
                    # Log
                    # LogString = "INFO  ==>  " + str(len(FilebeatSendQueueArray)) + " JSON Filebeat messages has been flushed"
                    # logging.info(LogString)
                    
                    # Recording that queue has been flushed, or tried to
                    FilebeatQueueFlushed = True
                    SendToFilebeat(BulkJSON, BulkSize)
   
            else:                
                # No Filebeat server available or Bulk max size not reached, waiting for next loop
                FilebeatSendQueueArray.append(JSONToSend)

        
    ### Logstash Pool
    if MesssageOutput == 'Logstash':

        # Checking if JSON message need to be queued or sent
        if (LogstashServersAvailable and len(LogstashSendQueueArray) >= BulkMaxSize and JSONToSend != 'Flush'):

            # Checking if history messages are in the queue
            if len(LogstashSendQueueArray) == BulkMaxSize:
                # No historical message present
                if BulkMaxSize <= 1:
                    # If BulkMaxSize is 0 or 1, we sent the JSON message directly
                    BulkJSON = '\n{ "index":{} }\n' + JSONToSend + '\n'
                        
                else:
                    # Creating Bulk JSON message
                    separator = '\n{ "index":{} }\n'
                    BulkJSON = '{ "index":{} }\n' + str(separator.join(LogstashSendQueueArray[0:BulkMaxSize])) + '\n'
                    BulkSize = BulkMaxSize
                    
                    # Queuing the current message from function call, waiting for next loop execution
                    LogstashSendQueueArray.append(JSONToSend)
                    
            else:
                # Historical messages are queued, let's send them one by one to the current message
                # Creating Bulk JSON message
                BulkJSON = '{ "index":{} }\n' + str(LogstashSendQueueArray[0]) + '\n{ "index":{} }\n' + JSONToSend + '\n' 
                BulkSize = 1
            
            # Recording that queue has been flushed, or tried to
            LogstashQueueFlushed = True
            SendToLogstash(BulkJSON, BulkSize)

        else:
            # Checking if flush order has been sent
            if JSONToSend == 'Flush':
                # Creating Bulk JSON message and flushing the queue content
                if BulkMaxSize <= 1:
                    # If BulkMaxSize is 0 or 1, we sent the message directly
                    BulkJSON = '\n{ "index":{} }\n' + LogstashSendQueueArray[0] + '\n'
                    
                    # Log
                    # LogString = "INFO  ==>  " + str(len(LogstashSendQueueArray)) + " JSON Logstash messages has been FORCE flushed"
                    # logging.info(LogString)
                    
                    # Recording that queue has been flushed, or tried to
                    LogstashQueueFlushed = True
                    SendToLogstash(BulkJSON, 1)

                else:
                    # Checking for the correct size of the flush
                    if len(LogstashSendQueueArray) > BulkMaxSize:
                        BulkSize = BulkMaxSize
                    else:
                        BulkSize = len(LogstashSendQueueArray)
                    
                    separator = '\n{ "index":{} }\n'
                    BulkJSON = '{ "index":{} }\n' + str(separator.join(LogstashSendQueueArray[0:len(LogstashSendQueueArray)])) + '\n'
                    
                    # Log
                    # LogString = "INFO  ==>  " + str(len(LogstashSendQueueArray)) + " JSON Logstash messages has been flushed"
                    # logging.info(LogString)
                    
                    # Recording that queue has been flushed, or tried to
                    LogstashQueueFlushed = True
                    SendToLogstash(BulkJSON, BulkSize)
   
            else:                
                # No Logstash server available or Bulk max size not reached, waiting for next loop
                LogstashSendQueueArray.append(JSONToSend)

def WorkOnMetrics():
    """ This function will check execution timers and, if necessary, execute item work.
        Items can be builtin Metricbeat Metricsets or Custom Metricsets.

        Some work on specific items are executed in background because execution duration is too long.
    
        TODO: Describe the function, all vars and its content
    """
    
    # Sharing CustomMetricsConfigsArray with main script
    global CustomMetricsConfigsArray
    global CrashDumpDaemon

    # Launch metricset timer comparison and schedule the work if timer is reached, insinde try/catch for debug and stability purpose
    
    try:
        # Checking timer for SystemCoreAndCpu
        ComparisonTimer = CompareTimer("SystemCoreAndCpu", SystemCoreAndCpuWaitValue)
        if ComparisonTimer != devnull:
            SystemCoreAndCpu(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
        
    try:
        # Checking timer for ErrptLog
        ComparisonTimer = CompareTimer("ErrptLog", ErrptLogWaitValue)
        if ComparisonTimer != devnull:
            ErrptLog(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
    
    try:
        # Checking timer for SystemLoad
        ComparisonTimer = CompareTimer("SystemLoad", SystemLoadWaitValue)
        if ComparisonTimer != devnull:
            SystemLoad(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:
        # Checking timer for SystemMemory
        global SystemMemoryThread
        ComparisonTimer = CompareTimer("SystemMemory", SystemMemoryWaitValue)
        if (ComparisonTimer != devnull) and (SystemMemoryThread.is_alive() != True):
            SystemMemoryThread = threading.Thread(target=SystemMemory, args=(ComparisonTimer,))
            SystemMemoryThread.start()
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:
        # Checking timer for SystemNetwork
        ComparisonTimer = CompareTimer("SystemNetwork", SystemNetworkWaitValue)
        if ComparisonTimer != devnull:
            SystemNetwork(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:
        # Checking timer for SystemFc
        ComparisonTimer = CompareTimer("SystemFc", SystemFcWaitValue)
        if ComparisonTimer != devnull:
            SystemFc(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:        
        # Checking timer for SystemSocketSummary
        ComparisonTimer = CompareTimer("SystemSocketSummary", SystemSocketSummaryWaitValue)
        if ComparisonTimer != devnull:
            SystemSocketSummary(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:        
        # Checking timer for SystemSocket
        global SystemSocketThread
        ComparisonTimer = CompareTimer("SystemSocket", SystemSocketWaitValue)
        if (ComparisonTimer != devnull) and (SystemSocketThread.is_alive() != True):
            SystemSocketThread = threading.Thread(target=SystemSocket, args=(ComparisonTimer,))
            SystemSocketThread.start()
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:
        # Checking timer for SystemProcessSummary
        ComparisonTimer = CompareTimer("SystemProcessSummary", SystemProcessSummaryWaitValue)
        if ComparisonTimer != devnull:
            SystemProcessSummary(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:
        # Checking timer for SystemProcess
        global SystemProcessThread
        ComparisonTimer = CompareTimer("SystemProcess", SystemProcessWaitValue)
        if (ComparisonTimer != devnull) and (SystemProcessThread.is_alive() != True):
            SystemProcessThread = threading.Thread(target=SystemProcess, args=(ComparisonTimer,))
            SystemProcessThread.start()
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:
        # Checking timer for SystemDiskIO
        global SystemDiskIOThread
        ComparisonTimer = CompareTimer("SystemDiskIO", SystemDiskIOWaitValue)
        if (ComparisonTimer != devnull) and (SystemDiskIOThread.is_alive() != True):
            SystemDiskIOThread = threading.Thread(target=SystemDiskIO, args=(ComparisonTimer,))
            SystemDiskIOThread.start()
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:
        # Checking timer for SystemFilesystemAndFstat
        ComparisonTimer = CompareTimer("SystemFilesystemAndFstat", SystemFilesystemAndFstatWaitValue)
        if ComparisonTimer != devnull:
            SystemFilesystemAndFstat(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:        
        # Checking timer for PingPlotter
        global PingPlotterThread
        ComparisonTimer = CompareTimer("PingPlotter", PingPlotterWaitValue)
        if (ComparisonTimer != devnull) and (PingPlotterThread.is_alive() != True):
            PingPlotterThread = threading.Thread(target=PingPlotter, args=(ComparisonTimer,))
            PingPlotterThread.start()
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:    
        # Checking timer for SystemHypervisor, if enabled in Parameters.conf file
        if IfSystemHypervisorEnable == "yes":
            ComparisonTimer = CompareTimer("SystemHypervisor", SystemHypervisorWaitValue)
            if ComparisonTimer != devnull:
                SystemHypervisor(ComparisonTimer)
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    try:           
        # Checking timer for SystemHPMStat, if enabled in Parameters.conf file
        global SystemHPMStatThread
        if IfSystemHPMStatEnable == "yes":
            ComparisonTimer = CompareTimer("SystemHPMStat", SystemHPMStatWaitValue)
            if (ComparisonTimer != devnull) and (SystemHPMStatThread.is_alive() != True):
                SystemHPMStatThread = threading.Thread(target=SystemHPMStat, args=(ComparisonTimer,))
                SystemHPMStatThread.start()
    except Exception as e:
        # Metricset has crashed
        # Creating the crash dump file and filling it with crash dump data
        with open(CrashDumpDaemon, 'a') as f:
            f.write('\n\n')
            f.write(str(datetime.datetime.now()))
            f.write(':\n')
            f.write(str(e))
            f.write(traceback.format_exc())
            f.write('\n')

        # Print and log error stack for debug purpose
        logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
        print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
        # traceback.print_exc()
        
        # Exiting
        # os._exit(2)
    
    # Checking if any Custom Metric need to be executed
    # IMPROVEMENT - Threading execution of each Custom metric as it will slow down the script loop
    for CustomMetricItem in CustomMetricsConfigsArray:
        # Spliting the result line to get content
        CustomMetricSplitedLine = CustomMetricsConfigsArray[CustomMetricItem].split(',')

        # Creating a short name for the current Custom config
        CustomMetricItemName = CustomMetricItem.replace('.custom.conf','')

        # Gathering config values from splitted line
        CustomMetricItemOSScript = CustomMetricSplitedLine[0]
        CustomMetricItemWaitValue = int(CustomMetricSplitedLine[1])
        CustomMetricItemOutput = CustomMetricSplitedLine[2] 
        
        try:
            # Checking timer for the current Custom Metric into try/catch, third parameter is only for user log formating
            ComparisonTimer = CompareTimer(CustomMetricItemName, CustomMetricItemWaitValue, '(Custom metrics)')
            if ComparisonTimer != devnull:
                CustomMetricExec(CustomMetricItemOSScript, CustomMetricItemName, ComparisonTimer, CustomMetricItemOutput)
        except Exception as e:
            # Metricset has crashed
            # Creating the crash dump file and filling it with crash dump data
            with open(CrashDumpDaemon, 'a') as f:
                f.write('\n\n')
                f.write(str(datetime.datetime.now()))
                f.write(':\n')
                f.write(str(e))
                f.write(traceback.format_exc())
                f.write('\n')

            # Print and log error stack for debug purpose
            logging.info('\n Metraixbeat encountered an error ! See ' + CrashDumpDaemon + ' for more informations\n')
            print('\n Metraixbeat encountered an error ! See ', CrashDumpDaemon, ' for more informations\n')
            # traceback.print_exc()
            
            # Exiting
            # os._exit(2)
    pass
    
def FilebeatTail(FilebeatConfigName):
    """ This function will check if tailed file is still "alive" or "dead" in multiple way

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    
    # Using global FilebeatConfigsArray, TargetFileCurrentPosArray and TailStateArray dictionary for follow up purpose
    global FilebeatConfigsArray
    global TailStateArray
    global TargetFileCurrentPosArray
    # global TargetFileMTimeCountArray

    # Getting parameters from FilebeatConfigsArray
    ConfigSplitLine = FilebeatConfigsArray[FilebeatConfigName].split(',')
    CurrentTargetFile = ConfigSplitLine[0]
    TargetFile = ConfigSplitLine[1]
    PatternMatch = ConfigSplitLine[2]
    LastTailLine = ConfigSplitLine[3]
    StartInode = ConfigSplitLine[4]
    TargetSize = ConfigSplitLine[5]
    MultilineSeparator = ConfigSplitLine[6]
    Output = ConfigSplitLine[7]


    # Defining name for the thread
    FilebeatConfigThreadName = FilebeatConfigName + 'Thread'.replace('.','')
    FilebeatConfigThreadName = FilebeatConfigThreadName.replace('.','')

    # Checking if FilebeatTail process already running for this config file
    if (bool(re.search(FilebeatConfigThreadName, str(threading.enumerate())))):
        # This config has already a thread running, let's go checking CurrentTargetFile freshness
        # Log
        logging.info("   - Checking " + FilebeatConfigName + " Tail process status")

        # Checking if file is still here
        if not os.path.exists(CurrentTargetFile):
        # The file does not exists
            # Log
            logging.info("            * File is not there anymore: stopping Tail thread !")

            # Sending order to stop thread
            TailStateArray[FilebeatConfigName] = False

            # Resting last tailed line for CurrentTargetFile as the file has changed
            TargetFileCurrentPosArray[FilebeatConfigName] = 0

            # Exiting function
            return
        else:
            # Log
            logging.info("            * Presence check: Ok !")

        # Checking if CurrentTargetFile size is less then starting size
        CurrentTargetFileSize = os.stat(CurrentTargetFile).st_size
        if int(TargetSize) > CurrentTargetFileSize:
            # The reference size is less than the current size.
            # File has changed. Let's send order to stop background tail process on that CurrentTargetFile
            TailStateArray[FilebeatConfigName] = False

            # Resting last tailed line for CurrentTargetFile as the file has changed
            TargetFileCurrentPosArray[FilebeatConfigName] = 0

            # Log
            logging.info("            * The reference size is less than the current size: stopping Tail thread !")
            # Exiting function
            return
        else:
            # Log
            logging.info("            * Size check: Ok !")

        # Checking if CurrentTargetFile inode has changed
        CurrentTargetFileInode = os.stat(CurrentTargetFile).st_ino
        if int(StartInode) != CurrentTargetFileInode:
            # The inode has changed. Let's send order to stop background tail process on that CurrentTargetFile
            TailStateArray[FilebeatConfigName] = False

            # Resting last tailed line for CurrentTargetFile as the file has changed
            TargetFileCurrentPosArray[FilebeatConfigName] = 0

            # Log
            logging.info("            * The reference inode is different than the current inode: stopping Tail thread !")
            # Exiting function
            return
        else:
            # Log
            logging.info("            * Inode check: Ok !")
        
        # Converting date format from original TargetFile string, if any
        IfNewTargetFile = ConvertFileName(TargetFile)
        
        # Looking for corresponding file
        OSCommand = "ls -lart " + IfNewTargetFile + " | tail -n 1 | awk '{print $NF}' 2>/dev/null"
        CheckTargetFile = subprocess.Popen(OSCommand, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
        CheckTargetFile = CheckTargetFile.read().decode().split()
  
        # Handling case where file not found from OS command
        if len(CheckTargetFile) != 0:
            # Checking if CurrentTargetFile name still match with original pattern
            if str(CheckTargetFile[0]) != CurrentTargetFile:
                # Mismatch detected, checking if a new file exists when applying Target File naming
                # Checking if file exists or not
                if os.path.exists(str(CheckTargetFile[0])):
                    # A new file currently exists
                    TailStateArray[FilebeatConfigName] = False
                    
                    # Resting last tailed line for CurrentTargetFile as the file has changed
                    TargetFileCurrentPosArray[FilebeatConfigName] = 0
                    
                    # Log
                    logging.info("            * File name pattern in configuration file does not match anymore with current file: stopping Tail thread !")
                    # Exiting function
                    return
            else:
                # Log
                logging.info("            * Refreshing filename: Ok !")  
        else:
            # No file exists corresponding to this name stopping, threads
            TailStateArray[FilebeatConfigName] = False
                
            # Resting last tailed line for CurrentTargetFile as the file has changed
            TargetFileCurrentPosArray[FilebeatConfigName] = 0
            
            # Log
            logging.info("            * File name pattern in configuration file does not match anymore with an existing file: stopping Tail thread !")
            # Exiting function
            return
    else:
        # No thread are running for this config, let's start a new one
        
        # Converting date format, if any, in target file  
        CurrentTargetFile = ConvertFileName(TargetFile)
        
        # Looking for corresponding file
        OSCommand = "ls -lart " + CurrentTargetFile + " | tail -n 1 | awk '{print $NF}' 2>/dev/null"
        CheckTargetFile = subprocess.Popen(OSCommand, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
        CheckTargetFile = CheckTargetFile.read().decode().split()
        
        # Handling case where file not found from OS command
        if len(CheckTargetFile) != 0:
            # Checking if file exists or not
            if os.path.exists(str(CheckTargetFile[0])):
                # The file currently exists
                CurrentTargetFile = str(CheckTargetFile[0])
                
                # Log
                logging.info("    * Initiating tail process on " + CurrentTargetFile)

                # Setting thread as active
                TailStateArray[FilebeatConfigName] = True

                # Refreshing CurrentTargetFile inode and size
                CurrentTargetFileSize = str(os.stat(CurrentTargetFile).st_size)
                CurrentTargetFileInode = str(os.stat(CurrentTargetFile).st_ino)

                # Formating string and storing into
                ConfigString = CurrentTargetFile + ',' + TargetFile + ',' + PatternMatch + ',' + LastTailLine + ',' + CurrentTargetFileInode + ',' + CurrentTargetFileSize + ',' + MultilineSeparator + ',' + Output
                FilebeatConfigsArray[FilebeatConfigName] = ConfigString

                # Launching thread
                FilebeatConfigThread = threading.Thread(target=TailPythonStyle, name=FilebeatConfigThreadName, args=(FilebeatConfigName, CurrentTargetFile, PatternMatch, MultilineSeparator, Output))
                FilebeatConfigThread.start()
            else:
                # The file does not exists
                logging.info("    * Initiating tail process on Target File " + CurrentTargetFile + " impossible, the file does not exists !")
                
                # Initializing state value to start tail from line 1 when file will be available
                TargetFileCurrentPosArray[FilebeatConfigName] = 0
        else:
            # The file does not exists
            logging.info("    * Initiating tail process on Target File " + CurrentTargetFile + " impossible, the file does not exists !")
            
            # Initializing state value to start tail from line 1 when file will be available
            TargetFileCurrentPosArray[FilebeatConfigName] = 0

    # Debug
    # print('\nDEBUG\n')
    # print('<!> DEBUG ', 'ConfigSplitLine', ConfigSplitLine)
    # print('<!> DEBUG ', 'TargetFile', TargetFile)
    # print('<!> DEBUG ', 'TargetInfoPattern', TargetInfoPattern)
    # print('<!> DEBUG ', 'TargetWarningPattern', TargetWarningPattern)
    # print('<!> DEBUG ', 'TargetErrorPattern', TargetErrorPattern)
    # print('<!> DEBUG ', 'PatternMatch', PatternMatch)
    # print('<!> DEBUG ', 'LastTailLine', LastTailLine)
    # print('<!> DEBUG ', 'StartInode', StartInode)
    # print('<!> DEBUG ', 'TargetSize', TargetSize)
    # print('<!> DEBUG ', 'MultilineSeparator', MultilineSeparator)
    # print('\nFINDEBUG\n')
    pass

def TailPythonStyle(FilebeatConfigName, TargetFile, PatternMatch, MultilineSeparator, Output):
    """ This function will tail a txt file in python style, as tail does not esists :-(

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    
    # Sharing TailStateArray and TargetFileCurrentPosArray with other threads
    global TailStateArray
    global TargetFileCurrentPosArray

    # Remove "" from input vars
    PatternMatch = PatternMatch.replace('"','')
    MultilineSeparator = MultilineSeparator.replace('"','')

    # Setting vars for threads follow up
    CurrentThread = threading.current_thread()

    # Opening TargetFile
    OpenedTargetFile = open(TargetFile,'r')

    # Checking TargetFile size to start tail at the last line
    TargetFileStats = os.stat(TargetFile)
    TargetFileSize = TargetFileStats[6]

    # Positionning cursor at the end of the file
    # Checking if TargetFileCurrentPosArray[FilebeatConfigName] is empty with try/catch

    try:
        # If value exists in plugin state dictionary, that's to say parsing was already running in this daemon execution
        # We reset it to 0 to start parsing the new file from begining
        TargetFileCurrentPosArray[FilebeatConfigName]
        OpenedTargetFile.seek(0)
        
    except:
        # Na value inside dictionnary, that's to say this is the first daemon execution
        # We put the cursor on the last line of the file
        OpenedTargetFile.seek(TargetFileSize)

    # Multi-line mode
    
    if (len(MultilineSeparator) != 0):
        # Going to make all work into try/catch to avoid exception and daemon crash
        # if something unexpected happen to the TargetFile
        
        # Initializing vars
        LogLineStart = False
        SeqIdTimestamp = ''
        FinalLogLine = ''
        Matched = False
        TailTimer = 0
        
        try:
            # Start looping indefintly until TailStateArray[ThreadName] is different then True
            # It give control on this sub-thread from main thread to stop/clean it when necessary
            while (True and TailStateArray[FilebeatConfigName]):
                # Storing the current TargetFile's "last line" position
                TargetFileCurrentPosArray[FilebeatConfigName] = OpenedTargetFile.tell()
                # Gathering new lines if any
                NewLine = OpenedTargetFile.readline()

                # Checking if there are new lines happened to the TargetFile
                if not NewLine:
                    # No new line detected
                    # Then we set file position to the previous recoreded one
                    # to check any new lines in the next loop execution
                    OpenedTargetFile.seek(TargetFileCurrentPosArray[FilebeatConfigName])
                    
                    # Going to sleep 1 sec to save CPU
                    time.sleep(1)
                    
                    # Incrementing safety sleep before sending current message if matched
                    # Maybe a line will comes out ?!
                    if len(FinalLogLine) != 0:
                        TailTimer = TailTimer + 1
                    
                    # Checking if something to send and if we have wait enough
                    if TailTimer > 4:
                        if Matched:
                            # Removing \n at the end of the Message
                            # FinalLogLine = re.sub('\n', '\\\n', FinalLogLine)

                            # Formatting message
                            Message = re.sub('[\\\[\]\(\)\{\}"\b\t\a\r\n]', ' ', FinalLogLine)
                            
                            # Sending message
                            CustomJSONToSend = (''
                            ','
                            '\"log\":{'
                            '\"file\":{'
                            '\"path\":\"' + TargetFile + '\"'
                            '},'
                            '\"offset\":' + str(MatchLineOffset) + ','
                            '\"pattern\":\"' + PatternMatch + '\"},'
                            '\"message\":\"' + Message + '\",'
                            '\"input\":{'
                            '\"type\":\"log\"'
                            '},'
                            '\"service\":{'
                            '\"name\":\"customfilebeat\"'
                            '},'
                            '\"event\":{'
                            '\"timezone\":\"+00:00\",'
                            '\"module\":\"customfilebeat\",'
                            '\"dataset\":\"custom.' + FilebeatConfigName + '\"'
                            '}'
                            '')
                            
                            # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
                            JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSONFilebeat + CustomJSONToSend + '}'
                            
                            # Let's send JSON message to Elastic, Filebeat or Logstash server
                            if Output == 'Metricbeat':
                                SendJSON(JSONToSend)
                            elif Output == 'Logstash':
                                SendJSON(JSONToSend, 'Logstash')
                            else:
                                SendJSON(JSONToSend, 'Filebeat')
                            # print('JSONToSend: ', JSONToSend)
                            
                        # Reseting vars for next log line
                        SeqIdTimestamp = ''
                        LogLineStart = False
                        Matched = False
                        FinalLogLine = ''
                        TailTimer = 0

                else:
                    # New line has been written, let's store datetime if not already
                    if (len(SeqIdTimestamp) == 0):
                        SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
                    
                    # Checking if log line start
                    if (bool(re.search(MultilineSeparator, NewLine))) and (LogLineStart == False):
                        # Setting var to true
                        LogLineStart = True

                        # Storing line content
                        FinalLogLine = str(NewLine)
                        
                        # Checking if line content the pattern
                        if (bool(re.search(PatternMatch, NewLine)) and Matched == False):
                            Matched = True
                            
                            # Getting the current line of the file
                            MatchLineOffset = OpenedTargetFile.tell()
                        
                    elif (bool(re.search(MultilineSeparator, NewLine))) and (LogLineStart == True):
                        # New line detected, sending the message  if matched is detected
                        if Matched:
                            # Removing \n at the end of the Message
                            # FinalLogLine = re.sub('\n', '\\\n', FinalLogLine)
                            
                            # Formatting message
                            Message = re.sub('[\\\[\]\(\)\{\}"\b\t\a\r\n]', ' ', FinalLogLine)  
                            
                            # Sending message
                            CustomJSONToSend = (''
                            ','
                            '\"log\":{'
                            '\"file\":{'
                            '\"path\":\"' + TargetFile + '\"'
                            '},'
                            '\"offset\":' + str(MatchLineOffset) + ','
                            '\"pattern\":\"' + PatternMatch + '\"},'
                            '\"message\":\"' + Message + '\",'
                            '\"input\":{'
                            '\"type\":\"log\"'
                            '},'
                            '\"service\":{'
                            '\"name\":\"customfilebeat\"'
                            '},'
                            '\"event\":{'
                            '\"timezone\":\"+00:00\",'
                            '\"module\":\"customfilebeat\",'
                            '\"dataset\":\"custom.' + FilebeatConfigName + '\"'
                            '}'
                            '')
                            
                            # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
                            JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSONFilebeat + CustomJSONToSend + '}'
                            
                            # Let's send JSON message to Elastic, Filebeat or Logstash server
                            if Output == 'Metricbeat':
                                SendJSON(JSONToSend)
                            elif Output == 'Logstash':
                                SendJSON(JSONToSend, 'Logstash')
                            else:
                                SendJSON(JSONToSend, 'Filebeat')
                            # print('JSONToSend: ', JSONToSend)
                        
                        # Reseting vars for next log line
                        SeqIdTimestamp = ''
                        LogLineStart = False
                        Matched = False
                        FinalLogLine = ''
                        TailTimer = 0

                        # Fetching file to the previous position
                        OpenedTargetFile.seek(TargetFileCurrentPosArray[FilebeatConfigName])
                        
                        # Going to the next loop execution
                        continue

                    else:    
                        # This line is the continuation of the previous one, let's add it and loop
                        FinalLogLine = FinalLogLine + str(NewLine)
                        
                        # Checking if line content the pattern
                        if (bool(re.search(PatternMatch, NewLine)) and Matched == False):
                            Matched = True
                            
                            # Getting the current line of the file
                            MatchLineOffset = OpenedTargetFile.tell()
  
                    # Going to sleep 0,1 sec to wait for next line for CPU reasons
                    time.sleep(0.1)   

            # When we reached that point, thread is dead by order
            # print('thread ' + CurrentThread.name + ' is dead by order')
            pass
        except:
            # Something happened to the thread, thread is dead by crash
            print('thread ' + CurrentThread.name + ' is dead by crash')
            # traceback.print_exc()
            pass
    else:
        # No Multi-line mode
        
        # Going to make all work into try/catch to avoid exception and daemon crash
        # if something unexpected happen to the TargetFile
        try:
            # Start looping indefintly until TailStateArray[ThreadName] is different then True
            # It give control on this sub-thread from main thread to stop/clean it when necessary
            while (True and TailStateArray[FilebeatConfigName]):
                # Storing the current TargetFile's "last line" position
                TargetFileCurrentPosArray[FilebeatConfigName] = OpenedTargetFile.tell()
                # Gathering new lines if any
                NewLine = OpenedTargetFile.readline()

                # Checking if there are new lines happened to the TargetFile
                if not NewLine:
                    # No new line detected
                    # Then we set file position to the previous recoreded one
                    # to check any new lines in the next loop execution
                    OpenedTargetFile.seek(TargetFileCurrentPosArray[FilebeatConfigName])
                    # Going to sleep 1 sec to save CPU
                    time.sleep(1)

                else:
                    # Removing \n at the end of thr readline() output
                    NewLine = re.sub('\n$', '', NewLine)
                    # New line has been written, let's store datetime and check for patterns
                    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
                    
                    # We check if pattern is detected
                    if bool(re.search(PatternMatch, NewLine)):
                        
                        # Getting the current line of the file
                        MatchLineOffset = OpenedTargetFile.tell()
                        
                        CustomJSONToSend = (''
                        ','
                        '\"log\":{'
                        '\"file\":{'
                        '\"path\":\"' + TargetFile + '\"'
                        '},'
                        '\"offset\":' + str(MatchLineOffset) + ','
                        '\"pattern\":\"' + PatternMatch + '\"},'
                        '\"message\":\"' + re.sub('[\\\[\]\(\)\{\}"\b\t\n\a\r]', ' ', NewLine) + '\",'
                        '\"input\":{'
                        '\"type\":\"log\"'
                        '},'
                        '\"service\":{'
                        '\"name\":\"customfilebeat\"'
                        '},'
                        '\"event\":{'
                        '\"timezone\":\"+00:00\",'
                        '\"module\":\"customfilebeat\",'
                        '\"dataset\":\"custom.' + FilebeatConfigName + '\"'
                        '}'
                        '')
                        
                        # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
                        JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSONFilebeat + CustomJSONToSend + '}'
                        
                        # Let's send JSON message to Elastic, Filebeat or Logstash server
                        if Output == 'Metricbeat':
                            SendJSON(JSONToSend)
                        elif Output == 'Logstash':
                            SendJSON(JSONToSend, 'Logstash')
                        else:
                            SendJSON(JSONToSend, 'Filebeat')
                            
                        # print('JSONToSend: ', JSONToSend)

            # When we reached that point, thread is dead by order
            # print('thread ' + CurrentThread.name + ' is dead by order')
            pass
        except:
            # Something happened to the thread, thread is dead by crash
            print('thread ' + CurrentThread.name + ' is dead by crash')
            # traceback.print_exc()
            pass
    pass

def CustomMetricExec(OSScript, ItemName, ComparisonTimer, Output):
    """ This function analyse Disks activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """

    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Gathering data from OS command
    OSCmdResult = subprocess.Popen(OSScript, shell=True, stdout=subprocess.PIPE).stdout
    OSCmdResult = OSCmdResult.read().decode().split('\n')
    # print('OSCmdResult: ', str(OSCmdResult))

    for CurrLine in OSCmdResult:
        if CurrLine != '':
            CurrLine = CurrLine.split(' ')

            # Let's construct JSON output for Custom script execution (ELK 7.5.0)
            EmptyString = " "
            JSONToSendValues = (''
            '\"system\":{\"custom\":{\"' + ItemName + '\":{\"name\":\"' + CurrLine[0] + '\",\"value\":\"' + EmptyString.join(CurrLine[1:]).replace('"','') + '\"}}}')
           
            # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
            JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
            
            # Adding JSON metrics values gathered from OS command
            JSONToSend = JSONToSend + ',' + JSONToSendValues
            
            # Gathering "ELK formatted" dynamic JSON values
            RetDynamicJSON = GenerateDynamicJson("system.customexec", "system", "customexec", ComparisonTimer)
            
            CustomExec = "system.customexec." + ItemName
            CustomExecShort = "customexec_" + ItemName
            RetDynamicJSON = GenerateDynamicJson(CustomExec, "system", CustomExecShort, ComparisonTimer)
            
            # Adding dynamic "ELK Formating" JSON values into final JSON message
            JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
            
            # Let's send JSON message to Elastic, Filebeat or Logstash server
            if Output == 'Filebeat':
                SendJSON(JSONToSend, 'Filebeat')
            elif Output == 'Logstash':
                SendJSON(JSONToSend, 'Logstash')
            else:
                SendJSON(JSONToSend)
            # print('\JSONToSend\n', JSONToSend, '\n')
            pass

def PingPlotter(ComparisonTimer):
    """ This function analyse ping against multiple configured targets and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    
    # Setting vars for threads follow up
    global PingPlotterTargets
    global PingPlotterThread
    global PingSamples
    global PingTimeout
    PingPlotterThread = threading.currentThread()
    
    # Making test ping for all target in config file
    for PingTarget in PingPlotterTargets.split(','):
        if len(PingTarget) != 0:
            # Generating current ELK timestamp for JSON message
            SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
            
            # To move both fields to Parameter.conf file
            PingSamples = 5
            PingTimeout = "1s"
            
            # Configuring pingparsin package
            ping_parser = pingparsing.PingParsing()
            transmitter = pingparsing.PingTransmitter()

            # Setting ping destination and timeout
            transmitter.destination = PingTarget
            transmitter.timeout = PingTimeout

            # Setting the number of ping to execute
            transmitter.count = PingSamples
            PingResult = transmitter.ping()

            if 'returncode=0' in str(PingResult):
                # Ping is ok, let's format output and JSON message
                ResultDict = json.loads(json.dumps(ping_parser.parse(PingResult).as_dict()))
                
                # Let's construct JSON output for SystemPingPlotter(ELK 7.5.0)
                JSONToSendValues = (''
                '\"system\":{\"pingplotter\":{\"destination\":\"' + str(ResultDict["destination"]) + '\",'
                '\"packet_loss_rate\":' + str(float(ResultDict["packet_loss_rate"]) / 100) + ',\"rtt_avg\":' + str(ResultDict["rtt_avg"]) + ','
                '\"rtt_max\":' + str(ResultDict["rtt_max"]) + ',\"packet_duplicate_rate\":' + str(float(ResultDict["packet_duplicate_rate"]) / 100) + '}}')
               
                # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
                JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
                
                # Adding JSON metrics values gathered from OS command
                JSONToSend = JSONToSend + ',' + JSONToSendValues
                
                # Gathering "ELK formatted" dynamic JSON values
                RetDynamicJSON = GenerateDynamicJson("system.pingplotter", "system", "pingplotter", ComparisonTimer)
                
                # Adding dynamic "ELK Formating" JSON values into final JSON message
                JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
                
                # Let's send JSON message to ELK servers
                SendJSON(JSONToSend)
                
                # print('\JSONToSend\n', JSONToSend, '\n')
                
            else:
                # An error has been thrown by pingparsing, maybe resolution error. 
                # Setting all counters to 0 and packet lost to 100%
                
                # Let's construct JSON output for SystemPingPlotter(ELK 7.5.0)
                JSONToSendValues = (''
                '\"system\":{\"pingplotter\":{\"destination\":\"' + PingTarget + '\",\"packet_loss_rate\":100,\"rtt_avg\":0,\"rtt_max\":0,\"packet_duplicate_rate\":0}}')
               
                # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
                JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
                
                # Adding JSON metrics values gathered from OS command
                JSONToSend = JSONToSend + ',' + JSONToSendValues
                
                # Gathering "ELK formatted" dynamic JSON values
                RetDynamicJSON = GenerateDynamicJson("system.customping", "system", "customping", ComparisonTimer)
                
                # Adding dynamic "ELK Formating" JSON values into final JSON message
                JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
                
                # Let's send JSON message to ELK servers
                SendJSON(JSONToSend)
                
                # print('\JSONToSend\n', JSONToSend, '\n')
                pass

def ErrptLog(ComparisonTimer):
    """ This function detects new Errorlogs and send them to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    global LastErrpt
    
    # Checking if value is initialized with try/catch
    try:
        # Gathering last errorlog line
        CurrErrpt = subprocess.Popen("errpt -a | grep \"Sequence Number\" | awk '{print $NF}'", shell=True, stdout=subprocess.PIPE).stdout
        CurrErrpt = CurrErrpt.read().decode().split('\n')

        # Checking if last errlog entrie is the same or new
        if str(CurrErrpt[0]) not in str(LastErrpt):
            # New log detected, gathering its id in list
            for i in range(0, len(CurrErrpt)): 
                if str(CurrErrpt[i]) in str(LastErrpt): 
                    CurrErrptID = i
                    break
                    
            # Sending all required error log entries in correct order
            for i in reversed(range(0, CurrErrptID)):
                ErrorLogMessageCmd = 'errpt -l ' + str(CurrErrpt[i]) + ' | tail -n +2'
                ErrorLogMessage = subprocess.Popen(ErrorLogMessageCmd, shell=True, stdout=subprocess.PIPE).stdout
                ErrorLogMessage = ErrorLogMessage.read().decode()
                
                # Generating current ELK timestamp for JSON message
                SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
                
                # Custom message
                CustomJSONToSend = (''
                '\"log\":{'
                '\"file\":{'
                '\"path\":\"AIX ERRORLOG\"'
                '},'
                '\"offset\":' + str(CurrErrptID) + ','
                '\"pattern\":\"AIX ERRORLOG\"},'
                '\"message\":\"' + re.sub('[\\\[\]\(\)\{\}"\b\t\n\a\r]', ' ', str(ErrorLogMessage)) + '\",'
                '\"input\":{'
                '\"type\":\"log\"'
                '},'
                '\"service\":{'
                '\"name\":\"aixerrorlog\"'
                '},'
                '\"event\":{'
                '\"timezone\":\"+00:00\",'
                '\"module\":\"aixerrorlog\",'
                '\"dataset\":\"custom.aixerrorlog\"'
                '}'
                '')
                
                # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
                JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSONFilebeat + ',' + CustomJSONToSend + '}'
                
                # Let's send JSON message to ELK Filebeat server
                SendJSON(JSONToSend, 'Filebeat')
                # print('JSONToSend: ', JSONToSend)
                
            # Setting last errorlog to the first occurence of the list
            LastErrpt = CurrErrpt[0]
            
    except:
        # First execution, gathering last errorlog line and setting LastErrpt
        LastErrpt = subprocess.Popen("errpt -a | grep \"Sequence Number\" | awk '{print $NF}' | head -1", shell=True, stdout=subprocess.PIPE).stdout
        LastErrpt = LastErrpt.read().decode()

def SystemCoreAndCpu(ComparisonTimer):
    """ This function analyse CPU activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    global NMONSeq
    global LPARCPUMode
    
    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    # Gathering data from OS command for LPAR allocations
    CmdLine = 'lparstat -i | egrep "SMT|Online Virtual CPUs|Entitled Capacity" | head -3'
    LPARStatCmd = subprocess.Popen(CmdLine, shell=True, stdout=subprocess.PIPE).stdout
    LPARStatCmd = LPARStatCmd.read().decode().split('\n')

    # LPARSTAT Custom metrics
    LPARCPUMode = str(LPARStatCmd[0].split(' ')[-1])
    CpuEntAlloc = str(LPARStatCmd[1].split(' ')[-1])
    VCPUAlloc = str(LPARStatCmd[2].split(' ')[-1])
    
    # Gathering current number of threads
    OnlineCPUThreads = subprocess.Popen("mpstat -w 1 1 | sed '1,4d' | grep -v U", shell=True, stdout=subprocess.PIPE).stdout
    OnlineCPUThreads = OnlineCPUThreads.read().decode().split('\n')

    # Removing last line if empty
    if OnlineCPUThreads[-1] == '':
        OnlineCPUThreads = OnlineCPUThreads[:-1]
       
    # Calculating number of online threads
    OnlineCPUThreadsCount = len(OnlineCPUThreads) - 1
    CurrOnlineVCPU = round(OnlineCPUThreadsCount / int(LPARSMTMode))
    
    # Gather data for system CPU internal values
    AllmpstatLine = OnlineCPUThreads[-1].split()
    CpuInterrupt = AllmpstatLine[4]
    ContextSwitch = AllmpstatLine[5]
    InvolContextSwitch = AllmpstatLine[6]
    VolContextSwitch = int(ContextSwitch) - int(InvolContextSwitch)
    SysCall = AllmpstatLine[10]
    LogicalContextSwitch = AllmpstatLine[-1]

    # IMPROVEMENT - To generalize -  Check in all script if casting value is necessary or not !!!

    # MPSTAT Custom metrics
    CpuEntAlloc =  str(CpuEntAlloc)
    VCPUAlloc = str(VCPUAlloc)
    OnlineCPUThreadsCount = str(OnlineCPUThreadsCount)
    CurrOnlineVCPU = str(CurrOnlineVCPU)
    CpuInterrupt = str(CpuInterrupt)
    ContextSwitch = str(ContextSwitch)
    InvolContextSwitch = str(InvolContextSwitch)
    VolContextSwitch = str(VolContextSwitch)
    SysCall = str(SysCall)
    LogicalContextSwitch = str(LogicalContextSwitch)
    
    # Gathering data from OS command for CPU usage
    SystemCoreAndCpuCmd = subprocess.Popen("vmstat -IWwt 1:kthr:r 1 | tail -1", shell=True, stdout=subprocess.PIPE).stdout
    SystemCoreAndCpuCmd = SystemCoreAndCpuCmd.read().decode().split()

    # Defining vars from command output
    CPUIdlePCTNorm = str(float(SystemCoreAndCpuCmd[17]) / 100)
    CPUUserPCTNorm = float(SystemCoreAndCpuCmd[15]) / 100
    CPUSystemPCTNorm = float(SystemCoreAndCpuCmd[16]) / 100
    CPUIOWaitPCTNorm = str(float(SystemCoreAndCpuCmd[18]) / 100)
    CPUTotalNorm = CPUUserPCTNorm + CPUSystemPCTNorm
    CPUTotalNorm = str(round(CPUTotalNorm, 2))
    CPUUserPCTNorm = str(CPUUserPCTNorm)
    CPUSystemPCTNorm = str(CPUSystemPCTNorm)

    # VMSTAT Custom metrics
    if "Dedicated" in LPARCPUMode:
        # If LPAR is dedicated CPU mode
        CPUPhysc = str(AllmpstatLine[15])
        CPUEntcPCT = "1"
    else:
        # If not
        CPUPhysc = str(SystemCoreAndCpuCmd[19])
        CPUEntcPCT = str(float(SystemCoreAndCpuCmd[20]) / 100)
    
    CPURunQueue = str(float(SystemCoreAndCpuCmd[0]))
    CPUBlockQueue = str(float(SystemCoreAndCpuCmd[1]))
    CPURawIOQueue = str(float(SystemCoreAndCpuCmd[2]))
    CPUWaitQueue = str(float(SystemCoreAndCpuCmd[3]))
    
    # If LPAR is a VIOS nad NMON running, gathering CPU pool information from current NMON file
    if IfVIOS:
        # Making try/catch to avoid any unpredicted situation (and no NMON running of course)... To improve...
        try:
            # Checking if any NMON is running
            NMONRunningPath = subprocess.Popen("ps -ef | grep nmon | grep -v grep | tail -1", shell=True, stdout=subprocess.PIPE).stdout
            NMONRunningPath = NMONRunningPath.read().decode().split()
            
            # Getting current NMON file
            NMONRunningFileCmd = ('ls -lart ' + NMONRunningPath[13].split('=')[1] + '* | tail -n 1')
            NMONRunningFile = subprocess.Popen(NMONRunningFileCmd, shell=True, stdout=subprocess.PIPE).stdout
            NMONRunningFile = NMONRunningFile.read().decode().split()
            
            # Gathering metrics from NMON file
            NMONGatheringCmd = ('cat ' + NMONRunningFile[-1] + ' | grep LPAR | tail -n 1')
            NMONGathering = subprocess.Popen(NMONGatheringCmd, shell=True, stdout=subprocess.PIPE).stdout
            NMONGathering = NMONGathering.read().decode().split(',')
            CpuPoolIdle = NMONGathering[8]
            CurrNMONSeq = NMONGathering[1]
            
            
            if int(CurrNMONSeq.replace('T', '')) != NMONSeq:
                # New data detected, adding metrics to message
                NMONSeq = int(CurrNMONSeq.replace('T', ''))
                NewNMONData = True
            else:
                # No new data
                NewNMONData = False
        except:
            #NMON not running
            NewNMONData = False

    # IMPROVEMENT - Don't know how to translate,  = "0" (type str for string manipulation)
    CPUSoftIRQPCT = "0"
    CPUSoftIRQPCTNorm = "0"
    CPUStealPCT = "0"
    CPUStealPCTNorm = "0"
    CPUIRQPCT = "0"
    CPUIRQPCTNorm = "0"
    CPUNicePCT = "0"
    CPUNicePCTNorm = "0"
    
    # Let's construct JSON output for SystemCore (ELK 7.5.0)
    JSONToSendValues = (''
    '\"system\":{'
    '\"core\":{'
    '\"softirq\":{\"norm\": {'
    '\"pct\":' + CPUSoftIRQPCTNorm + '}},'
    '\"steal\":{\"norm\": {'
    '\"pct\":' + CPUStealPCTNorm + '}},'
    '\"idle\":{\"norm\": {'
    '\"pct\":' + CPUIdlePCTNorm + '}},'
    '\"system\":{\"norm\": {'
    '\"pct\":' + CPUSystemPCTNorm + '}},'
    '\"irq\":{\"norm\": {'
    '\"pct\":' + CPUIRQPCTNorm + '}},'
    '\"nice\":{\"norm\": {'
    '\"pct\":' + CPUNicePCTNorm + '}},'
    '\"id\":1,'
    '\"user\":{\"norm\": {'
    '\"pct\":' + CPUUserPCTNorm + '}},'
    '\"iowait\":{\"norm\": {'
    '\"pct\":' + CPUIOWaitPCTNorm + '}}}}')   
   
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.core", "system", "core", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    # print('\JSONToSend\n', JSONToSend, '\n')
       
    # Let's construct JSON output for SystemCPU(ELK 7.5.0)
    JSONToSendValues = (''
    # For now, replacing the number of threads by the number of VCPU because of Linux metricbeat uniformization
    # '\"system\":{\"cpu\":{\"cores\":' + NumProcString + ','
    '\"system\":{\"cpu\":{\"cores\":' + VCPUAlloc + ','
    '\"custom\":{\"cpuphysusage\":' + CPUPhysc + ','
    '\"cpuentusagepct\":' + CPUEntcPCT + ','
    '\"onlinevcpu\":' + CurrOnlineVCPU + ','
    '\"onlinethreads\":' + OnlineCPUThreadsCount + ','
    '\"cpuentalloc\":' + CpuEntAlloc + ','
    '\"vcpualloc\":' + VCPUAlloc + ','
    '\"cpuinterrupt\":' + CpuInterrupt + ','
    '\"contextswitch\":' + ContextSwitch + ','
    '\"involcontextswitch\":' + InvolContextSwitch + ','
    '\"volcontextswitch\":' + VolContextSwitch + ','
    '\"syscall\":' + SysCall + ','
    '\"LogicalContextSwitch\":' + LogicalContextSwitch + ','
    '\"cpurunqueue\":' + CPURunQueue + ','
    '\"cpublockqueue\":' + CPUBlockQueue + ','
    '\"cpurawioqueue\":' + CPURawIOQueue + ','
    '\"cpuwaitqueue\":' + CPUWaitQueue + '')
    
    # Adding CPU Pool metrics for VIOS
    if IfVIOS and NewNMONData:
        JSONToSendValues = JSONToSendValues + ',\"cpupoolidle\":' + str(CpuPoolIdle) + ''
        
    # Then, adding the rest of the metrics
    JSONToSendValues = JSONToSendValues + ('},'
    '\"steal\":{\"norm\": {\"pct\":' + CPUStealPCTNorm + '}},'
    '\"idle\":{\"norm\": {\"pct\":' + CPUIdlePCTNorm + '}},'
    '\"nice\":{\"norm\": {\"pct\":' + CPUNicePCTNorm + '}},'
    '\"softirq\":{\"norm\": {\"pct\":' + CPUSoftIRQPCTNorm + '}},'
    '\"system\":{\"norm\": {\"pct\":' + CPUSystemPCTNorm + '}},'
    '\"iowait\":{\"norm\": {\"pct\":' + CPUIOWaitPCTNorm + '}},'
    '\"total\":{\"norm\": {\"pct\":' + CPUTotalNorm + '}},'
    '\"user\":{\"norm\": {\"pct\":' + CPUUserPCTNorm + '}},'
    '\"irq\":{\"norm\": {\"pct\":' + CPUIRQPCTNorm + '}}'
    '}}')
   
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.cpu", "system", "cpu", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    # print('\JSONToSend\n', JSONToSend, '\n')
    pass

def SystemFc(ComparisonTimer):
    """ This function analyse FC activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    # Setting vars for threads follow up
    # global SystemFcThread
    # SystemFcThread = threading.currentThread()
    
    
    # For each FC card with link ok
    for FcCard in FcCards:
        # Removing empty lines
        if(len(FcCard) != 0):
            # Generating current ELK timestamp for JSON message
            SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

            # Gathering data from OS command
            SystemFCCmd = 'fcstat ' + FcCard + ' | egrep -p "FC SCSI Traffic Statistics|FC SCSI Adapter Driver Information"'
            SystemFC = subprocess.Popen(SystemFCCmd, shell=True, stdout=subprocess.PIPE).stdout
            SystemFC = SystemFC.read().decode().split('\n')

            # Get data from multiple lines
            # For No DMA
            NoDMA = SystemFC[1].split()
            # For No Adapter Elements
            NoAdapterElements = SystemFC[2].split()
            # For No Command Resource
            NoCommandResource = SystemFC[3].split()
            # For Input Requests
            InputRequests = SystemFC[6].split()
            # For Output Requests
            OutputRequests = SystemFC[7].split()
            # For Input Bytes
            InputBytes = SystemFC[9].split()
            # Output Bytes
            OutputBytes = SystemFC[10].split()
            CurrFcCardWriteBytes = str(OutputBytes[2])

            # Filling values for this network interface
            # Grouping all kind of errors into one counter
            # IMPROVEMENT- Can be done by error counter but group method is easyer for counters in ELK...
            CurrFcCardErrors1 = int(NoDMA[4])
            CurrFcCardErrors2 = int(NoAdapterElements[4])
            CurrFcCardErrors3 = int(NoCommandResource[4])
            TotalFCError = CurrFcCardErrors1 + CurrFcCardErrors2 + CurrFcCardErrors3
            TotalFCError = str(TotalFCError)
            CurrFcCardErrors1 = str(CurrFcCardErrors1)
            CurrFcCardErrors2 = str(CurrFcCardErrors2)
            CurrFcCardErrors3 = str(CurrFcCardErrors3)
            # No disctinction between read/write errors in FC
            CurrFcCardWriteErrors = TotalFCError
            CurrFcCardWriteDropped = TotalFCError
            CurrFcCardReadErrors = TotalFCError
            CurrFcCardReadDropped = TotalFCError
            # Gathering Bytes and Packets values
            CurrFcCardWriteBytes = str(OutputBytes[2])
            CurrFcCardWritePackets = str(OutputRequests[2])
            CurrFcCardReadBytes = str(InputBytes[2])
            CurrFcCardReadPackets = str(InputRequests[2])
            
            # Let's construct JSON output for SystemFc (ELK 7.5.0)
            JSONToSendValues = (''
            '\"system\":{\"fc\":{\"name\":\"' + FcCard + '\",'
            '\"in\":{\"packets\":' + CurrFcCardReadPackets + ','
            '\"errors\":' + CurrFcCardReadErrors + ','
            '\"dropped\":' + CurrFcCardReadDropped + ','
            '\"bytes\":' + CurrFcCardReadBytes + '},'
            '\"out\":{\"errors\":' + CurrFcCardWriteErrors + ','
            '\"dropped\":' + CurrFcCardWriteDropped + ','
            '\"packets\":' + CurrFcCardWritePackets + ','
            '\"bytes\":' + CurrFcCardWriteBytes + '}}}')

            # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
            JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
            
            # Adding JSON metrics values gathered from OS command
            JSONToSend = JSONToSend + ',' + JSONToSendValues
            
            # Gathering "ELK formatted" dynamic JSON values
            RetDynamicJSON = GenerateDynamicJson("system.fc", "system", "fc", ComparisonTimer)
            
            # Adding dynamic "ELK Formating" JSON values into final JSON message
            JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
            
            # Let's send JSON message to ELK servers
            SendJSON(JSONToSend)
            # print('\JSONToSend\n', JSONToSend, '\n')
            pass

def SystemNetwork(ComparisonTimer):
    """ This function analyse Network activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """

    # Setting vars for threads follow up
    # global SystemNetworkThread
    # SystemNetworkThread = threading.currentThread()

    for NetworkCard in NetworkCards:
        # Removing empty lines
        if(len(NetworkCard) != 0):
            # Generating current ELK timestamp for JSON message
            SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

            # Gathering data from OS command
            SystemNetworkCmd = 'entstat ' + NetworkCard + ' | egrep "Packets|Bytes|Errors" | head -4'
            SystemNetwork = subprocess.Popen(SystemNetworkCmd, shell=True, stdout=subprocess.PIPE).stdout
            SystemNetwork = SystemNetwork.read().decode().split('\n')

            # Get data from multiple lines
            # For input/output packets
            PacketsLine = SystemNetwork[0].split()
            CurrNetCardReadPackets = str(PacketsLine[3])
            CurrNetCardWritePackets = str(PacketsLine[1])

            # For input/output bytes
            BytesLine = SystemNetwork[1].split()
            CurrNetCardReadBytes = str(BytesLine[3])
            CurrNetCardWriteBytes = str(BytesLine[1])

            # For input/output errors packets
            ErrorsLine = SystemNetwork[2].split()
            CurrNetCardReadErrors = str(ErrorsLine[5])
            CurrNetCardWriteErrors = str(ErrorsLine[2])

            # For input/output dropped packets
            DroppedLine = SystemNetwork[3].split()
            CurrNetCardReadDropped = str(DroppedLine[5])
            CurrNetCardWriteDropped = str(DroppedLine[2])

            # Let's construct JSON output for SystemNetwork (ELK 7.5.0)
            JSONToSendValues = (''
            '\"system\":{\"network\":{\"name\":\"' + NetworkCard + '\",'
            '\"in\":{\"packets\":' + CurrNetCardReadPackets + ','
            '\"errors\":' + CurrNetCardReadErrors + ','
            '\"dropped\":' + CurrNetCardReadDropped + ','
            '\"bytes\":' + CurrNetCardReadBytes + '},'
            '\"out\":{\"errors\":' + CurrNetCardWriteErrors + ','
            '\"dropped\":' + CurrNetCardWriteDropped + ','
            '\"packets\":' + CurrNetCardWritePackets + ','
            '\"bytes\":' + CurrNetCardWriteBytes + '}}}')

            
            # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
            JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
            
            # Adding JSON metrics values gathered from OS command
            JSONToSend = JSONToSend + ',' + JSONToSendValues
            
            # Gathering "ELK formatted" dynamic JSON values
            RetDynamicJSON = GenerateDynamicJson("system.network", "system", "network", ComparisonTimer)
            
            # Adding dynamic "ELK Formating" JSON values into final JSON message
            JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
            
            # Let's send JSON message to ELK servers
            SendJSON(JSONToSend)
            # print('\JSONToSend\n', JSONToSend, '\n')
            pass
 
def SystemLoad(ComparisonTimer):
    """ This function analyse CPU load and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """

    # Setting vars for threads follow up
    # global SystemLoadThread
    # SystemLoadThread = threading.currentThread()

    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Gathering data from OS command
    SystemLoadCmd = subprocess.Popen("uptime", shell=True, stdout=subprocess.PIPE).stdout
    SystemLoadCmd = SystemLoadCmd.read().decode().split()

    # Defining vars from command output
    LoadOne = float(SystemLoadCmd[-3].replace(',',''))
    LoadFive = float(SystemLoadCmd[-2].replace(',',''))
    LoadFifteen = float(SystemLoadCmd[-1])

    # Calculating per core values
    LoadOnePerCore = LoadOne / NumProc
    LoadFivePerCore = LoadFive / NumProc
    LoadFifteenPerCore = LoadFifteen / NumProc

    # Converting to string for JSON formating
    LoadOne = str(LoadOne)
    LoadFive = str(LoadFive)
    LoadFifteen = str(LoadFifteen)
    LoadOnePerCore = str(LoadOnePerCore)
    LoadFivePerCore = str(LoadFivePerCore)
    LoadFifteenPerCore = str(LoadFifteenPerCore)
    
    # Let's construct JSON output for SystemLoad (ELK 7.5.0)
    JSONToSendValues = (''
    '\"system\":{\"load\":{\"1\":' + LoadOne + ','
    '\"5\":' + LoadFive + ','
    '\"15\":' + LoadFifteen + ','
    '\"norm\":{\"1\":' + LoadOnePerCore + ','
    '\"5\":' + LoadFivePerCore + ','
    '\"15\":' + LoadFifteenPerCore + '},'
    '\"cores\":' + NumProcString + '}}')
    
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.load", "system", "load", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    # print('\JSONToSend\n', JSONToSend, '\n')
    pass

def SystemMemory(ComparisonTimer):
    """ This function analyse Memory activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """

    # Setting vars for threads follow up
    global SystemMemoryThread
    SystemMemoryThread = threading.currentThread()

    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Gathering data from OS command
    SystemMemory = subprocess.Popen('svmon -G -O unit=KB | egrep "memory|space"', shell=True, stdout=subprocess.PIPE).stdout
    SystemMemory = SystemMemory.read().decode().split('\n')

    # Get data from multiple lines
    # For Memory line
    MemoryLine = SystemMemory[0].split()
    # print('MemoryLine', MemoryLine)
    # For Space line
    PagingLine = SystemMemory[1].split()
    # print('PagingLine', PagingLine)

    # Get MEMORY usage informations and convert to B
    RealMemTotal = int(MemoryLine[1]) * 1000
    RealMemFree = int(MemoryLine[3]) * 1000
    RealMemUsed = int(MemoryLine[2]) * 1000    

    # Calculating percentage for memory
    # BUG - Removed ' * 100 ' for ELK correct formating but strange...
    RealMemUsedPCT = RealMemUsed / RealMemTotal

    # Custom metrics
    VirtualMemUsed = int(MemoryLine[5]) * 1000
    VirtualMemUsedPCT = VirtualMemUsed / RealMemTotal
    VirtualMemFreePCT = 1 - VirtualMemUsedPCT
    VirtualMemFree = VirtualMemUsedPCT * RealMemTotal
    CacheMemUsed = RealMemUsed - VirtualMemUsed
    CacheMemUsedPCT = CacheMemUsed / RealMemTotal

    # Get SWAP usage informations and convert MB to B
    TotalSwapBytes = int(PagingLine[2]) * 1000
    UsedSwapBytes = int(PagingLine[3]) * 1000
    
    FreeSwapBytes = TotalSwapBytes - UsedSwapBytes

    # Calculating percentage for paging
    UsedSwapPCT = UsedSwapBytes / TotalSwapBytes

    # Converting to string
    RealMemTotal = str(RealMemTotal)
    RealMemFree = str(RealMemFree)
    RealMemUsed = str(RealMemUsed)
    RealMemUsedPCT = str(RealMemUsedPCT)
    VirtualMemUsed = str(VirtualMemUsed)
    VirtualMemUsedPCT = str(VirtualMemUsedPCT)
    VirtualMemFree = str(VirtualMemFree)
    CacheMemUsed = str(CacheMemUsed)
    CacheMemUsedPCT = str(CacheMemUsedPCT)
    TotalSwapBytes = str(TotalSwapBytes)
    UsedSwapBytes = str(UsedSwapBytes)
    FreeSwapBytes = str(FreeSwapBytes)
    UsedSwapPCT = str(UsedSwapPCT)

    # IMPROVEMENT- If LargePages are used on AIX, this part will need some work to define correct values
    # For now, setting to str = "0"
    hugepagesfree = "0"
    hugepagesreserved = "0"
    hugepagessurplus = "0"
    readaheadpages = "0"
    readaheadcached = "0"
    # IMPROVEMENT - This is the default pagesize for LARGEPAGE AIX, can implement huge page detection but not used for now in our AIX env
    hugepagesdefaultsize = "16384000"
    hugepagestotal = "0"
    hugepagesbytes = "0"
    hugepagespct = "0"

    # Gathering data from OS command N+0
    SystemMemoryA = subprocess.Popen('vmstat -vs', shell=True, stdout=subprocess.PIPE).stdout
    SystemMemoryA = SystemMemoryA.read().decode().split('\n')
    
    # Sleeping for 1 sec to make second measurement
    time.sleep(1)
   
    # Gathering data from OS command N+1
    SystemMemoryB = subprocess.Popen('vmstat -vs', shell=True, stdout=subprocess.PIPE).stdout
    SystemMemoryB = SystemMemoryB.read().decode().split('\n')
    
    # Converting into string and calulating diference between values
    pagefault = str(int(SystemMemoryB[0].split()[0]) - int(SystemMemoryA[0].split()[0]))
    rampagein = str(int(SystemMemoryB[1].split()[0]) - int(SystemMemoryA[1].split()[0]))
    rampageout = str(int(SystemMemoryB[2].split()[0]) - int(SystemMemoryA[2].split()[0]))
    swappagein = str(int(SystemMemoryB[3].split()[0]) - int(SystemMemoryA[3].split()[0]))
    swappageout = str(int(SystemMemoryB[4].split()[0]) - int(SystemMemoryA[4].split()[0]))
    reclaims = str(int(SystemMemoryB[5].split()[0]) - int(SystemMemoryA[5].split()[0]))
    pagescanned = str(int(SystemMemoryB[8].split()[0]) - int(SystemMemoryA[8].split()[0]))
    pagesfreed = str(int(SystemMemoryB[10].split()[0]) - int(SystemMemoryA[10].split()[0]))
    pendingiowait = str(int(SystemMemoryB[14].split()[0]) - int(SystemMemoryA[14].split()[0]))
    pagenumber = str(int(SystemMemoryB[26].split()[0]) - int(SystemMemoryA[26].split()[0]))
    lruablepages = str(int(SystemMemoryB[27].split()[0]) - int(SystemMemoryA[27].split()[0]))
    freepages = str(int(SystemMemoryB[28].split()[0]) - int(SystemMemoryA[28].split()[0]))
    pinnedpages = str(int(SystemMemoryB[30].split()[0]) - int(SystemMemoryA[30].split()[0]))
    numpermpct = str(float(SystemMemoryB[34].split()[0]) / 100)
    filepages = str(int(SystemMemoryB[35].split()[0]) - int(SystemMemoryA[35].split()[0]))
    numclientpct = str(float(SystemMemoryB[38].split()[0]) / 100)
    clientpages = str(int(SystemMemoryB[40].split()[0]) - int(SystemMemoryA[40].split()[0]))
    diskblockedio = str(int(SystemMemoryB[42].split()[0]) - int(SystemMemoryA[42].split()[0]))
    swapblockedio = str(int(SystemMemoryB[43].split()[0]) - int(SystemMemoryA[43].split()[0]))
    fsblockedio = str(int(SystemMemoryB[44].split()[0]) - int(SystemMemoryA[44].split()[0]))
    clientfsblockedio = str(int(SystemMemoryB[45].split()[0]) - int(SystemMemoryA[45].split()[0]))
    externalpagerfsblockedio = str(int(SystemMemoryB[46].split()[0]) - int(SystemMemoryA[46].split()[0]))
    computpagespct = str(float(SystemMemoryB[47].split()[0]) / 100)

    # Formatting custom metrics JSON string
    CustomMetricJSON = (''
    '\"custom\":{\"virtualmemory\":{\"value\":' + VirtualMemUsed + ',\"pct\":' + VirtualMemUsedPCT + '},\"cachedmemory\":{\"value\":' + CacheMemUsed + ',\"pct\":' + CacheMemUsedPCT + '},'
    '\"pagefaultpersec\":' + pagefault + ',\"ram\":{\"pageinpersec\":' + rampagein + ',\"pageoutpersec\":' + rampageout + '},'
    '\"swap\":{\"pageinpersec\":' + swappagein + ',\"pageoutpersec\":' + swappageout + '},\"reclaimspersec\":' + reclaims + ',\"pagescannedpersec\":' + pagescanned + ','
    '\"pagesfreedpersec\":' + pagesfreed + ',\"pendingiowaitpersec\":' + pendingiowait + ',\"pagenumberpersec\":' + pagenumber + ',\"lruablepagespersec\":' + lruablepages + ','
    '\"freepagespersec\":' + freepages + ',\"pinnedpagespersec\":' + pinnedpages + ',\"numpermpct\":' + numpermpct + ',\"filepagespersec\":' + filepages + ','
    '\"numclientpct\":' + numclientpct + ',\"clientpagespersec\":' + clientpages + ',\"blockedio\":{\"diskpersec\":' + diskblockedio + ',\"swappersec\":' + swapblockedio + ','
    '\"fspersec\":' + fsblockedio + ',\"clientfspersec\":' + clientfsblockedio + ',\"externalpagerfspersec\":' + externalpagerfsblockedio + '},\"computpagespct\":' + computpagespct + '},')

    # Let's construct JSON output for SystemMemory (ELK 7.5.0)
    JSONToSendValues = (''
    '\"system\":{'
    '\"memory\":{' + CustomMetricJSON + ''
    '\"total\":' + RealMemTotal + ','
    '\"used\":{'
    '\"bytes\":' + RealMemUsed + ','
    '\"pct\":' + RealMemUsedPCT + '},'
    '\"free\":' + RealMemFree + ','
    '\"actual\":{'
    '\"free\":' + VirtualMemFree + ','
    '\"used\":{'
    '\"pct\":' + VirtualMemUsedPCT + ','
    '\"bytes\":' + VirtualMemUsed + '}},'
    '\"swap\":{'
    '\"in\":{'
    '\"pages\":' + swappagein + '},'
    '\"out\":{'
    '\"pages\":' + swappageout + '},'
    '\"readahead\":{'
    '\"pages\":' + readaheadpages + ','
    '\"cached\":' + readaheadcached + '},'
    '\"total\":' + TotalSwapBytes + ','
    '\"used\":{'
    '\"bytes\":' + UsedSwapBytes + ','
    '\"pct\":' + UsedSwapPCT + '},'
    '\"free\":' + FreeSwapBytes + '},'
    '\"hugepages\":{'
    '\"total\":' + hugepagestotal + ','
    '\"used\":{'
    '\"pct\":' + hugepagespct + ','
    '\"bytes\":' + hugepagesbytes + '},'
    '\"free\":' + hugepagesfree + ','
    '\"reserved\":' + hugepagesreserved + ','
    '\"surplus\":' + hugepagessurplus + ','
    '\"default_size\":' + hugepagesdefaultsize + ','
    '\"swap\":{'
    '\"out\":{'
    '\"fallback\":' + pagefault + ','
    '\"pages\":' + swappageout + '}}}}}')

    
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.memory", "system", "memory", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    # print('\JSONToSend\n', JSONToSend, '\n')
    pass

def SystemProcessSummary(ComparisonTimer):
    """ This function analyse processes activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Gathering data from OS command
    SystemProcessSummary = subprocess.Popen("ps -ef -m -o status | awk '{print $NF}'", shell=True, stdout=subprocess.PIPE).stdout
    SystemProcessSummary = SystemProcessSummary.read().decode().split()

    # Defining vars from command output
    # CPUIdlePCTNorm = str(float(SystemCoreAndCpuCmd[17]) / 100)

    # Defining counters for increment loop
    TotalProcessesCount = 0
    ActivePS = 0
    SwappedPS = 0
    IdlePS = 0
    CanceledPS = 0
    StoppedPS = 0
    RunningPS = 0
    SleepingPS = 0
    SwappedPS = 0
    UnknownPS = 0
    ZombiePS = 0
    DeadPS = 0

    # Incrementing counters depending of the type of process
    # IMPROVEMENT - Can be imporved by unsing Python's style swith/case but maybe incompatible with python2.7, to check !
    for State in SystemProcessSummary:
        if "A" in State:
            ActivePS = ActivePS + 1
            TotalProcessesCount = TotalProcessesCount + 1
        elif "W" in State:
            SwappedPS = SwappedPS + 1
            TotalProcessesCount = TotalProcessesCount + 1
        elif "I" in State:
            IdlePS = IdlePS + 1
            TotalProcessesCount = TotalProcessesCount + 1
        elif "Z" in State:
            CanceledPS = CanceledPS + 1
            TotalProcessesCount = TotalProcessesCount + 1
        elif "T" in State:
            StoppedPS = StoppedPS + 1
            TotalProcessesCount = TotalProcessesCount + 1
        elif "R" in State:
            RunningPS = RunningPS + 1
            TotalProcessesCount = TotalProcessesCount + 1
        elif "S" in State:
            SleepingPS = SleepingPS + 1
            TotalProcessesCount = TotalProcessesCount + 1
        else:
            UnknownPS = UnknownPS + 1
            TotalProcessesCount = TotalProcessesCount + 1

    # Gathering data from OS command Zombie processes
    SystemProcessSummaryZombiePS = subprocess.Popen("ps -ef | grep -i defunct | grep -v grep | wc -l | awk '{print $NF}'", shell=True, stdout=subprocess.PIPE).stdout
    ZombiePS = SystemProcessSummaryZombiePS.read().decode().split()[0]

    # Calculating dead process upon Stopped and Canceled states
    DeadPS = CanceledPS + StoppedPS

    # Converting to string
    TotalProcessesCount = str(TotalProcessesCount)
    ActivePS = str(ActivePS)
    SwappedPS = str(SwappedPS)
    IdlePS = str(IdlePS)
    CanceledPS = str(CanceledPS)
    StoppedPS = str(StoppedPS)
    RunningPS = str(RunningPS)
    SleepingPS = str(SleepingPS)
    SwappedPS = str(SwappedPS)
    UnknownPS = str(UnknownPS)
    ZombiePS = str(ZombiePS)
    DeadPS = str(DeadPS)

    # Let's construct JSON output for SystemProcessSummary (ELK 7.5.0)
    JSONToSendValues = (''
    '\"system\":{\"process\":{\"summary\":{\"zombie\":' + ZombiePS + ','
    '\"active\":' + ActivePS + ','
    '\"unknown\":' + UnknownPS + ','
    '\"dead\":' + DeadPS + ','
    '\"total\":' + TotalProcessesCount + ','
    '\"sleeping\":' + SleepingPS + ','
    '\"running\":' + RunningPS + ','
    '\"idle\":' + IdlePS + ','
    '\"stopped\":' + StoppedPS + '}}}')
    
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.process.summary", "system", "process_summary", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    # print('\JSONToSend\n', JSONToSend, '\n')
    pass

def SystemDiskIO(ComparisonTimer):
    """ This function analyse disks activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """

    # Setting vars for threads follow up
    global SystemDiskIOThread
    SystemDiskIOThread = threading.currentThread()

    # Checking if some restrictions are in place for HDISKs list
    if HdiskRestricted == 'all':
        # Gathering disk list from OS command
        SystemDiskIO = subprocess.Popen("lspv | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout
        SystemDiskIO = SystemDiskIO.read().decode().split()
        
        # Getting system command ready
        SystemDiskIOCmd = 'iostat -D ' + str(DiskSampleRate) + ' 1'
        
    else:
        # Restriction is in place,reducing disk list to specified disks
        SystemDiskIO = []
        SystemDiskIOStat = HdiskRestricted.replace(',',' ')
        # logging.info("SystemDiskIOStat " + str(SystemDiskIOStat))
        SystemDiskIO = HdiskRestricted.split(',')
        # logging.info("SystemDiskIO " + str(SystemDiskIO))
        
        # Getting system command ready
        SystemDiskIOCmd = 'iostat -D ' + str(SystemDiskIOStat) + ' ' + str(DiskSampleRate) + ' 1'
        
    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    # Gathering data for disks
    SystemDiskIOResultArray = subprocess.Popen(SystemDiskIOCmd, shell=True, stdout=subprocess.PIPE).stdout
    SystemDiskIOResultArray = SystemDiskIOResultArray.read().decode().split('\n')
    
    # Initializing start ID's for result lines
    NameSplitedLineId = 3
    XferSplitedLineId = 4
    ReadSplitedLineId = 6
    WriteSplitedLineId = 8
    QueueSplitedLineId = 10

    # Looping on all disks
    for Disk in SystemDiskIO:
        # Split cmd result into different lines
        NameSplitedLine = SystemDiskIOResultArray[NameSplitedLineId].split()
        XferSplitedLine = SystemDiskIOResultArray[XferSplitedLineId].split()
        ReadSplitedLine = SystemDiskIOResultArray[ReadSplitedLineId].split()
        WriteSplitedLine = SystemDiskIOResultArray[WriteSplitedLineId].split()
        QueueSplitedLine = SystemDiskIOResultArray[QueueSplitedLineId].split()
        
        # Incrementing Id's to switch to the next disk on the next diskio loop execution
        NameSplitedLineId = NameSplitedLineId + 8
        XferSplitedLineId = XferSplitedLineId + 8
        ReadSplitedLineId = ReadSplitedLineId + 8
        WriteSplitedLineId = WriteSplitedLineId + 8
        QueueSplitedLineId = QueueSplitedLineId + 8
        
        # Setting disk name
        DiskName = NameSplitedLine[0]
        
        # Getting disk size
        DiskIOSizeCmd = 'bootinfo -s ' + str(DiskName)
        DiskIOSize = subprocess.Popen(DiskIOSizeCmd, shell=True, stdout=subprocess.PIPE).stdout
        DiskIOSize = DiskIOSize.read().decode().split()
        DiskIOSize = int(float(str(DiskIOSize[0])) * 1000 * 1000)

        # Gathering data for write counters
        DiskWriteCount = WriteSplitedLine[0]
        DiskWriteTime = WriteSplitedLine[1]
        DiskWriteBytes = XferSplitedLine[4]

        # Converting value depending of the unit
        if DiskWriteBytes.endswith("K"):
            
            # DiskWriteBytes = DiskWriteBytes.replace(".", "")
            DiskWriteBytes = float(DiskWriteBytes.replace("K", "")) * 1000
            pass
        elif DiskWriteBytes.endswith("M"):
            # DiskWriteBytes = DiskWriteBytes.replace(".", "")
            # DiskWriteBytes = DiskWriteBytes.replace("M", "") + "00000"
            DiskWriteBytes = float(DiskWriteBytes.replace("M", "")) * 1000 * 1000
            pass
        elif DiskWriteBytes.endswith("G"):
            # DiskWriteBytes = DiskWriteBytes.replace(".", "")
            # DiskWriteBytes = DiskWriteBytes.replace("G", "") + "00000000"
            DiskWriteBytes = float(DiskWriteBytes.replace("G", "")) * 1000 * 1000 * 1000
            pass

        # Gathering data for write counters
        DiskReadCount = ReadSplitedLine[0]
        DiskReadTime = ReadSplitedLine[1]
        DiskReadBytes = XferSplitedLine[3]

        # Converting value depending of the unit
        if DiskReadBytes.endswith("K"):
            # DiskReadBytes = DiskReadBytes.replace(".", "")
            # DiskReadBytes = DiskReadBytes.replace("K", "") + "00"
            DiskReadBytes = float(DiskReadBytes.replace("K", "")) * 1000
            pass
        elif DiskReadBytes.endswith("M"):
            # DiskReadBytes = DiskReadBytes.replace(".", "")
            # DiskReadBytes = DiskReadBytes.replace("M", "") + "00000"
            DiskReadBytes = float(DiskReadBytes.replace("M", "")) * 1000 * 1000
            pass
        elif DiskReadBytes.endswith("G"):
            # DiskReadBytes = DiskReadBytes.replace(".", "")
            # DiskReadBytes = DiskReadBytes.replace("G", "") + "00000000"
            DiskReadBytes = float(DiskReadBytes.replace("G", "")) * 1000 * 1000 * 1000
            pass

        # Gathering IO Queue size and busy counters
        IoWaitQueueAVGSize = QueueSplitedLine[3]
        IoServiceQueueAVGSize = QueueSplitedLine[4]
        IoQueueFullSize = QueueSplitedLine[5]
        IoBusy = XferSplitedLine[0]

        # Calculating value depending of disk measurement period
        DiskWriteRequestPerSec = float(DiskWriteCount) * DiskSampleRate
        DiskWriteBytesPerSec = float(DiskWriteBytes) * DiskSampleRate
        DiskReadRequestPerSec = float(DiskReadCount) * DiskSampleRate
        DiskReadBytesPerSec = float(DiskReadBytes) * DiskSampleRate

        # IMPROVEMENT - IoTime - Je sais pas le traduire =0 pour le moment...
        IoTime = 0
        # IMPROVEMENT - IoRequestAVGSize - Je sais pas le traduire =0 pour le moment...
        IORequestAVGSize = 0
        # IMPROVEMENT - IoAwait - Je sais pas le traduire =0 pour le moment...
        IoAwait = 0
        # IMPROVEMENT - DiskWriteAwait - Je sais pas le traduire =0 pour le moment...
        DiskWriteAwait = 0
        # IMPROVEMENT - DiskWriteRequestMergePerSec - Je sais pas le traduire =0 pour le moment...
        DiskWriteRequestMergePerSec = 0
        # IMPROVEMENT - DiskReadAwait - Je sais pas le traduire =0 pour le moment...
        DiskReadAwait = 0
        # IMPROVEMENT - DiskReadRequestMergePerSec - Je sais pas le traduire =0 pour le moment...
        DiskReadRequestMergePerSec = 0

        # Calculating
        Globalawait = int(float(DiskWriteAwait)) + int(float(DiskReadAwait)) / 2
        IoServiceTime = int(float(DiskWriteTime)) + int(float(DiskReadTime)) / 2

        # Converting all vars to string type
        DiskName = str(DiskName)
        XferSplitedLine = str(XferSplitedLine)
        ReadSplitedLine = str(ReadSplitedLine)
        WriteSplitedLine = str(WriteSplitedLine)
        QueueSplitedLine = str(QueueSplitedLine)
        DiskWriteCount = str(DiskWriteCount)
        DiskWriteTime = str(DiskWriteTime)
        DiskWriteBytes = str(DiskWriteBytes)
        DiskReadCount = str(DiskReadCount)
        DiskReadTime = str(DiskReadTime)
        DiskReadBytes = str(DiskReadBytes)
        IoWaitQueueAVGSize = str(IoWaitQueueAVGSize)
        IoServiceQueueAVGSize = str(IoServiceQueueAVGSize)
        IoQueueFullSize = str(IoQueueFullSize)
        IoBusy = str(IoBusy)
        DiskWriteRequestPerSec = str(DiskWriteRequestPerSec)
        DiskWriteBytesPerSec = str(DiskWriteBytesPerSec)
        DiskReadRequestPerSec = str(DiskReadRequestPerSec)
        DiskReadBytesPerSec = str(DiskReadBytesPerSec)
        Globalawait = str(Globalawait)
        IoServiceTime = str(IoServiceTime)
        IoTime = str(IoTime)
        IORequestAVGSize = str(IORequestAVGSize)
        IoAwait = str(IoAwait)
        DiskWriteAwait = str(DiskWriteAwait)
        DiskWriteRequestMergePerSec = str(DiskWriteRequestMergePerSec)
        DiskReadAwait = str(DiskReadAwait)
        DiskReadRequestMergePerSec = str(DiskReadRequestMergePerSec)
        DiskIOSize = str(DiskIOSize)

        # Let's construct JSON output for SystemDiskIO (ELK 7.5.0)       
        JSONToSendValues = (''
        '\"system\":{\"diskio\":{\"iostat\":{'
        '\"await\":' + Globalawait + ','
        '\"service_time\":' + IoServiceTime + ','
        '\"busy\":' + IoBusy + ','
        '\"read\":{\"per_sec\":{'
        '\"bytes\":' + DiskReadBytes + '},'
        '\"await\":' + DiskReadAwait + ','
        '\"request\":{'
        '\"merges_per_sec\":' + DiskReadRequestMergePerSec + ','
        '\"per_sec\":' + DiskReadCount + '}},'
        '\"write\":{'
        '\"request\":{'
        '\"merges_per_sec\":' + DiskWriteRequestMergePerSec + ','
        '\"per_sec\":' + DiskWriteCount + '},'
        '\"per_sec\":{'
        '\"bytes\":' + DiskWriteBytes + '},'
        '\"await\":' + DiskWriteAwait + ''
        '},\"queue\":{'
        '\"avg_size\":' + IoWaitQueueAVGSize + ','
        '\"sq_avg_size\":' + IoServiceQueueAVGSize + ','
        '\"sq_full_size\":' + IoQueueFullSize + '},'
        '\"request\":{'
        '\"avg_size\":' + IORequestAVGSize + '}},'
        '\"name\":\"' + DiskName + '\",'
        '\"size\":\"' + DiskIOSize + '\",'
        '\"read\":{'
        '\"bytes\":' + DiskReadBytes + ','
        '\"count\":' + DiskReadCount + ','
        '\"time\":' + DiskReadTime + '},'
        '\"write\":{'
        '\"bytes\":' + DiskWriteBytes + ','
        '\"count\":' + DiskWriteCount + ','
        '\"time\":' + DiskWriteTime + '},'
        '\"io\":{\"time\":' + IoAwait + '}}}')
        
        # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
        JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
        
        # Adding JSON metrics values gathered from OS command
        JSONToSend = JSONToSend + ',' + JSONToSendValues
        
        # Gathering "ELK formatted" dynamic JSON values
        RetDynamicJSON = GenerateDynamicJson("system.diskio", "system", "diskio", ComparisonTimer)
        
        # Adding dynamic "ELK Formating" JSON values into final JSON message
        JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
        
        # Let's send JSON message to ELK servers
        SendJSON(JSONToSend)
        # print('\nJSONToSend\n', JSONToSend, '\n')
        pass

    pass

def SystemFilesystemAndFstat(ComparisonTimer):
    """ This function analyse FS activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """

    # Setting vars for threads follow up
    # global SystemFilesystemAndFstatThread
    # SystemFilesystemAndFstatThread = threading.currentThread()

    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Gathering disk list from OS command
    SystemFilesystemAndFstat = subprocess.Popen('df -k | egrep -v "(Filesystem|:|/proc|/aha)"', shell=True, stdout=subprocess.PIPE).stdout
    SystemFilesystemAndFstat = SystemFilesystemAndFstat.read().decode().split('\n')

    # Initializing counters for Total FS Size message and FS loop
    FSTotalFiles = 0
    FSTotalSizeFree = 0
    FSTotalSizeUsed = 0
    FSTotalSize = 0
    FSTotalCount = 0

    # First, we send message for each FS metrics in SystemFilesystem
    for FSLine in SystemFilesystemAndFstat:
        # Removing empty lines
        if(len(FSLine) != 0):
            # Spitting the current line
            SplitFSLine = FSLine.split()

            # Filling all necessary values
            FSDeviceName = SplitFSLine[0]
            FSNameShort = FSDeviceName.replace('/','')
            FSAvailable = int(SplitFSLine[2]) * 1000
            FSUsedPCT = int(SplitFSLine[3].replace('%','')) / 100
            FSTotal = int(SplitFSLine[1]) * 1000
            FSUsed = FSTotal - FSAvailable
            FSMountPoint = SplitFSLine[6]
            InodeUsed = int(SplitFSLine[4])
            InodeUsedPCTShort = int(SplitFSLine[5].replace('%','')) / 100
            InodeFree = 100 * int(InodeUsed) / InodeUsedPCTShort
            InodeTotal = InodeFree + InodeUsed

            # Incrementing counters for Total FS Size message
            FSTotalFiles = FSTotalFiles + InodeUsed
            FSTotalSizeFree = FSTotalSizeFree + FSAvailable
            FSTotalSizeUsed = FSTotalSizeUsed + FSUsed
            FSTotalSize = FSTotalSize + FSTotal
            FSTotalCount = FSTotalCount + 1

            # Convert vars into strings
            FSDeviceName = str(FSDeviceName)
            FSMountPoint = str(FSMountPoint)
            FSAvailable = str(FSAvailable)
            FSUsedPCT = str(FSUsedPCT)
            FSTotal = str(FSTotal)
            FSUsed = str(FSUsed)
            InodeUsed = str(InodeUsed)
            InodeUsedPCTShort = str(InodeUsedPCTShort)
            InodeFree = str(InodeFree)
            InodeTotal = str(InodeTotal)
            FSNameShort = str(FSNameShort)

            # Let's construct JSON output for SystemFilesystem (ELK 7.5.0)
            JSONToSendValues = (''
            '\"system\": {\"filesystem\": {\"type\": \"jfs\",'
            '\"total\": ' + FSTotal + ','
            '\"mount_point\": \"' + FSMountPoint + '\",'
            '\"available\": ' + FSAvailable + ','
            '\"files\": ' + InodeUsed + ','
            '\"free_files\": ' + InodeFree + ','
            '\"device_name\": \"' + FSDeviceName + '\",'
            '\"free\": ' + FSAvailable + ','
            '\"used\": {\"pct\": ' + FSUsedPCT + ','
            '\"bytes\": ' + FSUsed + '}}}'
            '')
            
            # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
            JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
            
            # Adding JSON metrics values gathered from OS command
            JSONToSend = JSONToSend + ',' + JSONToSendValues
            
            # Gathering "ELK formatted" dynamic JSON values
            RetDynamicJSON = GenerateDynamicJson("system.filesystem", "system", "filesystem", ComparisonTimer)
            
            # Adding dynamic "ELK Formating" JSON values into final JSON message
            JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
            
            # Let's send JSON message to ELK servers
            SendJSON(JSONToSend)
            # print('\JSONToSend\n', JSONToSend, '\n')

    # Convert vars into strings
    FSTotalFiles = str(FSTotalFiles)
    FSTotalSizeFree = str(FSTotalSizeFree)
    FSTotalSizeUsed = str(FSTotalSizeUsed)
    FSTotalSize = str(FSTotalSize)
    FSTotalCount = str(FSTotalCount)

    # Let's construct JSON output for SystemFstat (ELK 7.5.0)
    JSONToSendValues = (''
    '\"system\":{\"fsstat\":{\"total_size\":{\"free\":' + FSTotalSizeFree + ','
    '\"used\":' + FSTotalSizeUsed + ','
    '\"total\":' + FSTotalSize + '},'
    '\"count\":' + FSTotalCount + ','
    '\"total_files\":' + FSTotalFiles + '}}')
    
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.fsstat", "system", "fsstat", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    # print('\JSONToSend\n', JSONToSend, '\n')
    pass

def SystemHPMStat(ComparisonTimer):
    """ This function analyse Hypervisor and LPAR activity with hpmstat command and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    # Intitalize thread for follow up
    global SystemHPMStatThread
    SystemHPMStatThread = threading.currentThread()
    
    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Defining which values we want to take from output for General group
    # If some fields are added or remove, all the code has to be reviewed as positions will change...
    
    # We can get several "HPM Counter reserved" errors, then hidding them
    try:
        # Checking Power Hardware to get correct counters (all counters are not available on all architecture...)
        if LPARArch == "PowerPC_POWER8":
            # For Power 8
            HPMStatInclude = 'Cycles per instruction|Instructions per cycles|ITLB miss rate per inst|L2 Instruction Miss Rate|L3 Instruction Miss Rate'

            # Gathering data from OS command
            SystemHPMGrpGeneralCmd = 'hpmstat -m General:uk | egrep -w "' + HPMStatInclude + '"'
            
            SystemHPMGrpGeneral = subprocess.Popen(SystemHPMGrpGeneralCmd, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
            SystemHPMGrpGeneral = SystemHPMGrpGeneral.read().decode().split('\n')
            
            CyclePerInst = SystemHPMGrpGeneral[0].split()[-1]
            InstPerCycle = SystemHPMGrpGeneral[1].split()[-1]
            L2MissRate = SystemHPMGrpGeneral[2].split()[-2]
            L3MissRate = SystemHPMGrpGeneral[3].split()[-2]
            ITLBMissRate = SystemHPMGrpGeneral[4].split()[-2]

            FinalString = '{\"cpugeneral\":{\"cycleperinst\":' + CyclePerInst + ',\"instpercycle\":' + InstPerCycle + ',\"l2missrate\":' + L2MissRate + ',\"l3missrate\":' + L3MissRate + ',\"itlbmissrate\":' + ITLBMissRate + '},'

        elif LPARArch == "PowerPC_POWER9":
            # For Power 9
            HPMStatInclude = 'Run cycles per run instruction|% ITLB miss rate per inst|L2 demand Load Miss Rate |L3 demand Load Miss Rate '
            
            # Gathering data from OS command
            SystemHPMGrpGeneralCmd = 'hpmstat -m General:uk | egrep -w "' + HPMStatInclude + '"'
            
            SystemHPMGrpGeneral = subprocess.Popen(SystemHPMGrpGeneralCmd, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
            SystemHPMGrpGeneral = SystemHPMGrpGeneral.read().decode().split('\n')
            
            CyclePerInst = SystemHPMGrpGeneral[0].split()[-1]
            L2MissRate = SystemHPMGrpGeneral[1].split()[-2]
            L3MissRate = SystemHPMGrpGeneral[2].split()[-2]
            ITLBMissRate = SystemHPMGrpGeneral[3].split()[-2]

            FinalString = '{\"cpugeneral\":{\"cycleperinst\":' + CyclePerInst + ',\"l2missrate\":' + L2MissRate + ',\"l3missrate\":' + L3MissRate + ',\"itlbmissrate\":' + ITLBMissRate + '},'
            
        elif LPARArch == "PowerPC_POWER7":
            # For Power 7
            HPMStatInclude = 'Cycles per instruction|Instructions per cycles|L2 Instruction Miss Rate |L3 Instruction Miss Rate ' 
            
            # Gathering data from OS command
            SystemHPMGrpGeneralCmd = 'hpmstat -m General:uk | egrep -w "' + HPMStatInclude + '"'

            SystemHPMGrpGeneral = subprocess.Popen(SystemHPMGrpGeneralCmd, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
            SystemHPMGrpGeneral = SystemHPMGrpGeneral.read().decode().split('\n')

            CyclePerInst = SystemHPMGrpGeneral[0].split()[-2]
            InstPerCycle = SystemHPMGrpGeneral[1].split()[-2]
            L2MissRate = SystemHPMGrpGeneral[2].split()[-1]
            L3MissRate = SystemHPMGrpGeneral[3].split()[-1]

            FinalString = '{\"cpugeneral\":{\"cycleperinst\":' + CyclePerInst + ',\"instpercycle\":' + InstPerCycle + ',\"l2missrate\":' + L2MissRate + ',\"l3missrate\":' + L3MissRate + '},'
    except:
        # Error detected, exiting function wand wait for next schedule
        # traceback.print_exc()
        return
    
    # No SMT or Cache reload counters exist for Power 9 (Need more investigation maybe...)
    
    # SMT and CPU Cache reload counters exists for Power8
    if LPARArch == "PowerPC_POWER8":
        # Defining which values we want to take from output for group 4
        # If some fields are added or remove, all the code has to be reviewed as positions will change...
        HPMStatInclude = "PM_RUN_CYC_SMT2_MODE|PM_RUN_CYC_SMT4_MODE|PM_RUN_CYC_SMT8_MODE"
        
        # Gathering data from OS command
        SystemHPMGrp4Cmd = "/usr/bin/hpmstat -g4:uk -r | egrep -w \"" + HPMStatInclude + "\""
        SystemHPMGrp4 = subprocess.Popen(SystemHPMGrp4Cmd, shell=True, stdout=subprocess.PIPE).stdout
        SystemHPMGrp4 = SystemHPMGrp4.read().decode().split('\n')
        
        Smt2Inst = SystemHPMGrp4[0].split()[-1]
        Smt4Inst = SystemHPMGrp4[1].split()[-1]
        Smt8Inst = SystemHPMGrp4[2].split()[-1]
        
        FinalString = str(FinalString) + '\"smtmode\":{\"smt2\":' + Smt2Inst + ',\"smt4\":' + Smt4Inst + ',\"smt8\":' + Smt8Inst + ','
        
        # Defining which values we want to take from output for group 3
        # If some fields are added or remove, all the code has to be reviewed as positions will change...
        HPMStatInclude = "PM_RUN_CYC_ST_MODE"
        
        # Gathering data from OS command
        SystemHPMGrp3Cmd = "/usr/bin/hpmstat -g3:uk -r | egrep -w \"" + HPMStatInclude + "\""
        SystemHPMGrp3 = subprocess.Popen(SystemHPMGrp3Cmd, shell=True, stdout=subprocess.PIPE).stdout
        SystemHPMGrp3 = SystemHPMGrp3.read().decode().split('\n')
        
        Smt1Inst = SystemHPMGrp3[0].split()[-1]
        
        FinalString = str(FinalString) + '\"smt1\":' + Smt1Inst + '},'
        
        # Defining which values we want to take from output for group 53
        # If some fields are added or remove, all the code has to be reviewed as positions will change...
        HPMStatInclude = "PM_DATA_FROM_L2MISS_MOD|PM_DATA_FROM_LMEM|PM_DATA_FROM_RMEM|PM_DATA_FROM_DMEM"
        
        # Gathering data from OS command
        SystemHPMGrp53Cmd = "/usr/bin/hpmstat -g53:uk -r | egrep -w \"" + HPMStatInclude + "\""
        SystemHPMGrp53 = subprocess.Popen(SystemHPMGrp53Cmd, shell=True, stdout=subprocess.PIPE).stdout
        SystemHPMGrp53 = SystemHPMGrp53.read().decode().split('\n')
        
        L2cachemiss = SystemHPMGrp53[0].split()[-1]
        LocalCacheReload = SystemHPMGrp53[1].split()[-1]
        RemoteCacheReload = SystemHPMGrp53[2].split()[-1]
        DistantCacheReload = SystemHPMGrp53[3].split()[-1]
        
        FinalString = str(FinalString) + '\"cpucachereload\":{\"l2cachemiss\":' + L2cachemiss + ',\"local\":' + LocalCacheReload + ',\"remote\":' + RemoteCacheReload + ',\"distant\":' + DistantCacheReload + '},'
    
    # Cache reload counters only exists for Power7 in differrent and separate group id
    if LPARArch == "PowerPC_POWER7":
        # Defining which values we want to take from output for group 53
        # If some fields are added or remove, all the code has to be reviewed as positions will change...
        HPMStatInclude = "PM_DATA_FROM_LMEM|PM_DATA_FROM_RMEM|PM_DATA_FROM_DMEM"
        
        # Gathering data from OS command
        SystemHPMGrp53Cmd = "/usr/bin/hpmstat -g97,99:uk -r | egrep -w \"" + HPMStatInclude + "\""
        SystemHPMGrp53 = subprocess.Popen(SystemHPMGrp53Cmd, shell=True, stdout=subprocess.PIPE).stdout
        SystemHPMGrp53 = SystemHPMGrp53.read().decode().split('\n')
        
        LocalCacheReload = SystemHPMGrp53[1].split()[-1]
        RemoteCacheReload = SystemHPMGrp53[2].split()[-1]
        DistantCacheReload = SystemHPMGrp53[0].split()[-1]
        
        FinalString = str(FinalString) + '\"cpucachereload\":{\"local\":' + LocalCacheReload + ',\"remote\":' + RemoteCacheReload + ',\"distant\":' + DistantCacheReload + '},'
        
    # Gathering data from OS command
    SystemHPMMpStat = subprocess.Popen("mpstat -d 1 1 | grep ALL", shell=True, stdout=subprocess.PIPE).stdout
    SystemHPMMpStat = SystemHPMMpStat.read().decode().split() 
    
    S0rd = str(float(SystemHPMMpStat[8]) / 100)
    S1rd = str(float(SystemHPMMpStat[9]) / 100)
    S2rd = str(float(SystemHPMMpStat[10]) / 100)
    S3rd = str(float(SystemHPMMpStat[11]) / 100)
    S4rd = str(float(SystemHPMMpStat[12]) / 100)
    S5rd = str(float(SystemHPMMpStat[13]) / 100)
    # Following value placement depends of CPU mode
    if "Dedicated" in LPARCPUMode:
        S3hrd = str(float(SystemHPMMpStat[14]) / 100)
        S4hrd = str(float(SystemHPMMpStat[15]) / 100)
        S5hrd = str(float(SystemHPMMpStat[16]) / 100)
    else:
        S3hrd = str(float(SystemHPMMpStat[16]) / 100)
        S4hrd = str(float(SystemHPMMpStat[17]) / 100)
        S5hrd = str(float(SystemHPMMpStat[18]) / 100)

    FinalString = str(FinalString) + '\"cpuaffinity\":{\"S0rd\":' + S0rd + ',\"S1rd\":' + S1rd + ',\"S2rd\":' + S2rd + ',\"S3rd\":' + S3rd + ',\"S4rd\":' + S4rd + ',\"S5rd\":' + S5rd + ',\"S3hrd\":' + S3hrd + ',\"S4hrd\":' + S4hrd + ',\"S5hrd\":' + S5hrd + '}}'
      
    # Let's construct JSON output for SystemHPMStat (ELK 7.5.0)
    JSONToSendValues = (''
    '\"system\":{\"hpmstat\":' + FinalString + '}')
    
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.hpmstat", "system", "hpmstat", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    
    # print('\JSONToSend\n', JSONToSend, '\n')
    pass

def SystemHypervisor(ComparisonTimer):
    """ This function analyse LPAR activity with lparstat command and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """

    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    # Defining which values we want to take from output
    # If some fields are added or remove, all the code has to be reviewed as positions will change...
    PHYPInclude = "cede|confer|prod|read|enter|remove|bulk_remove|get_ppp|set_ppp|clear_ref|eoi|ipi|cppr|migrate_dma|send_logical_lan|add_logicl_lan_buf|xirr|PURR|others|page_init"
    
    # Gathering data from OS command
    SystemHypervisorCmd = "lparstat -H 1 1 | egrep -w \"" + PHYPInclude + "\""
    SystemHypervisor = subprocess.Popen(SystemHypervisorCmd, shell=True, stdout=subprocess.PIPE).stdout
    SystemHypervisor = SystemHypervisor.read().decode().split('\n')
    
    # Defining the Final String containing all JSON fieslds and values
    FinalStringConcat = ""
    
    # Looping on each line of the OS command output
    for lineID in range(len(SystemHypervisor)):
        # Discarding empty line
        if len(SystemHypervisor[lineID]) != 0:
            FinalString = ""
            # Splitting the current line in list
            SystemHypervisorSplitted = SystemHypervisor[lineID].split()
            
            # Filling vars with values
            SystemHypervisorName = SystemHypervisorSplitted[0]
            SystemHypervisorNbcall = str(SystemHypervisorSplitted[1])
            SystemHypervisorAVGCalltime = str(SystemHypervisorSplitted[4])
            SystemHypervisorMAXCalltime = str(SystemHypervisorSplitted[5])
            # Making some calculation for percentages
            SystemHypervisorLpartimePCT = str(round((float(SystemHypervisorSplitted[2]) / 100), 2))
            SystemHypervisorHypervisortimePCT = str(round((float(SystemHypervisorSplitted[3]) / 100), 2))
            
            # Generating JSON for the current line
            FinalString = '\"' + SystemHypervisorName + '\":{\"nbcall\":' + SystemHypervisorNbcall + ',\"lpartimepct\":' + SystemHypervisorLpartimePCT + ',\"phyptimepct\":' + SystemHypervisorHypervisortimePCT + ',\"avgcalltime\":' + SystemHypervisorAVGCalltime + ',\"maxcalltime\":' + SystemHypervisorMAXCalltime + '}'

            # Adding the JSON line to Final String
            FinalStringConcat = FinalStringConcat + ',' +  FinalString
    
    # Removeing the first caracter of FinalStringConcat which is a ","
    FinalStringConcat = FinalStringConcat[1:]
    
    # Let's construct JSON output for SystemHypervisor (ELK 7.5.0)
    JSONToSendValues = (''
    '\"system\":{\"hypervisor\":{' + FinalStringConcat + '}}')
    
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.hypervisor", "system", "hypervisor", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    # print('\JSONToSend\n', JSONToSend, '\n')
    pass

def SystemProcess(ComparisonTimer):
    """ This function analyse processes CPU and RAM activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    
    # Setting vars for threads follow up
    global SystemProcessThread
    SystemProcessThread = threading.currentThread()

    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Checking if a limit is set for Processes analysis
    if TopProcesses != 0:
        # Get Processs CPU usage for a limited number of processes
        # The maximum number of processes in defined in TopProcesses var
        SystemProcessCmd = "ps -ef -o pid,ppid,pgid,command,status,vsz,rssize,pmem,uname,time,pcpu,start,args | sed '1 d' | sort -rk 11 | head -" + str(TopProcesses)
        SystemProcess = subprocess.Popen(SystemProcessCmd, shell=True, stdout=subprocess.PIPE).stdout
    else:
        # Get CPU usage values from ps command for all processes -- current version
        SystemProcess = subprocess.Popen("ps -ef -o pid,ppid,pgid,command,status,vsz,rssize,pmem,uname,time,pcpu,start,args | sed '1 d'", shell=True, stdout=subprocess.PIPE).stdout

    # Split result into list
    SystemProcess = SystemProcess.read().decode().split('\n')

    for CPUProcessLine in SystemProcess:
        # Removing empty lines
        if(len(CPUProcessLine) != 0):
            CPUProcessLine = CPUProcessLine.split()
            ProcessPid = CPUProcessLine[0]
            ProcessPpid = CPUProcessLine[1]
            ProcessPgid = CPUProcessLine[2]
            ProcessName = CPUProcessLine[3]
            ProcessState = CPUProcessLine[4]

            # Handling defunct/exiting/idle process cases
            ExcludedProcesses = ['<defunct>', '<exiting>', '<idle>']
            if any(ExcludedProcess in ProcessName for ExcludedProcess in ExcludedProcesses):
                # If it is a defunct process, maybe we will makesomething with that...
                # ProcessMemorySize = 0
                # ProcessMemoryRssBytes = 0
                # ProcessMemoryRssPCT = 0
                # ProcessUsername = 0
                # ProcessCpuTotalValue = 0
                # ProcessCpuTotalPCTNorm = 0
                # ProcessCpuTotalPCT = 0
                # ProcessFDPath = 0
                # ProcessFdOpen = 0
                # ProcessCpuStartTime = 0
                # ProcessCmdline = 0
                # ProcessMemoryShare = 0
                # ProcessFdOpenlimitSoft = 0
                # ProcessFdOpenlimitHard = 0
                # ProcessCwd = 0
                # ProcessExecutable = 0
                # FinalCmdString = str(0)
                # ProcessPpid = CPUProcessLine = 0
                # ProcessPgid = CPUProcessLine = 0
                pass

            else:
                # For other processes
                ProcessMemorySize = CPUProcessLine[5]
                # Converting KB in B
                ProcessMemorySize = int(ProcessMemorySize) * 1000
                ProcessMemoryRssBytes = CPUProcessLine[6]
                # Converting KB in B
                ProcessMemoryRssBytes = int(ProcessMemoryRssBytes) * 1000
                ProcessMemoryRssPCT = CPUProcessLine[7]
                # Formating pct to ELK format
                ProcessMemoryRssPCT = float(ProcessMemoryRssPCT) / 100
                ProcessUsername = CPUProcessLine[8]
                ProcessCpuTotalValue = CPUProcessLine[9]
                ProcessCpuTotalPCTNorm = CPUProcessLine[10]

                # Converting CPU total value HH:MM:SS in seconds
                # Detecting if value contains a number of days as a prefix
                if len(ProcessCpuTotalValue.split('-')) == 2:
                    # If yes, making a custom formating and converting values
                    ProcessCpuDays = ProcessCpuTotalValue.split('-')[0]
                    ProcessCpuDaysInSec = (int(ProcessCpuDays) * 24) * 3600
                    ProcessCpuDateTime = ProcessCpuTotalValue.split('-')[1]
                    ProcessCpuDateTime = ProcessCpuDateTime.split(':')
                    ProcessCpuTotalValue = ProcessCpuDaysInSec + (int(ProcessCpuDateTime[0]) * 3600) + (int(ProcessCpuDateTime[1]) * 60) + int(ProcessCpuDateTime[2])
                else:
                    ProcessCpuTotalValueSplit = ProcessCpuTotalValue.split(':')
                    ProcessCpuTotalValue = (int(ProcessCpuTotalValueSplit[0]) * 3600) + (int(ProcessCpuTotalValueSplit[1]) * 60) + int(ProcessCpuTotalValueSplit[2])

                # Calculating values for CPUTotal metrics
                if ProcessCpuTotalPCTNorm != "0,0":
                    # Changing . in , for calculation and converting to ELK PCT format
                    ProcessCpuTotalPCTNorm = float(ProcessCpuTotalPCTNorm.replace(',', '.')) / 100
                    ProcessCpuTotalPCT = ProcessCpuTotalPCTNorm * int(NumProc)
                else:
                    ProcessCpuTotalPCTNorm = 0
                    ProcessCpuTotalPCT = 0

                # Detecting and gathering file opened metric with try/catch
                try:
                    ProcessFDPath = '/proc/' + ProcessPid + '/fd'
                    if os.path.exists(ProcessFDPath):
                        path, dirs, files = next(os.walk(ProcessFDPath))
                        ProcessFdOpen = len(files) + len(dirs)
                    else:
                        ProcessFdOpen=0
                except:
                    ProcessFdOpen=0

                # Calculating ProcessCpuStartTime depending on its format
                ProcessCpuStartTime = CPUProcessLine[11]
                ProcessCmdline = ''
                if ':' in ProcessCpuStartTime:
                    # Formating output to ELK timestamp
                    ProcessCmdDate = datetime.datetime.now().strftime("%Y-%m-%dT")
                    ProcessCpuStartTime = str(ProcessCmdDate) + ProcessCpuStartTime

                    # Filling the CmdLine metric with the rest of the columns, starting at 12
                    for i in range(12, len(CPUProcessLine)):
                        # Removing invalid caracters from JSON message
                        ProcessCmdline = ProcessCmdline + " " + re.sub('[\\\[\]\(\)\{\}"\b\t\n\a\r]', ' ', str(CPUProcessLine[i]))
                else:
                    month = ProcessCpuStartTime
                    day = CPUProcessLine[12]
                    year = str(datetime.datetime.now().strftime("%Y"))

                    # Making switch case for formating month
                    if "Jan" in month:
                        mon = '01'
                    elif "Feb" in month:
                        mon = '02'
                    elif "Mar" in month:
                        mon = '03'
                    elif "Apr" in month:
                        mon = '04'
                    elif "May" in month:
                        mon = '05'
                    elif "Jun" in month:
                        mon = '06'
                    elif "Jul" in month:
                        mon = '07'
                    elif "Aug" in month:
                        mon = '08'
                    elif "Sep" in month:
                        mon = '09'
                    elif "Oct" in month:
                        mon = '10'
                    elif "Nov" in month:
                        mon = '11'
                    elif "Dec" in month:
                        mon = '12'

                    # Formating output to ELK timestamp
                    ProcessCpuStartTime = year + '-' + mon + '-' + day + 'T00:00:00.000'

                    # Filling the CmdLine metric with the rest of the columns, starting at 13
                    for i in range(13, len(CPUProcessLine)):
                        # Removing invalid caracters from JSON message
                        ProcessCmdline = ProcessCmdline + " " + re.sub('[\\\[\]\(\)\{\}"\b\t\n\a\r]', ' ', str(CPUProcessLine[i]))

                # COST -- Too much CPU consumer.... Need IPCS or svmon information grouping functions...
                ProcessMemoryShare=0

                # COST -- The following is very costly, need to know if really necessary
                # We can change and force the limit to 0 anyway, saving CPU
                # ProcessFdOpenlimitSoft=0
                # ProcessFdOpenlimitHard=0

                # Get soft ulimit values from OS command
                ProcessFdOpenlimitSoftCmd = "su " + ProcessUsername + " -c ulimit -Sa | egrep -w 'nofiles|open files' | awk '{print $NF}'\n"
                ProcessFdOpenlimitSoft = subprocess.Popen(ProcessFdOpenlimitSoftCmd, shell=True, stdout=subprocess.PIPE).stdout
                ProcessFdOpenlimitSoft = ProcessFdOpenlimitSoft.read().decode().split('\n')
                ProcessFdOpenlimitSoft = ProcessFdOpenlimitSoft[0]
                
                # Setting limit to zero if unlimited
                if (ProcessFdOpenlimitSoft == 'unlimited') or (ProcessFdOpenlimitSoft == '-1'):
                    # We set limit to 0 as unlimited
                    ProcessFdOpenlimitSoft = 0

                # Get hard ulimit values from OS command
                ProcessFdOpenlimitHardCmd = "su " + ProcessUsername + " -c ulimit -Ha  | egrep -w 'nofiles|open files' | awk '{print $NF}'\n"
                ProcessFdOpenlimitHard = subprocess.Popen(ProcessFdOpenlimitHardCmd, shell=True, stdout=subprocess.PIPE).stdout
                ProcessFdOpenlimitHard = ProcessFdOpenlimitHard.read().decode().split('\n')
                ProcessFdOpenlimitHard = ProcessFdOpenlimitHard[0]
                # Checking if hard limits are set
                if ProcessFdOpenlimitHard == "":
                    ProcessFdOpenlimitHard = ProcessFdOpenlimitSoft
                else:
                    # Setting limit to zero if unlimited
                    if ProcessFdOpenlimitHard == 'unlimited':
                        # We set limit to 0 as unlimited
                        ProcessFdOpenlimitHard = 0

                # Get CWD value from OS command
                ProcessCwdCmd = "lsof -p " + ProcessPid + " | grep cwd | awk '{print $9}'"
                ProcessCwd = subprocess.Popen(ProcessCwdCmd, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
                # , stdout = subprocess.PIPE, stderr = subprocess.PIPE
                ProcessCwd = ProcessCwd.read().decode().split('\n')
                ProcessCwd = ProcessCwd[0]

                # Generate args value into a JSON tab format
                FinalCmdString = '[\"' + ProcessCmdline.replace(' ','\",\"') + '\"]'
                # Then removing first empty entrie
                FinalCmdString = FinalCmdString.replace('"",','')

                # Gathering process executable name
                ProcessExecutableSplited = ProcessCmdline.split('/')
                ProcessExecutableSplitedLen = len(ProcessExecutableSplited) - 1
                ProcessExecutable = ProcessExecutableSplited[ProcessExecutableSplitedLen]

                # Convert vars into strings
                CPUProcessLine = str(CPUProcessLine)
                ProcessPid = str(ProcessPid)
                ProcessPpid = str(ProcessPpid)
                ProcessPgid = str(ProcessPgid)
                ProcessName = str(ProcessName)
                ProcessState = str(ProcessState)
                ProcessMemorySize = str(ProcessMemorySize)
                ProcessMemoryRssBytes = str(ProcessMemoryRssBytes)
                ProcessMemoryRssPCT = str(ProcessMemoryRssPCT)
                ProcessUsername = str(ProcessUsername)
                ProcessCpuTotalValue = str(ProcessCpuTotalValue)
                ProcessCpuTotalPCTNorm = str(ProcessCpuTotalPCTNorm)
                ProcessCpuTotalPCT = str(ProcessCpuTotalPCT)
                ProcessFDPath = str(ProcessFDPath)
                ProcessFdOpen = str(ProcessFdOpen)
                ProcessCpuStartTime = str(ProcessCpuStartTime)
                ProcessCmdline = str(ProcessCmdline)
                ProcessMemoryShare = str(ProcessMemoryShare)
                ProcessFdOpenlimitSoft = str(ProcessFdOpenlimitSoft)
                ProcessFdOpenlimitHard = str(ProcessFdOpenlimitHard)
                ProcessCwd = str(ProcessCwd)
                ProcessExecutable = str(ProcessExecutable).replace('"', '\"')
                
                # Let's construct JSON output for SystemProcess (ELK 7.5.0)
                JSONToSendValues = (''
                '\"system\": {'
                '\"process\": {'
                '\"memory\": {'
                '\"rss\": {'
                '\"pct\": ' + ProcessMemoryRssPCT + ','
                '\"bytes\": ' + ProcessMemoryRssBytes + '},'
                '\"share\": ' + ProcessMemoryShare + ','
                '\"size\": ' + ProcessMemorySize + '},'
                '\"cmdline\": \"' + ProcessCmdline + '\",'
                '\"cpu\": {'
                '\"total\": {'
                '\"value\": ' + ProcessCpuTotalValue + ','
                '\"pct\": ' + ProcessCpuTotalPCT + ','
                '\"norm\": {'
                '\"pct\": ' + ProcessCpuTotalPCTNorm + '}},'
                '\"start_time\": \"' + ProcessCpuStartTime + '\"},'
                '\"fd\": {'
                '\"open\": ' + ProcessFdOpen + ','
                '\"limit\": {'
                '\"soft\": ' + ProcessFdOpenlimitSoft + ','
                '\"hard\": ' + ProcessFdOpenlimitHard + '}},'
                '\"state\": \"' + ProcessState + '\"}},'
                '\"process\": {'
                '\"args\": ' + FinalCmdString + ','
                '\"name\": \"' + ProcessExecutable + '\",'
                '\"pid\": ' + ProcessPid + ','
                '\"ppid\": ' + ProcessPpid + ','
                '\"pgid\": ' + ProcessPgid + ','
                '\"working_directory\": \"' + ProcessCwd + '\",'
                '\"executable\": \"' + ProcessName + '\"},'
                '\"user\": {'
                '\"name\": \"' + ProcessUsername + '\"}')
               
               
                # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
                JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
                
                # Adding JSON metrics values gathered from OS command
                JSONToSend = JSONToSend + ',' + JSONToSendValues
                
                # Gathering "ELK formatted" dynamic JSON values
                RetDynamicJSON = GenerateDynamicJson("system.process", "system", "process", ComparisonTimer)
                
                # Adding dynamic "ELK Formating" JSON values into final JSON message
                JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
                
                # Let's send JSON message to ELK servers
                SendJSON(JSONToSend)
                # print('\JSONToSend\n', JSONToSend, '\n')
                pass

def SystemSocketSummary(ComparisonTimer):
    """ This function analyse processes network connections activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
            
    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Gathering data from OS command for SystemSocketSummarySummary
    SystemSocketSummary = subprocess.Popen("netstat -an -f inet | tail -n +3", shell=True, stdout=subprocess.PIPE).stdout
    SystemSocketSummary = SystemSocketSummary.read().decode().split('\n')
    
    # Initializing counters
    TotalConnections = 0
    CountTCP = 0
    CountUDP = 0
    CountSYNRECEIVED = 0
    CountSYNSEND = 0
    CountESTABLISHED = 0
    CountLISTEN = 0
    CountFIN_WAIT_1 = 0
    CountTIMED_WAIT = 0
    CountCLOSE_WAIT = 0
    CountFIN_WAIT_2 = 0
    CountLAST_ACK = 0
    CountCLOSED = 0
    
    for ConnectId in range(len(SystemSocketSummary)):
        # Removing last empty line
        if SystemSocketSummary[ConnectId] != "":
            # Incrementing total counter
            TotalConnections = TotalConnections + 1
            
            # Splitting connection line
            SplitedConnection = SystemSocketSummary[ConnectId].split()

            # Checking connection protocol
            if ('tcp' or 'tcp4' or 'tcp6') in SplitedConnection[0]:
                # Incrementing TCP connection counter
                CountTCP = CountTCP + 1
                # Checking connection state for TCP
                if 'SYN_RECEIVED' in SplitedConnection[5]:
                    # Incrementing SYN_RECEIVED counter
                    # Server just received SYN from the client
                    CountSYNRECEIVED = CountSYNRECEIVED + 1
                elif 'ESTABLISHED' in SplitedConnection[5]:
                    # Incrementing ESTABLISHED counter
                    # Client received server's SYN and session is established
                    CountESTABLISHED = CountESTABLISHED + 1
                elif 'SYN_SEND' in SplitedConnection[5]:
                    # Incrementing SYN_SEND counter
                    # Indicates active open
                    CountSYNSEND = CountSYNSEND + 1
                elif 'LISTEN' in SplitedConnection[5]:
                    # Incrementing LISTEN counter
                    # Server is ready to accept connection
                    CountLISTEN = CountLISTEN + 1
                elif 'FIN_WAIT_1' in SplitedConnection[5]:
                    # Incrementing FIN_WAIT_1 counter
                    # Indicates active close
                    CountFIN_WAIT_1 = CountFIN_WAIT_1 + 1
                elif 'TIMED_WAIT' in SplitedConnection[5]:
                    # Incrementing TIMED_WAIT counter
                    # Client enters this state after active close
                    CountTIMED_WAIT = CountTIMED_WAIT + 1
                elif 'CLOSE_WAIT' in SplitedConnection[5]:
                    # Incrementing CLOSE_WAIT counter
                    # Indicates passive close. Server just received first FIN from a client
                    CountCLOSE_WAIT = CountCLOSE_WAIT + 1
                elif 'FIN_WAIT_2' in SplitedConnection[5]:
                    # Incrementing FIN_WAIT_2 counter
                    # Client just received acknowledgment of its first FIN from the server
                    CountFIN_WAIT_2 = CountFIN_WAIT_2 + 1
                elif 'LAST_ACK' in SplitedConnection[5]:
                    # Incrementing LAST_ACK counter
                    # Server is in this state when it sends its own FIN
                    CountLAST_ACK = CountLAST_ACK + 1
                elif 'CLOSED' in SplitedConnection[5]:
                    # Incrementing CLOSED counter
                    # Server received ACK from client and connection is closed
                    CountCLOSED = CountCLOSED + 1
       
            elif ('udp' or 'udp4' or 'udp6') in SplitedConnection[0]:
                # Incrementing UDP connection counter
                CountUDP = CountUDP + 1

    # Converting to string
    TotalConnections = str(TotalConnections)
    CountTCP = str(CountTCP)
    CountUDP = str(CountUDP)
    CountSYNRECEIVED = str(CountSYNRECEIVED)
    CountSYNSEND = str(CountSYNSEND)
    CountESTABLISHED = str(CountESTABLISHED)
    CountLISTEN = str(CountLISTEN)
    CountFIN_WAIT_1 = str(CountFIN_WAIT_1)
    CountTIMED_WAIT = str(CountTIMED_WAIT)
    CountCLOSE_WAIT = str(CountCLOSE_WAIT)
    CountFIN_WAIT_2 = str(CountFIN_WAIT_2)
    CountLAST_ACK = str(CountLAST_ACK)
    CountCLOSED = str(CountCLOSED)
    
    # Let's construct JSON output for SystemSocketSummary (ELK 7.5.0)
    JSONToSendValues = (''
    '\"system\":{'
    '\"socket\":{'
    '\"summary\":{'
    '\"all\":{'
    '\"count\":' + TotalConnections + ','
    '\"listening\":' + CountLISTEN + '},'
    '\"tcp\":{'
    '\"memory\":0,'
    '\"all\":{'
    '\"listening\":' + CountLISTEN + ','
    '\"established\":' + CountESTABLISHED + ','
    '\"close_wait\":' + CountCLOSE_WAIT + ','
    '\"time_wait\":' + CountTIMED_WAIT + ','
    '\"fin_wait1\":' + CountFIN_WAIT_1 + ','
    '\"fin_wait2\":' + CountFIN_WAIT_2 + ','
    '\"closed\":' + CountCLOSED + ','
    '\"syn_send\":' + CountSYNSEND + ','
    '\"last_ack\":' + CountLAST_ACK + ','
    '\"syn_received\":' + CountSYNRECEIVED + ','
    '\"orphan\":0,'
    '\"count\":' + CountTCP + '}},'
    '\"udp\":{'
    '\"all\":{'
    '\"count\":' + CountUDP + '},'
    '\"memory\":0}}'
    '}}')
    
    # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
    JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
    
    # Adding JSON metrics values gathered from OS command
    JSONToSend = JSONToSend + ',' + JSONToSendValues
    
    # Gathering "ELK formatted" dynamic JSON values
    RetDynamicJSON = GenerateDynamicJson("system.socket.summary", "system", "socket_summary", ComparisonTimer)
    
    # Adding dynamic "ELK Formating" JSON values into final JSON message
    JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
    
    # Let's send JSON message to ELK servers
    SendJSON(JSONToSend)
    # print('\JSONToSend\n', JSONToSend, '\n')
    pass

def SystemSocket(ComparisonTimer):
    """ This function analyse  network connections activity and send metrics to ElasticSearch server
            
        WARNING: For now, this is not enabled (very big timer). It is working but requires too much CPU. To improve !!!
        
        TODO: Describe the function, all vars and its content
    """
    # Setting vars for threads follow up
    global SystemSocketThread
    SystemSocketThread = threading.currentThread()
            
    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Gathering data from OS command for SystemSocketSummarySummary
    SystemSocketSummary = subprocess.Popen("netstat -an -f inet | tail -n +3", shell=True, stdout=subprocess.PIPE).stdout
    SystemSocketSummary = SystemSocketSummary.read().decode().split('\n')
    
    # Lopping into all cmd Results
    for ConnectId in range(len(SystemSocketSummary)):
        # Removing last empty line
        if SystemSocketSummary[ConnectId] != "":
            # Splitting connection line
            SplitedConnection = SystemSocketSummary[ConnectId].split()

            # Checking connection protocol
            if ('tcp' or 'tcp4' or 'tcp6') in SplitedConnection[0]:
                    
                # Sending JSON message for current connection for ESTABLISHED or LISTEN connections only
                TargetStates = ['ESTABLISHED', 'LISTEN']
                if any(x in SplitedConnection[-1] for x in TargetStates):
                
                    # Detecting wich type of TCP connection it is IPV4 or IPV6
                    if ('tcp' or 'tcp4') in SplitedConnection[0]:
                        ConnectionIPVersion = "ipv4"
                        ConnectionIPVersionId = ConnectionIPVersion[-1]
                    else:
                        ConnectionIPVersion = "ipv6"
                        ConnectionIPVersionId = ConnectionIPVersion[-1]
                    
                    # Defining Local and Remote ports
                    LocalPort = SplitedConnection[3].split('.')[-1]
                    RemotePort = SplitedConnection[4].split('.')[-1]
                    
                    # Checking if local tcp port is linked with an AIX service
                    LocalPortTranslate = ""
                    try:
                        PortTranslateCmd = 'cat /etc/services | grep -w ' + LocalPort + '/tcp'
                        LocalPortTranslate = subprocess.Popen(PortTranslateCmd, shell=True, stdout=subprocess.PIPE).stdout
                        LocalPortTranslate = LocalPortTranslate.read().decode().split()[0]
                    except:
                        # Nothing to do
                        pass
 
                    # Checking if remote tcp port is linked with an AIX service
                    RemotePortTranslate = ""
                    try:
                        PortTranslateCmd = 'cat /etc/services | grep -w ' + RemotePort + '/tcp'
                        RemotePortTranslate = subprocess.Popen(PortTranslateCmd, shell=True, stdout=subprocess.PIPE).stdout
                        RemotePortTranslate = RemotePortTranslate.read().decode().split()[0]
                    except:
                        # Nothing to do
                        pass
                    
                    # Gathering local address and split it. Then, we force definition if port is listening
                    LocalAddrSplit = SplitedConnection[3].split('.')
                    if len(LocalAddrSplit) != 2:
                        LocalAddr = LocalAddrSplit[0] + '.' + LocalAddrSplit[1] + '.' + LocalAddrSplit[2] + '.' + LocalAddrSplit[3]
                    else:
                        LocalAddr = "0.0.0.0"
                    
                    # Gathering remote address and split it. Then, we force definition if port is listening
                    RemoteAddrSplit = SplitedConnection[4].split('.')
                    if len(RemoteAddrSplit) != 2:
                        RemoteAddr = RemoteAddrSplit[0] + '.' + RemoteAddrSplit[1] + '.' + RemoteAddrSplit[2] + '.' + RemoteAddrSplit[3]
                    else:
                        RemoteAddr = "0.0.0.0"
                        RemotePortTranslate = "LISTEN"
                    
                    # Checking if there is some match between AIX service ports and current TCP port
                    if RemotePortTranslate and (isinstance(RemotePortTranslate, str)):
                        if LocalPortTranslate and (isinstance(LocalPortTranslate, str)):
                            # local and remote TCP ports are matching an AIX service. Taking that name for LSOF command
                            LsofCmd = 'lsof -i :' + LocalPortTranslate + ' | grep ' + RemotePortTranslate + '| tail -1'
                        else:
                            # Remote TCP ports is matching an AIX service. Taking that name for LSOF command
                            LsofCmd = 'lsof -i :' + LocalPort + ' | grep ' + RemotePortTranslate + '| tail -1'
                    else:
                        if LocalPortTranslate and (isinstance(LocalPortTranslate, str)):
                            # Local TCP ports is matching an AIX service. Taking that name for LSOF command
                            LsofCmd = 'lsof -i :' + LocalPortTranslate + ' | grep ' + RemotePort + '| tail -1'
                        else:
                            # local and remote TCP ports are not matching an AIX service. 
                            LsofCmd = 'lsof -i :' + LocalPort + ' | grep ' + RemotePort + '| tail -1'
                    
                    # Getting process information linked to the current connection
                    LSOFResult = subprocess.Popen(LsofCmd, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
                    LSOFResult = LSOFResult.read().decode().split()
                    
                    # Filling vars with LSOF results
                    if LSOFResult:
                        ConnectionProcess = LSOFResult[0]
                        ConnectionProcessPID = LSOFResult[1]
                        ConnectionProcessuser = LSOFResult[2]
                    else:
                        # Defaulting values with "none" string
                        ConnectionProcess = "none"
                        ConnectionProcessPID = "0"
                        ConnectionProcessuser = "none"
                        ConnectionProcessArgsJoined = ""
                        
                    # Get CPU args value from ps command for current process if PID defined
                    if ConnectionProcessPID != "none":
                        CheckPSCommandCmd = "ps -ef -o pid,args | grep -w " + ConnectionProcessPID + " | grep -v grep"
                        CheckPSCommand = subprocess.Popen(CheckPSCommandCmd, shell=True, stdout=subprocess.PIPE).stdout
                        
                        # Split result into list
                        ConnectionProcessArgs = CheckPSCommand.read().decode().split()
                        
                        # Removing first line because it is the pid
                        del ConnectionProcessArgs[0]
                        
                        # Removing invalid ELK JSON caracters
                        for i in range(0, len(ConnectionProcessArgs)):
                            ConnectionProcessArgs[i] = re.sub('[\\\[\]\(\)\{\}"\b\t\n\a\r]', ' ', str(ConnectionProcessArgs[i]))
                        
                        # Joining list to make the final arg string
                        StrSeparator = " "
                        ConnectionProcessArgsJoined = StrSeparator.join(ConnectionProcessArgs)
                        
                        # Then, transforming this string to JSON tab format
                        FinalCmdString = '[\"' + ConnectionProcessArgsJoined.replace(' ','\",\"') + '\"]'
                        # Then removing first empty entrie
                        FinalCmdString = FinalCmdString.replace('"",','')
                        
                    # Defining username id if not "none"
                    # Tryin that into try/catch if grep is not giving any results
                    try:
                        if ConnectionProcessuser != "none":
                            # Executing OS command
                            CheckUserIdCmd = 'lsuser -a id ' + ConnectionProcessuser
                            CheckPSUserId = subprocess.Popen(CheckUserIdCmd, shell=True, stdout=subprocess.PIPE).stdout
                            CheckPSUserId = CheckPSUserId.read().decode().split('=')
                            
                            # Split result into list and defining user ID                        
                            ConnectionProcessuserId = CheckPSUserId[1].replace('\n', '')
                        else:
                            # Defaulting user id to "none"
                            ConnectionProcessuserId = "none"
                    except:
                        # Defaulting user id to "none"
                        ConnectionProcessuserId = "none"
                        
                    # Checking if remote or local port is egal to "*". If yes, forcing it to 0
                    if RemotePort == "*":
                        RemotePort = "0"
                    if LocalPort == "*":
                        LocalPort = "0"
                    
                    # Triggering JSON sending
                    JSONTriggered = "yes"
                else:
                    # Avoid sending JSON for this connection
                    JSONTriggered = "no"
                    
            # Connection is UDP type
            elif ('udp' or 'udp4' or 'udp6') in SplitedConnection[0]:

                # Checcking IP version
                if ('udp' or 'udp4') in SplitedConnection[0]:
                    ConnectionIPVersion = "ipv4"
                    ConnectionIPVersionId = ConnectionIPVersion[-1]
                else:
                    ConnectionIPVersion = "ipv6"
                    ConnectionIPVersionId = ConnectionIPVersion[-1]
                
                # Defining Local and Remote ports
                LocalPort = SplitedConnection[3].split('.')[-1]
                RemotePort = SplitedConnection[4].split('.')[-1]
                
                # Checking if local UDP port is linked with an AIX service
                LocalPortTranslate = ""
                try:
                    PortTranslateCmd = 'cat /etc/services | grep -w ' + LocalPort + '/udp'
                    LocalPortTranslate = subprocess.Popen(PortTranslateCmd, shell=True, stdout=subprocess.PIPE).stdout
                    LocalPortTranslate = LocalPortTranslate.read().decode().split()[0]
                except:
                    pass

                # Checking if remote UDP port is linked with an AIX service
                RemotePortTranslate = ""
                try:
                    PortTranslateCmd = 'cat /etc/services | grep -w ' + RemotePort + '/udp'
                    RemotePortTranslate = subprocess.Popen(PortTranslateCmd, shell=True, stdout=subprocess.PIPE).stdout
                    RemotePortTranslate = RemotePortTranslate.read().decode().split()[0]
                except:
                    # Nothing to do
                    pass
                
                # Gathering local address and split it. Then, we force definition if port is listening
                LocalAddrSplit = SplitedConnection[3].split('.')
                if len(LocalAddrSplit) != 2:
                    LocalAddr = LocalAddrSplit[0] + '.' + LocalAddrSplit[1] + '.' + LocalAddrSplit[2] + '.' + LocalAddrSplit[3]
                else:
                    LocalAddr = "0.0.0.0"
                
                # Gathering remote address and split it. Then, we force definition if port is listening
                RemoteAddrSplit = SplitedConnection[4].split('.')
                if len(RemoteAddrSplit) != 2:
                    RemoteAddr = RemoteAddrSplit[0] + '.' + RemoteAddrSplit[1] + '.' + RemoteAddrSplit[2] + '.' + RemoteAddrSplit[3]
                else:
                    RemoteAddr = "0.0.0.0"
                    RemotePortTranslate = "LISTEN"
                
                # Checking if there is some match between AIX service ports and current UDP port
                if RemotePortTranslate and (isinstance(RemotePortTranslate, str)):
                    if LocalPortTranslate and (isinstance(LocalPortTranslate, str)):
                        # local and remote UDP ports are matching an AIX service. Taking that name for LSOF command
                        LsofCmd = 'lsof -i :' + LocalPortTranslate + '| tail -1'
                    else:
                        # Remote UDP ports is matching an AIX service. Taking that name for LSOF command
                        LsofCmd = 'lsof -i :' + LocalPort + ' | tail -1'
                else:
                    if LocalPortTranslate and (isinstance(LocalPortTranslate, str)):
                        # Local UDP ports is matching an AIX service. Taking that name for LSOF command
                        LsofCmd = 'lsof -i :' + LocalPortTranslate + ' | tail -1'
                    else:
                        # local and remote UDP ports are not matching an AIX service. 
                        LsofCmd = 'lsof -i :' + LocalPort + ' | tail -1'
                
                # Getting process information linked to the current connection
                # Gathering data from OS command for SystemSocketSummarySummary
                LSOFResult = subprocess.Popen(LsofCmd, shell=True, stdout=subprocess.PIPE, stderr = devnull).stdout
                LSOFResult = LSOFResult.read().decode().split()
                
                # Filling vars with LSOF results
                if LSOFResult:
                    ConnectionProcess = LSOFResult[0]
                    ConnectionProcessPID = LSOFResult[1]
                    ConnectionProcessuser = LSOFResult[2]
                else:
                    # Defaulting values with "none" string
                    ConnectionProcess = "none"
                    ConnectionProcessPID = "0"
                    ConnectionProcessuser = "none"
                    ConnectionProcessArgsJoined = ""
                
                # Get CPU args value from ps command for current process if PID defined
                if ConnectionProcessPID != "none":
                    CheckPSCommandCmd = "ps -ef -o pid,args | grep -w " + ConnectionProcessPID + " | grep -v grep"
                    CheckPSCommand = subprocess.Popen(CheckPSCommandCmd, shell=True, stdout=subprocess.PIPE).stdout
                    
                    # Split result into list
                    ConnectionProcessArgs = CheckPSCommand.read().decode().split()
                    
                    # Removing first line because it is the pid
                    del ConnectionProcessArgs[0]
                    
                    # Removing invalid ELK JSON caracters
                    for i in range(0, len(ConnectionProcessArgs)):
                        ConnectionProcessArgs[i] = re.sub('[\\\[\]\(\)\{\}"\b\t\n\a\r]', ' ', str(ConnectionProcessArgs[i]))
                    
                    # Joining list to make the final arg string
                    StrSeparator = " "
                    ConnectionProcessArgsJoined = StrSeparator.join(ConnectionProcessArgs)
                    
                    # Then, transforming this string to JSON tab format
                    FinalCmdString = '[\"' + ConnectionProcessArgsJoined.replace(' ','\",\"') + '\"]'
                    # Then removing first empty entrie
                    FinalCmdString = FinalCmdString.replace('"",','')
                    
                # Defining username id if not "none"
                # Tryin that into try/catch if grep is not giving any results
                try:
                    if ConnectionProcessuser != "none":
                        # Executing OS command
                        CheckUserIdCmd = 'lsuser -a id ' + ConnectionProcessuser
                        CheckPSUserId = subprocess.Popen(CheckUserIdCmd, shell=True, stdout=subprocess.PIPE).stdout
                        CheckPSUserId = CheckPSUserId.read().decode().split('=')
                        
                        # Split result into list and defining user ID                        
                        ConnectionProcessuserId = CheckPSUserId[1].replace('\n', '')
                    else:
                        # Defaulting user id to "none"
                        ConnectionProcessuserId = "none"
                except:
                    # Defaulting user id to "none"
                    ConnectionProcessuserId = "none"
                
                # Checking if remote or local port is egal to "*". If yes, forcing it to 0
                if RemotePort == "*":
                    RemotePort = "0"
                if LocalPort == "*":
                    LocalPort = "0"

                # Triggering JSON sending
                JSONTriggered = "yes"
            
            else:        
                # Avoid sending JSON for this connection
                JSONTriggered = "no"
                
            # IMPROVEMENT - How to know it the connection is inbound or outbound other than ephemeral port analysis and comparison ? For now, it is set to "unknown"

            # Sending JSON message only for TCP ESTABLISED/LISTEN and UDP connections
            if JSONTriggered == "yes":
                
                # Formatings vars to string
                ConnectionIPVersionId = str(ConnectionIPVersionId)
                ConnectionProcessuserId = str(ConnectionProcessuserId)
                LocalPort = str(LocalPort)
                RemotePort = str(RemotePort)
                
                # Let's construct JSON output for SystemSocket (ELK 7.5.0)
                JSONToSendValues=(''
                '\"network\":{'
                '\"type\":\"' + ConnectionIPVersion + '\",'
                '\"iana_number\":\"' + ConnectionIPVersionId + '\",'
                '\"direction\":\"unknown\"'
                '},'
                '\"user\":{'
                '\"id\":\"' + ConnectionProcessuserId + '\",'
                '\"name\":\"' + ConnectionProcessuser + '\",'
                '\"full_name\":\"' + ConnectionProcessuser + '\"'
                '},'
                '\"process\":{'
                '\"pid\":' + ConnectionProcessPID + ','
                '\"executable\":\"' + ConnectionProcess + '",'
                '\"name\":\"' + ConnectionProcess + '\",'
                '\"args\":' + FinalCmdString + ''
                '},'
                '\"system\":{'
                '\"socket\":{'
                '\"local\":{'
                '\"ip\":\"' + LocalAddr + '\",'
                '\"port\":' + LocalPort + ''
                '},'
                '\"process\":{'
                '\"cmdline\":\"' + ConnectionProcess + '\"'
                '},'
                '\"remote\":{'
                '\"ip\":\"' + RemoteAddr + '\",'
                '\"port\":' + RemotePort + ''
                '}'
                '}'
                '},'
                '\"destination\":{'
                '\"ip\":\"' + RemoteAddr + '\",'
                '\"port\":' + RemotePort + ''
                '},'
                '\"source\":{'
                '\"ip\":\"' + LocalAddr + '\",'
                '\"port\":' + LocalPort + ''
                '}')
                
                # Adding Timestamp and static "ELK Formating" JSON values into final JSON message
                JSONToSend = '{\"@timestamp\":\"' + SeqIdTimestamp + 'Z\",' + StaticJSON
                
                # Adding JSON metrics values gathered from OS command
                JSONToSend = JSONToSend + ',' + JSONToSendValues
                
                # Gathering "ELK formatted" dynamic JSON values
                RetDynamicJSON = GenerateDynamicJson("system.socket.summary", "system", "socket_summary", ComparisonTimer)
                
                # Adding dynamic "ELK Formating" JSON values into final JSON message
                JSONToSend = JSONToSend + ',' + RetDynamicJSON + '}'
                
                # Let's send JSON message to ELK servers
                SendJSON(JSONToSend)
                
                # print('\nJSONToSend\n', JSONToSend, '\n')
                pass

def StartLogging():
    """ This function handle logging different informations into file 

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    global LogFilePath
    global StartupLogFile
    global StartupLogFileLast
    global MainLogFile
    global MainLogFileLast
    global CrashDumpCheckLog
    global CrashDumpSendLog
    global CrashDumpDaemon
    
    # Adding trailing / if necessary to LogFilePath
    if not LogFilePath.endswith('/'):
        LogFilePath = LogFilePath + '/'
        
    # Checking if log folder exists
    if not os.path.exists(LogFilePath):
        print('Error: Log directory does not exists. Exiting')
        sys.exit(2)
    
    # Defining Startup logging informations
    StartupLogFile = LogFilePath + "Metraixbeat.Startup.log"
    StartupLogFileLast = LogFilePath + "Metraixbeat.Startup.log.last"
    
    # print('LogFilePath: ', LogFilePath)
    # print('StartupLogFile: ', StartupLogFile)
    
    # sys.exit(2)
    
    # Defining Monitoring logging informations
    MainLogFile = LogFilePath + "Metraixbeat.log"
    MainLogFileLast = LogFilePath + "Metraixbeat.log.last"
    
    # Defining Crash logging informations
    CrashDumpCheckLog = LogFilePath + "Metraixbeat.crash.HTTP-Check.log"
    CrashDumpCheckLogLast = LogFilePath + "Metraixbeat.crash.HTTP-Check.log.last"
    CrashDumpSendLog = LogFilePath + "Metraixbeat.crash.HTTP-Send.log"
    CrashDumpSendLogLast = LogFilePath + "Metraixbeat.crash.HTTP-Send.log.last"
    CrashDumpDaemon = LogFilePath + "Metraixbeat.crash.Daemon.log"
    CrashDumpDaemonLast = LogFilePath + "Metraixbeat.crash.Daemon.log.last"

    # Checking if old Startup log file exists
    if os.path.exists(StartupLogFile):
        # Rotating logs
        shutil.move(StartupLogFile, StartupLogFileLast)

    # Checking if old Monitoring log file exists
    if os.path.exists(MainLogFile):
        # Rotating logs
        logging.shutdown()
        shutil.move(MainLogFile, MainLogFileLast)
        
    # Checking if old crash log files exist
    if os.path.exists(CrashDumpCheckLog):
        # Rotating logs
        logging.shutdown()
        shutil.move(CrashDumpCheckLog, CrashDumpCheckLogLast)
    if os.path.exists(CrashDumpSendLog):
        # Rotating logs
        logging.shutdown()
        shutil.move(CrashDumpSendLog, CrashDumpSendLogLast)
    if os.path.exists(CrashDumpDaemon):
        # Rotating logs
        logging.shutdown()
        shutil.move(CrashDumpDaemon, CrashDumpDaemonLast)

    # Configuring Startup log file options

def main(argv):
    """ This is the main function
    
        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    
    # Define global variables
    global LogFilePath
    global ConfigFilePath
    global LogDir
    global ElasticServers
    global FilebeatServers
    global LogstashServers
    global ELKUsername
    global ELKPassword
    global ElasticPort
    global ELKWebProtocol
    global ElasticIndexName
    global FilebeatIndexName
    global ElasticServersAvailable
    global ElasticServersFailed
    global FilebeatServersAvailable
    global FilebeatServersFailed
    global LogstashServersAvailable
    global LogstashServersFailed
    global ElasticServerCnx
    global FilebeatServerCnx
    global LogstashServerCnx
    global devnull
    global LPARName
    global ExecutionTimers
    global TargetFileCurrentPosArray
    # global TargetFileMTimeCountArray
    global SendQueueArray
    global FilebeatSendQueueArray
    global LogstashSendQueueArray
    global FilebeatConfigsArray
    global CustomMetricsConfigsArray
    global TailStateArray
    global PingPlotterArray
    global SystemProcessThread
    global SystemSocketThread
    global SystemDiskIOThread
    global SystemMemoryThread
    global PingPlotterThread
    global SystemHPMStatThread
    global StartupLogFile
    global StartupLogFileLast
    global MainLogFile
    global MainLogFileLast
    global CrashDumpCheckLog
    global CrashDumpSendLog
    
    # Define null var
    devnull = subprocess.DEVNULL
    # Defining LPAR Name
    LPARName = socket.gethostname()
    # Define ExecutionTimers dictionary
    ExecutionTimers = {}
    # Defining arrays for ELK servers follow-up
    ElasticServers = []
    ElasticServersAvailable = []
    ElasticServersFailed = []
    FilebeatServers = []
    FilebeatServersAvailable = []
    FilebeatServersFailed = []
    LogstashServers = []
    LogstashServersAvailable = []
    LogstashServersFailed = []
    # Define TargetFileCurrentPosArray dictionary
    TargetFileCurrentPosArray = {}
    # Define TargetFileCTargetFileMTimeCountArray dictionary
    # TargetFileMTimeCountArray = {}
    # Define SendQueueArray list
    SendQueueArray = []
    # Define FilebeatSendQueueArray list
    FilebeatSendQueueArray = []
    # Define Logstash SendQueueArray list
    LogstashSendQueueArray = []
    # Define FilebeatConfigsArray for storing Filebeat config files content
    FilebeatConfigsArray = {}
    # Define FilebeatConfigsArray for storing Custom Metrics config files content
    CustomMetricsConfigsArray = {}
    # Define FilebeatConfigsArray for storing Tail process states
    TailStateArray = {}

    # Initializing background threads for long executions
    SystemProcessThread = threading.Thread(target=SystemProcess, args=())
    SystemDiskIOThread = threading.Thread(target=SystemDiskIO, args=())
    SystemSocketThread = threading.Thread(target=SystemSocket, args=())
    SystemMemoryThread = threading.Thread(target=SystemMemory, args=())
    PingPlotterThread = threading.Thread(target=PingPlotter, args=())
    SystemHPMStatThread = threading.Thread(target=SystemHPMStat, args=())
    
    # Initializing requests.sessions
    ElasticServerCnx = requests.session()
    FilebeatServerCnx = requests.session()
    LogstashServerCnx = requests.session()
    
    # Define Empty vars for daemon config file and PID file
    LogFilePath = ''
    ConfigFilePath = ''
    
    # Checking given arguments with try/catch
    try:
        # Testing args
        opts, args = getopt.getopt(argv,"hc:l:",["ConfigFilePath=","LogFilePath="])
    except getopt.GetoptError:
        # Required args not provided
        print('Usage:')
        print('metraixbeat -c <Parameters.conf file path> -l <Logs directory path>')
        sys.exit(2)
        
    # Looping on each args given
    for opt, arg in opts:
        # Case of help
        if opt == '-h':
            print('Usage:')
            print('metraixbeat -c <Parameters.conf file path> -l <Logs directory path>')
            sys.exit()
        elif opt in ("-c", "--ConfigFilePath"):
            ConfigFilePath = arg
        elif opt in ("-l", "--LogFilePath"):
            LogFilePath = arg
            
    # Checking given parameters
    if not ConfigFilePath or not LogFilePath:
        print('Usage:')
        print('metraixbeat -c <Parameters.conf file path> -l <Logs directory path>')
        sys.exit()

    # Start logging events
    StartLogging()
    
    # Log
    logging.info('==> Starting "Metraixbeat" daemon...\n')

    # Loading daemon's configuration
    LoadDaemonConfig()

    # Gather all LPAR informations
    GetLPARInformations()

    # Loading plugin's configurations
    LoadPluginConfig()

    # Log
    logging.info("==> Configuration loaded, switching to Realtime monitoring !\n")

    # Creating Startup log file from cuurent logging file
    logging.shutdown()
    shutil.move(MainLogFile, StartupLogFile)

    # Main loop / Infinite loop
    while True:
        # Checking if old Monitoring log file exists
        if os.path.exists(MainLogFile):
            # Rotating logs
            logging.shutdown()
            shutil.move(MainLogFile, MainLogFileLast)
            
        # Log
        logging.info("\n ---------------------------------------------SUMMARY------------------------------------------------------\n")
        
        # Check ELK server's availability
        CheckServers()

        # Compare timers and schedule work for each metricset
        WorkOnMetrics()

        # Analyse and schedule work for each Tail plugins if timer is reached
        ComparisonTimer = CompareTimer("TailPluginsRefresh", TailRefreshValue)
        if ComparisonTimer != devnull:
            for TailPlugin in FilebeatConfigsArray:
                # Launch analyse/work on current Tail plugin config
                FilebeatTail(TailPlugin)

        # Log threading summary
        logging.info('INFO     ==> Running threads: ' + str(threading.enumerate()))

        # Enable the following loop to print internal daemon vars for stability
        logging.info('INFO     ==> Internal vars count: ' + str(len(globals())))

        # Sleep for specified time
        time.sleep(CycleSleepTime)

# Script entry point
if __name__ == "__main__":

    # Setting PID file location
    PIDFile = "/var/run/metraixbeat.pid"
    
    # Checking if PID file already exists
    if os.path.exists(PIDFile):
        # If yes, checking if process is running or not
        OpenedPIDFile = open(PIDFile,"r")
        CurrentPID = OpenedPIDFile.read()
        
        # Checking if process is still running
        PSCommand = "ps -ef | grep " + CurrentPID + " | grep -v grep"
        GrepCurrentPID = subprocess.Popen(PSCommand, shell=True, stdout=subprocess.PIPE).stdout
        # GrepCurrentPID = GrepCurrentPID.read().decode().split('\n')
        GrepCurrentPID = GrepCurrentPID.read().decode()
        
        # Checking result
        if GrepCurrentPID:
            # Process is already running, exiting...
            print('Process already running \n' + GrepCurrentPID + '\nExiting...')
            sys.exit(2)
        else:
            # Cleaning vars
            del PSCommand
            del GrepCurrentPID
    
    # Do the Unix double-fork magic; 
    # see Stevens's book "Advanced Programming in the UNIX Environment" (Addison-Wesley) for details
    try:
        pid = os.fork()
        if pid > 0:
            # Exit first parent
            sys.exit(0)

    except OSError as e:
        sys.exit(1)

    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # Do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # Creating the PID file
            OpenedPIDFile = open(PIDFile,"w+")

            # Filling it with data
            OpenedPIDFile.write(str(pid))

            # Close the PID file
            OpenedPIDFile.close()

            # Exit first parent
            sys.exit(0)

    except OSError as e:
        sys.exit(1)

    # Start the daemon main loop
    main(sys.argv[1:])

