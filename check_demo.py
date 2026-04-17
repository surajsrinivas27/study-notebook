#!/usr/bin/env python3
"""
Pre-Demo Checklist Script
Run this to verify everything is working before your presentation
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def check_backend():
    """Check if backend is running"""
    print(f"{Colors.BOLD}Checking Backend...{Colors.END}")
    try:
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.status_code == 200:
            print(f"{Colors.GREEN}✓ Backend is running on http://localhost:8000{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}✗ Backend returned status {response.status_code}{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}✗ Backend not responding: {e}{Colors.END}")
        return False

def check_frontend():
    """Check if frontend is running"""
    print(f"{Colors.BOLD}Checking Frontend...{Colors.END}")
    try:
        response = requests.get('http://localhost:5173', timeout=2)
        if response.status_code == 200:
            print(f"{Colors.GREEN}✓ Frontend is running on http://localhost:5173{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}✗ Frontend returned status {response.status_code}{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}✗ Frontend not responding: {e}{Colors.END}")
        return False

def check_files():
    """Check if all necessary files exist"""
    print(f"{Colors.BOLD}Checking File Structure...{Colors.END}")
    
    required_files = [
        'backend/main.py',
        'backend/requirements.txt',
        'frontend/package.json',
        'frontend/vite.config.js',
        'frontend/src/App.jsx',
        'frontend/src/pages/Login.jsx',
        'frontend/src/pages/Chat.jsx',
        'HACKATHON_SETUP.md',
        'PROJECT_SUMMARY.md',
    ]
    
    all_good = True
    for file in required_files:
        if Path(file).exists():
            print(f"{Colors.GREEN}✓ {file}{Colors.END}")
        else:
            print(f"{Colors.RED}✗ {file} - MISSING!{Colors.END}")
            all_good = False
    
    return all_good

def check_api_endpoints():
    """Check if all API endpoints are working"""
    print(f"{Colors.BOLD}Checking API Endpoints...{Colors.END}")
    
    endpoints = [
        ('GET', '/health'),
        ('GET', '/models'),
    ]
    
    all_good = True
    for method, endpoint in endpoints:
        try:
            if method == 'GET':
                response = requests.get(f'http://localhost:8000{endpoint}', timeout=2)
            if response.status_code in [200, 401]:
                print(f"{Colors.GREEN}✓ {method} {endpoint}{Colors.END}")
            else:
                print(f"{Colors.RED}✗ {method} {endpoint} - Status {response.status_code}{Colors.END}")
                all_good = False
        except Exception as e:
            print(f"{Colors.RED}✗ {method} {endpoint} - {e}{Colors.END}")
            all_good = False
    
    return all_good

def check_features():
    """Check if key features are mentioned in the code"""
    print(f"{Colors.BOLD}Checking Features Implementation...{Colors.END}")
    
    features = {
        'Login': 'frontend/src/pages/Login.jsx',
        'Memory': 'frontend/src/pages/Chat.jsx',
        'Voice': 'frontend/src/utils/voice.js',
        'Typing Animation': 'frontend/src/components/TypingAnimation.jsx',
        'Chat Window': 'frontend/src/components/ChatWindow.jsx',
        'Quiz': 'backend/main.py',
    }
    
    all_good = True
    for feature, file in features.items():
        if Path(file).exists() and os.path.getsize(file) > 100:
            print(f"{Colors.GREEN}✓ {feature} ({file}){Colors.END}")
        else:
            print(f"{Colors.RED}✗ {feature} ({file}) - MISSING or EMPTY!{Colors.END}")
            all_good = False
    
    return all_good

def print_instructions():
    """Print setup instructions if something is missing"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}Setup Instructions:{Colors.END}")
    print(f"""
{Colors.YELLOW}If services are not running, follow these steps:{Colors.END}

{Colors.BOLD}Terminal 1 - Backend:{Colors.END}
    cd backend
    python -m venv venv
    venv\\Scripts\\activate  (Windows) or source venv/bin/activate
    pip install -r requirements.txt
    python main.py

{Colors.BOLD}Terminal 2 - Frontend:{Colors.END}
    cd frontend
    npm install
    npm run dev

{Colors.BOLD}Or use one-click launch:{Colors.END}
    Windows:   double-click START_ALL.bat
    Mac/Linux: bash START_ALL.sh
    """)

def print_summary(results):
    """Print final summary"""
    print_header("Pre-Demo Checklist Results")
    
    passed = sum(results.values())
    total = len(results)
    percentage = (passed / total) * 100
    
    for check, result in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if result else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"{status} - {check}")
    
    print(f"\n{Colors.BOLD}Overall:{Colors.END} {passed}/{total} checks passed ({percentage:.0f}%)")
    
    if percentage == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All systems go! You're ready to demo! 🎉{Colors.END}\n")
        return True
    elif percentage >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Most systems ready, but fix the failures above{Colors.END}\n")
        return False
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Please fix the failed checks before demoing{Colors.END}\n")
        return False

def main():
    print_header("Mini Notebook LLM - Pre-Demo Verification")
    
    results = {
        'Backend Running': check_backend(),
        'Frontend Running': check_frontend(),
        'File Structure': check_files(),
        'API Endpoints': check_api_endpoints(),
        'Features Implemented': check_features(),
    }
    
    success = print_summary(results)
    
    if not success:
        print_instructions()
    
    print(f"{Colors.BOLD}Documentation Files:{Colors.END}")
    print(f"  📄 HACKATHON_SETUP.md  - Complete setup guide")
    print(f"  📄 PROJECT_SUMMARY.md  - Project overview")
    print(f"  📄 DEMO_GUIDE.md       - Demo talking points")
    print(f"  📄 FRONTEND_READY.md   - Frontend details")
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
