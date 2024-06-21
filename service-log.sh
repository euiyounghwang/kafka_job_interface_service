#!/bin/bash
set -e

#tail -f ./logs/kafkajob-interface-api.log
sudo journalctl -u kafkajob_interface_api.service -f