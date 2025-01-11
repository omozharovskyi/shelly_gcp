import os
import zipfile

# Create a directory named 'python' if it doesn't exist
os.makedirs('python', exist_ok=True)

# Install required libraries into the 'python' directory
os.system('pip install google-cloud-storage google-auth -t ./python')

# Package the 'python' directory into a zip archive named 'google-storage.zip'
with zipfile.ZipFile('google-storage.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('python'):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, os.path.join('python', '..')))

# The following line is commented out; uncomment it to upload the layer to AWS Lambda
# os.system('aws lambda publish-layer-version --layer-name google-storage-layer --zip-file fileb://google-storage.zip')

print("Layer creation script has completed.")