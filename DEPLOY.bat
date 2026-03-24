@echo off
REM Quick deployment launcher
REM Just run this and paste your GitHub URL

cls
echo.
echo ============================================================================
echo        HOTEL BOOKING PREDICTION - INSTANT DEPLOYMENT
echo ============================================================================
echo.
echo This will push your code to GitHub in seconds.
echo.

python deploy_now.py

if errorlevel 1 (
    echo.
    echo Deployment failed. Press any key for troubleshooting tips.
    pause
) else (
    pause
)
