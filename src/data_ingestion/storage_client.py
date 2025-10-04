import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class AzureStorageClient:
    def __init__(self):
        self.connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
        self.container_name = settings.STORAGE_CONTAINER
        self.blob_service_client = None
        self.container_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize Azure Storage clients and create container if it doesn't exist"""
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
            
            # Check if container exists, create if it doesn't
            try:
                self.container_client = self.blob_service_client.get_container_client(
                    self.container_name
                )
                # Test if container exists by getting properties
                self.container_client.get_container_properties()
                logger.info(f"✅ Container '{self.container_name}' already exists")
            except Exception:
                # Container doesn't exist, create it
                logger.info(f"📦 Creating container '{self.container_name}'...")
                self.container_client = self.blob_service_client.create_container(
                    self.container_name
                )
                logger.info(f"✅ Container '{self.container_name}' created successfully")
            
            logger.info("✅ Azure Storage clients initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Azure Storage clients: {str(e)}")
            raise
    
    def upload_file(self, file_path, blob_name=None):
        """
        Upload a file to Azure Blob Storage
        
        Args:
            file_path (str): Local path to the file
            blob_name (str): Name for the blob in storage (optional)
        
        Returns:
            str: URL of the uploaded blob
        """
        if not blob_name:
            blob_name = os.path.basename(file_path)
        
        try:
            with open(file_path, "rb") as data:
                blob_client = self.container_client.get_blob_client(blob_name)
                blob_client.upload_blob(data, overwrite=True)
            
            blob_url = f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}"
            logger.info(f"✅ File uploaded successfully: {blob_name}")
            logger.info(f"📎 Blob URL: {blob_url}")
            return blob_url
            
        except Exception as e:
            logger.error(f"❌ Failed to upload file {file_path}: {str(e)}")
            raise

    def generate_sas_url(self, blob_name, expiry_hours=1):
        """
        Generate a SAS URL for temporary secure access to a blob
        
        Args:
            blob_name (str): Name of the blob
            expiry_hours (int): Hours until SAS token expires
        
        Returns:
            str: SAS URL for secure access
        """
        try:
            # Create SAS token
            sas_token = generate_blob_sas(
                account_name=self.blob_service_client.account_name,
                container_name=self.container_name,
                blob_name=blob_name,
                account_key=self.blob_service_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=expiry_hours)
            )
            
            # Construct SAS URL
            sas_url = f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"
            
            logger.info(f"🔐 Generated SAS URL for {blob_name} (expires in {expiry_hours} hours)")
            return sas_url
            
        except Exception as e:
            logger.error(f"❌ Failed to generate SAS URL for {blob_name}: {str(e)}")
            raise
    
    def list_blobs(self):
        """List all blobs in the container"""
        try:
            blobs = list(self.container_client.list_blobs())
            logger.info(f"📁 Found {len(blobs)} blobs in container '{self.container_name}'")
            for blob in blobs:
                logger.info(f"   - {blob.name} (Size: {blob.size} bytes)")
            return blobs
        except Exception as e:
            logger.error(f"❌ Failed to list blobs: {str(e)}")
            raise
    
    def test_connection(self):
        """Test the connection to Azure Storage"""
        try:
            # Try to list containers to test connection
            containers = self.blob_service_client.list_containers()
            logger.info("✅ Azure Storage connection test: PASS")
            return True
        except Exception as e:
            logger.error(f"❌ Azure Storage connection test: FAILED - {str(e)}")
            return False