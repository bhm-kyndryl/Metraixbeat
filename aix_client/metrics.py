#!/usr/bin/python


import logging
import subprocess
import datetime
import threading
from time import time
import traceback
from samples import CompareTimer
from utils import ErrptLog, GenerateDynamicJson, PingPlotter, SendJSON
from values import( 
    DiskSampleRate,
    ErrptLogWaitValue,
    FcCards,
    HdiskRestricted,
    IfSystemHPMStatEnable,
    IfSystemHypervisorEnable,
    IfVIOS,
    LPARArch,
    NetworkCards,
    NumProc,
    NumProcString,
    PingPlotterWaitValue,
    StaticJSON, 
    SystemCoreAndCpuWaitValue, 
    SystemDiskIOWaitValue, 
    SystemFcWaitValue,
    SystemFilesystemAndFstatWaitValue,
    SystemHPMStatWaitValue,
    SystemHypervisorWaitValue, 
    SystemLoadWaitValue, 
    SystemMemoryWaitValue, 
    SystemNetworkWaitValue, 
    SystemProcessSummaryWaitValue, 
    SystemProcessWaitValue, 
    SystemSocketSummaryWaitValue, 
    SystemSocketWaitValue, 
    devnull,
    SystemDiskIOThread,
    CustomMetricsConfigsArray,
    CrashDumpDaemon,
    SystemSocketThread,
    SystemHPMStatThread,
    SystemMemoryThread
)

import values

def WorkOnMetrics():
    """ This function will check execution timers and, if necessary, execute item work.
        Items can be builtin Metricbeat Metricsets or Custom Metricsets.

        Some work on specific items are executed in background because execution duration is too long.
    
        TODO: Describe the function, all vars and its content
    """
    

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

def SystemCoreAndCpu(ComparisonTimer):
    """ This function analyse CPU activity and send metrics to ElasticSearch server

        Please refer to README.md
    
        TODO: Describe the function, all vars and its content
    """   
    
    # Generating current ELK timestamp for JSON message
    SeqIdTimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    # Gathering data from OS command for LPAR allocations
    CmdLine = 'lparstat -i | egrep "SMT|Online Virtual CPUs|Entitled Capacity" | head -3'
    LPARStatCmd = subprocess.Popen(CmdLine, shell=True, stdout=subprocess.PIPE).stdout
    LPARStatCmd = LPARStatCmd.read().decode().split('\n')

    # LPARSTAT Custom metrics
    values.LPARCPUMode = str(LPARStatCmd[0].split(' ')[-1])
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
    CurrOnlineVCPU = round(OnlineCPUThreadsCount / int(values.LPARSMTMode))
    
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
    if "Dedicated" in values.LPARCPUMode:
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
    if "Dedicated" in values.LPARCPUMode:
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
