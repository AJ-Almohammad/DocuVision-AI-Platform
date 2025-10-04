#!/usr/bin/env python3
"""
Azure Cost Monitoring Script
Check your current Azure spending
"""
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def check_costs():
    print("💰 Azure Cost Check")
    print("=" * 50)
    
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    
    # Check current subscription
    print("\n📋 Subscription Info:")
    sub_info = subprocess.run(
        f"az account show --subscription {subscription_id}",
        shell=True, capture_output=True, text=True
    )
    if sub_info.returncode == 0:
        import json
        sub_data = json.loads(sub_info.stdout)
        print(f"   Name: {sub_data.get('name', 'N/A')}")
        print(f"   State: {sub_data.get('state', 'N/A')}")
    
    # Check resource group costs (estimated)
    print("\n💡 Cost Information:")
    print("""
    Your current resources (FREE TIER ELIGIBLE):
    
    🔹 Azure Blob Storage:
      - First 5 GB: FREE per month
      - Beyond 5 GB: ~$0.023 per GB/month
    
    🔹 Document Intelligence:
      - First 500 pages: FREE per month  
      - Beyond 500 pages: ~$1.50 per 100 pages
    
    🔹 Estimated Monthly Cost (Low Usage): $0-2
    """)
    
    # List current resources
    print("\n📊 Current Resources:")
    resources = subprocess.run(
        f"az resource list --resource-group tuv-sud-document-ai-rg --subscription {subscription_id}",
        shell=True, capture_output=True, text=True
    )
    
    if resources.returncode == 0 and resources.stdout.strip():
        import json
        resource_data = json.loads(resources.stdout)
        for resource in resource_data:
            print(f"   - {resource['type']}: {resource['name']}")
    else:
        print("   No resources found (or resource group doesn't exist)")
    
    print("\n💡 Recommendations:")
    print("1. Monitor usage in Azure Portal > Cost Management")
    print("2. Set up spending alerts")
    print("3. Use cleanup script when done testing")
    print("4. Most services have free tiers for low usage")

if __name__ == "__main__":
    check_costs()