import tkinter as tk
import tkinter.ttk as ttk


class UIManager:
    def __init__(self, root, update_callback):
        self.root = root

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Attribute for advanced updates
        self.update_callback = update_callback

        # Create notebook for groups (tab structure) and prevent traversal
        self.notebook = ttk.Notebook(self.root, takefocus=0)

        # Create frames for image details
        self.initialize_detail_frames()

        # Create frame for image control menu
        self.initialize_image_controls_frame()

        # Create frame for tag adding/removing menu
        self.initialize_tag_frame()

        self.layout_widgets()

        # Boolean attributes for toggleable UI elements
        self.details_visible = False
        self.details_adv_visible = False
        self.notebook_visible = False
        self.image_controls_visible = False
        self.tag_visible = False


    def create_notebook(self, groups):
        # Add all groups to the notebook
        for group in groups:
            tab = tk.Frame(self.notebook)
            self.notebook.add(tab, text=group.name)
            # print(f"Added {group.name}")

        # Bind arrow keys to prevent tab traversal on notebook so that image traversal keybinds still work
        self.notebook.bind("<Left>", self.lock_keybind)
        self.notebook.bind("<Right>", self.lock_keybind)

    def update_notebook(self, current_group_name):
        for i, tab_id in enumerate(self.notebook.tabs()):
            if self.notebook.tab(tab_id, "text") == current_group_name:
                self.notebook.select(i)
                break

    def initialize_detail_frames(self):
        self.image_details = tk.Frame(self.root, bg="gainsboro", relief=tk.GROOVE, padx=10, pady=10)
        self.image_details_advanced = tk.Frame(self.root, bg="gainsboro", relief=tk.GROOVE, padx=10, pady=10)

        # Basic image details StringVars
        self.name_var = tk.StringVar()
        self.group_var = tk.StringVar()
        self.tags_var = tk.StringVar()
        self.favorite_var = tk.StringVar()

        # Basic image details labels
        self.label_name = tk.Label(self.image_details, text="Name:", bg="gainsboro")
        self.label_group = tk.Label(self.image_details, text="Group:", bg="gainsboro")
        self.label_tags = tk.Label(self.image_details, text="Tags:", bg="gainsboro")
        self.label_favorite = tk.Label(self.image_details, text="Favorite:", bg="gainsboro")

        self.label_name_value = tk.Label(self.image_details, textvariable=self.name_var, bg="gainsboro")
        self.label_group_value = tk.Label(self.image_details, textvariable=self.group_var, bg="gainsboro")
        self.label_tags_value = tk.Label(self.image_details, textvariable=self.tags_var, bg="gainsboro")
        self.label_favorite_value = tk.Label(self.image_details, textvariable=self.favorite_var, bg="gainsboro")

        # Advanced image details StringVars
        self.zoom_var = tk.StringVar()
        self.panx_var = tk.StringVar()
        self.pany_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.series_var = tk.StringVar()
        self.index_var = tk.StringVar()
        self.path_var = tk.StringVar()

        # Advanced image details labels
        self.label_zoom = tk.Label(self.image_details_advanced, text="Zoom Level:", bg="gainsboro")
        self.label_panx = tk.Label(self.image_details_advanced, text="Pan X:", bg="gainsboro")
        self.label_pany = tk.Label(self.image_details_advanced, text="Pan Y:", bg="gainsboro")
        self.label_weight = tk.Label(self.image_details_advanced, text="Weight:", bg="gainsboro")
        self.label_series = tk.Label(self.image_details_advanced, text="Series:", bg="gainsboro")
        self.label_index = tk.Label(self.image_details_advanced, text="Index:", bg="gainsboro")
        self.label_path = tk.Label(self.image_details_advanced, text="Path:", bg="gainsboro")

        self.label_zoom_value = tk.Label(self.image_details_advanced, textvariable=self.zoom_var, bg="gainsboro")
        self.label_panx_value = tk.Label(self.image_details_advanced, textvariable=self.panx_var, bg="gainsboro")
        self.label_pany_value = tk.Label(self.image_details_advanced, textvariable=self.pany_var, bg="gainsboro")
        self.label_weight_value = tk.Label(self.image_details_advanced, textvariable=self.weight_var, bg="gainsboro")
        self.label_series_value = tk.Label(self.image_details_advanced, textvariable=self.series_var, bg="gainsboro")
        self.label_index_value = tk.Label(self.image_details_advanced, textvariable=self.index_var, bg="gainsboro")
        self.label_path_value = tk.Label(self.image_details_advanced, textvariable=self.path_var, bg="gainsboro")

    def initialize_image_controls_frame(self):

        self.controls = tk.Frame(self.root, bg="gainsboro", relief=tk.GROOVE, padx=10, pady=10)
        self.reset_button = tk.Button(self.controls, text="Reset", command=lambda: self.root.event_generate('<Control-r>'))
        self.save_default_button = tk.Button(self.controls, text="Save Default", command=lambda: self.root.event_generate('<Control-Shift-s>'))
        self.save_button = tk.Button(self.controls, text="Save", command=lambda: self.root.event_generate('<Control-s>'))
        self.load_button = tk.Button(self.controls, text="Load", command=lambda: self.root.event_generate('<Control-l>'))
        self.default_reset_button = tk.Button(self.controls, text="Default Reset", command=lambda: self.root.event_generate('<Control-Shift-R>'))

    def initialize_tag_frame(self):

        self.tag = tk.Frame(self.root, bg="gainsboro", relief=tk.GROOVE, padx=10, pady=10)

        # Entry for tags
        self.tag_entry = tk.Entry(self.tag, width=50)
        
        # Checkbutton to apply tags to the entire group
        self.apply_to_group = tk.BooleanVar()
        tk.Checkbutton(self.tag, text="Apply to entire group", variable=self.apply_to_group).pack(side=tk.LEFT, padx=5, pady=5)

        # Entry for range
        self.range_label = tk.Label(self.tag, text="Range (-x, y):")
        
        self.range_entry = tk.Entry(self.tag, width=10)
        
        # Button to add tags
        self.add_tag_button = tk.Button(self.tag, text="Add Tags", command=self.add_tags)

        # Button to remove tags
        self.remove_tag_button = tk.Button(self.tag, text="Remove Tags", command=self.remove_tags)

    def layout_widgets(self):

        # Pack the basic details labels
        self.label_name.grid(row=0, column=0, sticky=tk.W)
        self.label_name_value.grid(row=0, column=1, sticky=tk.W)
        self.label_group.grid(row=1, column=0, sticky=tk.W)
        self.label_group_value.grid(row=1, column=1, sticky=tk.W)
        self.label_tags.grid(row=2, column=0, sticky=tk.W)
        self.label_tags_value.grid(row=2, column=1, sticky=tk.W)
        self.label_favorite.grid(row=3, column=0, sticky=tk.W)
        self.label_favorite_value.grid(row=3, column=1, sticky=tk.W)

        # Pack the advanced details labels
        self.label_zoom.grid(row=0, column=0, sticky=tk.W)
        self.label_zoom_value.grid(row=0, column=1, sticky=tk.W)
        self.label_panx.grid(row=1, column=0, sticky=tk.W)
        self.label_panx_value.grid(row=1, column=1, sticky=tk.W)
        self.label_pany.grid(row=2, column=0, sticky=tk.W)
        self.label_pany_value.grid(row=2, column=1, sticky=tk.W)
        self.label_weight.grid(row=3, column=0, sticky=tk.W)
        self.label_weight_value.grid(row=3, column=1, sticky=tk.W)
        self.label_series.grid(row=4, column=0, sticky=tk.W)
        self.label_series_value.grid(row=4, column=1, sticky=tk.W)
        self.label_index.grid(row=5, column=0, sticky=tk.W)
        self.label_index_value.grid(row=5, column=1, sticky=tk.W)
        self.label_path.grid(row=6, column=0, sticky=tk.W)
        self.label_path_value.grid(row=6, column=1, sticky=tk.W)

        # Controls menu
        self.reset_button.pack(side=tk.LEFT)
        self.save_default_button.pack(side=tk.LEFT)
        self.save_button.pack(side=tk.LEFT)
        self.load_button.pack(side=tk.LEFT)
        self.default_reset_button.pack(side=tk.LEFT)

        # Tag menu
        self.tag_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.range_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.range_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_tag_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.remove_tag_button.pack(side=tk.LEFT, padx=5, pady=5)

    def update_image_details(self, image):
        # Update the basic details
        self.name_var.set(image.name)
        self.group_var.set(image.group)
        self.tags_var.set(", ".join(image.tags))
        self.favorite_var.set("Yes" if image.favorite else "No")

        # Update the advanced details
        self.zoom_var.set(str(image.zoom_level))
        self.panx_var.set(str(image.panx))
        self.pany_var.set(str(image.pany))
        self.weight_var.set(str(image.weight))
        self.series_var.set(image.series)
        self.index_var.set(str(image.index))
        self.path_var.set(str(image.path))

        # Call the update callback to notify ImageViewerApp
        self.update_callback()

    def lock_keybind(self, event):
            return

