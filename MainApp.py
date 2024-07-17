import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pickle
from ImageViewerApp import ImageViewerApp
from Structures import SmartImage


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer Main Application")

        # Initially withdraw the main window
        self.root.withdraw()

        # Initialize attributes
        self.image_viewer_app = None
        self.collections = []

        self.initialize_ui()

        # Boolean for visibility
        self.hidden = False

    def initialize_ui(self):
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title("Load Folder")
        self.dialog.geometry("400x300")

        self.frame = tk.Frame(self.dialog)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Entry for whitelist
        self.whitelist_label = tk.Label(self.frame, text="Whitelist (comma-separated):")
        self.whitelist_label.pack(padx=10, pady=5)
        self.whitelist_entry = tk.Entry(self.frame, width=50)
        self.whitelist_entry.pack(padx=10, pady=5)

        # Entry for blacklist
        self.blacklist_label = tk.Label(self.frame, text="Blacklist (comma-separated):")
        self.blacklist_label.pack(padx=10, pady=5)
        self.blacklist_entry = tk.Entry(self.frame, width=50)
        self.blacklist_entry.pack(padx=10, pady=5)

        # Button to load folder
        self.load_button = tk.Button(self.frame, text="Load Folder", command=self.load_folder)
        self.load_button.pack(padx=10, pady=10)

        # Bind hotkey to hide and show dialog
        self.root.bind('<Control-h>', self.hide_window)

        # Add a Treeview to display the folder structure
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def hide_window(self, event=None):
        if not self.hidden:
            self.dialog.withdraw()
        else:
            self.dialog.deiconify()
        self.hidden = not self.hidden

    def load_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            whitelist = self.whitelist_entry.get().split(",")
            blacklist = self.blacklist_entry.get().split(",")

            if whitelist:
                whitelist = [item.strip() for item in whitelist if item.strip()]
            if blacklist:
                blacklist = [item.strip() for item in blacklist if item.strip()]

            self.image_viewer_app = ImageViewerApp(self.root, self.update_widgets)
            self.image_viewer_app.load_collections(folder_path, whitelist, blacklist)
            self.display_collections_in_treeview()
            self.dialog.withdraw()  # Hide the dialog after loading the folder
            self.root.deiconify()   # Show the main window

    def display_collections_in_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for collection in self.image_viewer_app.collections:
            col_id = self.tree.insert("", tk.END, text=collection.name)
            for group in collection.groups:
                group_id = self.tree.insert(col_id, tk.END, text=group.name)
                for image in group.images:
                    self.tree.insert(group_id, tk.END, text=image.name)

    def save_image_data(self, image):
        data = {
            "path": image.path,
            "name": image.name,
            "group": image.group,
            "default_zoom_level": image.default_zoom_level,
            "default_panx": image.default_panx,
            "default_pany": image.default_pany,
            "series": image.series,
            "index": image.index,
            "offset": image.offset,
            "weight": image.weight,
            "tags": image.tags,
            "favorite": image.favorite,
            "preconfig": image.preconfig,
        }
        filename = os.path.basename(image.path) + ".pkl"
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    def load_image_data(self, image_path):
        filename = os.path.basename(image_path) + ".pkl"
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                data = pickle.load(f)
            return SmartImage(**data)
        return None

    def update_widgets(self, *args, **kwargs):
        # Placeholder method for update callback
        print("Widgets updated with args:", args, "and kwargs:", kwargs)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()