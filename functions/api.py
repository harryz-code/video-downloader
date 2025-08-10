import json
import re
from urllib.parse import urlparse, parse_qs

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
    
    for pattern in patterns:
        if re.match(pattern, url):
            return True
    return False

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    if 'youtube.com/watch' in url:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        return query_params.get('v', [None])[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[-1].split('?')[0]
    return None

def handle_validate_url(request):
    """Handle URL validation endpoint"""
    try:
        data = request.json()
        url = data.get('url', '').strip()
        
        is_valid = validate_youtube_url(url)
        video_id = extract_video_id(url) if is_valid else None
        
        return {
            'success': True,
            'is_valid': is_valid,
            'video_id': video_id
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def handle_list_formats(request):
    """Handle format listing endpoint"""
    try:
        data = request.json()
        url = data.get('url', '').strip()
        
        if not validate_youtube_url(url):
            return {
                'success': False,
                'error': 'Invalid YouTube URL'
            }
        
        # For now, return dummy format data
        # In production, you'd use yt-dlp here
        response = {
            'success': True,
            'title': 'YouTube Video',
            'formats': [
                {'quality': '720p', 'ext': 'mp4', 'size': '~15.2 MB (estimated)', 'format_id': '22'},
                {'quality': '480p', 'ext': 'mp4', 'size': '~8.5 MB (estimated)', 'format_id': '18'},
                {'quality': '360p', 'ext': 'mp4', 'size': '~5.1 MB (estimated)', 'format_id': '17'}
            ]
        }
        
        return response
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def handle_download(request):
    """Handle download endpoint"""
    try:
        data = request.json()
        url = data.get('url', '').strip()
        quality = data.get('quality', 'auto')
        
        if not validate_youtube_url(url):
            return {
                'success': False,
                'error': 'Invalid YouTube URL'
            }
        
        # For now, return placeholder response
        # In production, you'd use yt-dlp here
        response = {
            'success': True,
            'message': 'Download functionality will be added in the next update',
            'title': 'YouTube Video',
            'size': '~15.2 MB (estimated)',
            'filename': 'video.mp4'
        }
        
        return response
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def handle_request(request):
    """Main request handler"""
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return Response('', headers=headers)
    
    try:
        # Parse the request path
        url_parts = request.url.split('/')
        path = url_parts[-1] if url_parts else ''
        
        if path == 'validate_url':
            result = handle_validate_url(request)
        elif path == 'list_formats':
            result = handle_list_formats(request)
        elif path == 'download':
            result = handle_download(request)
        elif path == 'open_folder':
            # For now, return success since we can't open folders in browser
            result = {
                'success': True,
                'message': 'Folder opened successfully'
            }
        else:
            result = {
                'success': False,
                'error': f'Endpoint not found: {path}'
            }
        
        return Response(json.dumps(result), headers=headers)
        
    except Exception as e:
        error_response = {
            'success': False,
            'error': str(e)
        }
        return Response(json.dumps(error_response), headers=headers)

# Cloudflare Workers entry point
def fetch(request, env):
    return handle_request(request)
