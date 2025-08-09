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
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Download location
        ttk.Label(main_frame, text="Download to:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.location_entry = ttk.Entry(main_frame, width=40)
        self.location_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.location_entry.insert(0, os.path.expanduser("~/Downloads"))
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_location)
        browse_btn.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Quality selection
        ttk.Label(main_frame, text="Quality:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                    values=["best", "worst", "720p", "480p", "360p", "auto"], 
                                    state="readonly", width=15)
        quality_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # List formats button
        list_formats_btn = ttk.Button(main_frame, text="List Available Formats", 
                                     command=self.list_formats)
        list_formats_btn.grid(row=3, column=2, padx=(5, 0), pady=5)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download Video", 
                                      command=self.start_download, style="Accent.TButton")
        self.download_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to download", 
                                     font=("Arial", 10))
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
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
        
        # Disable download button and show progress
        self.download_btn.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="Downloading...")
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_video, args=(url, download_path))
        thread.daemon = True
        thread.start()
    
    def list_formats(self):
        """List available formats for the video"""
        url = self.url_entry.get().strip()
        
        if not self.validate_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL first")
            return
        
        # Show progress
        self.status_label.config(text="Fetching available formats...")
        self.progress.start()
        
        # Start format listing in separate thread
        thread = threading.Thread(target=self.fetch_formats, args=(url,))
        thread.daemon = True
        thread.start()
    
    def fetch_formats(self, url):
        """Fetch available formats for the video"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Format the formats list for display
                format_list = []
                for f in formats:
                    if f.get('height') and f.get('ext'):
                        quality = f"{f['height']}p"
                        ext = f['ext']
                        filesize = f.get('filesize', 'N/A')
                        if filesize != 'N/A':
                            filesize = f"{filesize / (1024*1024):.1f} MB"
                        format_list.append(f"{quality} ({ext}) - {filesize}")
                
                # Update UI with formats
                self.root.after(0, self.show_formats, format_list, info.get('title', 'Unknown'))
                
        except Exception as e:
            self.root.after(0, self.show_formats_error, str(e))
    
    def show_formats(self, formats, title):
        """Display available formats in a new window"""
        self.progress.stop()
        self.status_label.config(text="Formats fetched successfully")
        
        # Create new window to show formats
        format_window = tk.Toplevel(self.root)
        format_window.title(f"Available Formats - {title}")
        format_window.geometry("500x400")
        format_window.resizable(True, True)
        
        # Title
        title_label = ttk.Label(format_window, text=f"Available Formats for: {title}", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=10)
        
        # Formats list
        frame = ttk.Frame(format_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create text widget with scrollbar
        text_widget = tk.Text(frame, wrap=tk.WORD, height=15)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert formats
        if formats:
            text_widget.insert(tk.END, "Available formats:\n\n")
            for fmt in formats:
                text_widget.insert(tk.END, f"• {fmt}\n")
        else:
            text_widget.insert(tk.END, "No formats found or video extraction failed.")
        
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = ttk.Button(format_window, text="Close", command=format_window.destroy)
        close_btn.pack(pady=10)
    
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
        if d['status'] == 'downloading':
            # You could update progress here if needed
            pass
    
    def download_complete(self, success, error_msg=""):
        self.progress.stop()
        self.download_btn.config(state='normal')
        
        if success:
            self.status_label.config(text="Download completed successfully!")
            messagebox.showinfo("Success", "Video downloaded successfully!")
        else:
            # Clean up error message for better display
            clean_error = error_msg.replace('[0;31mERROR:', '').replace('[0m', '').strip()
            self.status_label.config(text=f"Download failed: {clean_error}")
            messagebox.showerror("Error", f"Download failed:\n\n{clean_error}")

def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
