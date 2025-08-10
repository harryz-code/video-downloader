from http.server import BaseHTTPRequestHandler
import json
import yt_dlp
import re

def validate_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    youtube_regex = r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+'
    return bool(re.match(youtube_regex, url))

def list_formats(url):
    """List available formats for a YouTube video"""
    try:
        # Configure yt-dlp options for format listing
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'skip_download': True,
            'no_color': True,
            'no_check_certificate': True,
            'socket_timeout': 10,
            'retries': 1
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            title = info.get('title', 'Unknown Video')
            
            # Format the formats list
            formatted_formats = []
            seen_qualities = set()

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
                        'format_id': fmt.get('format_id', 'best')
                    })
            
            # Sort by quality (highest first) - limit to top 5 for speed
            formatted_formats.sort(key=lambda x: int(x['quality'][:-1]) if x['quality'][:-1].isdigit() else 0, reverse=True)
            formatted_formats = formatted_formats[:5]
            
            return {
                'success': True,
                'title': title,
                'formats': formatted_formats
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
                response = list_formats(url)
            
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
