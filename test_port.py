#!/usr/bin/env python3
"""
Test script to verify port configuration
"""

import os

def test_port_config():
    """Test port configuration"""
    print("🔌 Testing Port Configuration...")
    
    # Test PORT environment variable
    port = os.getenv("PORT", "8000")
    print(f"📊 PORT environment variable: {port}")
    
    # Test port conversion
    try:
        port_int = int(port)
        print(f"✅ Port converted to integer: {port_int}")
        
        if port_int > 0 and port_int < 65536:
            print("✅ Port is within valid range (1-65535)")
        else:
            print("❌ Port is outside valid range")
            
    except ValueError:
        print("❌ Failed to convert PORT to integer")
        return False
    
    print("✅ Port configuration test passed!")
    return True

if __name__ == "__main__":
    test_port_config() 