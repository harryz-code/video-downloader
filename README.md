# 🎥 YouTube Video Downloader

A **simple, powerful, and user-friendly** YouTube video downloader built with Python and tkinter. Features a clean GUI interface with smart fallback strategies and comprehensive format detection.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Cross--platform-lightgrey.svg)

## ✨ Features

- **🎯 Smart Quality Selection** - Choose specific resolutions or let the app auto-select the best available
- **📋 Format Detection** - List all available formats before downloading
- **🔄 Fallback Strategy** - Automatic retry with alternative methods if download fails
- **🎨 Clean GUI** - Modern, intuitive interface built with tkinter
- **📁 Custom Locations** - Choose where to save your downloads
- **⚡ Progress Tracking** - Visual feedback during downloads
- **🛡️ Error Handling** - Robust error handling with user-friendly messages
- **🌐 Cross-Platform** - Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python youtube_downloader.py
   ```

## 📖 Usage Guide

### Basic Download
1. **Enter YouTube URL** - Paste any YouTube video URL
2. **Select Quality** - Choose from available options or use "auto" for best results
3. **Choose Location** - Pick where to save your video
4. **Click Download** - The app handles the rest!

### Advanced Features

#### 📋 List Available Formats
- Click **"List Available Formats"** to see all available resolutions and file sizes
- Helps you choose the best quality for your needs
- Shows file format and estimated size

#### 🎯 Quality Options
- **best** - Highest quality available
- **worst** - Lowest quality available  
- **720p, 480p, 360p** - Specific resolutions (with fallback)
- **auto** - Smart automatic selection

#### 🔄 Smart Fallback
- If your preferred quality isn't available, the app automatically tries alternatives
- Handles YouTube API changes gracefully
- Ensures successful downloads even when specific formats fail

## 🛠️ How It Works

This application uses **yt-dlp**, a powerful and actively maintained fork of youtube-dl that:

- **Regularly updates** to handle YouTube's changing systems
- **Supports multiple formats** including video and audio
- **Handles region restrictions** and age-gated content
- **Provides detailed progress** and error information

The GUI is built with **tkinter** for maximum compatibility across platforms.

## 📁 Project Structure

```
youtube-downloader/
├── youtube_downloader.py    # Main application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .gitignore              # Git ignore rules
└── venv/                   # Virtual environment (not tracked)
```

## 🔧 Troubleshooting

### Common Issues

#### **"Module not found" errors**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### **Download failures**
```bash
# Update yt-dlp to the latest version
pip install --upgrade yt-dlp
```

#### **Permission errors**
- Ensure you have write permissions to the download directory
- Try running as administrator (Windows) or with sudo (Linux/macOS)

#### **Format not available**
- Use the **"List Available Formats"** button to see what's actually available
- Try the **"auto"** quality setting for automatic selection
- The app will automatically fall back to available formats

### YouTube Changes
YouTube frequently updates their systems. If downloads stop working:

1. **Update yt-dlp:**
   ```bash
   pip install --upgrade yt-dlp
   ```

2. **Check for issues:**
   - Visit [yt-dlp GitHub issues](https://github.com/yt-dlp/yt-dlp/issues)
   - Check if others are experiencing similar problems

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If you have dev dependencies
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Notice

**Important:** This tool is for downloading videos you have permission to download. Please respect:

- **YouTube's Terms of Service**
- **Copyright laws** in your jurisdiction
- **Content creators' rights**

**Only download content you own or have explicit permission to download.**

## 🙏 Acknowledgments

- **yt-dlp team** for the excellent video downloading library
- **Python community** for the robust tkinter GUI framework
- **Contributors** who help improve this project

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information:
   - Operating system and Python version
   - Error messages and logs
   - Steps to reproduce the problem

---

**Made with ❤️ for the open-source community**
