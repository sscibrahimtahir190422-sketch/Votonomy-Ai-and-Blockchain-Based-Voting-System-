#!/usr/bin/env python3
"""
Simple script to check and update admin email.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app import app, db
    from models import Admin
    
    print("✅ Imports successful")
    
    with app.app_context():
        print("\n📋 Checking Admin records in database...")
        
        all_admins = Admin.query.all()
        print(f"Total admins: {len(all_admins)}")
        
        for admin in all_admins:
            print(f"\n  Email: {admin.email}")
            print(f"  ID: {admin.id}")
        
        # Try to update
        old_email = "IbrahimTahir1144@yahoo.com"
        new_email = "ssc.ibrahimtahir.190422@gmail.com"
        
        admin = Admin.query.filter_by(email=old_email).first()
        
        if admin:
            print(f"\n🔄 Updating email...")
            admin.email = new_email
            db.session.commit()
            print(f"✅ Updated: {old_email} → {new_email}")
        else:
            print(f"\n⚠️  Admin with email '{old_email}' not found")
            print(f"   Will create/update admin with new email: {new_email}")
            
            # Check if new email already exists
            existing = Admin.query.filter_by(email=new_email).first()
            if existing:
                print(f"   Admin already exists with new email")
            else:
                print(f"   No admin with new email either")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
