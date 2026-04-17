# Deploy to GitHub & Render

Complete guide to deploy your Mini Notebook LLM backend to Render via GitHub.

## Prerequisites

- A GitHub account (https://github.com)
- A Render account (https://render.com) - sign up with GitHub for easier integration
- Git installed on your computer

## Step 1: Prepare Your Local Repository

### Initialize Git (If not already done)

```bash
cd "c:\Users\madhusudhan\OneDrive\Desktop\project 2\mini notebook llm"
git init
git add .
git commit -m "Initial commit: Mini Notebook LLM Backend"
```

### Verify Git Status

```bash
git status
```

You should see "On branch main" or "On branch master" with no uncommitted changes.

## Step 2: Create a GitHub Repository

1. Go to https://github.com/new
2. Fill in the form:
   - **Repository name**: `mini-notebook-llm`
   - **Description**: "AI-powered notebook backend with LLM integration"
   - **Visibility**: Public (Render requires public repos on free tier)
   - **Don't initialize README** (you already have one)
   - Click **Create repository**

3. You'll see commands to push your code. Run these in your terminal:

```bash
git remote add origin https://github.com/YOUR_USERNAME/mini-notebook-llm.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

## Step 3: Add Your API Key to Render

⚠️ **IMPORTANT**: Never commit your `.env` file to GitHub!

The `.env` file is already in `.gitignore`, so it won't be pushed. Instead, you'll add the API key directly in Render's dashboard.

## Step 4: Deploy on Render

### 4.1 Connect GitHub to Render

1. Go to https://render.com
2. Click **Sign up** or **Sign in** (use GitHub)
3. Authorize Render to access your GitHub account
4. Click the **GitHub** button to connect repositories

### 4.2 Create a New Web Service

1. On your Render dashboard, click **New +** → **Web Service**
2. Choose **Connect a repository**
3. Find and select `mini-notebook-llm`
4. Click **Connect**

### 4.3 Configure the Service

Fill in the deployment settings:

| Setting | Value |
|---------|-------|
| **Name** | `mini-notebook-llm` |
| **Runtime** | `Python 3.11` |
| **Region** | Choose nearest to you |
| **Start Command** | `pip install -r requirements.txt && python main.py` |
| **Plan** | Free (or Paid) |

### 4.4 Add Environment Variables

1. Scroll down to **Environment**
2. Click **Add Environment Variable**
3. Add your API key:
   - **Key**: `OPENROUTER_API_KEY`
   - **Value**: `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`

4. Optionally add:
   - **Key**: `DEBUG`
   - **Value**: `False`

### 4.5 Deploy

1. Review all settings
2. Click **Create Web Service**
3. Wait for the deployment (3-5 minutes)
4. Once deployed, you'll get a URL like: `https://mini-notebook-llm.onrender.com`

## Step 5: Test Your Deployed API

Once deployment is complete:

```bash
# Test health endpoint
curl https://YOUR_RENDER_URL/health

# Test chat endpoint
curl -X POST https://YOUR_RENDER_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# View interactive docs
# Visit: https://YOUR_RENDER_URL/docs
```

## Step 6: Connect Frontend

Update your frontend to use the Render URL:

```javascript
// Before (local development)
const API_URL = "http://localhost:8000";

// After (production)
const API_URL = "https://your-app.onrender.com";
```

## Troubleshooting Deployment

### Service keeps crashing

Check logs in Render dashboard:
1. Click on your service
2. Go to **Logs**
3. Look for errors

Common issues:
- **Port binding error**: Ensure `main.py` binds to port 8000
- **Missing environment variables**: Check API key is set
- **Build timeout**: Free tier has 60-second limit

### "Build failed"

1. Run locally to test: `python main.py`
2. Check `requirements.txt` is correct
3. Ensure all imports work: `pip install -r requirements.txt`
4. View full build logs in Render dashboard

### API times out

- Free tier Render instances sleep after 15 minutes of inactivity
- First request will take 30+ seconds while instance spins up
- Consider upgrading to paid tier for always-on service

## Automatic Deployments

Render automatically redeploys when you push to GitHub:

```bash
# Make a change
echo "# Updated" >> README.md

# Commit and push
git add .
git commit -m "Update documentation"
git push origin main

# Render detects the push and automatically deploys!
```

## Managing Secrets Securely

### Never push secrets:

❌ **DON'T DO THIS:**
```bash
git add .env          # This would commit the API key!
```

✅ **DO THIS:**
```bash
# .env is already in .gitignore
# Add secrets only in Render's dashboard
```

### Rotating Your API Key

If you ever need to change your API key:

1. Update it in Render dashboard
2. Your service will restart automatically
3. No need to push code changes

## Custom Domain (Optional)

To use your own domain:

1. In Render dashboard, go to **Settings**
2. Scroll to **Custom Domain**
3. Add your domain (requires DNS configuration)
4. Follow Render's instructions for DNS setup

## Monitoring Your Service

### View Logs
```
Render Dashboard → Your Service → Logs
```

### Monitor Resource Usage
```
Render Dashboard → Your Service → Metrics
```

### Set Alerts (Paid Plan)
Monitor uptime and errors

## Upgrading from Free Tier

Free tier limitations:
- ⏸️ Service spins down after 15 minutes of inactivity
- 📊 500 build minutes/month
- 📈 Limited resources

To upgrade:
1. Click **Settings** on your service
2. Change **Plan** to **Starter** or higher
3. Update billing information

## Useful Commands

### View deployment status
```bash
# Check if everything is committed
git status

# View recent commits
git log --oneline -5

# Push changes to GitHub
git push origin main
```

### Local testing before deploying
```bash
# Install fresh dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Test endpoints
curl http://localhost:8000/health
```

## API Endpoint After Deployment

Your deployed API endpoints:

| Endpoint | URL |
|----------|-----|
| Base URL | `https://your-app.onrender.com` |
| Health Check | `https://your-app.onrender.com/health` |
| Chat | `https://your-app.onrender.com/chat` |
| Code Complete | `https://your-app.onrender.com/code-complete` |
| Explain | `https://your-app.onrender.com/explain` |
| Models List | `https://your-app.onrender.com/models` |
| API Docs | `https://your-app.onrender.com/docs` |

## Important Notes

1. **API Key Security**: Never commit `.env` to GitHub
2. **Cold Starts**: Free tier services take 30+ seconds on first request
3. **Cost**: Render free tier is free, but has limitations
4. **Uptime**: Free tier is not guaranteed 99.9% uptime
5. **Backups**: Render doesn't backup free tier services

## Next Steps

After deployment:

1. ✅ Test all endpoints on deployed service
2. ✅ Update frontend to use deployed URL
3. ✅ Monitor logs for errors
4. ✅ Set up custom domain (optional)
5. ✅ Consider upgrading to paid tier for production

## Support

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Get Help: https://render.com/support

---

Your backend is now live! 🚀
