#!/usr/bin/env python3
"""
Secure Azure Resource Setup Script for TÜV SÜD Document AI
Run this once to create the necessary Azure resources
"""
import subprocess
import json
import os
import time

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def run_azure_cli_command(command):
    """Run Azure CLI command and return result"""
    try:
        print(f"Running: az {command}")
        result = subprocess.run(f"az {command}", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def main():
    print("=== Secure Azure Resource Setup for TÜV SÜD Document AI ===")
    print("This will create the necessary Azure resources for our project.\n")
    
    # Check if user is logged into Azure CLI
    print("1. Checking Azure CLI login...")
    login_check = run_azure_cli_command("account show")
    if not login_check:
        print("❌ Please login to Azure CLI first: run 'az login'")
        return
    
    # Get subscription ID from environment
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        print("❌ AZURE_SUBSCRIPTION_ID not found in .env file")
        return
    
    print(f"✅ Using subscription: {subscription_id}")
    
    # Create resource group
    resource_group = "tuv-sud-document-ai-rg"
    location = "germanywestcentral"  # Good for German companies
    
    print(f"\n2. Creating Resource Group: {resource_group}")
    create_rg = f"group create --name {resource_group} --location {location} --subscription {subscription_id}"
    if run_azure_cli_command(create_rg):
        print("✅ Resource group created")
    
    # Create storage account (needs unique name)
    print("\n3. Creating Storage Account...")
    storage_account = "tuvsuddocs" + subscription_id.replace("-", "")[:10]
    create_storage = f"storage account create --name {storage_account} --resource-group {resource_group} --location {location} --sku Standard_LRS --encryption-services blob --subscription {subscription_id}"
    if run_azure_cli_command(create_storage):
        print(f"✅ Storage account created: {storage_account}")
    
    # Create container in storage account
    print("\n4. Creating Storage Container...")
    create_container = f"storage container create --name technical-reports --account-name {storage_account} --resource-group {resource_group} --subscription {subscription_id}"
    if run_azure_cli_command(create_container):
        print("✅ Storage container 'technical-reports' created")
    
    # Create Form Recognizer (Document Intelligence) resource
    print("\n5. Creating Document Intelligence Resource...")
    form_recognizer = "tuv-sud-doc-intel"
    create_fr = f"cognitiveservices account create --name {form_recognizer} --resource-group {resource_group} --kind FormRecognizer --sku S0 --location {location} --yes --subscription {subscription_id}"
    if run_azure_cli_command(create_fr):
        print("✅ Document Intelligence resource created")
    
    # Wait a bit for resources to propagate
    print("\n6. Waiting for resources to be ready...")
    time.sleep(30)
    
    print("\n7. Getting connection details...")
    
    # Get storage connection string
    get_storage_conn = f"storage account show-connection-string --name {storage_account} --resource-group {resource_group} --query connectionString --subscription {subscription_id}"
    conn_string = run_azure_cli_command(get_storage_conn)
    
    # Get Form Recognizer details
    get_fr_key = f"cognitiveservices account keys list --name {form_recognizer} --resource-group {resource_group} --query key1 --subscription {subscription_id}"
    fr_key = run_azure_cli_command(get_fr_key)
    
    get_fr_endpoint = f"cognitiveservices account show --name {form_recognizer} --resource-group {resource_group} --query properties.endpoint --subscription {subscription_id}"
    fr_endpoint = run_azure_cli_command(get_fr_endpoint)
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\nAdd these values to your .env file:\n")
    print(f"AZURE_STORAGE_CONNECTION_STRING={conn_string if conn_string else 'GET_MANUALLY_FROM_AZURE_PORTAL'}")
    print(f"AZURE_FORMRECOGNIZER_ENDPOINT={fr_endpoint if fr_endpoint else 'GET_MANUALLY_FROM_AZURE_PORTAL'}")
    print(f"AZURE_FORMRECOGNIZER_KEY={fr_key if fr_key else 'GET_MANUALLY_FROM_AZURE_PORTAL'}")
    print("\n" + "="*60)
    print("\nNext steps:")
    print("1. Copy the above values to your .env file")
    print("2. Run the security validation again: python scripts/validate_security.py")
    print("3. Your Azure infrastructure will be ready!")

if __name__ == "__main__":
    main()