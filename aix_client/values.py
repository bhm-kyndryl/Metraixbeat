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
BulkMaxSize = 0
TailRefreshValue = 0
CycleSleepTime = 0
DiskSampleRate = 0
TopProcesses = 0
PingPlotterTargets = None
PingSamples = 0
PingTimeout = None
IfSystemHypervisorEnable = None
IfSystemHPMStatEnable = None
EntRestricted = None
FcsRestricted = None
HdiskRestricted = None
SystemSocketWaitValue = 0
PingPlotterWaitValue = 0
ErrptLogWaitValue = 0
SystemHypervisorWaitValue = 0
SystemProcessWaitValue = 0
SystemSocketSummaryWaitValue = 0
SystemFilesystemAndFstatWaitValue = 0
SystemDiskIOWaitValue = 0
SystemProcessSummaryWaitValue = 0
SystemHPMStatWaitValue = 0
SystemLoadWaitValue = 0
SystemMemoryWaitValue = 0
SystemFcWaitValue = 0
SystemNetworkWaitValue = 0
SystemCoreAndCpuWaitValue = 0


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
NMONSeq = 0


# Using FilebeatConfigsArray and CustomMetricsConfigsArray dictionary for follow up purpose
FilebeatConfigsArray = {}
CustomMetricsConfigsArray = {}
PingPlotterArray = None
TargetFileCurrentPosArray = {}


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
AIXVersion = None
LPARRndID = None
AgentID = None
NetworkCards = []
FcCards = []
# FcCards list need to be formated before being used for get necessary LPAR informations
FcCards = []
NumProc = None
NumProcString = None
IfVIOS = False

# Switching FilebeatConfigsArray, TargetFileCurrentPosArray and TailStateArray dictionary for follow up purpose
TailStateArray = {}


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

LastErrpt = None