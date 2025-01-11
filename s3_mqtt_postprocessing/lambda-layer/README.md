# AWS Lambda Layer Creation and Configuration Guide
This document describes the manual creation and configuration of a Lambda Layer for an AWS Lambda function. It also provides description to scripts that can simplify the process of creating and packaging the Lambda Layer.
## Scripts to Simplify the Process:
1. **Bash Script**
   - **File Name**: `create_layer.sh`
   - **Usage**:
     ```
     chmod +x create_layer.sh
     ./create_layer.sh
     ```
2. **PowerShell Script**
   - **File Name**: `create_layer.ps1`
   - **Usage**:
     ```
     .\create_layer.ps1
     ```
3. **Batch File**
   - **File Name**: `create_layer.bat`
   - **Usage**:
     Open Command Prompt, navigate to the directory containing the script, and type:
     ```
     create_layer.bat
     ```
4. **Python Script**
   - **File Name**: `create_layer.py`
   - **Usage**:
     ```
     python create_layer.py
     ```

Each script will create a directory named 'python', install necessary libraries (google-cloud-storage and google-auth), and pack this directory into a ZIP file named 'google-storage.zip'. The step to upload the layer to AWS Lambda is commented out in each script. You can either uncomment this step in the script or follow the manual upload instructions below.

## Manual Creation and Configuration of Lambda Layer:
### Step 1: Create and Package the Layer
1. Create a directory named 'python' in current directory.
2. Install the required libraries:
```
pip install google-cloud-storage google-auth -t ./python
```
3. Pack 'python' directory into a ZIP file named 'google-storage.zip'.

### Step 2: Upload the Layer to AWS Lambda
1. Navigate to the AWS Management Console.
2. Go to the Lambda service.
3. Click on "Layers" in the left sidebar.
4. Click "Create layer".
5. Enter a name for your layer, e.g., 'google-storage-layer'.
6. Upload the 'google-storage.zip' file.
7. Choose compatible runtimes, e.g., Python 3.12.
8. Click "Create".

### Step 3: Attach the Layer to Your Lambda Function
1. Navigate to the Lambda function 'shelly_tunel_data_s3_gcp_lambda.py'.
2. In the function configuration, scroll to the "Layers" section.
3. Click "Add a layer".
4. Select "Custom layers" and choose the 'google-storage-layer' you created.
5. Click "Add".
