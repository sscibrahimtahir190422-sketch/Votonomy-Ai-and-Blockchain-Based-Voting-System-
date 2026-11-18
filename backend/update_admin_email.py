#!/usr/bin/env python3
"""
Script to update admin email in the database.
This script updates the admin email from the old address to the new one.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app import app, db
from models import Admin

def update_admin_email():
    """Update admin email in the database."""
    old_email = "IbrahimTahir1144@yahoo.com"
    new_email = "ssc.ibrahimtahir.190422@gmail.com"
    
    with app.app_context():
        # Check if admin with old email exists
        admin = Admin.query.filter_by(email=old_email).first()
        
        if not admin:
            print(f"❌ No admin found with email: {old_email}")
            print("\nExisting admins in database:")
            all_admins = Admin.query.all()
            if all_admins:
                for a in all_admins:
                    print(f"  - {a.email}")
            else:
                print("  - No admins found in database")
            return False
        
        # Update the email
        admin.email = new_email
        db.session.commit()
        
        print(f"✅ Admin email updated successfully!")
        print(f"   Old email: {old_email}")
        print(f"   New email: {new_email}")
        return True

if __name__ == "__main__":
    success = update_admin_email()
    sys.exit(0 if success else 1)
