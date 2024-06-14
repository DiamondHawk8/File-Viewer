import tkinter as tk
from tkinter import ttk, filedialog
import vlc
from platform import system

class MediaViewer(tk.Frame):
    """MediaViewer integrates a basic video player into a tkinter frame."""

    def __init__(self, parent):
        """
        Initialize the MediaViewer instance.
        Args:
            parent (tk.Widget): The paent widget, typically the main application window.
        """
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=1)

        # VLC player setup
        self.vlc_instance = vlc.Instance()  # Create a new VLC instance
        self.player = self.vlc_instance.media_player_new()  # Create a new media player for this instance

        # UI setup
        self.video_panel = ttk.Frame(self)  # Frame to hold the video display
        self.canvas = tk.Canvas(self.video_panel, bg='black')  # Canvas where video will be rendered
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.video_panel.pack(fill=tk.BOTH, expand=1)

        # Load media button
        self.load_button = ttk.Button(self, text="Load Media", command=self.load_media)
        self.load_button.pack(side=tk.BOTTOM)

    def load_media(self, file_path=None):
        """
        Load media from a file path or open a file dialog to select media.
        Args:
            file_path (str, optional): Direct path to a media file.
        """
        if not file_path:  # If no file path provided, open a file dialog to select a file
            file_path = filedialog.askopenfilename()

        if file_path:  # If a file path is provided or selected, play the media
            self.play_media(file_path)

    def play_media(self, media_path):
        """
        Play media from the specified path using the VLC media player.
        Args:
            media_path (str): Path to the media file to be played
        """
        media = self.vlc_instance.media_new(media_path)  # Load media at the specified path
        self.player.set_media(media)  # Set the media to be played by the player

        # Set video output to the canvas widget
        if system() == "Windows":
            self.player.set_hwnd(self.canvas.winfo_id())  # Use the Windows handle for video output
        else:
            self.player.set_xwindow(self.canvas.winfo_id())  # Use the X Window ID for video output on Unix-based systems

        self.player.play()  # Start playing the media

def main():
    """Create the main aplication window and run the media viewer."""
    root = tk.Tk()
    root.title("Media Viewer")
    root.geometry("800x600")  # Set the size of the main window
    viewer = MediaViewer(root)  # Create an instance of MediaViewer
    root.mainloop()  # Start the tkinter event loop

if __name__ == "__main__":
    main()  # Run the main function when the script is executed directly