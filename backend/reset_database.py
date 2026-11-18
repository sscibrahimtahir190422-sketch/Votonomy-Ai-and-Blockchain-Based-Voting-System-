#!/usr/bin/env python3
"""
Database Reset Script
Clears all voting data and creates fresh database
Keeps voter and candidate master data if needed
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def reset_database(keep_voters=False, keep_candidates=False):
    """
    Reset database - clear all voting records
    
    Args:
        keep_voters: If True, preserves voter master data
        keep_candidates: If True, preserves candidate master data
    """
    try:
        from app import app, db
        from models import (
            Vote, BehaviorLog, FraudAlert, IPCluster, 
            PreSurvey, PreSurveyNLP, SentimentAnalytics, 
            Complaint, Voter, Candidate, Admin
        )
        
        print("=" * 70)
        print("🗑️  DATABASE RESET UTILITY")
        print("=" * 70)
        
        with app.app_context():
            print("\n📊 Current Database Status:")
            print(f"   Votes: {Vote.query.count()}")
            print(f"   Behavior Logs: {BehaviorLog.query.count()}")
            print(f"   Fraud Alerts: {FraudAlert.query.count()}")
            print(f"   IP Clusters: {IPCluster.query.count()}")
            print(f"   Pre-Surveys: {PreSurvey.query.count()}")
            print(f"   Complaints: {Complaint.query.count()}")
            print(f"   Voters: {Voter.query.count()}")
            print(f"   Candidates: {Candidate.query.count()}")
            print(f"   Admins: {Admin.query.count()}")
            
            print("\n🧹 Clearing voting records...")
            
            # Clear all voting-related data
            Vote.query.delete()
            print("   ✅ Cleared all votes")
            
            BehaviorLog.query.delete()
            print("   ✅ Cleared all behavior logs")
            
            FraudAlert.query.delete()
            print("   ✅ Cleared all fraud alerts")
            
            IPCluster.query.delete()
            print("   ✅ Cleared all IP clusters")
            
            PreSurvey.query.delete()
            print("   ✅ Cleared all pre-surveys (structured)")
            
            PreSurveyNLP.query.delete()
            print("   ✅ Cleared all pre-surveys (NLP/old)")
            
            SentimentAnalytics.query.delete()
            print("   ✅ Cleared sentiment analytics")
            
            Complaint.query.delete()
            print("   ✅ Cleared all complaints")
            
            # Optional: Clear voters and candidates
            if not keep_voters:
                Voter.query.delete()
                print("   ✅ Cleared all voters")
            else:
                print("   ℹ️  Kept voter master data")
            
            if not keep_candidates:
                Candidate.query.delete()
                print("   ✅ Cleared all candidates")
            else:
                print("   ℹ️  Kept candidate master data")
            
            # Commit all changes
            db.session.commit()
            
            print("\n✅ DATABASE RESET COMPLETE!")
            print("\n📊 New Database Status:")
            print(f"   Votes: {Vote.query.count()}")
            print(f"   Behavior Logs: {BehaviorLog.query.count()}")
            print(f"   Fraud Alerts: {FraudAlert.query.count()}")
            print(f"   IP Clusters: {IPCluster.query.count()}")
            print(f"   Pre-Surveys: {PreSurvey.query.count()}")
            print(f"   Complaints: {Complaint.query.count()}")
            print(f"   Voters: {Voter.query.count()}")
            print(f"   Candidates: {Candidate.query.count()}")
            print(f"   Admins: {Admin.query.count()}")
            
            print("\n" + "=" * 70)
            print("🚀 Database is ready for fresh voting!")
            print("=" * 70)
            
    except Exception as e:
        print(f"\n❌ Error during reset: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Reset Votonomy database")
    parser.add_argument("--keep-voters", action="store_true", 
                       help="Preserve voter master data")
    parser.add_argument("--keep-candidates", action="store_true", 
                       help="Preserve candidate master data")
    parser.add_argument("--confirm", action="store_true",
                       help="Skip confirmation prompt (auto-confirm)")
    
    args = parser.parse_args()
    
    if args.confirm:
        confirm = "YES"
    else:
        try:
            confirm = input("\nWARNING: This will DELETE all voting records!\n" + 
                           "Continue? (type 'YES' to confirm): ").strip()
        except UnicodeEncodeError:
            # Handle encoding issues on Windows
            import sys
            sys.stdout.write("\nWARNING: This will DELETE all voting records!\n")
            sys.stdout.write("Continue? (type 'YES' to confirm): ")
            sys.stdout.flush()
            confirm = sys.stdin.readline().strip()
    
    if confirm.upper() == "YES":
        reset_database(
            keep_voters=args.keep_voters,
            keep_candidates=args.keep_candidates
        )
    else:
        print("Reset cancelled.")
        sys.exit(1)
