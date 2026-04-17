"""
Test script for Mini Notebook LLM Backend
Run this to verify the API is working correctly.
"""
import asyncio
import httpx
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

async def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing Health Check...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"   Response: {json.dumps(data, indent=2)}")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_chat():
    """Test chat endpoint"""
    print("\n💬 Testing Chat Endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "message": "What is Python in 2 sentences?",
                "temperature": 0.7,
                "max_tokens": 200
            }
            response = await client.post(f"{BASE_URL}/chat", json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"   Query: {payload['message']}")
                print(f"   Response: {data['response']}")
                print(f"   Tokens Used: {data['tokens_used']}")
                return True
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_code_complete():
    """Test code completion endpoint"""
    print("\n📝 Testing Code Completion...")
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "message": "def greet(name)",
                "temperature": 0.5,
                "max_tokens": 150
            }
            response = await client.post(f"{BASE_URL}/code-complete", json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"   Input: {payload['message']}")
                print(f"   Suggestion:\n{data['completion']}")
                return True
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_explain():
    """Test explanation endpoint"""
    print("\n📚 Testing Code Explanation...")
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "message": "What are list comprehensions in Python?",
                "temperature": 0.7,
                "max_tokens": 300
            }
            response = await client.post(f"{BASE_URL}/explain", json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"   Question: {payload['message']}")
                print(f"   Explanation:\n{data['response']}")
                return True
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_models():
    """Test models listing endpoint"""
    print("\n🤖 Testing Models List...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/models", timeout=30.0)
            if response.status_code == 200:
                data = response.json()
                models_count = len(data.get("data", []))
                print(f"✅ Status: {response.status_code}")
                print(f"   Available models: {models_count}")
                if models_count > 0:
                    print(f"   Sample models:")
                    for model in data["data"][:3]:
                        print(f"     - {model.get('id', 'Unknown')}")
                return True
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Mini Notebook LLM Backend - Test Suite")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    
    results = []
    
    # Run tests
    results.append(("Health Check", await test_health()))
    results.append(("Chat", await test_chat()))
    results.append(("Code Completion", await test_code_complete()))
    results.append(("Code Explanation", await test_explain()))
    results.append(("Models List", await test_models()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your backend is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")

if __name__ == "__main__":
    print("\n⚠️  Make sure the backend is running before executing tests!")
    print("   Run: python main.py\n")
    
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("\n💡 Tip: Is the backend server running? Run: python main.py")
