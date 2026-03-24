# Quick Start: Deploy Your Predictive Model to GitHub & Streamlit Cloud

## ⚡ TL;DR - 3 Easy Steps (15 minutes total)

### Step 1: Create GitHub Repository (2 minutes)
1. Go to: https://github.com/new
2. Enter:
   - **Repository name**: `hotel-booking-prediction`
   - **Description**: `Hotel booking cancellation predictor with Streamlit`
   - **Visibility**: `PUBLIC` ← Important for free Streamlit Cloud
3. Click **"Create repository"**
4. **Copy the HTTPS URL** (e.g., `https://github.com/YOUR_USERNAME/hotel-booking-prediction.git`)

### Step 2: Push Your Code (5 minutes)
Open your terminal in the project folder and run:

```powershell
# Option A: Run the Python automation script (easiest)
python deploy.py

# Option B: Manual git commands
git remote add github https://github.com/YOUR_USERNAME/hotel-booking-prediction.git
git branch -M main
git push -u github main
```

**That's it!** Your code is now on GitHub.

### Step 3: Deploy to Streamlit Cloud (3 minutes)
1. Go to: https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select:
   - **Repository**: `hotel-booking-prediction`
   - **Branch**: `main`
   - **Main file**: `app.py`
5. Click **"Deploy"**
6. Wait 2-3 minutes... Done! Your app will be live at:
   ```
   https://hotel-booking-prediction.streamlit.app
   ```

---

## 📋 What You Get

✅ **Live Web App**: Real-time hotel cancellation predictions
✅ **Auto-Retraining**: Model retrains on every GitHub commit (via GitHub Actions)
✅ **Free Hosting**: Streamlit Community Cloud (no credit card required)
✅ **Shareable Link**: Send the URL to anyone

---

## 🎯 How to Use Your Deployed App

1. **Adjust Decision Threshold** → Slider (0.05 - 0.95)
2. **Enter Booking Details**:
   - Lead time, arrival date, country
   - Length of stay, party size
   - Market segment, deposit type
3. **Get Prediction**: "Canceled" or "Not Canceled" with probability
4. **Use for**: Risk assessment, overbooking management

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "git: command not found" | Install Git: https://git-scm.com/download/win |
| "Permission denied" in Streamlit | Check GitHub repo is PUBLIC, not private |
| deployment stuck | Check Python version 3.11+ in Streamlit settings |
| "Model not found" error | GitHub Actions automatically trains model on first push |

---

## 🔧 Advanced: Manual Git Push (Alternative)

If the automation script doesn't work, use these commands:

```powershell
# Clone your GitHub repo
git clone https://github.com/YOUR_USERNAME/hotel-booking-prediction.git temp-repo
cd temp-repo

# Copy all project files here
Copy-Item -Path "C:\Users\Acer-pc\Desktop\IT20\Predictive_Modeling_v3\*" -Destination "." -Recurse -Force

# Push to GitHub
git add .
git commit -m "Initial commit: Hotel booking prediction with Streamlit"
git push origin main
```

---

## 📊 Model Info

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 89.38%
- **ROC-AUC**: 0.9593
- **Training Data**: 119,390 hotel bookings
- **Features**: Lead time, deposit, country, market segment, stay duration, etc.

---

## 🚀 Next Steps After Deployment

1. **Share your app URL** with colleagues/stakeholders
2. **Monitor performance** via Streamlit Cloud dashboard
3. **View training logs** in GitHub Actions tab
4. **Make updates**: Push new changes to GitHub → Auto-redeploys!

---

## 📞 Questions?

- **Streamlit Docs**: https://docs.streamlit.io/
- **GitHub Help**: https://docs.github.com/en/get-started
- **Deployment Issues**: Check GitHub Actions logs for training errors

---

**Your predictive model is production-ready! Deploy now with just 3 steps.** 🎉
