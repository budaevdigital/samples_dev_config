#!/bin/bash

echo "Start copy..."

CURRENT_DIR=$PWD
PROJECT_FILE_ZIP=samples_dev_config-master.zip

wget https://github.com/budaevdigital/samples_dev_config/archive/master.zip -O $PROJECT_FILE_ZIP
unzip $PROJECT_FILE_ZIP -d "$CURRENT_DIR"
rm $PROJECT_FILE_ZIP

echo "Done!"
