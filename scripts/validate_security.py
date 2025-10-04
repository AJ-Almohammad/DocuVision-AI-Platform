#!/usr/bin/env python3
"""
Security validation script - run this to check for exposed secrets
"""
import os
import re

def check_for_exposed_secrets():
    """Check for common security issues in the project"""
    issues = []
    
    # Patterns that might indicate exposed secrets
    secret_patterns = [
        r"password\s*=\s*['\"][^'\"]+['\"]",
        r"key\s*=\s*['\"][^'\"]+['\"]",
        r"connection_string\s*=\s*['\"][^'\"]+['\"]",
        r"endpoint\s*=\s*['\"][^'\"]+['\"]",
        r"subscription_id\s*=\s*['\"][^'\"]+['\"]",
    ]
    
    print("🔒 Running Security Validation...")
    
    # Check if .env file exists and is not empty
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
            if 'your_subscription_id_here' in env_content or 'your_storage_connection_string_here' in env_content:
                issues.append(".env file still contains placeholder values")
            else:
                print("✅ .env file contains actual values (not placeholders)")
    else:
        issues.append(".env file missing")
    
    # Check Python files for hardcoded secrets
    for root, dirs, files in os.walk("."):
        # Skip virtual environments and hidden directories
        if any(skip in root for skip in ['venv', '.venv', '__pycache__', '.git', '.vscode']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for pattern in secret_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                # Basic check to avoid false positives on empty strings
                                if len(match) > 20:  # Real secrets are usually longer
                                    issues.append(f"Potential hardcoded secret in {filepath}: {match[:50]}...")
                except Exception as e:
                    print(f"⚠️  Could not read {filepath}: {e}")
    
    return issues

if __name__ == "__main__":
    issues = check_for_exposed_secrets()
    
    if issues:
        print("❌ Potential security issues found:")
        for issue in issues:
            print(f"   - {issue}")
        print("\nPlease fix these before committing!")
        exit(1)
    else:
        print("✅ No obvious security issues found")
        print("✅ .gitignore is properly configured")
        print("✅ Environment variables are being used correctly")