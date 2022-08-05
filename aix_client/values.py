# constant loadby parameters.conf for ELK 
ELKMonitoringVersion = None
ECSVersion = None
ElasticServers = []
ElasticPort = None
ElasticIndexName = None
FilebeatServers = []
FilebeatPort = None
FilebeatIndexName = None
LogstashServers = []
LogstashPort = None
ELKUsername = None
ELKPassword = None
ELKWebProtocol = None
ELKCertificate = None
BypassProxy= None
FQDN = None
Tags = []
Labels = []
BulkMaxSize = None
TailRefreshValue = None
CycleSleepTime = None
DiskSampleRate = None
TopProcesses = None
PingPlotterTargets = None
PingSamples = None
PingTimeout = None
IfSystemHypervisorEnable = None
IfSystemHPMStatEnable = None
EntRestricted = None
FcsRestricted = None
HdiskRestricted = None
SystemSocketWaitValue = None
PingPlotterWaitValue = None
ErrptLogWaitValue = None
SystemHypervisorWaitValue = None
SystemProcessWaitValue = None
SystemSocketSummaryWaitValue = None
SystemFilesystemAndFstatWaitValue = None
SystemDiskIOWaitValue = None
SystemProcessSummaryWaitValue = None
SystemHPMStatWaitValue = None
SystemLoadWaitValue = None
SystemMemoryWaitValue = None
SystemFcWaitValue = None
SystemNetworkWaitValue = None
SystemCoreAndCpuWaitValue = None


# Defining arrays for ELK servers follow-up
BaseDir = None
LogFilePath = None
ConfigFilePath = None
ElasticServersAvailable = []
FilebeatServersAvailable = []
LogstashServersAvailable = []
ElasticServersFailed = []
FilebeatServersFailed = []
LogstashServersFailed = []
Tagz = []
NMONSeq = None


# Using FilebeatConfigsArray and CustomMetricsConfigsArray dictionary for follow up purpose
FilebeatConfigsArray = []
CustomMetricsConfigsArray = []
PingPlotterArray = None
TargetFileCurrentPosArray = []


# Setting vars for send to metricbeat
SendQueueArray = []
FilebeatSendQueueArray = []
LogstashSendQueueArray = []
ELKCreds = None
ElasticServerCnx = None
FilebeatServerCnx = None
LogstashServerCnx = None
MetricbeatQueueFlushed = None
FilebeatQueueFlushed = None
LogstashQueueFlushed = None


# Switching vars to for get necessary LPAR informations
LPARName = None
LPARSMTMode = None
LPARArch = None
LPARHost = None
AIXVersion = ''
LPARRndID = None
AgentID = None
NetworkCards = []
FcCards = []
# FcCards list need to be formated before being used for get necessary LPAR informations
FcCards = []
NumProc = None
NumProcString = None
IfVIOS = None

# Switching FilebeatConfigsArray, TargetFileCurrentPosArray and TailStateArray dictionary for follow up purpose
TailStateArray = []


# Switching value for this function  start logging
StartupLogFile = None
StartupLogFileLast = None
MainLogFile = None
MainLogFileLast = None
CrashDumpCheckLog = None
CrashDumpSendLog = None
CrashDumpDaemon = None

# Formating string
EphemeralID = None

# Setting vars for threads follow up for the function Ping Flotter
PingPlotterThread = None

# Define variables for the function main
devnull = None
ExecutionTimers = {}
# TargetFileMTimeCountArray fro the function main
SystemProcessThread = None
SystemSocketThread = None
SystemDiskIOThread = None
SystemMemoryThread = None
SystemHPMStatThread = None

# Setting vars for the function GenerateStaticJSON
StaticJSON = None
StaticJSONFilebeat = None

# Setting vars
AllElasticServersFailedDate = None
AllFilebeatServersFailedDate = None
AllLogstashServersFailedDate = None

# Sharing TailStateArray and TargetFileCurrentPosArray with other threads

global LastErrpt