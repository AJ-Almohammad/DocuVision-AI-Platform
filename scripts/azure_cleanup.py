#!/usr/bin/env python3
"""
Azure Resource Cleanup Script
Use this to delete resources and avoid charges
"""
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def run_azure_command(command):
    """Run Azure CLI command"""
    try:
        result = subprocess.run(f"az {command}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command.split()[0]} successful")
            return True
        else:
            print(f"❌ {command.split()[0]} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("🔧 Azure Resource Cleanup Script")
    print("⚠️  WARNING: This will DELETE your Azure resources!")
    print("   Only run this if you want to stop using the services.\n")
    
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = "tuv-sud-document-ai-rg"
    
    confirm = input("Type 'DELETE' to confirm resource deletion: ")
    if confirm != "DELETE":
        print("❌ Cleanup cancelled")
        return
    
    print(f"\n🗑️  Deleting resource group: {resource_group}")
    
    # Delete the entire resource group (this deletes everything in it)
    delete_command = f"group delete --name {resource_group} --yes --subscription {subscription_id}"
    if run_azure_command(delete_command):
        print(f"🎉 Successfully deleted resource group: {resource_group}")
        print("\n📝 Next steps:")
        print("1. Remove Azure credentials from your .env file")
        print("2. The following resources have been deleted:")
        print("   - Storage Account")
        print("   - Document Intelligence Service")
        print("   - Resource Group")
        print("\n💡 You won't be charged for deleted resources.")
    else:
        print("❌ Failed to delete resource group")

if __name__ == "__main__":
    main()