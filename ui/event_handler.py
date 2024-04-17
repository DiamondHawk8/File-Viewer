import os
from tkinter import Tk, Frame
from PIL import Image, ImageTk
import cv2
from bs4 import BeautifulSoup
import json

class EventHandler:
    def on_next_media(self):
        pass

    def on_previous_media(self):
        pass

    def on_tag_assigned(self, file_path, tag):
        pass