# ----------------Toggle Methods----------------

    def toggle_details(self, event = None):
        if self.details_visible:
            self.image_details.place_forget()
        else:
            self.image_details.place(anchor=tk.NE, relx=0.95, rely=0.05)
        self.details_visible = not self.details_visible

    def toggle_adv_details(self, event = None):
        if self.details_adv_visible:
            self.image_details_advanced.place_forget()
        else:
            self.image_details_advanced.place(anchor=tk.NW, relx=0, rely=0.05)
        self.details_adv_visible = not self.details_adv_visible

    def toggle_notebook(self, event = None):
        if self.notebook_visible:
            self.notebook.place_forget()
        else:
            self.notebook.place(relx=0.0, rely=0.0, anchor=tk.NW, relwidth=1)
        self.notebook_visible = not self.notebook_visible
    
    def toggle_controls(self, event = None):
        if self.image_controls_visible:
            self.controls.place_forget()
        else:
            self.controls.place(relx=0.0, rely=1.0, anchor=tk.SW, width=290)
        self.image_controls_visible = not self.image_controls_visible

    def toggle_tag(self, event = None):
        if self.tag_visible:
            self.tag.place_forget()
        else:
            self.tag.place(relx = 0.5, rely = 1, anchor = tk.S)


# Other
    def add_tags(self):
            tags = self.tag_entry.get()
            if self.apply_to_group.get():
                self.update_callback("add_group", tags)
            else:
                range_text = self.range_entry.get()
                try:
                    if range_text:
                        start, end = map(int, range_text.split(','))
                        self.update_callback("add_range", tags, start, end)
                    else:
                        self.update_callback("add_current", tags)
                except ValueError:
                    print("Invalid range format. Use '-x,y' format.")

    def remove_tags(self):  
        tags = self.tag_entry.get()
        if self.apply_to_group.get():
            self.update_callback("remove_group", tags)
        else:
            range_text = self.range_entry.get()
            try:
                if range_text:
                    start, end = map(int, range_text.split(','))
                    self.update_callback("remove_range", tags, start, end)
                else:
                    self.update_callback("remove_current", tags)
            except ValueError:
                print("Invalid range format. Use '-x,y' format.")