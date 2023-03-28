import requests
import json
from azure.identity import ClientSecretCredential
from azure.core.pipeline.transport import RequestsTransport

# Define the search service endpoint URL with the private IP address
endpoint_url = 'https://<search-service-name>.search.private.azure.us'

# Define the Azure Storage account credentials
storage_account_name = '<storage-account-name>'
storage_account_key = '<storage-account-key>'
container_name = '<container-name>'
blob_name = '<blob-name>'

# Define the search index name and API version
index_name = '<index-name>'
api_version = '2021-11-01-Preview'

# Define the Azure Active Directory credentials for authentication
tenant_id = '<tenant-id>'
client_id = '<client-id>'
client_secret = '<client-secret>'
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Define the search index documents API endpoint URL
api_url = f'{endpoint_url}/indexes/{index_name}/docs/index?api-version={api_version}'

# Define the HTTP headers for the API request
headers = {
    'Content-Type': 'application/json',
    'api-key': '<admin-key>'
}

# Define the JSON payload for the API request
payload = {
    'value': []
}

# Read the CSV file from Azure Storage and add each row as a document in the payload
storage_url = f'https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}'
response = requests.get(storage_url, headers={'x-ms-version': '2019-02-02', 'x-ms-date': ''}, stream=True)
response.raise_for_status()
for line in response.iter_lines():
    line = line.decode('utf-8')
    if line.strip():
        row = line.split(',')
        document = {
            '@search.action': 'upload',
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'category': row[3]
        }
        payload['value'].append(document)

# Send the API request to index the documents
transport = RequestsTransport()
response = transport.send(requests.Request('POST', api_url, json=payload, headers=headers), credential=credential)
response.raise_for_status()
