# kafka_job_interface_service
<i>kafka_job_interface_service

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python.
This is a repository that provides to deliver the records to the Prometheus-Export application.

Kafka API for Prometheus(https://github.com/euiyounghwang/prometheus-export) to send an email or other things


#### Python V3.9 Install
```bash
sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel git 
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz 
tar –zxvf Python-3.9.0.tgz or tar -xvf Python-3.9.0.tgz 
cd Python-3.9.0 
./configure --libdir=/usr/lib64 
sudo make 
sudo make altinstall 

# python3 -m venv .venv --without-pip
sudo yum install python3-pip

sudo ln -s /usr/lib64/python3.9/lib-dynload/ /usr/local/lib/python3.9/lib-dynload

python3 -m venv .venv
source .venv/bin/activate

# pip install -r ./dev-requirement.txt
pip install prometheus-client
pip install requests
pip install JPype1
pip install psycopg2-binary
pip install jaydebeapi
pip install pytz
pip install httpx

# when error occur like this
# ImportError: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168
pip install urllib3==1.26.18
pip install pytz
```


### Using Poetry: Create the virtual environment in the same directory as the project and install the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install poetry

# --
poetry config virtualenvs.in-project true
poetry init
poetry add fastapi
poetry add uvicorn
poetry add pytz
poetry add httpx
poetry add requests
```
or you can run this shell script `./create_virtual_env.sh` to make an environment. then go to virtual enviroment using `source .venv/bin/activate`



### Register Service
- sudo service kafkajob_interface_api status/stop/start/restart
```bash
#-- /etc/systemd/system/kafkajob_interface_api.service
[Unit]
Description=KafkaJob Interface Service

[Service]
User=devuser
Group=devuser
Type=simple
ExecStart=/bin/bash /home/devuser/kafkajob_interface_api/service-start.sh
ExecStop= /usr/bin/killall kafkajob_interface_api

[Install]
WantedBy=default.target


# Service command
sudo systemctl daemon-reload 
sudo systemctl enable kafkajob_interface_api.service
sudo systemctl start kafkajob_interface_api.service 
sudo systemctl status kafkajob_interface_api.service 
sudo systemctl stop kafkajob_interface_api.service 

sudo service kafkajob_interface_api status/stop/start
```



### Run Custom Promethues Exporter
- Run this command : $ `http://localhost:8008/docs`
