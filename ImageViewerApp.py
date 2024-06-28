import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

class ImageViewerApp:
    def __init__(self, root):
        
        self.root = root

        root.attributes('-fullscreen', True)
        root.configure(bg='grey') 

        self.zoom_level = 1.0  # Initial zoom level

        # Store screen width and height
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.root.title("Image Viewer")
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')

        self.entry_var = tk.StringVar()
        self.create_widgets()
        self.layout_widgets()
        self.initialize_keybinds()


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

        new_width = int(image.width * scale_factor * self.zoom_level)
        new_height = int(image.height * scale_factor * self.zoom_level)

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


def testing_method1(event):
        print("Test method 1 called")

def testing_method2():
        print("Test method 2 called")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
