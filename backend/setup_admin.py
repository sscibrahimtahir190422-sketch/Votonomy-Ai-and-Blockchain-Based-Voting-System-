#!/usr/bin/env python3
"""
Interactive admin email update script.
"""

import os
import sys
from pathlib import Path
from werkzeug.security import generate_password_hash

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("=" * 60)
    print("ADMIN EMAIL UPDATE TOOL")
    print("=" * 60)
    
    try:
        from app import app, db
        from models import Admin
        print("✅ Successfully imported database modules\n")
    except Exception as e:
        print(f"❌ Error importing modules: {e}")
        return
    
    old_email = "IbrahimTahir1144@yahoo.com"
    new_email = "ssc.ibrahimtahir.190422@gmail.com"
    
    with app.app_context():
        # Check if database is initialized
        try:
            admin_count = Admin.query.count()
            print(f"📊 Database initialized")
            print(f"   Total admin accounts: {admin_count}\n")
        except Exception as e:
            print(f"⚠️  Database error: {e}")
            print("   Creating database tables...\n")
            db.create_all()
        
        # List all existing admins
        print("📋 Existing Admin Accounts:")
        all_admins = Admin.query.all()
        if all_admins:
            for idx, admin in enumerate(all_admins, 1):
                print(f"   {idx}. Email: {admin.email}")
        else:
            print("   None found\n")
        
        print()
        
        # Check for old email
        old_admin = Admin.query.filter_by(email=old_email).first()
        
        # Check for new email
        new_admin = Admin.query.filter_by(email=new_email).first()
        
        if old_admin:
            print(f"🔄 Found admin with old email: {old_email}")
            print(f"   Updating to new email: {new_email}\n")
            old_admin.email = new_email
            db.session.commit()
            print(f"✅ Email updated successfully!")
            
        elif new_admin:
            print(f"✅ Admin already has the new email: {new_email}")
            print(f"   No action needed.\n")
            
        else:
            print(f"⚠️  No admin found with either email address")
            print(f"   Old: {old_email}")
            print(f"   New: {new_email}\n")
            
            # Ask if user wants to create a new admin
            response = input("Would you like to create a new admin with the new email? (y/n): ").strip().lower()
            if response == 'y':
                password = input("Enter admin password: ").strip()
                if password:
                    password_hash = generate_password_hash(password)
                    new_admin_obj = Admin(email=new_email, password_hash=password_hash)
                    db.session.add(new_admin_obj)
                    db.session.commit()
                    print(f"✅ New admin created with email: {new_email}\n")
                else:
                    print("❌ Password cannot be empty\n")
        
        # Final verification
        print("=" * 60)
        print("FINAL STATUS:")
        print("=" * 60)
        final_admin = Admin.query.filter_by(email=new_email).first()
        if final_admin:
            print(f"✅ Admin account ready for login:")
            print(f"   Email: {new_email}")
            print(f"   Status: Ready to login\n")
        else:
            print(f"❌ No admin account found with email: {new_email}\n")

if __name__ == "__main__":
    main()
