from flask import Flask, render_template, request, jsonify, send_file, session
from flask_socketio import SocketIO, emit, join_room
import yt_dlp
import os
import tempfile
import threading
import time
import uuid
from urllib.parse import urlparse
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

socketio = SocketIO(app, cors_allowed_origins="*")

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
            
            # Emit progress update
            socketio.emit('download_progress', {
                'session_id': self.session_id,
                'progress': self.progress,
                'downloaded_mb': self.downloaded_bytes / (1024*1024),
                'total_mb': self.total_bytes / (1024*1024),
                'speed': self.speed,
                'eta': self.eta,
                'status': 'downloading',
                'download_dir': os.path.expanduser("~/Downloads")
            }, room=self.session_id)
            
        elif d['status'] == 'finished':
            self.status = "processing"
            socketio.emit('download_progress', {
                'session_id': self.session_id,
                'status': 'processing'
            }, room=self.session_id)
    
    def download_video(self, url, quality, format_only=False):
        """Download video with specified quality or format ID"""
        try:
            self.status = "starting"
            socketio.emit('download_progress', {
                'session_id': self.session_id,
                'status': 'starting',
                'download_dir': os.path.expanduser("~/Downloads")
            }, room=self.session_id)
            
            # Create temporary directory for downloads
            temp_dir = tempfile.mkdtemp()
            
            # Configure yt-dlp options
            # quality can be either a format ID (e.g., "18") or a quality string (e.g., "720p")
            if quality == "auto":
                format_spec = "best"
            elif quality.isdigit():
                # If it's a number, treat it as a format ID
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
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'format': format_spec,
                'progress_hooks': [self.progress_hook],
                'ignoreerrors': False,
                'no_warnings': False,
                'extractaudio': False,
            }
            
            if format_only:
                # Just get format info - ultra-optimized for speed
                ydl_opts['quiet'] = True
                ydl_opts['no_warnings'] = True
                ydl_opts['extract_flat'] = True  # Faster extraction
                ydl_opts['skip_download'] = True  # Skip download info
                ydl_opts['no_color'] = True  # Disable colors
                ydl_opts['no_check_certificate'] = True  # Skip SSL verification for speed
                ydl_opts['socket_timeout'] = 10  # 10 second timeout
                ydl_opts['retries'] = 1  # Minimal retries for speed
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get('formats', [])
                    title = info.get('title', 'Unknown Video')
                    
                    # Format the formats list - ultra-optimized processing
                    formatted_formats = []
                    seen_qualities = set()  # Avoid duplicates

                    # Only process video formats (skip audio-only)
                    video_formats = [f for f in formats if f.get('height') and f.get('ext') in ['mp4', 'webm']]

                    for fmt in video_formats:
                        height = fmt.get('height')
                        ext = fmt.get('ext')
                        quality = f"{height}p"

                        # Only add if we haven't seen this quality
                        if quality not in seen_qualities:
                            seen_qualities.add(quality)

                            # Try multiple ways to get file size
                            filesize = fmt.get('filesize') or fmt.get('filesize_approx')
                            if filesize:
                                size_mb = f"{filesize / (1024*1024):.1f} MB"
                            else:
                                # Estimate size based on quality and duration
                                duration = info.get('duration', 0)
                                if duration and height:
                                    # Rough estimate: 1MB per minute for 720p, 2MB for 1080p
                                    if height >= 1080:
                                        estimated_mb = (duration / 60) * 2
                                    elif height >= 720:
                                        estimated_mb = (duration / 60) * 1.5
                                    else:
                                        estimated_mb = (duration / 60) * 1
                                    size_mb = f"~{estimated_mb:.1f} MB (estimated)"
                                else:
                                    size_mb = "Size unknown"

                            formatted_formats.append({
                                'quality': quality,
                                'ext': ext,
                                'size': size_mb,
                                'format_id': fmt.get('format_id', 'best')  # Store the actual format ID
                            })
                    
                    # Sort by quality (highest first) - limit to top 5 for speed
                    formatted_formats.sort(key=lambda x: int(x['quality'][:-1]) if x['quality'][:-1].isdigit() else 0, reverse=True)
                    formatted_formats = formatted_formats[:5]  # Only show top 5 qualities
                    
                    return {
                        'success': True,
                        'title': title,
                        'formats': formatted_formats
                    }
            else:
                # Download the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Find the downloaded file
                files = os.listdir(temp_dir)
                if files:
                    self.filename = files[0]
                    file_path = os.path.join(temp_dir, self.filename)
                    
                    # Move to permanent location
                    downloads_dir = os.path.expanduser("~/Downloads")
                    final_path = os.path.join(downloads_dir, self.filename)
                    
                    # Ensure unique filename
                    counter = 1
                    while os.path.exists(final_path):
                        name, ext = os.path.splitext(self.filename)
                        final_path = os.path.join(downloads_dir, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    # Move file
                    os.rename(file_path, final_path)
                    
                    # Clean up temp directory
                    os.rmdir(temp_dir)
                    
                    self.status = "completed"
                    socketio.emit('download_progress', {
                        'session_id': self.session_id,
                        'status': 'completed',
                        'filename': self.filename,
                        'filepath': final_path
                    }, room=self.session_id)
                    
                    return {
                        'success': True,
                        'filename': self.filename,
                        'filepath': final_path
                    }
                else:
                    raise Exception("No file was downloaded")
                    
        except Exception as e:
            self.status = "error"
            self.error = str(e)
            socketio.emit('download_progress', {
                'session_id': self.session_id,
                'status': 'error',
                'error': str(e)
            }, room=self.session_id)
            
            return {
                'success': False,
                'error': str(e)
            }

@app.route('/')
def index():
    """Main page with web-based downloader"""
    return render_template('web_downloader.html')

@app.route('/api/validate_url', methods=['POST'])
def validate_url():
    """Validate YouTube URL"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'valid': False, 'error': 'URL is required'})
    
    # Check if it's a YouTube URL
    parsed = urlparse(url)
    is_valid = 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc
    
    return jsonify({
        'valid': is_valid,
        'error': 'Please enter a valid YouTube URL' if not is_valid else None
    })

@app.route('/api/list_formats', methods=['POST'])
def list_formats():
    """List available formats for a video"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'})
    
    # Get formats immediately (no background thread needed for format-only)
    try:
        # Create a temporary download manager for format fetching
        temp_download_mgr = DownloadManager("temp")
        result = temp_download_mgr.download_video(url, "best", format_only=True)
        
        if result['success']:
            return jsonify({
                'success': True,
                'formats': result['formats'],
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

@socketio.on('join_download_session')
def handle_join_session(data):
    """Join a download session for real-time updates"""
    session_id = data.get('session_id')
    if session_id:
        join_room(session_id)

@socketio.on('disconnect')
def handle_disconnect():
    """Clean up when client disconnects"""
    pass

if __name__ == '__main__':
    print("🚀 Starting Web-Based YouTube Downloader...")
    
    # Get port from environment variable (for Railway) or use 8080
    port = int(os.environ.get('PORT', 8080))
    
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("🌐 No installation required - works on any device!")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
