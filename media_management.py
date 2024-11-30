from azure.storage.blob import BlobServiceClient
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

# Azure Storage connection string
AZURE_STORAGE_CONNECTION_STRING = ""

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# Container name
container_name = "media"

@app.get("/")
def read_root():
    return 'Hello from desaman Media Api Management'

# Endpoint to upload media
@app.post("/media/upload")
async def upload_media(file: UploadFile = File(...)):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        blob_client.upload_blob(file.file, overwrite=True)
        return {"message": f"{file.filename} uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve media
@app.get("/media/{filename}")
async def get_media(filename: str):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        download_stream = blob_client.download_blob()
        return {
            "filename": filename,
            "content": download_stream.readall().decode("utf-8"),
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")

# Endpoint to delete media
@app.delete("/media/{filename}")
async def delete_media(filename: str):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        blob_client.delete_blob()
        return {"message": f"{filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")
