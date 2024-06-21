from fastapi import APIRouter
import json
import datetime
from injector import logger, JobHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import pandas as pd
from fastapi.responses import StreamingResponse
import datetime
import os

''' Enter the host name of the master node in the spark cluster to collect the list of running spark jobs. '''
app = APIRouter(
    prefix="/kafka",
)


'''
@app.get("/query", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/cluster/health?es_url=http://localhost:9200", 
          summary="DB Query")
async def get_db_query(es_url="http://localhost:9200"):
    # logger.info(es_url)
    # response =  SearchAPIHandlerInject.get_es_health(es_url)
    # if isinstance(response, dict):
    #     logger.info('SearchOmniHandler:get_es_info - {}'.format(json.dumps(response, indent=2)))

    return {}
'''


@app.get("/get_kafka_isr_list", 
          status_code=StatusHanlder.HTTP_STATUS_200,
        #   responses={
        #     200: {"description" : "OK"},
        #     404 :{"description" : "URl not found"}
        #   },
          description="Sample Payload : {}".format(os.environ["GET_KAFKA_ISR_SAMPLE_PAYLOAD"]), 
          summary="Get the list of kafka ISR")
async def get_kafka_isr_list(broker_list=os.environ["GET_KAFKA_ISR_PARAMS"]):
    ''' get the list of Kafka ISR's in the specific kafka cluster '''
    '''
    {
        "running_time": 2.24,
        "results": {
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
    }
    '''
    try:
        StartTime = datetime.datetime.now()
        
        response_json = await JobHandlerInject.get_kafka_isr_list(broker_list)
        
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        return {"running_time" : float(Delay_Time), "results" : response_json}
       
    except Exception as e:
        logger.error(e)
        return StatusException.raise_exception(e)

