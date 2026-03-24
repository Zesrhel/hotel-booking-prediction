@echo off
REM ============================================================================
REM Hotel Booking Prediction - GitHub & Streamlit Deployment Setup
REM ============================================================================
REM This script automates the deployment setup for GitHub and Streamlit Cloud
REM You must manually create the GitHub repo and push this script will help with that

echo.
echo ============================================================================
echo Hotel Booking Prediction - GitHub & Streamlit Deployment Setup
echo ============================================================================
echo.
echo This script will help you push your code to GitHub.
echo.

REM Step 1: Verify we're in the right directory
if not exist "app.py" (
    echo ERROR: app.py not found. Please run this script from the project root.
    pause
    exit /b 1
)

echo [Step 1/3] Preparing GitHub Repository...
echo.
echo You need to create a GitHub repository manually:
echo   1. Go to https://github.com/new
echo   2. Fill in these details:
echo      - Repository name: hotel-booking-prediction
echo      - Description: Hotel booking cancellation predictor with Streamlit
echo      - Visibility: PUBLIC (required for free Streamlit Cloud)
echo   3. Click "Create repository"
echo   4. Copy the HTTPS URL (looks like: https://github.com/YOUR_USERNAME/hotel-booking-prediction.git)
echo.
set /p REPO_URL="Paste your repository HTTPS URL here: "

if "%REPO_URL%"=="" (
    echo ERROR: Repository URL is empty.
    pause
    exit /b 1
)

echo.
echo [Step 2/3] Pushing Code to GitHub...
echo.

REM Create a temporary directory for the GitHub repo
set TEMP_DIR=%TEMP%\hotel-prediction-repo
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

echo Cloning your GitHub repository...
cd /d "%TEMP_DIR%"
git clone "%REPO_URL%" .

if errorlevel 1 (
    echo ERROR: Failed to clone repository. Check your URL and try again.
    pause
    exit /b 1
)

echo Copying project files...
xcopy "C:\Users\Acer-pc\Desktop\IT20\Predictive_Modeling_v3\*" "." /E /I /Y

echo Adding files to git...
git add .

echo Committing changes...
git commit -m "Initial commit: Hotel booking prediction with Streamlit web interface

- Trained Random Forest model with 89.38%% accuracy
- Streamlit web app for real-time predictions
- GitHub Actions CI/CD for automated model retraining
- Comprehensive documentation for deployment"

echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo ERROR: Failed to push to GitHub. Check your credentials and try again.
    pause
    exit /b 1
)

echo.
echo [Step 3/3] Streamlit Cloud Deployment Instructions...
echo.
echo Your code is now on GitHub! Next, deploy to Streamlit Cloud:
echo.
echo   1. Go to https://streamlit.io/cloud
echo   2. Sign in with your GitHub account
echo   3. Click "New app"
echo   4. Select:
echo      - GitHub account: YOUR_USERNAME
echo      - Repository: hotel-booking-prediction
echo      - Branch: main
echo      - Main file path: app.py
echo   5. Click "Deploy"
echo   6. Wait 2-3 minutes for deployment
echo   7. Your app URL: https://hotel-booking-prediction.streamlit.app
echo.
echo ============================================================================
echo Deployment Setup Complete!
echo ============================================================================
echo.
pause
