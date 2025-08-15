#!/usr/bin/env python3
"""
Simple test script to check backend functionality
"""

import requests
import json

BACKEND_URL = "https://onemoretime-1u2v.onrender.com"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        print("Health Check Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Health check failed: {e}")
        return None

def test_root():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/")
        print("\nRoot Endpoint Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return None

def test_ask(question="What is your advice on starting a business?", personality="naval"):
    """Test the ask endpoint"""
    try:
        payload = {
            "question": question,
            "personality": personality
        }
        response = requests.post(f"{BACKEND_URL}/ask", json=payload)
        print(f"\nAsk Endpoint Response (personality: {personality}):")
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result.get('status')}")
            print(f"Answer: {result.get('answer', '')[:200]}...")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Ask endpoint failed: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testing Backend...")
    print("=" * 50)
    
    # Test health
    health = test_health()
    
    # Test root
    root = test_root()
    
    # Test ask if model is initialized
    if health and health.get("model_initialized"):
        print("\n✅ Model is initialized, testing ask endpoint...")
        test_ask()
    else:
        print("\n❌ Model is not initialized yet. Please check the backend logs.") 