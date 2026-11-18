"""Quick script to verify candidates in database"""
from app import app, db
from models import Candidate

with app.app_context():
    all_candidates = Candidate.query.all()
    print(f"\n📊 Total Candidates in Database: {len(all_candidates)}\n")
    
    for candidate in all_candidates:
        print(f"  ID: {candidate.candidate_id}")
        print(f"  Name: {candidate.candidate_name}")
        print(f"  Votes: {candidate.votes}\n")
