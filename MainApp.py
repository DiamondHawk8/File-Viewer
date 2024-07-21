import os
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk, messagebox
import pickle
from ImageViewerApp import ImageViewerApp
from Structures import Collection, SmartImage
import random

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

        # Bind hotkey to hide and show dialog
        self.root.bind('<Control-h>', self.hide_window)


    def initialize_ui(self):
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title("Load Folder")
        self.dialog.geometry("800x600")

        self.frame = tk.Frame(self.dialog)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Whitelist and Blacklist entries
        self.whitelist_label = tk.Label(self.frame, text="Whitelist (comma-separated):")
        self.whitelist_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.whitelist_entry = tk.Entry(self.frame, width=50)
        self.whitelist_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.blacklist_label = tk.Label(self.frame, text="Blacklist (comma-separated):")
        self.blacklist_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.blacklist_entry = tk.Entry(self.frame, width=50)
        self.blacklist_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Button to load folder
        self.select_folder_button = tk.Button(self.frame, text="Select Folder", command=self.select_folder)
        self.select_folder_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Button to load collections
        self.load_collections_button = tk.Button(self.frame, text="Load Collections", command=self.load_collections)
        self.load_collections_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Add a Treeview to display the folder structure
        self.tree = ttk.Treeview(self.frame)
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)

        # Save and Load buttons
        self.save_button = tk.Button(self.frame, text="Save Data", command=self.save_all_image_data)
        self.save_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.load_button = tk.Button(self.frame, text="Load Data", command=self.load_all_image_data)
        self.load_button.grid(row=5, column=1, padx=10, pady=5, sticky=tk.E)

        # Session Save and Load buttons
        self.save_session_button = tk.Button(self.frame, text="Save Session", command=self.save_session)
        self.save_session_button.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        self.load_session_button = tk.Button(self.frame, text="Load Session", command=self.load_session)
        self.load_session_button.grid(row=6, column=1, padx=10, pady=5, sticky=tk.E)

        # Auto-load checkbox
        self.auto_load_var = tk.BooleanVar(value=True)
        self.auto_load_checkbox = tk.Checkbutton(self.frame, text="Automatically Load Data", variable=self.auto_load_var)
        self.auto_load_checkbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Allow the Treeview to expand
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select Folder")
        if self.folder_path:
            print(f"Selected folder: {self.folder_path}")
            self.collections = []
            new_collection = Collection(self.folder_path, os.path.basename(self.folder_path))
            new_collection.load_groups()
            self.collections.append(new_collection)
            self.display_collections_in_treeview()


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

            if not self.image_viewer_app:
                self.image_viewer_app = ImageViewerApp(self.root, self.update_widgets)

            self.image_viewer_app.load_collections(folder_path, whitelist=whitelist, blacklist=blacklist)
            self.display_collections_in_treeview()
            self.hide_window()  # Automatically hide window
            self.root.deiconify()  # Show the main window now that groups have been loaded

            # Automatically load data if the checkbox is checked
            if self.auto_load_var.get():
                self.load_all_image_data()

    def load_collections(self):
        if hasattr(self, 'folder_path') and self.folder_path:
            whitelist = self.whitelist_entry.get().split(",")
            blacklist = self.blacklist_entry.get().split(",")

            if whitelist:
                whitelist = [item.strip() for item in whitelist if item.strip()]
            if blacklist:
                blacklist = [item.strip() for item in blacklist if item.strip()]

            self.image_viewer_app = ImageViewerApp(self.root, self.update_widgets)
            self.image_viewer_app.load_collections(self.folder_path, whitelist, blacklist)
            self.display_collections_in_treeview()
            self.hide_window()  # Automatically hide window
            self.root.deiconify()  # Show the main window now that groups have been loaded

            # Automatically load data if the checkbox is checked
            if self.auto_load_var.get():
                self.load_all_image_data()


    def display_collections_in_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for collection in self.collections:
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
        # Create directory structure
        base_dir = "data"
        group_dir = os.path.join(base_dir, image.group)
        self.ensure_directory(group_dir)
        filename = os.path.join(group_dir, os.path.basename(image.path) + ".pkl")
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    def load_image_data(self, image_path, group):
        base_dir = "data"
        group_dir = os.path.join(base_dir, group)
        filename = os.path.join(group_dir, os.path.basename(image_path) + ".pkl")
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                data = pickle.load(f)
                data['path'] = image_path  # Ensure the correct path is used
            return SmartImage(**data)
        return None

    def update_widgets(self, *args, **kwargs):
        # Placeholder method for update callback
        print("Widgets updated with args:", args, "and kwargs:", kwargs)

    def save_all_image_data(self):
        if self.image_viewer_app:
            for collection in self.image_viewer_app.collections:
                for group in collection.groups:
                    for image in group.images:
                        self.save_image_data(image)
            print("All image data saved.")

    def load_all_image_data(self):
        if self.image_viewer_app:
            for collection in self.image_viewer_app.collections:
                for group in collection.groups:
                    for image in group.images:
                        loaded_image = self.load_image_data(image.path, group.name)
                        if loaded_image:
                            image.__dict__.update(loaded_image.__dict__)
            print("All image data loaded.")
        
    def ensure_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)





    def save_session(self):
        session_name = simpledialog.askstring("Save Session", "Enter a name for the session:")
        if session_name:
            use_combined = messagebox.askyesno("Save Session", "Use combined collections?")
            if use_combined:
                collections_to_save = [self.image_viewer_app.collections[0]]  # Combined collection
                print(f"Saving combined collection: {collections_to_save}")
            else:
                collections_to_save = self.image_viewer_app.original_collections  # Original collections
                print(f"Saving original collections: {collections_to_save}")
            
            # Ensure the session directory exists
            session_dir = "sessions"
            if not os.path.exists(session_dir):
                os.makedirs(session_dir)

            # Save the session data
            session_path = os.path.join(session_dir, f"{session_name}.pkl")
            with open(session_path, "wb") as f:
                pickle.dump(collections_to_save, f)
            print(f"Session '{session_name}' saved.")

    def load_session(self):
        filename = filedialog.askopenfilename(title="Select Session File", initialdir="sessions", filetypes=[("Pickle Files", "*.pkl")])
        if filename:
            print(f"Loading session from {filename}")
            with open(filename, "rb") as f:
                loaded_collections = pickle.load(f)
            
            self.image_viewer_app = ImageViewerApp(self.root, self.update_widgets)
            self.image_viewer_app.collections = loaded_collections
            self.image_viewer_app.combine_collections()
            self.display_collections_in_treeview()
            self.hide_window()  # Automatically hide window
            self.root.deiconify()  # Show the main window now that collections have been loaded
            print(f"Session loaded from {filename}")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()