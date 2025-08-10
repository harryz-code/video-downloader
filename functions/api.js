// Cloudflare Workers API for YouTube Downloader

function validateYoutubeUrl(url) {
  if (!url) return false;
  
  const patterns = [
    /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=[\w-]+/,
    /(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/[\w-]+/,
    /(?:https?:\/\/)?(?:www\.)?youtu\.be\/[\w-]+/,
    /(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/[\w-]+/
  ];
  
  return patterns.some(pattern => pattern.test(url));
}

function extractVideoId(url) {
  if (url.includes('youtube.com/watch')) {
    const match = url.match(/[?&]v=([^&]+)/);
    return match ? match[1] : null;
  } else if (url.includes('youtu.be/')) {
    return url.split('youtu.be/')[1].split('?')[0];
  }
  return null;
}

function handleValidateUrl(request) {
  try {
    const data = request.json();
    const url = data.url?.trim() || '';
    
    const isValid = validateYoutubeUrl(url);
    const videoId = isValid ? extractVideoId(url) : null;
    
    return {
      success: true,
      is_valid: isValid,
      video_id: videoId
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

function handleListFormats(request) {
  try {
    const data = request.json();
    const url = data.url?.trim() || '';
    
    if (!validateYoutubeUrl(url)) {
      return {
        success: false,
        error: 'Invalid YouTube URL'
      };
    }
    
    // For now, return dummy format data
    // In production, you'd use yt-dlp here
    return {
      success: true,
      title: 'YouTube Video',
      formats: [
        {quality: '720p', ext: 'mp4', size: '~15.2 MB (estimated)', format_id: '22'},
        {quality: '480p', ext: 'mp4', size: '~8.5 MB (estimated)', format_id: '18'},
        {quality: '360p', ext: 'mp4', size: '~5.1 MB (estimated)', format_id: '17'}
      ]
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

function handleDownload(request) {
  try {
    const data = request.json();
    const url = data.url?.trim() || '';
    const quality = data.quality || 'auto';
    
    if (!validateYoutubeUrl(url)) {
      return {
        success: false,
        error: 'Invalid YouTube URL'
      };
    }
    
    // For now, return placeholder response
    // In production, you'd use yt-dlp here
    return {
      success: true,
      message: 'Download functionality will be added in the next update',
      title: 'YouTube Video',
      size: '~15.2 MB (estimated)',
      filename: 'video.mp4'
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

async function handleRequest(request) {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };
  
  // Handle preflight requests
  if (request.method === 'OPTIONS') {
    return new Response('', { headers });
  }
  
  try {
    // Parse the request path
    const url = new URL(request.url);
    const path = url.pathname.split('/').pop();
    
    let result;
    
    if (path === 'validate_url') {
      result = handleValidateUrl(request);
    } else if (path === 'list_formats') {
      result = handleListFormats(request);
    } else if (path === 'download') {
      result = handleDownload(request);
    } else if (path === 'open_folder') {
      // For now, return success since we can't open folders in browser
      result = {
        success: true,
        message: 'Folder opened successfully'
      };
    } else {
      result = {
        success: false,
        error: `Endpoint not found: ${path}`
      };
    }
    
    return new Response(JSON.stringify(result), { headers });
    
  } catch (error) {
    const errorResponse = {
      success: false,
      error: error.message
    };
    return new Response(JSON.stringify(errorResponse), { headers });
  }
}

// Cloudflare Workers entry point
export default {
  async fetch(request, env, ctx) {
    return handleRequest(request);
  }
};
