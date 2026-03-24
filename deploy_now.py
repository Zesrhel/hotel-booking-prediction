#!/usr/bin/env python3
"""
One-Click Deployment Script for Hotel Booking Prediction Model
Deploys to GitHub with minimal user input
"""

import os
import sys
import subprocess
from pathlib import Path


def run_cmd(cmd, check=True):
    """Run command and return result."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    return True


def main():
    print("\n" + "="*70)
    print("HOTEL BOOKING PREDICTION - ONE-CLICK DEPLOYMENT")
    print("="*70 + "\n")
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found. Please run from project root.")
        sys.exit(1)
    
    print("✓ Project files found")
    
    # Get repo URL from user
    print("\nTo complete deployment, you need your GitHub repo URL.")
    print("Format: https://github.com/USERNAME/hotel-booking-prediction.git\n")
    
    repo_url = input("Enter your GitHub repo HTTPS URL: ").strip()
    
    if not repo_url or "github.com" not in repo_url:
        print("❌ Invalid URL format.")
        sys.exit(1)
    
    print("\n" + "-"*70)
    print("DEPLOYING TO GITHUB...")
    print("-"*70 + "\n")
    
    # Add remote
    print("1. Adding GitHub remote...")
    run_cmd(f"git remote remove origin 2>nul", check=False)
    if not run_cmd(f'git remote add origin "{repo_url}"'):
        print("❌ Failed to add remote")
        sys.exit(1)
    print("   ✓ Remote added")
    
    # Set main branch
    print("2. Setting main branch...")
    run_cmd("git branch -M main")
    print("   ✓ Branch set to main")
    
    # Push to GitHub
    print("3. Pushing code to GitHub (this may take a moment)...")
    if not run_cmd("git push -u origin main"):
        print("❌ Push failed. Check your credentials and try again.")
        print("   Tip: Use Personal Access Token instead of password for HTTPS")
        sys.exit(1)
    print("   ✓ Code pushed successfully!")
    
    print("\n" + "="*70)
    print("✅ GITHUB DEPLOYMENT COMPLETE!")
    print("="*70)
    
    print("\n🚀 NEXT STEP: Deploy to Streamlit Cloud\n")
    print("1. Go to: https://streamlit.io/cloud")
    print("2. Click 'New app'")
    print("3. Select:")
    print("   - Repository: hotel-booking-prediction")
    print("   - Branch: main")
    print("   - Main file: app.py")
    print("4. Click 'Deploy'")
    print("5. Wait 2-3 minutes...")
    print("\n📱 Your live app: https://hotel-booking-prediction.streamlit.app")
    print("\nGitHub repo: " + repo_url.replace(".git", ""))
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
