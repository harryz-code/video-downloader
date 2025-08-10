import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import threading
from urllib.parse import urlparse

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("700x500")  # Increased window size
        self.root.resizable(True, True)  # Allow resizing
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame with better padding
        main_frame = ttk.Frame(root, padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive layout
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Downloader", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 25))
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.url_entry = ttk.Entry(main_frame, width=55, font=("Arial", 10))
        self.url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Download location
        ttk.Label(main_frame, text="Download to:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.location_entry = ttk.Entry(main_frame, width=45, font=("Arial", 10))
        self.location_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        self.location_entry.insert(0, os.path.expanduser("~/Downloads"))
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_location, width=12)
        browse_btn.grid(row=2, column=2, padx=(10, 0), pady=8)
        
        # Quality selection
        ttk.Label(main_frame, text="Quality:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                    values=["best", "worst", "720p", "480p", "360p", "auto"], 
                                    state="readonly", width=18, font=("Arial", 10))
        quality_combo.grid(row=3, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        # List formats button
        list_formats_btn = ttk.Button(main_frame, text="List Available Formats", 
                                     command=self.list_formats, width=20)
        list_formats_btn.grid(row=3, column=2, padx=(10, 0), pady=8)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download Video", 
                                      command=self.start_download, style="Accent.TButton", width=25)
        self.download_btn.grid(row=4, column=0, columnspan=3, pady=25)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Download Progress", padding="15")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar with percentage
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Progress details
        self.progress_details = ttk.Label(progress_frame, text="Ready to download", 
                                        font=("Arial", 9), foreground="gray")
        self.progress_details.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready to download", 
                                     font=("Arial", 10, "bold"))
        self.status_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Download info
        self.download_info = ttk.Label(progress_frame, text="", 
                                     font=("Arial", 9), foreground="blue")
        self.download_info.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # Initialize progress variables
        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.download_speed = "0 B/s"
        self.eta = "Unknown"
        
    def browse_location(self):
        folder = filedialog.askdirectory()
        if folder:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, folder)
    
    def validate_url(self, url):
        """Basic URL validation"""
        if not url:
            return False
        
        # Check if it's a YouTube URL
        parsed = urlparse(url)
        return 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc
    
    def start_download(self):
        url = self.url_entry.get().strip()
        download_path = self.location_entry.get().strip()
        
        if not self.validate_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        if not download_path or not os.path.exists(download_path):
            messagebox.showerror("Error", "Please select a valid download location")
            return
        
        # Reset progress
        self.progress['value'] = 0
        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.download_speed = "0 B/s"
        self.eta = "Unknown"
        
        # Disable download button and show progress
        self.download_btn.config(state='disabled')
        self.status_label.config(text="Starting download...")
        self.progress_details.config(text="Initializing...")
        self.download_info.config(text="")
        
        # Start download in thread
        download_thread = threading.Thread(target=self.download_video, args=(url, download_path))
        download_thread.daemon = True
        download_thread.start()
    
    def list_formats(self):
        """List available formats for the video"""
        url = self.url_entry.get().strip()
        if not self.validate_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL first")
            return
        
        # Start format fetching in thread
        format_thread = threading.Thread(target=self.fetch_formats, args=(url,))
        format_thread.daemon = True
        format_thread.start()
        
        # Show progress
        self.progress.start()
        self.status_label.config(text="Fetching available formats...")
    
    def fetch_formats(self, url):
        """Fetch available formats using yt-dlp"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                title = info.get('title', 'Unknown Video')
                
                # Format the formats list for display
                formatted_formats = []
                for fmt in formats:
                    if fmt.get('height') and fmt.get('ext'):
                        quality = f"{fmt['height']}p" if fmt['height'] else "Unknown"
                        ext = fmt['ext']
                        filesize = fmt.get('filesize')
                        if filesize:
                            size_mb = f"{filesize / (1024*1024):.1f} MB"
                        else:
                            size_mb = "Unknown size"
                        formatted_formats.append(f"{quality} ({ext}) - {size_mb}")
                
                # Update UI on main thread
                self.root.after(0, self.show_formats, formatted_formats, title)
                
        except Exception as e:
            self.root.after(0, self.show_formats_error, str(e))
    
    def show_formats(self, formats, title):
        """Show available formats in a new window"""
        self.progress.stop()
        self.status_label.config(text="Ready to download")
        
        format_window = tk.Toplevel(self.root)
        format_window.title(f"Available Formats - {title}")
        format_window.geometry("500x400")
        format_window.resizable(True, True)
        
        # Title
        title_label = ttk.Label(format_window, text=f"Available Formats for:\n{title}", 
                               font=("Arial", 12, "bold"), wraplength=450)
        title_label.pack(pady=15)
        
        # Scrollable text widget
        text_frame = ttk.Frame(format_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if formats:
            text_widget.insert(tk.END, "Available formats:\n\n")
            for fmt in formats:
                text_widget.insert(tk.END, f"• {fmt}\n")
        else:
            text_widget.insert(tk.END, "No formats found or video extraction failed.")
        
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = ttk.Button(format_window, text="Close", command=format_window.destroy)
        close_btn.pack(pady=15)
    
    def show_formats_error(self, error_msg):
        """Show error when fetching formats fails"""
        self.progress.stop()
        self.status_label.config(text="Failed to fetch formats")
        messagebox.showerror("Error", f"Failed to fetch formats:\n\n{error_msg}")
    
    def download_video(self, url, download_path):
        try:
            # Configure yt-dlp options with better format handling
            quality = self.quality_var.get()
            
            if quality == "auto":
                # Let yt-dlp automatically choose the best available format
                format_spec = "best"
            elif quality in ["720p", "480p", "360p"]:
                # Try specific quality, fallback to best if not available
                height = quality[:-1]  # Remove 'p' to get just the number
                format_spec = f"best[height<={height}],best"
            else:
                format_spec = quality
            
            # First attempt with standard options
            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'format': format_spec,
                'progress_hooks': [self.progress_hook],
                'ignoreerrors': False,
                'no_warnings': False,
                'extractaudio': False,  # Don't extract audio only
                'audioformat': 'mp3',
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                # Update UI on success
                self.root.after(0, self.download_complete, True)
                return
            except Exception as first_error:
                # If first attempt fails, try with more aggressive options
                self.root.after(0, lambda: self.status_label.config(text="First attempt failed, trying alternative method..."))
                
                # Try with different format selection
                fallback_opts = {
                    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                    'format': 'best',  # Just use best available
                    'progress_hooks': [self.progress_hook],
                    'ignoreerrors': False,
                    'no_warnings': False,
                    'extractaudio': False,
                }
                
                with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                    ydl.download([url])
                
                # Update UI on success
                self.root.after(0, self.download_complete, True)
            
        except Exception as e:
            # Update UI on error
            self.root.after(0, self.download_complete, False, str(e))
    
    def progress_hook(self, d):
        """Real-time progress tracking"""
        if d['status'] == 'downloading':
            # Update progress bar
            if '_percent_str' in d:
                try:
                    percent = float(d['_percent_str'].replace('%', ''))
                    self.root.after(0, lambda: self.progress.config(value=percent))
                except:
                    pass
            
            # Update downloaded/total bytes
            if '_downloaded_bytes_str' in d and '_total_bytes_str' in d:
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 0)
                
                if total > 0:
                    self.downloaded_bytes = downloaded
                    self.total_bytes = total
                    
                    # Calculate percentage
                    percent = (downloaded / total) * 100
                    self.root.after(0, lambda: self.progress.config(value=percent))
                    
                    # Update progress details
                    downloaded_mb = downloaded / (1024*1024)
                    total_mb = total / (1024*1024)
                    progress_text = f"Downloaded: {downloaded_mb:.1f} MB / {total_mb:.1f} MB ({percent:.1f}%)"
                    self.root.after(0, lambda: self.progress_details.config(text=progress_text))
            
            # Update speed and ETA
            if '_speed_str' in d:
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                
                info_text = f"Speed: {speed} | ETA: {eta}"
                self.root.after(0, lambda: self.download_info.config(text=info_text))
            
            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Downloading..."))
        
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.status_label.config(text="Processing..."))
    
    def download_complete(self, success, error_msg=""):
        self.progress.stop()
        self.download_btn.config(state='normal')
        
        if success:
            self.progress.config(value=100)
            self.status_label.config(text="Download completed successfully!")
            self.progress_details.config(text="Video saved to your download folder")
            self.download_info.config(text="")
            messagebox.showinfo("Success", "Video downloaded successfully!")
        else:
            # Clean up error message for better display
            clean_error = error_msg.replace('[0;31mERROR:', '').replace('[0m', '').strip()
            self.status_label.config(text=f"Download failed: {clean_error}")
            self.progress_details.config(text="Please check the URL and try again")
            self.download_info.config(text="")
            messagebox.showerror("Error", f"Download failed:\n\n{clean_error}")

def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
