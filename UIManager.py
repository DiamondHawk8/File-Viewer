import tkinter as tk
import tkinter.ttk as ttk


class UIManager:
    def __init__(self, root, update_callback):
        self.root = root

        # Attribute for advanced updates
        self.update_callback = update_callback

        # Create notebook for groups (tab structure)
        self.notebook = ttk.Notebook(self.root)

        # Create frames for image details
        self.initialize_detail_frames()

        # Boolean attributes for toggleable UI elements
        self.details_visible = False

    def create_notebook(self, groups):
        print("Method called")
        for group in groups:
            tab = tk.Frame(self.notebook)
            self.notebook.add(tab, text=group.name)
            # print(f"Added {group.name}")

        # Bind arrow keys to prevent tab traversal on notebook so that image traversal keybinds still work
        self.notebook.bind("<Left>", self.no_op)
        self.notebook.bind("<Right>", self.no_op)

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
    
    def layout_widgets(self):
        # Pack the frames
       # self.image_details.place(anchor=tk.NE, relx=0.95, rely=0.05)
        #self.image_details_advanced.place(anchor=tk.NW, relx=0, rely=0.05)

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

    def no_op(self, event):
            """No operation event handler to disable key traversal."""
            return "break"

    # TODO make seperate toggles for each
    def toggle_details(self):
        if self.details_visible:
            self.image_details.place_forget()
            self.image_details_advanced.place_forget()
            self.notebook.place_forget()
        else:
            self.image_details.place(anchor=tk.NE, relx=0.95, rely=0.05)
            self.image_details_advanced.place(anchor=tk.NW, relx=0, rely=0.05)
            self.notebook.place(relx=0.5, rely=0.5, anchor=tk.NW)
            self.notebook.lift()
        self.details_visible = not self.details_visible