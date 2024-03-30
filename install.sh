#!/bin/bash

CURRENT_DIR=.
PROJECT_FILE_ZIP=

wget https://github.com/budaevdigital/samples_dev_config/archive/master.zip -O $CURRENT_DIR
unzip $PROJECT_FILE_ZIP -d .
rm $PROJECT_FILE_ZIP

echo "Done!"
