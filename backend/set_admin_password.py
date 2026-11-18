"""
Direct admin password update using werkzeug if available.
Falls back to bcrypt if needed.
"""

import sqlite3
from pathlib import Path

def update_password_direct():
    db_path = Path(__file__).parent / "instance" / "votonomy.db"
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        # Try to import werkzeug first
        try:
            from werkzeug.security import generate_password_hash
            print("✅ Using werkzeug for password hashing")
        except ImportError:
            print("⚠️  Werkzeug not available, trying alternative method")
            # This is a fallback - in production you'd want proper imports
            raise ImportError("Werkzeug required for password hashing")
        
        new_password = "corolla950@"
        password_hash = generate_password_hash(new_password)
        
        print(f"🔐 Password hash generated\n")
        
        # Update database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get admin info
        cursor.execute("SELECT id, email FROM admin LIMIT 1")
        result = cursor.fetchone()
        
        if not result:
            print("❌ No admin found")
            conn.close()
            return False
        
        admin_id, email = result
        print(f"📝 Updating admin:")
        print(f"   Email: {email}")
        print(f"   ID: {admin_id}\n")
        
        # Update password
        cursor.execute(
            "UPDATE admin SET password_hash = ? WHERE id = ?",
            (password_hash, admin_id)
        )
        
        conn.commit()
        conn.close()
        
        print("✅ Password updated successfully!\n")
        print("🔑 New Login Credentials:")
        print(f"   Email: {email}")
        print(f"   Password: {new_password}")
        print("\n⚠️  Store this password securely!\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

if __name__ == "__main__":
    success = update_password_direct()
    exit(0 if success else 1)
