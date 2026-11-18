"""
Direct database migration to update admin email.
This can be run with: python migrate_admin_email.py
"""

import sqlite3
import os
from pathlib import Path

def migrate():
    db_path = Path(__file__).parent / "instance" / "votonomy.db"
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        old_email = "ibrahimtahir1144@yahoo.com"  # Must match case in database
        new_email = "ssc.ibrahimtahir.190422@gmail.com"
        
        print("🔍 Checking Admin table...\n")
        
        # Get all admins
        cursor.execute("SELECT id, email FROM admin")
        admins = cursor.fetchall()
        
        if not admins:
            print("⚠️  No admin records found in database")
            return False
        
        print(f"📊 Found {len(admins)} admin record(s):")
        for admin_id, email in admins:
            print(f"   - ID: {admin_id}, Email: {email}")
        
        print()
        
        # Update email
        cursor.execute(
            "UPDATE admin SET email = ? WHERE email = ?",
            (new_email, old_email)
        )
        
        if cursor.rowcount > 0:
            print(f"✅ Updated {cursor.rowcount} record(s)")
            print(f"   {old_email} → {new_email}")
            conn.commit()
            print("\n✅ Changes saved to database")
            return True
        else:
            print(f"⚠️  No records matched email: {old_email}")
            print(f"   Existing admin emails remain unchanged")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = migrate()
    exit(0 if success else 1)
