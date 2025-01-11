#!/bin/bash

# Create a directory named 'python'
mkdir -p python

# Install required libraries into the 'python' directory
pip install google-cloud-storage google-auth -t ./python

# Package the 'python' directory into a zip archive named 'google-storage.zip'
zip -r google-storage.zip python/

# The following line is commented out; uncomment it to upload the layer to AWS Lambda
# aws lambda publish-layer-version --layer-name google-storage-layer --zip-file fileb://google-storage.zip