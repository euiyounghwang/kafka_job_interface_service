
import json
from service.status_handler import (StatusHanlder, StatusException)
import requests
from fastapi import Response
import pandas as pd
from collections import defaultdict
import subprocess
import os


class ProcessHandler(object):
    ''' Get the process by the processname'''

    def __init__(self, logger):
         self.logger = logger
        

    ''' get ProcessID'''
    def isProcessRunning(self, name):
        ''' Get PID with process name'''
        try:
            call = subprocess.check_output("pgrep -f '{}'".format(name), shell=True)
            self.logger.info("Process IDs - {}".format(call.decode("utf-8")))
            return True
        except subprocess.CalledProcessError:
            return False
        
    
    ''' get command result'''
    def get_run_cmd_Running(self, cmd):
        ''' Get PID with process name'''
        try:
            self.logger.info("get_run_cmd_Running - {}".format(cmd))
            call = subprocess.check_output("{}".format(cmd), shell=True)
            output = call.decode("utf-8")
            # logging.info("CMD - {}".format(output))
            # logging.info(output.split("\n"))
            
            output = [element for element in output.split("\n") if len(element) > 0]

            return output
        except subprocess.CalledProcessError:
            return None   
        

class JobHandler(object):
    
    def __init__(self, logger, ProcessHandlerInject):
         self.logger = logger
         self.ProcessHandlerInject = ProcessHandlerInject
        

    async def get_kafka_ISR_lists(self, broker_list):
        ''' get kafka ISR lists'''
        GET_KAFKA_ISR_LIST = os.environ["GET_KAFKA_ISR_LIST"]
        self.logger.info(f"GET_KAFKA_ISR_LIST - {GET_KAFKA_ISR_LIST}")

        # kafka_topic_isr = '/home/biadmin/monitoring/custom_export/kafka_2.11-0.11.0.0/bin/kafka-topics.sh --describe --zookeeper  {} --topic ELASTIC_PIPELINE_QUEUE'.format(ZOOKEEPER_URLS)
        response = self.ProcessHandlerInject.get_run_cmd_Running(GET_KAFKA_ISR_LIST.format(broker_list))

        # logging.info(f"Kafka ISR : {response}")
        ''' ['Topic:ELASTIC_PIPELINE_QUEUE\tPartitionCount:16\tReplicationFactor:3\tConfigs:', '\ '''

        kafk_offsets_dict = defaultdict()
        for idx in range(1, len(response)):
            each_isr = [element for element in response[idx].split("\t") if len(element) > 0]
            self.logger.info(each_isr)
            kafk_offsets_dict.update({"{}_{}".format(each_isr[0],str(idx-1)) : each_isr})

        self.logger.info(f"get_kafka_ISR_lists - {json.dumps(kafk_offsets_dict, indent=2)}")

        return kafk_offsets_dict 

    async def get_kafka_isr_list(self, broker_list):
        ''' get_kafka_isr_list '''
        '''
        {
            "Topic: ELASTIC_PIPELINE_QUEUE_0": [
            "Topic: ELASTIC_PIPELINE_QUEUE",
            "Partition: 0",
            "Leader: 1",
            "Replicas: 3,1,2",
            "Isr: 1,2"
            ],
            "Topic: ELASTIC_PIPELINE_QUEUE_1": [
            "Topic: ELASTIC_PIPELINE_QUEUE",
            "Partition: 1",
            "Leader: 1",
            "Replicas: 1,2,3",
            "Isr: 1,2"
            ],
            ...
        }
        '''
        try:

            self.logger.info(f"get_kafka_isr_list : {broker_list}")
            # -- make a call to master node to get the information of activeapps
            response = await self.get_kafka_ISR_lists(broker_list)
            self.logger.info(f"get_kafka_isr_list [response]: {response}")
            
            return response
        
        except Exception as e:
           return StatusException.raise_exception(str(e))

   