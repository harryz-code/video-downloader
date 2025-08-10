from http.server import BaseHTTPRequestHandler
import json
import yt_dlp
import re
import os
import tempfile
import shutil

def validate_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    youtube_regex = r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+'
    return bool(re.match(youtube_regex, url))

def get_download_info(url, quality='auto'):
    """Get download information and direct download link"""
    try:
        # Configure yt-dlp options
        if quality == "auto":
            format_spec = "best"
        elif quality.isdigit():
            # If it's a number, treat it as a format ID
            format_spec = quality
        elif quality in ["720p", "480p", "360p"]:
            height = quality[:-1]
            format_spec = f"best[height<={height}],best"
        else:
            format_spec = quality
        
        ydl_opts = {
            'format': format_spec,
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'no_color': True,
            'no_check_certificate': True,
            'socket_timeout': 30,
            'retries': 3
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info without downloading
            info = ydl.extract_info(url, download=False)
            
            # Get the best format URL
            if 'url' in info:
                download_url = info['url']
            elif 'formats' in info and info['formats']:
                # Get the best format
                best_format = info['formats'][0]
                download_url = best_format.get('url', '')
            else:
                return {
                    'success': False,
                    'error': 'Could not extract download URL'
                }
            
            # Get video details
            title = info.get('title', 'Unknown Video')
            duration = info.get('duration', 0)
            filesize = info.get('filesize') or info.get('filesize_approx')
            
            if filesize:
                size_mb = f"{filesize / (1024*1024):.1f} MB"
            else:
                size_mb = "Size unknown"
            
            return {
                'success': True,
                'download_url': download_url,
                'title': title,
                'duration': duration,
                'size': size_mb,
                'filename': f"{title}.mp4"
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url', '').strip()
            quality = data.get('quality', 'auto')
            
            if not url:
                response = {
                    'success': False,
                    'error': 'URL is required'
                }
            elif not validate_youtube_url(url):
                response = {
                    'success': False,
                    'error': 'Invalid YouTube URL'
                }
            else:
                response = get_download_info(url, quality)
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {
                'success': False,
                'error': f'Server error: {str(e)}'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
