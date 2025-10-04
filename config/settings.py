import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Azure Subscription - loaded from environment variables
    SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    
    # These will be loaded from environment variables
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_FORMRECOGNIZER_ENDPOINT = os.getenv("AZURE_FORMRECOGNIZER_ENDPOINT")
    AZURE_FORMRECOGNIZER_KEY = os.getenv("AZURE_FORMRECOGNIZER_KEY")
    
    # Application settings
    API_KEY = os.getenv("API_KEY", "dev-key-change-in-production")
    STORAGE_CONTAINER = "technical-reports"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Create a global settings instance
settings = Settings()

# Validation
if not Settings.SUBSCRIPTION_ID:
    print("⚠️  Warning: AZURE_SUBSCRIPTION_ID not set in .env file")
else:
    print("✅ Azure subscription ID loaded successfully")