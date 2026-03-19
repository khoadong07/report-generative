#!/usr/bin/env python3
"""
Test script to verify .env loading works correctly
"""

from pathlib import Path
from dotenv import load_dotenv
import os

def test_env_loading():
    """Test the new environment loading logic"""
    print("🔍 Testing environment loading...")
    
    # Try multiple locations for .env file
    env_paths = [
        Path(__file__).parent / '.env',  # Root directory
        Path('/app/.env'),  # Docker container path
        Path('.env'),  # Current directory
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"✅ Loaded environment from: {env_path.absolute()}")
            break
    else:
        load_dotenv()  # Fallback to default behavior
        print("⚠️ Using default .env loading")
    
    # Check if variables are loaded
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    
    print(f"API_KEY loaded: {'✅ Yes' if api_key else '❌ No'}")
    print(f"BASE_URL loaded: {'✅ Yes' if base_url else '❌ No'}")
    
    if api_key and base_url:
        print("🎉 Environment variables loaded successfully!")
        return True
    else:
        print("❌ Failed to load environment variables")
        return False

if __name__ == "__main__":
    test_env_loading()