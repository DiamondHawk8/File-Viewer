import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from Structures import SmartImage, Group, Collection
from UIManager import UIManager
# Full path to current image: self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]

# TODO close groups and reopen
# TODO fix the way transparent images display (potentially offer different bg options)
# TODO Tag adding widget, with tag application within range or applied to entire group
# TODO gif structure
# TODO revise group structure to be able to take in a list of groups that it should open
# TODO Preloading if program is slow

        

class ImageViewerApp:
    def __init__(self, root):
        
        self.root = root

        # Attribute to represent a list of collections
        self.collections = []
        
        # Configurations to make it fullscreen and the background grey
        root.attributes('-fullscreen', True)
        root.configure(bg='grey') 
        
        # Store screen width and height
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Set title and set width and height
        self.root.title("Image Viewer")
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')

        # Universal string variable (not currently in use)
        self.entry_var = tk.StringVar()

        # Create and place base image widget
        self.create_widgets()
        self.layout_widgets()

        # Layout the more advanced widgets
        self.ui_manager = UIManager(root, self.update_widgets)
        self.ui_manager.layout_widgets()

        # Bind keys to respective functions
        self.initialize_keybinds()

        self.load_collections("ZTakeoutTest\Takeout\Drive")
        self.trim_groups()
        # Create notebook with groups from current collection
        if self.collections:
            self.ui_manager.create_notebook(self.collections[self.current_collection_index].groups) 

        # Boolean value for whether or not warning/confirmation dialogs should show
        self.show_dialogs = True

        # Boolean value for whether or not images should wrap arond when the index goes out of range
        self.image_wrap = False

        # print_collection_details(self.collections[0])

    def load_collections(self, folder_path=None, *collections):
        if folder_path:
            # Create a new Collection from the folder path and add it to the list
            new_collection = Collection(folder_path, "New Collection")
            new_collection.load_groups()
            self.collections.append(new_collection)
            

        for collection in collections:
            # Add existing Collection objects to the list
            if isinstance(collection, Collection):
                self.collections.append(collection)

        # Set initial indices for navigation if colletions has any Collection objects
        if self.collections:
            self.current_collection_index = 0
            self.current_group_index = 0
            self.current_image_index = 0

            
            """
            When switching groups, it is neccesary to maintain the index of the image the user was looking at for that particular group.
            Therefore, the stored_indicies attribute maintains a dictionary of the group path to its respective index
            """
            self.stored_indices = {}
            self.display_current_image()

    def create_widgets(self):

        # Label that holds the image
        self.image_label = tk.Label(self.root, padx = 0, pady = 0, bg = 'grey')

        
    def layout_widgets(self):
        self.image_label.pack()

    def update_widgets(self, mode=None, tags=None, start=None, end=None):
        print(f"AT UPDATE, MODE: {mode}")
        if mode == "add_group":
            self.add_tags_to_group(tags)
        elif mode == "add_range":
            self.add_tags_to_range(tags, start, end)
        elif mode == "add_current":
            print("AAA")
            self.add_tags_to_current(tags)
        elif mode == "remove_group":
            self.remove_tags_from_group(tags)
        elif mode == "remove_range":
            self.remove_tags_from_range(tags, start, end)
        elif mode == "remove_current":
            self.remove_tags_from_current(tags)
        
        # Kinda lazy, but im just going to leave this here, its to make the notebook reflect what group you're in
        current_group_name = self.collections[self.current_collection_index].groups[self.current_group_index].name
        self.ui_manager.update_notebook(current_group_name)

    def initialize_keybinds(self):

        self.root.bind('<Up>', self.zoom_in)
        self.root.bind('<Down>', self.zoom_out)

        self.root.bind('<Left>', self.previous_image)
        self.root.bind('<Right>', self.next_image)

        self.root.bind('<Control-Shift-Tab>', self.previous_group)
        self.root.bind('<Control-Tab>', self.next_group)

        self.root.bind('<a>', self.pan_left)
        self.root.bind('<d>', self.pan_right)
        self.root.bind('<w>', self.pan_up)
        self.root.bind('<s>', self.pan_down)

        self.root.bind('<Control-r>', self.reset)

        # Lowercase binds
        self.root.bind('<Control-Shift-s>', self.save_default_configuration)
        self.root.bind('<Control-s>', self.save_configuration)
        self.root.bind('<Control-l>', self.load_configuration)
        # Capital binds
        self.root.bind('<Control-Shift-S>', self.save_default_configuration)
        self.root.bind('<Control-S>', self.save_configuration)
        self.root.bind('<Control-L>', self.load_configuration)
        self.root.bind('<Control-Shift-R>', self.default_reset)

        self.root.bind('<Control-d>', self.toggle_dialogs)

        self.root.bind('<Control-f>', self.toggle_favorite)

        # --- UI binds ---
        self.root.bind('<Control-Key-1>', self.ui_manager.toggle_notebook)
        self.root.bind('<Control-Key-2>', self.ui_manager.toggle_details)
        self.root.bind('<Control-Key-3>', self.ui_manager.toggle_adv_details)
        self.root.bind('<Control-Key-4>', self.ui_manager.toggle_controls)
        self.root.bind('<Control-Key-5>', self.ui_manager.toggle_tag)
     
        # Notebook/tab binding
        self.ui_manager.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Testing
        self.root.bind('<Control-Right>', self.force_next_image)
        self.root.bind('<Control-p>', self.print_tags)

        # Locked
        self.root.bind('<Control-a>', self.lock_keybind)
        
    def trim_groups(self):
        # Method for deleting empty groups
        for collection in self.collections:
            for group in collection.groups[:]:  
                if group.images == []:
                    collection.groups.remove(group)

    def lock_keybind(self, event = None):
        return
