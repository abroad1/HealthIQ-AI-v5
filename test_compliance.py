#!/usr/bin/env python3
"""
Simple compliance test script
"""

import os
import sys

def main():
    print("🧪 Test Compliance Verification Report")
    print("=" * 50)
    
    # Check if TEST_LEDGER.md exists
    if os.path.exists("TEST_LEDGER.md"):
        print("✅ TEST_LEDGER.md exists")
        
        # Read content
        with open("TEST_LEDGER.md", "r") as f:
            content = f.read()
        
        # Check for required elements
        required_elements = [
            "Run Command",
            "Execution time", 
            "Coverage percentage",
            "Test counts",
            "Individual test methods"
        ]
        
        for element in required_elements:
            if element.lower() in content.lower():
                print(f"✅ {element} found")
            else:
                print(f"❌ {element} missing")
        
        # Check for test count format
        import re
        if re.search(r'\d+/\d+\s+tests', content):
            print("✅ Test count format found")
        else:
            print("❌ Test count format missing")
        
        # Check for run command format
        if re.search(r'python -m pytest.*-v', content):
            print("✅ Run command format found")
        else:
            print("❌ Run command format missing")
        
        # Check for coverage percentage
        if re.search(r'\d+%', content):
            print("✅ Coverage percentage found")
        else:
            print("❌ Coverage percentage missing")
        
        # Check for code blocks
        if "```bash" in content or "```powershell" in content:
            print("✅ Code blocks found")
        else:
            print("❌ Code blocks missing")
            
    else:
        print("❌ TEST_LEDGER.md does not exist")
    
    # Check test archive
    if os.path.exists("tests_archive"):
        print("✅ tests_archive directory exists")
    else:
        print("❌ tests_archive directory missing")
    
    # Check backend tests
    if os.path.exists("backend/tests"):
        print("✅ backend/tests directory exists")
    else:
        print("❌ backend/tests directory missing")
    
    # Check frontend tests
    if os.path.exists("frontend/tests"):
        print("✅ frontend/tests directory exists")
    else:
        print("❌ frontend/tests directory missing")

if __name__ == "__main__":
    main()
