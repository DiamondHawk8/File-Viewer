import tkinter as tk
from tkinter import ttk, filedialog
import vlc
from platform import system

class MediaViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=1)

        # VLC player setup
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        # UI setup
        self.video_panel = ttk.Frame(self)
        self.canvas = tk.Canvas(self.video_panel, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.video_panel.pack(fill=tk.BOTH, expand=1)

        # Controls
        self.load_button = ttk.Button(self, text="Load Media", command=self.load_media)
        self.load_button.pack(side=tk.BOTTOM)

    def load_media(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename()

        if file_path:
            self.play_media(file_path)

    def play_media(self, media_path):
        # Setup media for VLC player
        media = self.vlc_instance.media_new(media_path)
        self.player.set_media(media)

        # Set video output to the widget
        if system() == "Windows":
            self.player.set_hwnd(self.canvas.winfo_id())
        else:
            self.player.set_xwindow(self.canvas.winfo_id())

        self.player.play()

def main():
    root = tk.Tk()
    root.title("Media Viewer")
    root.geometry("800x600")
    viewer = MediaViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()