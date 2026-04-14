#!/usr/bin/env python3
"""
Database connection test script.
Run this to verify your database configuration is working.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.db.utils import check_database_health
import json

def main():
    print("🔍 Testing database connection...")
    print("=" * 50)

    health = check_database_health()

    print(f"📡 Connection: {'✅ SUCCESS' if health['connection'] else '❌ FAILED'}")

    db_info = health['database_info']
    print(f"🏗️  Database: {db_info['database']}")
    print(f"🌐 Host: {db_info['host']}:{db_info['port']}")
    print(f"👤 User: {db_info['user']}")

    if health.get('tables_exist'):
        print(f"📊 Tables: ✅ ({health.get('table_count', 0)} tables found)")
    else:
        print("📊 Tables: ⚠️  No tables found (run migrations)")

    if "error" in health:
        print(f"❌ Error: {health['error']}")
        return 1

    print("=" * 50)
    if health['connection']:
        print("🎉 Database connection is working!")
        return 0
    else:
        print("💥 Database connection failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())