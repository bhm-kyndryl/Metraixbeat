#!/usr/bin/python
import os
import shutil
import socket
import sys
import threading
import time
import requests
import getopt
import subprocess
import logging

# import modules 
import values
from samples import LoadDaemonConfig, CheckServers, CompareTimer, LoadPluginConfig
from metrics import SystemDiskIO, SystemHPMStat, SystemMemory, SystemProcess, SystemSocket,WorkOnMetrics
from utils import FilebeatTail, GetLPARInformations, PingPlotter


def StartLogging():
    """ This function handle logging different informations into file 

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s '
    # Adding trailing / if necessary to LogFilePath
    if not values.LogFilePath.endswith('/'):
        values.LogFilePath = values.LogFilePath + '/'
        
    # Checking if log folder exists
    if not os.path.exists(values.LogFilePath):
        logging.error('Error: Log directory does not exists. Exiting')
        sys.exit(2)
    
    # Defining Startup logging informations
    values.StartupLogFile = values.LogFilePath + "Metraixbeat.Startup.log"
    values.StartupLogFileLast = values.LogFilePath + "Metraixbeat.Startup.log.last"
    
    print('LogFilePath: ', values.LogFilePath)
    print('StartupLogFile: ', values.StartupLogFile)
    
    # sys.exit(2)
    
    # Defining Monitoring logging informations
    values.MainLogFile = values.LogFilePath + "Metraixbeat.log"
    values.MainLogFileLast = values.LogFilePath + "Metraixbeat.log.last"
    
    # Defining Crash logging informations
    values.CrashDumpCheckLog = values.LogFilePath + "Metraixbeat.crash.HTTP-Check.log"
    values.CrashDumpCheckLogLast = values.LogFilePath + "Metraixbeat.crash.HTTP-Check.log.last"
    values.CrashDumpSendLog = values.LogFilePath + "Metraixbeat.crash.HTTP-Send.log"
    values.CrashDumpSendLogLast = values.LogFilePath + "Metraixbeat.crash.HTTP-Send.log.last"
    values.CrashDumpDaemon = values.LogFilePath + "Metraixbeat.crash.Daemon.log"
    values.CrashDumpDaemonLast = values.LogFilePath + "Metraixbeat.crash.Daemon.log.last"

    # Checking if old Startup log file exists
    if os.path.exists(values.StartupLogFile):
        # Rotating logs
        shutil.move(values.StartupLogFile, values.StartupLogFileLast)

    # Checking if old Monitoring log file exists
    if os.path.exists(values.MainLogFile):
        # Rotating logs
        logging.shutdown()
        shutil.move(values.MainLogFile, values.MainLogFileLast)
        
    # Checking if old crash log files exist
    if os.path.exists(values.CrashDumpCheckLog):
        # Rotating logs
        logging.shutdown()
        shutil.move(values.CrashDumpCheckLog, values.CrashDumpCheckLogLast)
    if os.path.exists(values.CrashDumpSendLog):
        # Rotating logs
        logging.shutdown()
        shutil.move(values.CrashDumpSendLog, values.CrashDumpSendLogLast)
    if os.path.exists(values.CrashDumpDaemon):
        # Rotating logs
        logging.shutdown()
        shutil.move(values.CrashDumpDaemon, values.CrashDumpDaemonLast)

    # Configuring Startup log file options
    logging.basicConfig(filename=values.MainLogFile, level=logging.INFO, format='%(asctime)s %(message)s     ')

   

def main(argv):
    """ This is the main function
    
        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """    
   
    # Define null var
    values.devnull = subprocess.DEVNULL 
    # Defining LPAR Name
    values.LPARName = socket.gethostname()   

    # Initializing background threads for long executions
    values.SystemProcessThread = threading.Thread(target=SystemProcess, args=())
    values.SystemDiskIOThread = threading.Thread(target=SystemDiskIO, args=())
    values.SystemSocketThread = threading.Thread(target=SystemSocket, args=())
    values.SystemMemoryThread = threading.Thread(target=SystemMemory, args=())
    values.PingPlotterThread = threading.Thread(target=PingPlotter, args=())
    values.SystemHPMStatThread = threading.Thread(target=SystemHPMStat, args=())
    
    # Initializing requests.sessions
    values.ElasticServerCnx = requests.session()
    values.FilebeatServerCnx = requests.session()
    values.LogstashServerCnx = requests.session()
    
    # Define Empty vars for daemon config file and PID file
    values.LogFilePath = ''
    values.ConfigFilePath = ''
    
    # Checking given arguments with try/catch
    try:
        # Testing args
        opts, args = getopt.getopt(argv,"hc:l:",["ConfigFilePath=","LogFilePath="])
    except getopt.GetoptError:
        # Required args not provided
        #print('Usage:')
        logging.error('metraixbeat -c <Parameters.conf file path> -l <Logs directory path>')
        sys.exit(2)
        
    # Looping on each args given
    for opt, arg in opts:
        # Case of help
        if opt == '-h':
            print('Usage:')
            logging.error('metraixbeat -c <Parameters.conf file path> -l <Logs directory path>')
            sys.exit()
        elif opt in ("-c", "--ConfigFilePath"):
            values.ConfigFilePath = arg
        elif opt in ("-l", "--LogFilePath"):
            values.LogFilePath = arg
            
    # Checking given parameters
    if not values.ConfigFilePath or not values.LogFilePath:
        print('Usage:')
        logging.error('metraixbeat -c <Parameters.conf file path> -l <Logs directory path>')
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
    shutil.move(values.MainLogFile, values.StartupLogFile)

    # Main loop / Infinite loop
    while True:
        # Checking if old Monitoring log file exists
        if os.path.exists(values.MainLogFile):
            # Rotating logs
            logging.shutdown()
            shutil.move(values.MainLogFile, values.MainLogFileLast)
            
        # Log
        logging.info("\n ---------------------------------------------SUMMARY------------------------------------------------------\n")
        
        # Check ELK server's availability
        CheckServers()

        # Compare timers and schedule work for each metricset
        WorkOnMetrics()

        # Analyse and schedule work for each Tail plugins if timer is reached
        ComparisonTimer = CompareTimer("TailPluginsRefresh", values.TailRefreshValue)
        if ComparisonTimer != values.devnull:
            for TailPlugin in values.FilebeatConfigsArray:
                # Launch analyse/work on current Tail plugin config
                FilebeatTail(TailPlugin)

        # Log threading summary
        logging.info('INFO     ==> Running threads: ' + str(threading.enumerate()))

        # Enable the following loop to print internal daemon vars for stability
        logging.info('INFO     ==> Internal vars count: ' + str(len(globals())))

        # Sleep for specified time
        time.sleep(values.CycleSleepTime)

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
    
    #/opt/freeware/bin/python3 main.py -c /etc/metraixbeat/Parameters.conf -l /var/log/metraixbeat/

