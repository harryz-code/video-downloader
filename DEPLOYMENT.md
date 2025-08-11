# YouTube Downloader - Deployment Guide

## 🚀 Recommended Deployment: Railway

This project is optimized for **Railway deployment** because it requires:
- Python runtime with dependencies (`yt-dlp`)
- File system access for downloads
- Long-running processes for video downloads

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway CLI**: `npm install -g @railway/cli`

## 🚀 Deploy to Railway

### Option 1: Deploy via Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Railway will automatically detect the Python app and deploy

### Option 2: Deploy via CLI
```bash
# Login to Railway
railway login

# Deploy the project
railway up
```

## 🔧 Configuration

The project is already configured for Railway:
- `railway.json` - Railway deployment configuration
- `railway_app.py` - Main Flask application (serves both frontend and API)
- `templates/web_downloader.html` - v0.dev landing page
- `requirements.txt` - Python dependencies

## 🌐 Local Development

Run the complete application locally:

```bash
# Start the Railway backend (serves both frontend and API)
./start-local.sh

# Or manually:
source venv/bin/activate
python railway_app.py
```

## 📱 Access Your App

- **Local**: http://localhost:8080 (serves both frontend and API)
- **Railway**: Your Railway URL (e.g., `https://your-app.railway.app`)

## 🏗️ Architecture

The Railway app (`railway_app.py`) serves:
- **Frontend**: Beautiful v0.dev landing page at `/`
- **API Endpoints**: 
  - `/api/validate_url` - Validate YouTube URLs
  - `/api/list_formats` - Get available video formats
  - `/api/download` - Start video downloads
  - `/api/open_folder` - Open download folder
- **Health Check**: `/health` - API status

## ❌ Why Not Other Platforms?

- **Vercel**: No Python support, only static sites
- **Cloudflare Workers**: JavaScript-only, no Python/yt-dlp
- **Heroku**: Requires credit card, more complex setup

## 🐛 Troubleshooting

### Port Conflicts
```bash
# Kill processes on port 8080
lsof -ti:8080 | xargs kill -9
```

### Dependencies
```bash
# Reinstall Python dependencies
pip install -r requirements.txt
```

### Railway Issues
```bash
# Check Railway logs
railway logs

# Redeploy
railway up
```

## 📁 Project Structure

```
video-downloader/
├── railway_app.py              # Main Flask app (serves frontend + API)
├── templates/
│   └── web_downloader.html    # v0.dev landing page
├── requirements.txt            # Python dependencies
├── railway.json               # Railway deployment config
└── start-local.sh             # Local development script
```

## ✅ Success Checklist

- [ ] Railway deployment successful
- [ ] Frontend loads at Railway URL
- [ ] YouTube URL validation works
- [ ] Video download functionality works
- [ ] Progress tracking works
- [ ] Download folder opens correctly
