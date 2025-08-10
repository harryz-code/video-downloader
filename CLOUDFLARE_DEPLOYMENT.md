# Cloudflare Deployment Guide

## Overview
This project is now configured for Cloudflare Pages (frontend) + Cloudflare Workers (backend API).

## Prerequisites
1. Cloudflare account (free)
2. Domain name (optional, but recommended)
3. Wrangler CLI installed: `npm install -g wrangler`

## Step 1: Deploy the API (Cloudflare Workers)

1. **Login to Wrangler:**
   ```bash
   wrangler login
   ```

2. **Update the wrangler.toml configuration:**
   - Replace `yourdomain.com` with your actual domain
   - Or remove the routes section if you don't have a custom domain

3. **Deploy the Workers API:**
   ```bash
   wrangler deploy
   ```

4. **Note the Workers URL** (e.g., `https://youtube-downloader-api.your-subdomain.workers.dev`)

## Step 2: Deploy the Frontend (Cloudflare Pages)

1. **Push your code to GitHub**

2. **Go to Cloudflare Dashboard:**
   - Navigate to Pages
   - Click "Create a project"
   - Choose "Connect to Git"
   - Select your repository

3. **Configure the build settings:**
   - **Framework preset:** None
   - **Build command:** (leave empty)
   - **Build output directory:** `public`
   - **Root directory:** (leave empty)

4. **Environment variables:**
   - Add `API_BASE_URL` with your Workers URL from Step 1

5. **Deploy**

## Step 3: Update API URLs

After deployment, update the `_redirects` file with your actual Workers URL:

```
/api/*  https://your-actual-workers-url.workers.dev/api/:splat  200
```

## Step 4: Add yt-dlp Support (Optional)

To enable actual video downloading, you'll need to:

1. **Install yt-dlp in the Workers environment:**
   ```python
   # In functions/api.py, add:
   import subprocess
   import sys
   
   # Install yt-dlp if not available
   try:
       import yt_dlp
   except ImportError:
       subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
       import yt_dlp
   ```

2. **Update the download functions to use yt-dlp**

## Benefits of Cloudflare Deployment

✅ **Free tier is generous**
✅ **Global CDN for fast loading**
✅ **Better Python support than Vercel**
✅ **Easy domain management**
✅ **No cold starts**
✅ **Built-in DDoS protection**

## Troubleshooting

### API not working
- Check the Workers URL in `_redirects`
- Verify CORS headers are set correctly
- Check Workers logs in Cloudflare dashboard

### Frontend not loading
- Ensure `public/index.html` exists
- Check Pages build logs
- Verify the build output directory is correct

### Domain issues
- Add your domain in Cloudflare DNS
- Update `wrangler.toml` with correct domain
- Wait for DNS propagation (up to 24 hours)
