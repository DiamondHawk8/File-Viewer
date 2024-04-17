import os
from tkinter import Tk, Frame
from PIL import Image, ImageTk
import cv2
from bs4 import BeautifulSoup
import json

class MediaViewer:
    def __init__(self, root):
        self.display_area = Frame(root)
        self.display_area.pack()

    def display_image(self, image_path):
        pass

    def display_video(self, video_path):
        pass

    def resize_media(self, media):
        pass