# ----------------Display Methods----------------

    def display_current_image(self, event = None):

        # Access the current collection
        current_collection = self.collections[self.current_collection_index]
        # Access the current group
        current_group = current_collection.groups[self.current_group_index]

        # Make sure that the index is within the bounds of the number of images in a given group
        if self.current_image_index < len(current_group.images):
            # Retrieve the image at the specified index
            smart_image = current_group.images[self.current_image_index]
            self.display_image(smart_image)
            self.ui_manager.update_image_details(smart_image)

    def next_image(self, event = None):
        
        # Access the current collection
        current_collection = self.collections[self.current_collection_index]

        self.current_image_index += 1

        # If the index exceeds the number of images in the group
        if self.current_image_index >= len(current_collection.groups[self.current_group_index].images):
            # Wrap Around to the first image in the group
            self.current_image_index = 0
        
        # Display image
        self.display_current_image()

    def previous_image(self, event = None):
        
        # Access the current collection
        current_collection = self.collections[self.current_collection_index]

        self.current_image_index -= 1

        # If the index goes below zero
        if self.current_image_index < 0:
            # Wrap Around to the last image in the group
            self.current_image_index = len(current_collection.groups[self.current_group_index].images) - 1

        # Display image
        self.display_current_image()

    def next_group(self, event = None):
        # Access the current collection
        current_collection = self.collections[self.current_collection_index]
        # Access the current group
        current_group = current_collection.groups[self.current_group_index]

        # Store the current index of the group being swapped from
        self.stored_indices.update({current_group.name : self.current_image_index})

        self.current_group_index += 1

        # If the index exceeds the number of groups in the collection
        if self.current_group_index >= len(current_collection.groups):
            # Wrap around to the first group in the collection
            self.current_group_index = 0
        
        # Check to see if the new group has a stored index, and if so, set current index to such
        if current_collection.groups[self.current_group_index].name in self.stored_indices:
            self.current_image_index = self.stored_indices[current_collection.groups[self.current_group_index].name]
        else:
            self.current_image_index = 0

        # Display image from next group
        self.display_current_image()
            
    def previous_group(self, event = None):
        # Access the current collection
        current_collection = self.collections[self.current_collection_index]
        # Access the current group
        current_group = current_collection.groups[self.current_group_index]

        # Store the current index of the group being swapped from
        self.stored_indices.update({current_group.name : self.current_image_index})

        self.current_group_index -= 1

        # If the index goes below zero
        if self.current_group_index < 0:
            # Wrap around to the last group in the collection
            self.current_group_index = len(current_collection.groups) - 1
        
        # Check to see if the new group has a stored index, and if so, set current index to such
        if current_collection.groups[self.current_group_index].name in self.stored_indices:
            self.current_image_index = self.stored_indices[current_collection.groups[self.current_group_index].name]
        else:
            self.current_image_index = 0

        # Display image from next group
        self.display_current_image()
        
    def display_image(self, smart_image):

        # Open the image using the path from the SmartImage object
        image = Image.open(smart_image.path)

        # Retrieve zoom level, panx, and pany from the SmartImage object
        zoom_level = smart_image.zoom_level
        panx = smart_image.panx
        pany = smart_image.pany

        # Calculate the scaling factor to maintain the aspect ratio
        screen_ratio = self.screen_width / self.screen_height
        image_ratio = image.width / image.height

        if image_ratio > screen_ratio:
            # Image is wider relative to screen
            scale_factor = self.screen_width / image.width
        else:
            # Image is taller relative to screen
            scale_factor = self.screen_height / image.height

        # Calculate new dimensions with zoom level
        new_width = int(image.width * scale_factor * zoom_level)
        new_height = int(image.height * scale_factor * zoom_level)

        # Resize the image maintaining the aspect ratio
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Create a new blank image with the same size as the screen to apply pan
        result_image = Image.new("RGB", (self.screen_width, self.screen_height), (128, 128, 128))
        
        # Calculate the position to paste the image onto the blank image
        paste_x = (self.screen_width - new_width) // 2 + panx
        paste_y = (self.screen_height - new_height) // 2 + pany

        # Paste the resized image onto the blank image
        result_image.paste(image, (paste_x, paste_y))

        # Convert the final image to a PhotoImage for displaying in the label
        img = ImageTk.PhotoImage(result_image)
        self.image_label.config(image=img)
        self.image_label.image = img

