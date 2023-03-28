import requests
import json
import base64

# Replace with your own values
search_service_name = '<search-service-name>'
api_version = '2019-05-06'
admin_key = '<admin-key>'
index_name = '<index-name>'
storage_account_name = '<storage-account-name>'
container_name = '<container-name>'
blob_name = '<blob-name>'
csv_separator = ','

# Get the shared access signature (SAS) token for the blob
sas_token_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}?sv=2022-02-06&ss=b&srt=sco&sp=r&se=2023-04-01T00:00:00Z&st=2023-03-01T00:00:00Z&spr=https&sig=<signature>"
# Replace <signature> with the actual signature value

# Construct the REST API endpoint URL for the import data operation
endpoint_url = f"https://{search_service_name}.search.windows.net/indexes/{index_name}/docs/index?api-version={api_version}"

# Construct the headers and payload for the REST API call
headers = {
    'Content-Type': 'application/json',
    'api-key': admin_key
}

payload = {
    'value': []
}

# Download the CSV file from blob storage and convert it to JSON
imported_count = 0
csv_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}{sas_token_url}"
response = requests.get(csv_url)
response.raise_for_status()

csv_lines = response.text.split('\r\n')
header = csv_lines[0].split(csv_separator)
for i in range(1, len(csv_lines)):
    if csv_lines[i] == '':
        continue
    values = csv_lines[i].split(csv_separator)
    row = {}
    for j in range(len(header)):
        row[header[j]] = values[j]
    payload['value'].append(row)
    imported_count += 1

# Send the REST API request to import the data into Azure Cognitive Search
response = requests.post(endpoint_url, headers=headers, json=payload)
response.raise_for_status()

# Print the number of documents imported
print(f"{imported_count} documents imported to Azure Cognitive Search.")
