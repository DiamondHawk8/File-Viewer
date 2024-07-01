import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Structures import SmartImage, Group, Collection

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
        current_group = current_collection[self.current_group_index]

        # Make sure that the index is within the bounds of the number of images in a given group
        if self.current_image_index < len(current_collection.groups[self.current_group_index].images):
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

    def next_group(): 
        pass


    def display_image(self, image):

        # Calculate the scaling factor to maintain the aspect ratio
        screen_ratio = self.screen_width / self.screen_height
        image_ratio = image.width / image.height

        if image_ratio > screen_ratio:
            # Image is wider relative to screen
            scale_factor = self.screen_width / image.width
        else:
            # Image is taller relative to screen
            scale_factor = self.screen_height / image.height


       # new_width = int(image.width * scale_factor * self.zoom_level)
       # new_height = int(image.height * scale_factor * self.zoom_level)

        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)

        # Resize the image maintaining the aspect ratio
        image = image.resize((new_width, new_height), Image.LANCZOS)

        img = ImageTk.PhotoImage(image) 
        print(f"Displaying image: {img}")  # Debug print
        self.image_label.config(image = img)
        self.image_label.image = img

    def zoom_in(self, event=None):
        self.zoom_level += 0.01  # Increase zoom level
        self.display_image(self.image)

    def zoom_out(self, event=None):
        if self.zoom_level > 0.01:
            self.zoom_level -= 0.01  # Decrease zoom level
            self.display_image(self.image)


    # consider adding an update method to refresh all of the variables and placed images/widgets



def testing_method1(event):
        print("Test method 1 called")

def testing_method2():
    smartImage = SmartImage(r"C:\Users\darks\Downloads\image0.jpg", r"a pic")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
