"""
Script to update admin password in the database.
Usage: python update_admin_password.py
"""

import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

def update_password():
    db_path = Path(__file__).parent / "instance" / "votonomy.db"
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        # Get the new password
        new_password = "corolla950@"
        
        # Hash the password
        password_hash = generate_password_hash(new_password)
        
        print("🔐 Updating admin password...\n")
        
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get current admin info
        cursor.execute("SELECT id, email FROM admin LIMIT 1")
        admin = cursor.fetchone()
        
        if not admin:
            print("❌ No admin found in database")
            return False
        
        admin_id, email = admin
        print(f"📊 Admin found:")
        print(f"   ID: {admin_id}")
        print(f"   Email: {email}\n")
        
        # Update password
        cursor.execute(
            "UPDATE admin SET password_hash = ? WHERE id = ?",
            (password_hash, admin_id)
        )
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ Password updated successfully!")
            print(f"\n🔑 Login Credentials:")
            print(f"   Email: {email}")
            print(f"   Password: {new_password}")
            print(f"\n⚠️  Keep this password secure and do NOT share it!\n")
            return True
        else:
            print("❌ Failed to update password")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = update_password()
    exit(0 if success else 1)
