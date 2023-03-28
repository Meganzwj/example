import requests
import json
import os

# Set variables for Private Link configuration
service_endpoint = "https://<cognitive-search-service-name>.search.<region>.private.azure.com"
api_version = "2020-06-30-Preview"

# Set variables for Azure Blob Storage account and container
storage_account_name = "<storage-account-name>"
storage_container_name = "<container-name>"
storage_account_key = "<storage-account-key>"
blob_name = "<blob-name>"

# Set variables for Azure Cognitive Search index and API key
search_service_name = "<cognitive-search-service-name>"
search_index_name = "<index-name>"
api_key = "<admin-api-key>"

# Construct the SAS token for accessing the Blob Storage container
sas_token = BlobSASPermissions(read=True).generate_sas(storage_account_name, storage_container_name, storage_account_key)

# Construct the URL for the CSV file in the Blob Storage container
blob_url = f"https://{storage_account_name}.blob.core.windows.net/{storage_container_name}/{blob_name}?{sas_token}"

# Construct the URL for the Azure Cognitive Search document upload API
upload_url = f"{service_endpoint}/indexes/{search_index_name}/docs/index?api-version={api_version}"

# Set the HTTP headers for the Azure Cognitive Search document upload API
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Read the CSV file data from the Blob Storage container
response = requests.get(blob_url)
csv_data = response.content.decode("utf-8").splitlines()

# Convert the CSV data to JSON documents and upload them to Azure Cognitive Search
json_documents = []
for line in csv_data:
    # Assuming the first line of the CSV file contains the headers, split the remaining lines into values
    values = line.split(",")
    # Construct a JSON document from the CSV values
    json_document = {}
    for i, value in enumerate(values):
        header = csv_data[0].split(",")[i]
        json_document[header] = value
    json_documents.append(json.dumps(json_document))
    
# Upload the JSON documents to Azure Cognitive Search
payload = "\n".join(json_documents)
response = requests.post(upload_url, headers=headers, data=payload)

# Check if there was an error with the HTTP request
response.raise_for_status()

# If the HTTP request was successful, print the response content
print(response.content)
