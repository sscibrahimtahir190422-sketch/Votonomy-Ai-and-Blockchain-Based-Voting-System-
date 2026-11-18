#!/usr/bin/env python3
"""Direct candidate addition to database"""

import os
import sys

# Set up path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import after setting path
from app import app, db
from models import Candidate

def main():
    candidates_data = [
        ('Malik Taimoor Masood', 'I-10-PM-1'),
        ('Sami Ullah Butt', 'I-10-MNA-1'),
        ('Zeeshan Kayani', 'I-10-MPA-1'),
        ('Mujahid Ali Khan', 'I-10-PM-2'),
    ]
    
    with app.app_context():
        print("Adding candidates...\n")
        
        for name, candidate_id in candidates_data:
            # Check if exists
            existing = Candidate.query.filter_by(candidate_id=candidate_id).first()
            
            if existing:
                print(f"✓ {name} ({candidate_id}) - Already exists")
            else:
                candidate = Candidate(
                    candidate_name=name,
                    candidate_id=candidate_id,
                    votes=0
                )
                db.session.add(candidate)
                print(f"✓ {name} ({candidate_id}) - Added")
        
        db.session.commit()
        print("\n✅ All candidates processed!")

if __name__ == '__main__':
    main()
