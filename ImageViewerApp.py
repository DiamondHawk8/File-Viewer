import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Structures import SmartImage, Group, Collection

# Full path to current image: self.collections[self.current_collection_index].groups[self.current_group_index].images[self.current_image_index]

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

        # Create and place widgets
        self.create_widgets()
        self.layout_widgets()

        # Bind keys to respective functions
        self.initialize_keybinds()


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

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        # self.filter_button = tk.Button(self.root, text="Apply Grayscale", command=self.apply_filter)

    def layout_widgets(self):
        self.image_label.pack()
        self.load_button.pack(side=tk.LEFT) 
        # self.filter_button.pack(side=tk.LEFT)

    def initialize_keybinds(self):
        self.root.bind('<Return>', testing_method1)
        self.root.bind('<Up>', self.zoom_in)
        self.root.bind('<Down>', self.zoom_out)
        self.root.bind('<Left>', self.previous_image)
        self.root.bind('<Right>', self.next_image)
        self.root.bind('<Control-Shift-Tab>', self.previous_group)
        self.root.bind('<Shift-Tab>', self.next_group)



    def load_image(self):
        """
        file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")],
            parent=self.root
        )
        if file_path:
            self.image = Image.open(file_path)
            print(f"Loaded image: {self.image}")  # Debug print
            self.display_image(self.image)
        """
        # Debugging
        file_path = r"ZTakeoutTest\Takeout\Drive\Images\Cat03.jpg"
        self.image = Image.open(file_path)
        print(f"Loaded image: {self.image}")  # Debug print
        self.display_image(self.image)

    
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



    def zoom_in(self, event=None):
        self.zoom_level += 0.01  # Increase zoom level
        self.display_image(self.image)

    def zoom_out(self, event=None):
        if self.zoom_level > 0.01:
            self.zoom_level -= 0.01  # Decrease zoom level
            self.display_image(self.image)
  

#TODO consider adding an update method to refresh all of the variables and placed images/widgets
#TODO Preloading if program is slow

def testing_method1(event):
    smartImage = SmartImage(r"C:\Users\darks\Downloads\image0.jpg", r"a pic")
    

def testing_method2():
    smartImage = SmartImage(r"C:\Users\darks\Downloads\image0.jpg", r"a pic")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
