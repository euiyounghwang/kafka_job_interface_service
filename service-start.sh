

#!/bin/bash
set -e

JAVA_HOME='C:\Users\euiyoung.hwang\'
PATH=$PATH:$JAVA_HOME
export JAVA_HOME

# Activate virtualenv && run serivce

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTDIR

#--
export GET_KAFKA_ISR_LIST="$SCRIPTDIR/kafka_2.11-0.11.0.0/bin/kafka-topics.sh --describe --zookeeper {} --topic ELASTIC_PIPELINE_QUEUE"
export GET_KAFKA_ISR_SAMPLE_PAYLOAD="http://localhost:8008/kafka/get_kafka_isr_list?broker_list=localhost:2181,localhost:2181,localhost:2181"
export GET_KAFKA_ISR_PARAMS="localhost:2181,localhost:2181,localhost:2181"
#--

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $VENV/bin/activate
else
    source $VENV/Scripts/activate
fi


# -- background
#  sudo netstat -nlp | grep :8008
# nohup $SCRIPTDIR/service-start.sh &> /dev/null &

python -m uvicorn main:app --reload --host=0.0.0.0 --port=8008 --workers 4
# poetry run uvicorn main:app --reload --host=0.0.0.0 --port=8008 --workers 4
