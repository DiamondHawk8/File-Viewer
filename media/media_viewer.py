import cv2
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Frame

class MediaViewer:
    def __init__(self, master):
        self.master = master
        self.img_label = Label(master)  # To display images
        self.img_label.pack()

    def display_image(self, image_path):
        """ Load and display an image from the path. """
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=photo)
        self.img_label.image = photo  # Keep a reference!

    def play_video(self, video_path):
        pass

# Sample usage within a GUI context
def main():
    root = Tk()
    viewer = MediaViewer(root)
    viewer.display_image("ZTakeoutTest\Takeout\Drive\Images\Cat03.jpg")  # Path to an image in your takeout
    viewer.play_video("ZTakeoutTest/Takeout/Drive/Videos/A video1.mp4")  # Path to a video in your takeout
    root.mainloop()

if __name__ == '__main__':
    main()