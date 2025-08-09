# Free YouTube Video Downloader

A powerful, free YouTube video downloader that works both as a desktop application and a web-based service. Download YouTube videos in various qualities (1080p, 720p, 480p, 360p) to MP4 format without any registration or hidden costs.

## 🌟 Features

- **100% Free**: No registration, no subscription, no hidden costs
- **Multiple Formats**: Download in MP4 video or MP3 audio
- **Quality Options**: Choose from 1080p, 720p, 480p, 360p, or auto-select best quality
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Real-time Progress**: Track download progress with live updates
- **Format Detection**: See all available formats before downloading
- **Smart Fallback**: Automatic retry with alternative methods if preferred format fails

## 🚀 Quick Start

### Option 1: Web-Based Downloader (Recommended)

The web-based downloader runs in your browser and requires no software installation!

1. **Start the server:**
   ```bash
   # Make sure you're in the project directory
   cd video-downloader
   
   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Start the web server
   python start_web_downloader.py
   ```

2. **Open your browser** and go to the URL shown (usually `http://localhost:8080`)

3. **Paste a YouTube URL** and start downloading!

### Option 2: Desktop Application

For the traditional desktop GUI application:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python youtube_downloader.py
   ```

## 📱 Web-Based Downloader

The web-based version provides a modern, responsive interface that works on any device with a browser:

- **No Installation Required**: Works directly in your browser
- **Real-time Progress**: Live download progress with speed and ETA
- **Format Selection**: Choose quality before downloading
- **Mobile Friendly**: Responsive design works on phones and tablets
- **Instant Access**: No software to install or configure

### How to Use Web Downloader

1. **Paste YouTube URL**: Copy any YouTube video URL and paste it
2. **Select Quality**: Choose your preferred resolution or use "Auto" for best results
3. **List Formats**: Click "List Available Formats" to see all options
4. **Download**: Click "Download Video" and watch real-time progress
5. **Enjoy**: Your video downloads to your Downloads folder

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/harryz-code/video-downloader.git
   cd video-downloader
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   # For web-based downloader
   pip install -r web_requirements.txt
   
   # For desktop application
   pip install -r requirements.txt
   ```

## 🔧 Usage

### Web-Based Downloader

```bash
# Start the web server
python start_web_downloader.py

# Or start directly
python web_downloader.py
```

Then open your browser to the displayed URL (usually `http://localhost:8080`).

### Desktop Application

```bash
python youtube_downloader.py
```

## 📋 Requirements

### Web-Based Downloader
- Flask==2.3.3
- Flask-SocketIO==5.3.6
- yt-dlp==2025.7.21
- Other dependencies in `web_requirements.txt`

### Desktop Application
- tkinter (usually included with Python)
- yt-dlp
- Other dependencies in `requirements.txt`

## 🌐 How It Works

The downloader uses `yt-dlp`, a powerful YouTube download library that:

- Automatically handles YouTube's changing systems
- Provides multiple quality and format options
- Implements smart fallback strategies
- Maintains high download speeds
- Handles various YouTube URL formats

## 🚨 Legal Notice

This tool is for downloading videos you have permission to download. Please respect:

- YouTube's Terms of Service
- Copyright laws
- Content creator rights

Only download videos you own or have explicit permission to download.

## 🤝 Contributing

Contributions are welcome! This is an open-source project built for the community.

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Port Already in Use
If you get "Address already in use" errors:
- The startup script automatically finds available ports
- Or manually specify a different port in the code

### Dependencies Issues
```bash
# Reinstall dependencies
pip install --upgrade -r web_requirements.txt
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r web_requirements.txt
```

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review the code comments
- Open an issue on GitHub

---

**Enjoy downloading YouTube videos for free! 🎬✨**
