#!/bin/bash
echo "Creating zip file to upload to AWS..."
rootDir=$(pwd)
zip -r9 $rootDir/function.zip ./utilobot
zip -g function.zip main.py
zip -g function.zip requirements.txt
echo "Zip file creation completed. Upload function.zip to AWS"