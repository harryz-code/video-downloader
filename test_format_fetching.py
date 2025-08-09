#!/usr/bin/env python3
"""
Test script to verify optimized format fetching speed
"""

import time
import requests
import json

def test_format_fetching():
    """Test the format fetching API endpoint"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - short video
    
    print("🚀 Testing optimized format fetching...")
    print(f"📹 Testing with: {url}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            'http://localhost:8080/api/list_formats',
            json={'url': url},
            timeout=15  # 15 second timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Response time: {duration:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ Success! Found {len(result['formats'])} formats")
                print(f"📺 Video title: {result['title']}")
                
                for fmt in result['formats']:
                    print(f"   - {fmt['quality']} ({fmt['ext']}) - {fmt['size']}")
                
                if duration < 5:
                    print("🎉 Excellent! Format fetching is under 5 seconds!")
                elif duration < 10:
                    print("👍 Good! Format fetching is under 10 seconds!")
                else:
                    print("⚠️  Format fetching is still taking too long")
                    
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout! Format fetching took too long")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_format_fetching()
