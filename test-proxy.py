#!/usr/bin/env python3
"""
Test script for Coplay GLM Proxy
"""

import asyncio
import aiohttp
import json

async def test_proxy():
    """Test the proxy server endpoints"""
    
    proxy_url = "http://localhost:8080"
    
    print("Testing Coplay GLM Proxy...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{proxy_url}/health") as response:
                if response.status == 200:
                    health_data = await response.json()
                    print("✓ Health check passed:")
                    print(f"  Status: {health_data.get('status')}")
                    print(f"  Service: {health_data.get('service')}")
                    print(f"  Target API: {health_data.get('target_api')}")
                    print(f"  Model: {health_data.get('model')}")
                else:
                    print(f"✗ Health check failed: {response.status}")
                    return False
    except Exception as e:
        print(f"✗ Could not connect to proxy server: {e}")
        print("Make sure the proxy server is running first!")
        return False
    
    # Test models endpoint
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{proxy_url}/v1/models") as response:
                if response.status == 200:
                    models_data = await response.json()
                    print("\n✓ Models endpoint passed:")
                    print(f"  Object: {models_data.get('object')}")
                    print(f"  Models: {[m['id'] for m in models_data.get('data', [])]}")
                else:
                    print(f"✗ Models endpoint failed: {response.status}")
                    return False
    except Exception as e:
        print(f"✗ Models endpoint error: {e}")
        return False
    
    # Test chat completions endpoint (mock request)
    try:
        test_request = {
            "model": "glm-4.6",
            "messages": [
                {"role": "user", "content": "Hello, this is a test message."}
            ],
            "max_tokens": 50
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{proxy_url}/v1/chat/completions",
                json=test_request,
                headers={"Authorization": "Bearer df92b900aac94a60b659c341d9054464.PkbniOA3fCgPCtlu"}
            ) as response:
                response_text = await response.text()
                print(f"\n✓ Chat completions test:")
                print(f"  Status: {response.status}")
                
                if response.status == 200:
                    try:
                        response_data = json.loads(response_text)
                        print(f"  Response ID: {response_data.get('id')}")
                        print(f"  Model: {response_data.get('model')}")
                        print(f"  Choices: {len(response_data.get('choices', []))}")
                        if response_data.get('choices'):
                            content = response_data['choices'][0].get('message', {}).get('content', 'No content')
                            print(f"  Content preview: {content[:100]}...")
                    except json.JSONDecodeError:
                        print(f"  Raw response: {response_text[:200]}...")
                else:
                    print(f"  Error response: {response_text}")
                    return False
                    
    except Exception as e:
        print(f"✗ Chat completions test error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! The proxy server is working correctly.")
    print("\nNext steps:")
    print("1. Keep the proxy server running")
    print("2. Configure Coplay with the settings shown above")
    print("3. Start using Coplay with your GLM API!")
    
    return True

if __name__ == "__main__":
    print("Note: Make sure the proxy server is running before running this test.")
    print("Start it with: python coplay-glm-proxy.py")
    print()
    
    try:
        result = asyncio.run(test_proxy())
        if not result:
            print("\n❌ Some tests failed. Check the proxy server logs.")
    except KeyboardInterrupt:
        print("\nTest cancelled.")
    except Exception as e:
        print(f"\nTest error: {e}")
