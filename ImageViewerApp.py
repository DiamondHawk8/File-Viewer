import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        

        self.root.title("Image Viewer")
        self.root.geometry('600x400')

        self.entry_var = tk.StringVar()
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        self.image_label = tk.Label(self.root)
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.filter_button = tk.Button(self.root, text="Apply Grayscale", command=self.apply_filter)

    def layout_widgets(self):
        self.image_label.pack()
        self.load_button.pack(side=tk.LEFT) 
        self.filter_button.pack(side=tk.LEFT)

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
        img = ImageTk.PhotoImage(image) 
        print(f"Displaying image: {img}")  # Debug print
        self.image_label.config(image = img)
        self.image_label.image = img

    def apply_filter(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
