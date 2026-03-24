# ============================================================================
# Hotel Booking Prediction - GitHub & Streamlit Deployment Setup
# ============================================================================
# This script automates pushing your code to GitHub
# Prerequisites: Git must be installed and GitHub account configured
# 
# Usage: .\SETUP_DEPLOYMENT.ps1
# ============================================================================

$ErrorActionPreference = "Stop"

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "Hotel Booking Prediction - GitHub & Streamlit Deployment Setup" -ForegroundColor Cyan
Write-Host "============================================================================`n" -ForegroundColor Cyan

# Verify we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "ERROR: app.py not found. Please run this script from the project root." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Create GitHub Repository
Write-Host "[Step 1/3] GitHub Repository Setup" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "IMPORTANT: You must create a GitHub repository FIRST."
Write-Host ""
Write-Host "To create your repository:"
Write-Host "  1. Go to https://github.com/new"
Write-Host "  2. Fill in these details:"
Write-Host "     - Repository name: hotel-booking-prediction"
Write-Host "     - Description: Hotel booking cancellation predictor with Streamlit"
Write-Host "     - Visibility: PUBLIC (required for free Streamlit Cloud)"
Write-Host "  3. Click 'Create repository'"
Write-Host "  4. Copy the HTTPS URL from the Quick setup section"
Write-Host ""

$REPO_URL = Read-Host "Paste your repository HTTPS URL here (e.g., https://github.com/username/hotel-booking-prediction.git)"

if ([string]::IsNullOrWhiteSpace($REPO_URL)) {
    Write-Host "ERROR: Repository URL is empty." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Push Code to GitHub
Write-Host "`n[Step 2/3] Pushing Code to GitHub" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Yellow
Write-Host ""

$TEMP_DIR = Join-Path $env:TEMP "hotel-prediction-repo-$(Get-Random)"

try {
    Write-Host "Creating temporary directory: $TEMP_DIR"
    New-Item -ItemType Directory -Path $TEMP_DIR -Force | Out-Null
    
    Write-Host "Cloning your GitHub repository..."
    & git clone $REPO_URL $TEMP_DIR
    
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to clone repository. Check your URL and GitHub credentials."
    }
    
    Write-Host "Copying project files..."
    $SOURCE = "C:\Users\Acer-pc\Desktop\IT20\Predictive_Modeling_v3"
    Get-ChildItem -Path $SOURCE -Recurse | ForEach-Object {
        $RelativePath = $_.FullName.Substring($SOURCE.Length + 1)
        $DestPath = Join-Path $TEMP_DIR $RelativePath
        
        if ($_.PSIsContainer) {
            New-Item -ItemType Directory -Path $DestPath -Force -ErrorAction SilentlyContinue | Out-Null
        } else {
            # Skip .git directory
            if (-not $RelativePath.StartsWith(".git")) {
                Copy-Item -Path $_.FullName -Destination $DestPath -Force
            }
        }
    }
    
    Write-Host "Adding files to git..."
    Push-Location $TEMP_DIR
    & git add .
    
    Write-Host "Committing changes..."
    & git commit -m @"
Initial commit: Hotel booking prediction with Streamlit web interface

- Trained Random Forest model with 89.38% accuracy and 0.9593 ROC-AUC
- Streamlit web app for real-time hotel cancellation predictions
- GitHub Actions CI/CD workflow for automated model retraining
- Complete documentation for GitHub and Streamlit Cloud deployment
- Dataset: 119,390 hotel booking records
"@
    
    Write-Host "Pushing to GitHub (this may take a minute)..."
    & git push -u origin main
    
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to push to GitHub. Check your credentials and try again."
    }
    
    Pop-Location
}
catch {
    Write-Host "`nERROR: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "  - Ensure Git is installed and configured with GitHub credentials"
    Write-Host "  - Verify the repository URL is correct"
    Write-Host "  - Try running: git config --global user.name 'Your Name'"
    Write-Host "  - Try running: git config --global user.email 'your@email.com'"
    Write-Host "  - For HTTPS, you may need to use a Personal Access Token instead of password"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
finally {
    # Cleanup
    if (Test-Path $TEMP_DIR) {
        Write-Host "`nCleaning up temporary files..."
        Remove-Item -Path $TEMP_DIR -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Step 3: Streamlit Cloud Deployment Instructions
Write-Host "`n[Step 3/3] Streamlit Cloud Deployment" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "SUCCESS! Your code is now on GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps to deploy to Streamlit Cloud:"
Write-Host ""
Write-Host "  1. Go to https://streamlit.io/cloud"
Write-Host "  2. Sign in with your GitHub account (or create one)"
Write-Host "  3. Click 'New app'"
Write-Host "  4. Select:"
Write-Host "     - GitHub account: (your username)"
Write-Host "     - Repository: hotel-booking-prediction"
Write-Host "     - Branch: main"
Write-Host "     - Main file path: app.py"
Write-Host "  5. Click 'Deploy'"
Write-Host "  6. Wait 2-3 minutes for deployment to complete"
Write-Host "  7. Your live app will be at: https://hotel-booking-prediction.streamlit.app"
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Deployment Setup Complete!" -ForegroundColor Green
Write-Host "============================================================================`n" -ForegroundColor Cyan

Read-Host "Press Enter to exit"
