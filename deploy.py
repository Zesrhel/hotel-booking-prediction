#!/usr/bin/env python3
"""
Hotel Booking Prediction - GitHub & Streamlit Deployment Automation Script

This script automates all 3 deployment steps:
1. GitHub Repository Setup (guides user)
2. Push Code to GitHub
3. Streamlit Cloud Deployment Instructions

Prerequisites:
- Git installed and configured
- GitHub account with SSH or HTTPS credentials set up
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        if check and result.returncode != 0:
            raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
        return result
    except Exception as e:
        raise RuntimeError(f"Error running command: {e}")


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_step(step_num, title):
    """Print a step header."""
    print(f"\n[Step {step_num}/3] {title}")
    print("-" * 80)


def step_1_github_setup():
    """Step 1: Guide user through GitHub repository creation."""
    print_step(1, "GitHub Repository Setup")
    
    print("""
IMPORTANT: You must create a GitHub repository FIRST.

To create your repository:
  1. Open: https://github.com/new
  2. Fill in these details:
     - Repository name: hotel-booking-prediction
     - Description: Hotel booking cancellation predictor with Streamlit
     - Visibility: PUBLIC (required for free Streamlit Cloud)
     - Add .gitignore: Python
  3. Click "Create repository"
  4. Copy the HTTPS URL from the "Quick setup" section

It will look like: https://github.com/YOUR_USERNAME/hotel-booking-prediction.git
    """)
    
    repo_url = input("Paste your repository HTTPS URL: ").strip()
    
    if not repo_url or "github.com" not in repo_url:
        print("ERROR: Invalid repository URL.")
        sys.exit(1)
    
    return repo_url


def step_2_push_code(repo_url):
    """Step 2: Push code to GitHub."""
    print_step(2, "Push Code to GitHub")
    
    project_root = Path("C:/Users/Acer-pc/Desktop/IT20/Predictive_Modeling_v3")
    
    if not (project_root / "app.py").exists():
        print(f"ERROR: Could not find app.py in {project_root}")
        sys.exit(1)
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="hotel-prediction-")
    print(f"Creating temporary directory: {temp_dir}")
    
    try:
        # Clone repository
        print("Cloning your GitHub repository...")
        result = run_command(f'git clone "{repo_url}" "{temp_dir}"', check=False)
        if result.returncode != 0:
            print(f"ERROR: Failed to clone repository.\n{result.stderr}")
            sys.exit(1)
        
        # Copy project files (excluding .git from source)
        print("Copying project files...")
        for item in project_root.iterdir():
            if item.name == ".git":
                continue
            dest = Path(temp_dir) / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
        
        # Git operations
        print("Staging files...")
        run_command("git add .", cwd=temp_dir)
        
        print("Creating commit...")
        commit_msg = """Initial commit: Hotel booking prediction with Streamlit web interface

- Trained Random Forest model with 89.38% accuracy and 0.9593 ROC-AUC
- Streamlit web app for real-time hotel cancellation predictions
- GitHub Actions CI/CD workflow for automated model retraining
- Complete documentation and deployment guides
- Dataset: 119,390 hotel booking records"""
        
        run_command(
            f'git commit -m "{commit_msg}"',
            cwd=temp_dir
        )
        
        print("Pushing to GitHub (this may take a minute)...")
        result = run_command("git push -u origin main", cwd=temp_dir, check=False)
        if result.returncode != 0:
            print(f"ERROR: Failed to push to GitHub.\n{result.stderr}")
            print("\nTroubleshooting:")
            print("  - Ensure Git is installed and configured")
            print("  - Verify GitHub credentials (Personal Access Token if using HTTPS)")
            print("  - Try: git config --global user.name 'Your Name'")
            print("  - Try: git config --global user.email 'your@email.com'")
            sys.exit(1)
        
        print("✓ Code pushed successfully!")
        
    finally:
        # Cleanup
        if Path(temp_dir).exists():
            print(f"Cleaning up temporary files...")
            shutil.rmtree(temp_dir)


def step_3_streamlit_deployment():
    """Step 3: Display Streamlit Cloud deployment instructions."""
    print_step(3, "Streamlit Cloud Deployment Instructions")
    
    print("""
SUCCESS! Your code is now on GitHub!

Next steps to deploy to Streamlit Cloud:

  1. Go to: https://streamlit.io/cloud
  2. Sign in with your GitHub account (or create one)
  3. Click "New app"
  4. Select:
     - GitHub account: (your GitHub username)
     - Repository: hotel-booking-prediction
     - Branch: main
     - Main file path: app.py
  5. Click "Deploy"
  6. Wait 2-3 minutes for deployment to complete
  7. Your live app will be at: https://hotel-booking-prediction.streamlit.app

Features:
  - Real-time hotel booking cancellation predictions
  - Adjustable decision threshold (0.05 - 0.95)
  - Input prediction features directly in the web interface
  - Automatic model retraining on GitHub commits (via GitHub Actions)

Troubleshooting:
  - If deployment fails, check Python version (3.11+) in Streamlit settings
  - Check GitHub Actions for model training logs
  - Ensure requirements.txt has all dependencies

Your model will automatically retrain whenever you push changes to GitHub!
    """)


def main():
    """Main execution flow."""
    print_header("Hotel Booking Prediction - GitHub & Streamlit Deployment")
    
    # Step 1: GitHub Repository Setup
    repo_url = step_1_github_setup()
    
    # Step 2: Push Code to GitHub
    step_2_push_code(repo_url)
    
    # Step 3: Streamlit Cloud Instructions
    step_3_streamlit_deployment()
    
    print_header("Deployment Setup Complete!")
    print("Your predictive model is ready to serve predictions on Streamlit Cloud!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)
