import csv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import IndexDocumentsResult
from azure.storage.blob import BlobServiceClient

# Replace with your search service name and admin api key
service_name = "<your-search-service-name>"
admin_key = "<your-admin-api-key>"

# Replace with your blob storage connection string and container name
connection_string = "<your-blob-storage-connection-string>"
container_name = "<your-blob-storage-container-name>"
blob_name = "<your-blob-name>"

# Replace with your index name and field mappings
index_name = "<your-index-name>"
field_mappings = {
    "id": {"type": "Edm.String", "key": True, "searchable": False},
    "title": {"type": "Edm.String", "searchable": True, "analyzer": "standard"},
    "author": {"type": "Edm.String", "searchable": True, "analyzer": "standard"}
}

# Create a search index client
credential = AzureKeyCredential(admin_key)
client = SearchIndexClient(endpoint="https://{}.search.windows.net/".format(service_name), index_name=index_name, credential=credential)

# Create a blob service client and get a reference to the blob
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)

# Download the CSV file and transform each row into a document to upload to the search index
documents_to_upload = []
csv_contents = blob_client.download_blob().content_as_text()
reader = csv.reader(csv_contents.splitlines())
header = next(reader)
for row in reader:
    # Replace this with your own transformation logic
    document = {"id": row[0], "title": row[1], "author": row[2]}
    documents_to_upload.append(document)
result: IndexDocumentsResult = client.upload_documents(documents=documents_to_upload)
print("Uploaded {} documents".format(result.results_count))
