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

# Create a blob service client and get a reference to the container
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Download and transform each blob in the container, and upload the documents to the search index
documents_to_upload = []
for blob in container_client.list_blobs():
    blob_client = container_client.get_blob_client(blob.name)
    blob_contents = blob_client.download_blob().content_as_text()
    # Replace this with your own transformation logic
    document = {"id": blob.name, "title": blob_contents.splitlines()[0], "author": blob_contents.splitlines()[1]}
    documents_to_upload.append(document)
result: IndexDocumentsResult = client.upload_documents(documents=documents_to_upload)
print("Uploaded {} documents".format(result.results_count))
