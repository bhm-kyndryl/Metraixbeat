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

# function load json file, verify and test update value aix 
def load_json_metric(path):
    # Checking if LPAR is a VIOS
    if values.IfVIOS:
        values.OSFamily = 'VIOS'
    else:
        values.OSFamily = 'AIX'           

    if os.path.exists(path):
        logging.info(path)
        FILE_STATIC_JSON= os.path.join(path, "generate-static.json")
        if os.path.exists(FILE_STATIC_JSON):
            logging.info(FILE_STATIC_JSON)
            try:
                with open(os.path.join(FILE_STATIC_JSON),'r') as data_metric:
                    JSONValues = json.load(data_metric) 
                    # 
                    #JSONValues = json.dumps(data_metric, sort_keys=True, indent=4)
                    #logging.info(JSONValues)
                    values.StaticJSON = JSONValues["StaticJSON"]
                    logging.info(values.StaticJSON["host"]["os"]["name"])
                    values.StaticJSON["host"]["os"]["name"]= "AIX/7"
                    logging.info("------------------------")
                    logging.info(JSONValues["StaticJSON"])
            except:
                logging.info(str(traceback.print_exc()))
                traceback.print_exc()
                os._exit(2)
        else:
            logging.error(argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path"))

    else:
        logging.error(argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path"))

def print_test():
    values.StaticJSON =  {
        "tags": str(values.Tags),
        "rollup": {
            "tagz": str(values.Tagz),
            "hostname": values.LPARName
        },
        "agent": {
            "version": values.ELKMonitoringVersion,
            "type": "metricbeat",
            "ephemeral_id": values.EphemeralID,
            "hostname":  values.LPARName,
            "id":  values.AgentID
        },
        "host": {
            "name":  values.LPARName,
            "hostname":  values.LPARName,
            "architecture": values.LPARArch,
            "id": values.LPARRndID,
            "containerized": "false",
            "os": {
                "platform": "AIX",
                "version":  values.AIXVersion,
                "family": values.OSFamily,
                "name": "AIX",
                "kernel": values.AIXVersion,
                "codename": "AIX"
            }
        },
        "ecs": {
            "version": values.ECSVersion
        },
        "labels":{
            
        }
    }
    values.StaticJSON = json.dumps(values.StaticJSON, indent=4)
    logging.info("------------------------")
    print(values.StaticJSON)

#!/usr/bin/python



import logging
import os

from samples import signal_handler, parse_arguments, shutdown, load_json_metric, print_test

# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_METRICS = os.path.join(BASE_DIR, "data")

def main():
        
    args = parse_arguments()
    LogFilePath = "."
    MainLogFile = LogFilePath + "Metraixbeat.log"
    #conf_path(args.configFile)
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s '
    
    logging.StreamHandler()
    logging.basicConfig(
        level=logging.DEBUG, 
        encoding='utf-8', 
        format=log_format,
        datefmt='%d/%m/%Y %I:%M:%S %p'
    )
    
    logging.info('Starting server...')
    logging.info(BASE_DIR)
    load_json_metric(DATA_METRICS)
    print_test()
        
if __name__ == '__main__':
   main()