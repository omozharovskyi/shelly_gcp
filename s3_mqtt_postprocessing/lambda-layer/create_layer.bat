@echo off

REM Create a directory named 'python'
if not exist "python" mkdir "python"

REM Install required libraries into the 'python' directory
pip install google-cloud-storage google-auth -t .\python

REM Package the 'python' directory into a zip archive named 'google-storage.zip'
powershell Compress-Archive -Path ".\python\*" -DestinationPath ".\google-storage.zip"

REM The following line is commented out; uncomment it to upload the layer to AWS Lambda
REM aws lambda publish-layer-version --layer-name google-storage-layer --zip-file fileb://google-storage.zip

echo Layer creation script has completed.
pause