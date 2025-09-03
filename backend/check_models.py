#!/usr/bin/env python3
"""
Check available GROQ models
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)

from groq import Groq

def check_models():
    """Check available GROQ models"""
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found")
        return
    
    try:
        client = Groq(api_key=groq_api_key)
        
        # Try some common model names
        common_models = [
            "llama3.1-8b",
            "llama3.1-70b", 
            "llama3.1-405b",
            "mixtral-8x7b-32768",
            "gemma-7b-it",
            "llama3.1-8b-8192",
            "llama3.1-70b-8192"
        ]
        
        print("🔍 Testing available GROQ models...")
        print("=" * 50)
        
        working_models = []
        
        for model in common_models:
            try:
                # Try a simple completion to test if model works
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10
                )
                print(f"✅ {model} - WORKING")
                working_models.append(model)
            except Exception as e:
                error_msg = str(e)
                if "model_not_found" in error_msg:
                    print(f"❌ {model} - Not found")
                elif "decommissioned" in error_msg:
                    print(f"⚠️  {model} - Decommissioned")
                else:
                    print(f"❌ {model} - Error: {error_msg[:100]}...")
        
        print("\n" + "=" * 50)
        if working_models:
            print(f"🎉 Found {len(working_models)} working models:")
            for model in working_models:
                print(f"   • {model}")
        else:
            print("❌ No working models found")
            
    except Exception as e:
        print(f"❌ Error connecting to GROQ: {e}")

if __name__ == "__main__":
    check_models()
