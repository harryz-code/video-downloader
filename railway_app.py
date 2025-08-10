from flask import Flask, render_template, request, jsonify
import yt_dlp
import os
import tempfile
import threading
import time
import uuid
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Store download sessions
download_sessions = {}

class DownloadManager:
    def __init__(self, session_id):
        self.session_id = session_id
        self.progress = 0
        self.status = "initializing"
        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.speed = "0 B/s"
        self.eta = "Unknown"
        self.filename = ""
        self.error = None
        
    def progress_hook(self, d):
        """Progress callback for yt-dlp"""
        if d['status'] == 'downloading':
            # Update progress
            if '_percent_str' in d:
                try:
                    percent = float(d['_percent_str'].replace('%', ''))
                    self.progress = percent
                except:
                    pass
            
            # Update bytes info
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0)
            
            if total > 0:
                self.downloaded_bytes = downloaded
                self.total_bytes = total
                self.progress = (downloaded / total) * 100
            
            # Update speed and ETA
            if '_speed_str' in d:
                self.speed = d.get('_speed_str', 'N/A')
            if '_eta_str' in d:
                self.eta = d.get('eta_str', 'N/A')
            
        elif d['status'] == 'finished':
            self.status = "processing"
    
    def download_video(self, url, quality, format_only=False):
        """Download video with specified quality or format ID"""
        try:
            self.status = "starting"
            
            # Create temporary directory for downloads
            temp_dir = tempfile.mkdtemp()
            
            # Configure yt-dlp options
            if quality == "auto":
                format_spec = "best"
            elif quality.isdigit():
                format_spec = quality
                print(f"🎯 Using format ID: {quality}")
            elif quality in ["720p", "480p", "360p"]:
                height = quality[:-1]
                format_spec = f"best[height<={height}],best"
                print(f"🎯 Using quality filter: {format_spec}")
            else:
                format_spec = quality
                print(f"🎯 Using format spec: {format_spec}")
            
            ydl_opts = {
                'format': format_spec,
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': False,
                'no_warnings': False
            }
            
            if format_only:
                ydl_opts['listformats'] = True
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if format_only:
                    # Just get format info
                    info = ydl.extract_info(url, download=False)
                    return {
                        'success': True,
                        'title': info.get('title', 'Unknown'),
                        'formats': info.get('formats', [])
                    }
                else:
                    # Download the video
                    info = ydl.extract_info(url, download=True)
                    self.filename = info.get('title', 'video') + '.' + info.get('ext', 'mp4')
                    self.status = "completed"
                    
                    return {
                        'success': True,
                        'title': info.get('title', 'Unknown'),
                        'filename': self.filename,
                        'size': f"{self.total_bytes / (1024*1024):.1f} MB"
                    }
                    
        except Exception as e:
            self.error = str(e)
            self.status = "error"
            return {
                'success': False,
                'error': str(e)
            }

def validate_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    if not url:
        return False
    
    # YouTube URL patterns
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/[\w-]+'
    ]
    
    import re
    for pattern in patterns:
        if re.match(pattern, url):
            return True
    return False

@app.route('/')
def index():
    """Main page with web-based downloader"""
    return render_template('web_downloader.html')

@app.route('/health')
def health():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy', 'message': 'YouTube Downloader API is running'})

@app.route('/api/validate_url', methods=['POST'])
def validate_url():
    """Validate YouTube URL"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        is_valid = validate_youtube_url(url)
        
        return jsonify({
            'success': True,
            'is_valid': is_valid
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/list_formats', methods=['POST'])
def list_formats():
    """List available formats for a YouTube video"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not validate_youtube_url(url):
            return jsonify({
                'success': False,
                'error': 'Invalid YouTube URL'
            })
        
        # Create temporary download manager
        session_id = str(uuid.uuid4())
        download_mgr = DownloadManager(session_id)
        
        # Get format info
        result = download_mgr.download_video(url, 'auto', format_only=True)
        
        if result['success']:
            # Format the formats for frontend
            formats = []
            for fmt in result['formats']:
                if fmt.get('height') and fmt.get('ext'):
                    formats.append({
                        'quality': f"{fmt['height']}p",
                        'ext': fmt['ext'],
                        'size': f"{fmt.get('filesize', 0) / (1024*1024):.1f} MB" if fmt.get('filesize') else 'Unknown',
                        'format_id': str(fmt['format_id'])
                    })
            
            return jsonify({
                'success': True,
                'formats': formats[:5],  # Limit to 5 formats
                'title': result['title'],
                'message': 'Formats fetched successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to fetch formats')
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching formats: {str(e)}'
        })

@app.route('/api/download', methods=['POST'])
def start_download():
    """Start video download"""
    data = request.get_json()
    url = data.get('url', '').strip()
    quality = data.get('quality', 'best')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'})
    
    # Create download manager for this session
    session_id = str(uuid.uuid4())
    download_mgr = DownloadManager(session_id)
    download_sessions[session_id] = download_mgr
    
    # Start download in background
    def download():
        result = download_mgr.download_video(url, quality)
        # Clean up session after delay
        time.sleep(10)
        if session_id in download_sessions:
            del download_sessions[session_id]
    
    thread = threading.Thread(target=download)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': 'Download started'
    })

@app.route('/api/open_folder', methods=['POST'])
def open_folder():
    """Open the download folder in the system file manager"""
    data = request.get_json()
    folder_path = data.get('path', '').strip()
    
    if not folder_path:
        return jsonify({'success': False, 'error': 'Path is required'})
    
    try:
        # Use platform-specific commands to open folder
        import platform
        system = platform.system()
        
        if system == "Darwin":  # macOS
            import subprocess
            subprocess.run(['open', folder_path], check=True)
        elif system == "Windows":
            import subprocess
            subprocess.run(['explorer', folder_path], check=True)
        elif system == "Linux":
            import subprocess
            subprocess.run(['xdg-open', folder_path], check=True)
        else:
            return jsonify({'success': False, 'error': 'Unsupported operating system'})
        
        return jsonify({'success': True, 'message': 'Folder opened successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to open folder: {str(e)}'})

if __name__ == '__main__':
    print("🚀 Starting Web-Based YouTube Downloader...")
    
    # Get port from environment variable (for Railway) or use 8080
    port = int(os.environ.get('PORT', 8080))
    
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("🌐 No installation required - works on any device!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
