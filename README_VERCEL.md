# YouTube Downloader - Vercel Deployment

This is a Vercel-compatible version of the YouTube video downloader.

## 🚀 Quick Deploy to Vercel

1. **Fork this repository** to your GitHub account

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up/Login with GitHub
   - Click "New Project"
   - Import your forked repository

3. **Deploy:**
   - Vercel will automatically detect the configuration
   - Click "Deploy"
   - Your app will be live in minutes!

## 📁 Project Structure

```
├── api/                    # Vercel serverless functions
│   ├── validate_url.py    # URL validation
│   ├── list_formats.py    # Format listing
│   ├── download.py        # Download info
│   └── requirements.txt   # Python dependencies
├── public/                # Static files
│   └── index.html         # Main app
├── vercel.json           # Vercel configuration
└── package.json          # Build configuration
```

## 🔧 How It Works

- **Frontend**: Static HTML with beautiful v0.dev design
- **Backend**: Vercel serverless functions using yt-dlp
- **API**: RESTful endpoints for validation, format listing, and downloads
- **Downloads**: Direct download links (no server-side file storage)

## 🌟 Features

- ✅ Beautiful modern UI with animations
- ✅ URL validation
- ✅ Format listing
- ✅ Direct download links
- ✅ Quality selection
- ✅ Mobile responsive
- ✅ Global CDN
- ✅ Free hosting

## 🔗 API Endpoints

- `POST /api/validate_url` - Validate YouTube URLs
- `POST /api/list_formats` - List available formats
- `POST /api/download` - Get download information

## 🎯 Usage

1. Visit your deployed URL
2. Paste a YouTube URL
3. Select quality (optional)
4. Click download
5. Use the provided download link

## 📝 Notes

- Downloads are direct links (no server processing)
- No file storage on Vercel
- Works with most YouTube videos
- Respects YouTube's terms of service

## 🚀 Deploy Now!

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/video-downloader)
