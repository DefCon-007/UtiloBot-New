#!/bin/bash
echo "Creating zip file to upload to AWS..."
rootDir=$(pwd)
cd ./env/lib/python*/site-packages
zip -r9 $rootDir/function.zip .
cd $rootDir
zip -g function.zip *.py
echo "Zip file creation completed. Upload function.zip to AWS"