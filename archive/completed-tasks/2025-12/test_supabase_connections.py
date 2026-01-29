#!/usr/bin/env python3
"""
Test Supabase connections and configurations
"""

import os
import subprocess

def run_command(cmd, description):
    """Run a command and return success/failure"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ {description}: SUCCESS")
            return True
        else:
            print(f"❌ {description}: FAILED")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {e}")
        return False

def main():
    print("🔗 Testing Supabase Connections")
    print("=" * 40)
    
    # Check environment variables
    supabase_url = os.getenv('PUBLIC_SUPABASE_URL')
    anon_key = os.getenv('PUBLIC_SUPABASE_ANON_KEY') 
    service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    print(f"URL configured: {'✅' if supabase_url else '❌'}")
    print(f"Anon key configured: {'✅' if anon_key else '❌'}")
    print(f"Service key configured: {'✅' if service_key and service_key != 'your_service_role_key_here' else '❌'}")
    print()
    
    # Test basic connectivity
    if supabase_url and anon_key:
        # Test with curl
        url = f"{supabase_url}/rest/v1/listings?select=count"
        cmd = f"curl -s '{url}' -H 'apikey: {anon_key}' -H 'Authorization: Bearer {anon_key}'"
        run_command(cmd, "API connectivity")
    
    # Test Supabase CLI
    run_command("supabase --version", "Supabase CLI")
    run_command("supabase projects list", "CLI project access")
    
    # Test Python client (if available)
    try:
        import supabase
        print("✅ Supabase Python client: Available")
    except ImportError:
        print("❌ Supabase Python client: Not installed")
    
    print()
    print("📋 Next Steps:")
    if not service_key or service_key == 'your_service_role_key_here':
        print("1. Get service_role key from dashboard")
        print("2. Run: ./update_service_key.sh [key]")
        print("3. Run: python3 run_supabase_diagnostics.py")
    else:
        print("1. Run diagnostics: python3 run_supabase_diagnostics.py")
        print("2. Check issues: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/issues")

if __name__ == "__main__":
    main()
