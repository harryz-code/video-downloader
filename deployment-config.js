// Deployment Configuration for Railway
// This project is optimized for Railway deployment with Python backend

const configs = {
  // Local development
  local: {
    apiBase: 'http://localhost:8080',
    description: 'Local development with Railway backend'
  },
  
  // Railway deployment (production)
  railway: {
    apiBase: '', // Relative URLs work with Railway
    description: 'Railway deployment with Python backend and yt-dlp'
  }
};

// Current deployment mode
const currentMode = 'local'; // Change to 'railway' for production

// Export configuration
window.DEPLOYMENT_CONFIG = {
  ...configs[currentMode],
  mode: currentMode
};

console.log(`🚀 Deployment Mode: ${currentMode}`);
console.log(`📡 API Base: ${configs[currentMode].apiBase || 'Relative URLs'}`);
console.log(`ℹ️  ${configs[currentMode].description}`);
console.log(`🐍 Backend: Python with yt-dlp (Railway optimized)`);
