from http.server import BaseHTTPRequestHandler
import json
import re

def validate_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    youtube_regex = r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+'
    return bool(re.match(youtube_regex, url))

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
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
            else:
                data = {}
            
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
                # For now, return a simple response
                response = {
                    'success': True,
                    'title': 'YouTube Video',
                    'formats': [
                        {'quality': '720p', 'ext': 'mp4', 'size': '~15.2 MB (estimated)', 'format_id': '22'},
                        {'quality': '480p', 'ext': 'mp4', 'size': '~8.5 MB (estimated)', 'format_id': '18'},
                        {'quality': '360p', 'ext': 'mp4', 'size': '~5.1 MB (estimated)', 'format_id': '17'}
                    ]
                }
            
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
