# Deploy to Render - Quick Guide

## TL;DR (30 Minutes to Live)

### 1️⃣ Push to GitHub

```bash
git init
git add .
git commit -m "Initial: Mini Notebook LLM"
git remote add origin https://github.com/YOUR_NAME/mini-notebook-llm.git
git branch -M main
git push -u origin main
```

### 2️⃣ Deploy on Render

1. Go to https://render.com/sign-up (use GitHub)
2. Click **New +** → **Web Service**
3. Select **Connect a repository** → Choose `mini-notebook-llm`
4. Fill in:
   - **Name**: `mini-notebook-llm`
   - **Start Command**: Leave as default
   - **Plan**: Free
5. Add **Environment**: `OPENROUTER_API_KEY` = `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`
6. Click **Create Web Service**
7. Wait 3-5 minutes ⏳
8. Get your URL! 🎉

### 3️⃣ Test Your API

```bash
# Replace with your Render URL
curl https://YOUR_APP.onrender.com/docs
```

## Detailed Steps

See **DEPLOY_RENDER.md** for complete guide with troubleshooting.

## GitHub URL Format

Your GitHub URL should look like:
```
https://github.com/your_username/mini-notebook-llm.git
```

Replace `your_username` with your actual GitHub username.

## Files Needed for Render

✅ Already created:
- `render.yaml` - Render configuration
- `Procfile` - Process definition  
- `.gitignore` - Excludes `.env` (keeps API key safe)
- `requirements.txt` - Python packages

## Common Issues

| Issue | Fix |
|-------|-----|
| "Remote not found" | Check GitHub URL is correct |
| "Build failed" | Check `requirements.txt` locally works |
| "API timeout" | Free tier sleeps after 15min, try again |
| "API key error" | Verify it's in Render environment vars |

## Useful Links

- Create GitHub repo: https://github.com/new
- Render dashboard: https://dashboard.render.com
- Interactive API docs: `YOUR_URL/docs`

## After Deployment

1. Test all endpoints on Render URL
2. Update frontend to use Render URL instead of `localhost:8000`
3. Enable automatic deploys (already enabled!)
4. Monitor logs in Render dashboard

## File Locations

- Local: `c:\Users\madhusudhan\OneDrive\Desktop\project 2\mini notebook llm\`
- GitHub: `https://github.com/YOUR_NAME/mini-notebook-llm`
- Live: `https://mini-notebook-llm.onrender.com` (example)

## Commands Reference

```bash
# Check git status
git status

# View commits
git log --oneline

# Push changes
git push origin main

# Pull latest changes
git pull origin main
```

---

**Questions?** See DEPLOY_RENDER.md or visit render.com/docs
