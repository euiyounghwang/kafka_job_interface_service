from config.log_config import create_log
from dotenv import load_dotenv
# import yaml
import json
import os
from service.job_service import JobHandler, ProcessHandler

load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()


ProcessHandlerInject = ProcessHandler(logger)
JobHandlerInject = JobHandler(logger, ProcessHandlerInject)