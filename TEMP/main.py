import os
from tkinter import Tk, Frame
from PIL import Image, ImageTk
import cv2
from bs4 import BeautifulSoup
import json

from ui.ui_manager import UIManager
from media.media_viewer import MediaViewer
from data_management.file_manager import FileManager

def main():
    app_ui = UIManager()
    app_media = MediaViewer()
    app_files = FileManager()
    

if __name__ == "__main__":
    main()