# ----------------Transformation Methods----------------

    def zoom_in(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        current_image.zoom_level += 0.01  # Increase zoom level
        self.display_current_image()

    def zoom_out(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        if current_image.zoom_level > 0.01:
            current_image.zoom_level -= 0.01  # Decrease zoom level
            self.display_current_image()

    def pan_left(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        current_image.panx -= 5
        self.display_current_image()

    def pan_right(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        current_image.panx += 5
        self.display_current_image()

    def pan_up(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        current_image.pany -= 5
        self.display_current_image()

    def pan_down(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        current_image.pany += 5
        self.display_current_image()

# ----------------Configuaration Management Methods----------------

    def toggle_favorite(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        current_image.toggle_favorite()
        self.ui_manager.update_image_details(current_image)

    def toggle_dialogs(self, event=None):
        self.show_dialogs = not self.show_dialogs

    def reset(self, event=None):
        """Reset's current image view to default zoom and pan"""
        print("reset called")
        if self.show_dialogs:
            response = messagebox.askokcancel(title="Yes No", message="Do you want to reset this image to its default configuration?")
            if response:
                current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
                current_image.panx = current_image.default_panx
                current_image.pany = current_image.default_pany
                current_image.zoom_level = current_image.default_zoom_level
                self.display_current_image()
            else:   
                return
        else:
            current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
            current_image.panx = current_image.default_panx
            current_image.pany = current_image.default_pany
            current_image.zoom_level = current_image.default_zoom_level
            self.display_current_image()

    def save_default_configuration(self, event=None):
        """Save's whatever the current pan and zoom values are as the default for the image"""
        print("save_default_configuration called")
        if self.show_dialogs:
            current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
            response = messagebox.askokcancel(title="Confirm", message="Are you sure you want to save these parameters as the default configuration? "
                                        f"\n Pan x: {current_image.panx} Pan y: {current_image.pany} Zoom: {current_image.zoom_level}" )
            if response:
                current_image.default_panx = current_image.panx
                current_image.default_pany = current_image.pany
                current_image.default_zoom_level = current_image.zoom_level
            else:   
                return
        else:
            current_image.default_panx = current_image.panx
            current_image.default_pany = current_image.pany
            current_image.default_zoom_level = current_image.zoom_level

    def save_configuration(self, event=None):
        print("save_configuration called")
        if self.show_dialogs:
            current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
            response = messagebox.askokcancel(title="Confirm", message="Are you sure you want to save these parameters as a pre-configuration? "
                                        f"\n Pan x: {current_image.panx} Pan y: {current_image.pany} Zoom: {current_image.zoom_level}" )
            if response:
                # Ensure the preconfig list is initialized and has at least 3 elements
                if not hasattr(current_image, 'preconfig') or len(current_image.preconfig) < 3:
                    current_image.preconfig = [0, 0, 1.0]  

                current_image.preconfig[0] = current_image.panx
                current_image.preconfig[1] = current_image.pany
                current_image.preconfig[2] = current_image.zoom_level
            else:   
                return
        else:
            # Ensure the preconfig list is initialized and has at least 3 elements
            if not hasattr(current_image, 'preconfig') or len(current_image.preconfig) < 3:
                current_image.preconfig = [0, 0, 1.0]  

            current_image.preconfig[0] = current_image.panx
            current_image.preconfig[1] = current_image.pany
            current_image.preconfig[2] = current_image.zoom_level
    
    def load_configuration(self, event=None):
        print("save_configuration called")
        if self.show_dialogs:
            current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
            response = messagebox.askokcancel(title="Confirm", message="Are you sure you want to load this image's preconfig? "
                                        f"\n Pan x: {current_image.preconfig[0]} Pan y: {current_image.preconfig[1]} Zoom: {current_image.preconfig[2]}" )
            if response:
                current_image.panx = current_image.preconfig[0]
                current_image.pany = current_image.preconfig[1]
                current_image.zoom_level = current_image.preconfig[2]
                self.display_current_image()
            else:   
                return
        else:
            current_image.panx = current_image.preconfig[0]
            current_image.pany = current_image.preconfig[1]
            current_image.zoom_level = current_image.preconfig[2]
            self.display_current_image()

    def default_reset(self, event=None):
        """In case defaults ever get set to bad values, this method will reset them to 0 0 1.0"""
        print("default_reset called")
        # This method will always show dialogs
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        response = messagebox.askokcancel(title="Confirm", message="Are you sure you want to reset this image to default default?"
                                       f"\n Pan x: 0 Pan y: 0 Zoom:1.0" )
        if response:
            current_image.default_panx = 0
            current_image.default_pany = 0
            current_image.default_zoom_level = 1.0
        else:   
            return
    
# ----------------UI Methods----------------

    def on_tab_change(self, event):
        # Notebook/tab change method
        selected_tab = event.widget.tab(event.widget.select(), "text")

        # Access the current collection
        current_collection = self.collections[self.current_collection_index]
        # Access the current group
        current_group = current_collection.groups[self.current_group_index]

        # Store the current index of the group being swapped from
        self.stored_indices.update({current_group.name : self.current_image_index})

        for i, group in enumerate(self.collections[self.current_collection_index].groups):
            if group.name == selected_tab:
                self.current_group_index = i
                self.display_current_image()
                self.root.focus_set()
                break
    
# ----------------Tag Management ----------------

    def add_tags_to_group(self, tags):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        for image in current_group.images:
            image.add_tag(tags)

    def add_tags_to_range(self, tags, start, end):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        current_index = self.current_image_index

        for i in range(max(0, current_index + start), min(len(current_group.images), current_index + end + 1)):
            current_group.images[i].add_tag(tags)

    def add_tags_to_current(self, tags):
        
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        print(f"TESTING SECOND, adding tags to {current_image}")
        current_image.add_tag(tags)
        self.ui_manager.update_image_details(current_image)

    def remove_tags_from_group(self, tags):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        for image in current_group.images:
            image.remove_tag(tags)

    def remove_tags_from_range(self, tags, start, end):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        current_index = self.current_image_index

        for i in range(max(0, current_index + start), min(len(current_group.images), current_index + end + 1)):
            current_group.images[i].remove_tag(tags)

    def remove_tags_from_current(self, tags):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        current_image.remove_tag(tags)
        self.ui_manager.update_image_details(current_image)

# TESTING ONLY    --------------------------
    def create_test_collection(self):
        # Create some SmartImage instances with placeholder paths
        image1 = SmartImage(path=r"TestCollection\Group1\Cat03 copy 2.jpg", name="Image 1")
        image2 = SmartImage(path=r"TestCollection\Group1\Cat03 copy.jpg", name="Image 2")
        image3 = SmartImage(path=r"TestCollection\Group2\Cat03.jpg", name="Image 3")
        
        # Create a Group and add the images to it
        group1 = Group(folder_path=r"TestCollection\Group1", name="Group 1", images=[image1, image2])
        group2 = Group(folder_path=r"TestCollection\Group2", name="Group 2", images=[image3])
        
        # Create a Collection and add the groups to it
        test_collection = Collection(base_folder_path="TestCollection", name="Test Collection", groups=[group1, group2])
        
        # Add the test collection to the collections list
        self.collections.append(test_collection)

        # Initialize indices and display the first image
        if self.collections:
            self.current_collection_index = 0
            self.current_group_index = 0
            self.current_image_index = 0
            """
            When switching groups, it is neccesary to maintain the index of the image the user was looking at for that particular group.
            Therefore, the stored_indicies attribute maintains a dictionary of the group path to its respective index
            """
            self.stored_indices = {}
            self.display_current_image()

    def force_next_image(self):

        self.current_image_index += 1

        self.display_current_image

    def print_tags(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]
        print(f"Tags for image {current_image.name}: {current_image.tags}")
    
def print_collection_details(collection):
    for group in collection.groups:
        print(f"Group: {group.name}, Depth: {group.depth}, Images: {len(group.images)}")
        for image in group.images:
            print(f"  Image: {image.name}, Path: {image.path}")
        if group.children:
            print_child_groups(group.children)

def print_child_groups(children, level=1):
    for child in children:
        indent = "  " * level
        print(f"{indent}Child Group: {child.name}, Depth: {child.depth}, Images: {len(child.images)}")
        for image in child.images:
            print(f"{indent}  Image: {image.name}, Path: {image.path}")
        if child.children:
            print_child_groups(child.children, level + 1)





def testing_method1(event):
    smartImage = SmartImage(r"C:\Users\darks\Downloads\image0.jpg", r"a pic")
    



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()




