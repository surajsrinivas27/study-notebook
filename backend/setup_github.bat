@echo off
REM GitHub Setup Script for Mini Notebook LLM

setlocal enabledelayedexpansion

echo ========================================
echo GitHub Setup - Mini Notebook LLM
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git found
echo.

REM Initialize git if not already done
if not exist .git (
    echo Initializing git repository...
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
    echo ✅ Git initialized
) else (
    echo ✅ Git repository already exists
)

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Create a GitHub repository:
echo    - Go to https://github.com/new
echo    - Name it: mini-notebook-llm
echo    - Make it PUBLIC
echo    - Don't initialize README
echo    - Click Create
echo.
echo 2. Copy the HTTPS URL from GitHub (looks like:)
echo    https://github.com/YOUR_USERNAME/mini-notebook-llm.git
echo.
echo 3. Run these commands:
echo.
echo    git remote add origin PASTE_YOUR_GITHUB_URL_HERE
echo    git branch -M main
echo    git add .
echo    git commit -m "Initial commit: Mini Notebook LLM Backend"
echo    git push -u origin main
echo.
echo 4. Your code will be on GitHub! 🎉
echo.
echo 5. Go to Render.com and:
echo    - Click "New Web Service"
echo    - Connect your GitHub repository
echo    - Add environment variable OPENROUTER_API_KEY
echo    - Deploy!
echo.
echo ========================================
echo Documentation:
echo ========================================
echo See DEPLOY_RENDER.md for detailed instructions
echo.
pause
