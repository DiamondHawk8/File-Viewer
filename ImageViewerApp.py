import tkinter as tk
import os
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from Structures import Collection, GifImage
from UIManager import UIManager
import threading


class ImageViewerApp:
    def __init__(self, root, update_widgets_callback):

        self.root = root

        # Lock for use with gifs
        self.lock = threading.Lock()

        # Attribute to represent a list of collections
        self.collections = []

        # Attribute for original list of collections for saving purposes:
        self.original_collections = []

        # Structure for keeping track of the image you were looking at when switching groups
        self.stored_indices = {}

        # Indexing attributes
        self.current_collection_index = 0
        self.current_group_index = 0
        self.current_image_index = 0

        # Attribute to keep track of groups that were closed
        self.closed_groups = []

        # Callback for use with main class:
        self.update_widgets_callback = update_widgets_callback

        # Configurations to make it fullscreen and the background grey
        root.attributes('-fullscreen', True)
        root.configure(bg='grey')

        # Store screen width and height
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Set title and set width and height
        self.root.title("Image Viewer")
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')

        # Create and place base image widget
        self.image_label = tk.Label(self.root, padx=0, pady=0, bg='grey')
        self.layout_widgets()

        # Layout the more advanced widgets
        self.ui_manager = UIManager(root, self.update_widgets)

        # Bind keys to respective functions
        self.initialize_keybinds()

        # Notebook created boolean
        self.notebook = False

        # Boolean value for whether warning/confirmation dialogs should show
        self.show_dialogs = True

        # Boolean value for whether images should wrap around when the index goes out of range
        self.image_wrap = False

        # Bool for disabling typing key keybinds
        self.typing = True

        # Copy of the initial collections for saving purposes
        self.collections_copy = self.collections

        self.update_widgets()

        self.current_gif = None

    def load_collections(self, folder_path=None, whitelist=None, blacklist=None, collections=None):
        if collections is None:
            collections = []
        if folder_path:
            # Extract the folder name to use as the collection name
            collection_name = os.path.basename(folder_path)

            # Create a new Collection from the folder path and add it to the list
            new_collection = Collection(folder_path, collection_name)
            new_collection.load_groups(whitelist=whitelist, blacklist=blacklist)
            self.collections.append(new_collection)

        for collection in collections:
            # Add existing Collection objects to the list
            if isinstance(collection, Collection):
                self.collections.append(collection)

        # Store the original collections as a copy of the current collections
        self.original_collections = self.collections.copy()

        if self.collections:
            self.display_current_image()

    def layout_widgets(self):
        self.image_label.pack()

    def update_widgets(self, mode=None, tags=None, start=None, end=None, zoom_level=None, panx=None, pany=None,
                       default=None, preconfig=None, group_weight=None, group_favorite=None, new_duration=None):
        if mode == "add_group":
            self.add_tags_to_group(tags)
        elif mode == "add_range":
            self.add_tags_to_range(tags, start, end)
        elif mode == "add_current":
            self.add_tags_to_current(tags)
        elif mode == "remove_group":
            self.remove_tags_from_group(tags)
        elif mode == "remove_range":
            self.remove_tags_from_range(tags, start, end)
        elif mode == "remove_current":
            self.remove_tags_from_current(tags)
        elif mode == "apply_group":
            self.apply_zoom_pan_to_group(zoom_level, panx, pany, default, preconfig)
        elif mode == "apply_range":
            self.apply_zoom_pan_to_range(zoom_level, panx, pany, start, end, default, preconfig)
        elif mode == "apply_current":
            self.apply_zoom_pan_to_current(zoom_level, panx, pany, default, preconfig)
        elif mode == "update_group":
            self.update_group_details(group_weight, group_favorite)
        elif mode == "set_gif_duration":
            if self.current_gif:
                self.current_gif.set_all_frame_durations(new_duration)
                self.ui_manager.update_gif_frame_durations(self.current_gif.durations)

        if not self.notebook and self.collections:
            # Ensure that empty groups are not added to the list
            self.trim_groups()

            # Create the notebook if it hasn't been already
            self.ui_manager.create_notebook(self.collections[self.current_collection_index].groups)

            # Set created boolean to true so this code doesn't run again
            self.notebook = True
        if self.collections:
            current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
            current_group_name = current_group.name

            self.ui_manager.update_notebook(current_group_name)
            self.ui_manager.update_group_details(
                self.collections[self.current_collection_index].groups[self.current_group_index])

    def initialize_keybinds(self):

        # Image navigation and zoom
        self.root.bind('<Up>', self.zoom_in)
        self.root.bind('<Down>', self.zoom_out)
        self.root.bind('<Left>', self.previous_image)
        self.root.bind('<Right>', self.next_image)

        # Group navigation
        self.root.bind('<Control-Shift-Tab>', self.previous_group)
        self.root.bind('<Control-Tab>', self.next_group)

        # Panning
        self.root.bind('<a>', self.pan_left)
        self.root.bind('<d>', self.pan_right)
        self.root.bind('<w>', self.pan_up)
        self.root.bind('<s>', self.pan_down)

        # Reset and configuration
        self.root.bind('<Control-r>', self.reset)
        self.root.bind('<Control-Shift-R>', self.default_reset)

        # Save and load configurations
        self.root.bind('<Control-Shift-S>', self.save_default_configuration)
        self.root.bind('<Control-s>', self.save_configuration)
        self.root.bind('<Control-l>', self.load_configuration)

        # Toggle dialogs and favorites
        self.root.bind('<Control-d>', self.toggle_dialogs)
        self.root.bind('<Control-f>', self.toggle_favorite)
        self.root.bind('<Control-m>', self.toggle_wrap)

        # Group management
        self.root.bind('<Control-w>', self.close_group)
        self.root.bind('<Control-Shift-T>', self.reopen_group)

        # GIF controls
        self.root.bind('<space>', self.pause_gif)

        # UI toggles
        self.root.bind('<Control-Key-1>', self.ui_manager.toggle_name)
        self.root.bind('<Control-Key-2>', self.ui_manager.toggle_notebook)
        self.root.bind('<Control-Key-3>', self.ui_manager.toggle_details)
        self.root.bind('<Control-Key-4>', self.ui_manager.toggle_adv_details)
        self.root.bind('<Control-Key-5>', self.ui_manager.toggle_controls)
        self.root.bind('<Control-Key-6>', self.toggle_keybinds_and_tag_menu)
        self.root.bind('<Control-Key-7>', self.toggle_keybinds_and_zoom_pan_menu)
        self.root.bind('<Control-Key-8>', self.ui_manager.toggle_group)
        self.root.bind('<Control-Key-9>', self.toggle_gif_duration_menu_and_keybinds)

        # Collection management
        self.root.bind('<Control-Shift-C>', self.combine_collections)

        # Notebook/tab binding
        self.ui_manager.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.root.bind('<Control-k>', self.refresh_notebook)

        # Testing
        self.root.bind('<Control-Right>', self.force_next_image)
        self.root.bind('<Control-p>', self.print_group_weight)
        self.root.bind('<Control-m>', self.display_current_image)
        self.root.bind('<Control-x>', self.decrease_animation_speed)
        self.root.bind('<Control-f>', self.update_widgets)

        # Locked
        self.root.bind('<Control-a>', self.lock_keybind)

    def trim_groups(self):
        # Method for deleting empty groups
        for collection in self.collections:
            for group in collection.groups[:]:
                if not group.images:
                    collection.groups.remove(group)

    def lock_keybind(self, event=None):
        return

    # ----------------Display Methods----------------

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
        result_image = Image.new("RGBA", (self.screen_width, self.screen_height), (0, 0, 0, 0))

        # Calculate the position to paste the image onto the blank image
        paste_x = (self.screen_width - new_width) // 2 + panx
        paste_y = (self.screen_height - new_height) // 2 + pany

        # Paste the resized image onto the blank image
        result_image.paste(image, (paste_x, paste_y))

        # Convert the final image to a PhotoImage for displaying in the label
        img = ImageTk.PhotoImage(result_image)
        self.image_label.config(image=img)
        self.image_label.image = img

    def display_current_image(self, event=None):

        current_collection = self.collections[self.current_collection_index]
        current_group = current_collection.groups[self.current_group_index]

        if self.current_image_index < len(current_group.images):
            smart_image = current_group.images[self.current_image_index]

            if isinstance(smart_image, GifImage):
                self.display_gif(smart_image)
            else:
                print("Detected regular image, calling display_image method")
                self.display_image(smart_image)

            self.ui_manager.update_image_details(smart_image)
        else:
            print(
                f"Image index {self.current_image_index} is out of range for group '{current_group.name}' "
                f"with {len(current_group.images)} images")

    def display_gif(self, gif_image):
        """Play the GIF image."""
        self.current_gif = gif_image

        # Make is_animated attribute be true
        self.current_gif.play()

        self.update_gif_frame()

    def update_gif_frame(self):
        """Update the frame of the GIF."""
        with self.lock:
            if not self.current_gif or not self.current_gif.frames or not self.current_gif.is_animated:
                return

            # Image for getting dimensions
            frame = self.current_gif.frames[self.current_gif.current_frame]
            image = ImageTk.PhotoImage(frame)

            # Retrieve zoom level, panx, and pany from the GifImage object
            zoom_level = self.current_gif.zoom_level
            panx = self.current_gif.panx
            pany = self.current_gif.pany

            # Calculate the scaling factor to maintain the aspect ratio
            screen_ratio = self.screen_width / self.screen_height
            image_ratio = image.width() / image.height()

            if image_ratio > screen_ratio:
                # Image is wider relative to screen
                scale_factor = self.screen_width / image.width()
            else:
                # Image is taller relative to screen
                scale_factor = self.screen_height / image.height()

            # Calculate new dimensions with zoom level
            new_width = int(image.width() * scale_factor * zoom_level)
            new_height = int(image.height() * scale_factor * zoom_level)

            # Resize the image maintaining the aspect ratio
            frame = frame.resize((new_width, new_height), Image.LANCZOS)

            # Create a new blank image with the same size as the screen to apply pan
            result_image = Image.new("RGBA", (self.screen_width, self.screen_height), (0, 0, 0, 0))

            # Calculate the position to paste the image onto the blank image
            paste_x = (self.screen_width - new_width) // 2 + panx
            paste_y = (self.screen_height - new_height) // 2 + pany

            # Paste the resized image onto the blank image
            result_image.paste(frame, (paste_x, paste_y))

            # Convert the final image to a PhotoImage for displaying in the label
            img = ImageTk.PhotoImage(result_image)

            # Anti-Garbage collection line
            self.image_label.image = img

            if self.current_gif.is_animated and not self.current_gif.is_paused:
                self.image_label.config(image=img)
                self.current_gif.current_frame = (self.current_gif.current_frame + 1) % len(self.current_gif.frames)

                # Schedule the next frame update with the correct duration
                next_duration = self.current_gif.get_next_frame_duration()
                self.animation = self.root.after(next_duration, self.update_gif_frame)
            elif self.current_gif.is_animated and self.current_gif.is_paused:
                self.image_label.config(image=img)

    def decrease_animation_speed(self, event=None):
        print("AAA")
        self.current_gif.increase_frame_durations(100)

    def next_image(self, event=None):

        with self.lock:
            # Prevent any current gif from cycling
            if self.current_gif and self.current_gif.is_animated:
                self.current_gif.stop()

        # Access the current collection
        current_collection = self.collections[self.current_collection_index]

        self.current_image_index += 1

        # If the index exceeds the number of images in the group
        if self.current_image_index >= len(current_collection.groups[self.current_group_index].images):
            if self.image_wrap:
                # Wrap Around to the first image in the group
                self.current_image_index = 0
            else:
                self.current_image_index -= 1

        # Display image
        self.display_current_image()

    def previous_image(self, event=None):

        with self.lock:
            # Prevent any current gif from cycling
            if self.current_gif and self.current_gif.is_animated:
                self.current_gif.stop()

        # Access the current collection
        current_collection = self.collections[self.current_collection_index]

        self.current_image_index -= 1

        # If the index goes below zero
        if self.current_image_index < 0:
            if self.image_wrap:
                # Wrap Around to the last image in the group
                self.current_image_index = len(current_collection.groups[self.current_group_index].images) - 1
            else:
                self.current_image_index += 1

        # Display image
        self.display_current_image()

    def next_group(self, event=None):

        with self.lock:
            if self.current_gif and self.current_gif.is_animated:
                self.current_gif.stop()

        # Access the current collection
        current_collection = self.collections[self.current_collection_index]
        # Access the current group
        current_group = current_collection.groups[self.current_group_index]

        # Store the current index of the group being swapped from
        self.stored_indices.update({current_group.name: self.current_image_index})

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

        # Update Notebook
        self.update_widgets()

        # Display image from next group
        self.display_current_image()

    def previous_group(self, event=None):

        with self.lock:
            if self.current_gif and self.current_gif.is_animated:
                self.current_gif.stop()

        # Access the current collection
        current_collection = self.collections[self.current_collection_index]
        # Access the current group
        current_group = current_collection.groups[self.current_group_index]

        # Store the current index of the group being swapped from
        self.stored_indices.update({current_group.name: self.current_image_index})

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

        # Update Notebook
        self.update_widgets()

        # Display image from next group
        self.display_current_image()

    def toggle_wrap(self, event=None):
        self.image_wrap = not self.image_wrap

    def close_group(self, event=None):
        # removes the current tab if it is able to
        with self.lock:
            current_collection = self.collections[self.current_collection_index]
            if self.current_gif and self.current_gif.is_animated:
                self.current_gif.stop()

            if len(current_collection.groups) > 1:
                current_group = current_collection.groups[self.current_group_index]

                # Store the current index of the group being swapped from
                self.stored_indices.update({current_group.name: self.current_image_index})
                print(f"Stored index for group '{current_group.name}': {self.current_image_index}")

                # Store the current group and its index
                self.closed_groups.append((current_group, self.current_group_index))
                print(f"Closed group '{current_group.name}' at index {self.current_group_index}")

                # Remove from collections list and notebook
                self.collections[self.current_collection_index].groups.remove(current_group)
                self.ui_manager.remove_notebook_tab(self.current_group_index)
                print(f"Removed group '{current_group.name}' from collection")

                # Decide whether to increment or decrement current group
                if self.current_group_index > 0:
                    self.current_group_index -= 1
                else:
                    self.current_group_index += 1

                # Check to see if the new group has a stored index, and if so, set current index to such
                if current_collection.groups[self.current_group_index].name in self.stored_indices:
                    self.current_image_index = self.stored_indices[
                        current_collection.groups[self.current_group_index].name]
                    print(
                        f"Restored index for group '{current_collection.groups[self.current_group_index].name}': {self.current_image_index}")
                else:
                    self.current_image_index = 0
                    print(
                        "Set current image index to 0 for group '"
                        f"{current_collection.groups[self.current_group_index].name}'")

        self.update_widgets()
        self.display_current_image()
        print(f"Closed group and updated display to group '{current_collection.groups[self.current_group_index].name}'")

    def reopen_group(self, event=None):
        with self.lock:
            if self.current_gif and self.current_gif.is_animated:
                self.current_gif.stop()

            info = self.closed_groups.pop()
            index = info[1]
            group = info[0]
            print(f"Reopening group '{group.name}' at index {index}")

            # Insert the group at its previous index
            self.collections[self.current_collection_index].groups.insert(index, group)
            print(f"Inserted group '{group.name}' back into collection at index {index}")

            # Recreate the notebook tab
            self.ui_manager.add_notebook_tab(group.name, index)
            print(f"Recreated notebook tab for group '{group.name}' at index {index}")

            self.update_widgets()

            if group.name in self.stored_indices:
                self.current_image_index = self.stored_indices[group.name]
                print(f"Restored index for group '{group.name}': {self.current_image_index}")
            else:
                self.current_image_index = 0
                print(f"Set current image index to 0 for group '{group.name}'")
            self.current_group_index = index

        self.display_current_image()
        print(f"Reopened group '{group.name}' and updated display")

    def pause_gif(self, event=None):
        print("pausing gif")

        with self.lock:
            if self.current_gif and self.current_gif.is_paused:
                self.current_gif.resume()
            elif self.current_gif:
                self.current_gif.pause()

                # set the current frame back one so that it pauses on the correct frame:
                self.current_gif.current_frame = self.current_gif.current_frame - 1

        self.update_gif_frame()

    # ----------------Transformation Methods----------------

    def zoom_in(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.zoom_level += 0.01  # Increase zoom level
        if isinstance(current_image, GifImage):
            current_image.resize_frames()  # Resize GIF frames
        self.display_current_image()

    def zoom_out(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        if current_image.zoom_level > 0.01:
            current_image.zoom_level -= 0.01  # Decrease zoom level
            if isinstance(current_image, GifImage):
                current_image.resize_frames()  # Resize GIF frames
        self.display_current_image()

    def pan_left(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.panx -= 5
        if isinstance(current_image, GifImage):
            current_image.resize_frames()
        self.display_current_image()

    def pan_right(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.panx += 5
        if isinstance(current_image, GifImage):
            current_image.resize_frames()
        self.display_current_image()

    def pan_up(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.pany -= 5
        if isinstance(current_image, GifImage):
            current_image.resize_frames()
        self.display_current_image()

    def pan_down(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.pany += 5
        if isinstance(current_image, GifImage):
            current_image.resize_frames()
        self.display_current_image()

    def apply_zoom_pan_to_group(self, zoom_level, panx, pany, default, preconfig):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        for image in current_group.images:
            image.zoom_level = zoom_level
            image.panx = panx
            image.pany = pany
            if default:
                image.default_zoom_level = zoom_level
                image.default_panx = panx
                image.default_pany = pany
            if preconfig:
                if not hasattr(image, 'preconfig') or len(image.preconfig) < 3:
                    image.preconfig = [0, 0, 1.0]
                image.preconfig[0] = panx
                image.preconfig[1] = pany
                image.preconfig[2] = zoom_level
            if isinstance(image, GifImage):
                image.resize_frames()  # Resize GIF frames
        self.display_current_image()

    def apply_zoom_pan_to_current(self, zoom_level, panx, pany, default, preconfig):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.zoom_level = zoom_level
        current_image.panx = panx
        current_image.pany = pany
        if default:
            current_image.default_zoom_level = zoom_level
            current_image.default_panx = panx
            current_image.default_pany = pany
        if preconfig:
            if not hasattr(current_image, 'preconfig') or len(current_image.preconfig) < 3:
                current_image.preconfig = [0, 0, 1.0]
            current_image.preconfig[0] = panx
            current_image.preconfig[1] = pany
            current_image.preconfig[2] = zoom_level
        if isinstance(current_image, GifImage):
            current_image.resize_frames()  # Resize GIF frames
        self.display_current_image()

    def apply_zoom_pan_to_range(self, zoom_level, panx, pany, start, end, default, preconfig):
        print("applying to range")
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        current_index = self.current_image_index

        for i in range(max(0, current_index + start), min(len(current_group.images), current_index + end + 1)):
            image = current_group.images[i]
            image.zoom_level = zoom_level
            image.panx = panx
            image.pany = pany
            if default:
                image.default_zoom_level = zoom_level
                image.default_panx = panx
                image.default_pany = pany
            if preconfig:
                if not hasattr(image, 'preconfig') or len(image.preconfig) < 3:
                    image.preconfig = [0, 0, 1.0]
                image.preconfig[0] = panx
                image.preconfig[1] = pany
                image.preconfig[2] = zoom_level
            if isinstance(image, GifImage):
                image.resize_frames()  # Resize GIF frames
        self.display_current_image()

    # ----------------Configuration Management Methods----------------

    def toggle_favorite(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.toggle_favorite()
        self.ui_manager.update_image_details(current_image)

    def toggle_dialogs(self, event=None):
        self.show_dialogs = not self.show_dialogs

    def reset(self, event=None):
        """Reset's current image view to default zoom and pan"""
        print("reset called")
        if self.show_dialogs:
            response = messagebox.askokcancel(title="Yes No",
                                              message="Do you want to reset this image to its default configuration?")
            if response:
                current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
                    self.current_image_index]
                current_image.panx = current_image.default_panx
                current_image.pany = current_image.default_pany
                current_image.zoom_level = current_image.default_zoom_level
                self.display_current_image()
            else:
                return
        else:
            current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
                self.current_image_index]
            current_image.panx = current_image.default_panx
            current_image.pany = current_image.default_pany
            current_image.zoom_level = current_image.default_zoom_level
            self.display_current_image()

    def save_default_configuration(self, event=None):
        """Save's whatever the current pan and zoom values are as the default for the image"""
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        print("save_default_configuration called")
        if self.show_dialogs:
            response = messagebox.askokcancel(title="Confirm",
                                              message="Are you sure you want to save these parameters "
                                                      "as the default configuration? "
                                                      f"\n Pan x: {current_image.panx} "
                                                      f"Pan y: {current_image.pany} Zoom: {current_image.zoom_level}")
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

        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]

        # Ensure the preconfig list is initialized and has at least 3 elements
        if not hasattr(current_image, 'preconfig') or len(current_image.preconfig) < 3:
            current_image.preconfig = [0, 0, 1.0]

        if self.show_dialogs:
            response = messagebox.askokcancel(title="Confirm", message="Are you sure you want to save these "
                                                                       "parameters as a pre-configuration? "
                                                                       f"\n Pan x: {current_image.panx} "
                                                                       f"Pan y: {current_image.pany}"
                                                                       f"Zoom: {current_image.zoom_level}")
            if response:

                current_image.preconfig[0] = current_image.panx
                current_image.preconfig[1] = current_image.pany
                current_image.preconfig[2] = current_image.zoom_level
            else:
                return
        else:
            current_image.preconfig[0] = current_image.panx
            current_image.preconfig[1] = current_image.pany
            current_image.preconfig[2] = current_image.zoom_level

    def load_configuration(self, event=None):
        print("save_configuration called")
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        if self.show_dialogs:
            response = messagebox.askokcancel(title="Confirm",
                                              message="Are you sure you want to load this image's preconfig? "
                                                      f"\n Pan x: {current_image.preconfig[0]} "
                                                      f"Pan y: {current_image.preconfig[1]} "
                                                      f"Zoom: {current_image.preconfig[2]}")
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
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        response = messagebox.askokcancel(title="Confirm",
                                          message="Are you sure you want to reset this image to default default?"
                                                  f"\n Pan x: 0 Pan y: 0 Zoom:1.0")
        if response:
            current_image.default_panx = 0
            current_image.default_pany = 0
            current_image.default_zoom_level = 1.0
        else:
            return

    # ----------------UI Methods----------------

    def on_tab_change(self, event):

        with self.lock:
            if self.current_gif and self.current_gif.is_animated:
                self.current_gif.stop()
        # Notebook/tab change method
        selected_tab = event.widget.tab(event.widget.select(), "text")

        # Access the current collection
        current_collection = self.collections[self.current_collection_index]
        # Access the current group
        current_group = current_collection.groups[self.current_group_index]

        # Store the current index of the group being swapped from
        self.stored_indices.update({current_group.name: self.current_image_index})

        for i, group in enumerate(self.collections[self.current_collection_index].groups):
            if group.name == selected_tab:
                self.current_group_index = i
                self.display_current_image()
                self.root.focus_set()
                break

    def toggle_keybinds_and_tag_menu(self, event=None):
        self.toggle_keybinds()
        self.ui_manager.toggle_tag()

    def toggle_keybinds_and_zoom_pan_menu(self, event=None):
        self.toggle_keybinds()
        self.ui_manager.toggle_zoom_pan()

    def toggle_gif_duration_menu_and_keybinds(self, event=None):
        self.toggle_keybinds()
        self.toggle_gif_duration_menu()

    def toggle_gif_duration_menu(self):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        if isinstance(current_image, GifImage):
            self.ui_manager.toggle_gif_duration_frame()
        else:
            print("Current image is not a GIF.")
            self.toggle_keybinds()

    def toggle_keybinds(self):
        if self.typing:
            self.root.unbind('<Up>')
            self.root.unbind('<Down>')
            self.root.unbind('<Left>')
            self.root.unbind('<Right>')
            self.root.unbind('<Control-Shift-Tab>')
            self.root.unbind('<Control-Tab>')
            self.root.unbind('<a>')
            self.root.unbind('<d>')
            self.root.unbind('<w>')
            self.root.unbind('<s>')
        else:
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
        self.typing = not self.typing

    def refresh_notebook(self, event=None):
        # Clear the current tabs
        for tab in self.ui_manager.notebook.tabs():
            self.ui_manager.notebook.forget(tab)

        # Add new tabs for each group in the combined collection
        current_collection = self.collections[0]  # Assuming collections are combined in the first index
        for group in current_collection.groups:
            frame = ttk.Frame(self.ui_manager.notebook)
            self.ui_manager.notebook.add(frame, text=group.name)

        # Select the first tab
        if current_collection.groups:
            self.ui_manager.notebook.select(0)

        # Update the UI manager's current group index
        self.ui_manager.update_notebook(current_collection.groups[0].name)

    # ----------------Tag Management ----------------

    # All of these methods have a self.ui_manager.update_image_details(current_image) update statement so that if the
    # details menu is open when tags are added it will properly reflect it

    def add_tags_to_group(self, tags):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        for image in current_group.images:
            image.add_tag(tags)
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        self.ui_manager.update_image_details(current_image)

    def add_tags_to_range(self, tags, start, end):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        current_index = self.current_image_index

        for i in range(max(0, current_index + start), min(len(current_group.images), current_index + end + 1)):
            current_group.images[i].add_tag(tags)
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        self.ui_manager.update_image_details(current_image)

    def add_tags_to_current(self, tags):

        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.add_tag(tags)
        self.ui_manager.update_image_details(current_image)

    def remove_tags_from_group(self, tags):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        for image in current_group.images:
            image.remove_tag(tags)
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        self.ui_manager.update_image_details(current_image)

    def remove_tags_from_range(self, tags, start, end):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        current_index = self.current_image_index

        for i in range(max(0, current_index + start), min(len(current_group.images), current_index + end + 1)):
            current_group.images[i].remove_tag(tags)
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        self.ui_manager.update_image_details(current_image)

    def remove_tags_from_current(self, tags):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        current_image.remove_tag(tags)
        self.ui_manager.update_image_details(current_image)

    def update_group_details(self, group_weight, group_favorite):
        current_group = self.collections[self.current_collection_index].groups[self.current_group_index]
        current_group.weight = group_weight
        current_group.favorite = group_favorite
        self.ui_manager.update_image_details(
            self.collections[self.current_collection_index].groups[self.current_group_index].images[
                self.current_image_index],
            self.collections[self.current_collection_index].groups[self.current_group_index])

    # ----------------Collection/Save Management ----------------

    def combine_collections(self, event=None):
        if not self.collections:
            return

        # Store a copy of the original collections
        self.original_collections = self.collections.copy()

        # Combine all groups and images into the first collection
        main_collection = self.collections[0]
        for collection in self.collections[1:]:
            for group in collection.groups:
                main_collection.add_group(group)

        # Keep only the combined collection
        self.collections = [main_collection]

        # Trim empty groups
        self.trim_groups()

        # Refresh notebook widget
        self.refresh_notebook()

        # Update the treeview and UI
        self.update_widgets()

    def save_original_collections(self):
        # Restore the original collections before saving
        self.collections = self.original_collections.copy()

        # Save data logic here
        self.save_all_image_data()

        # Recombine the collections after saving
        self.combine_collections()

    # TESTING ONLY    --------------------------

    def force_next_image(self):

        self.current_image_index += 1

        self.display_current_image()

    def print_tags(self, event=None):
        current_image = self.collections[self.current_collection_index].groups[self.current_group_index].images[
            self.current_image_index]
        print(f"Tags for image {current_image.name}: {current_image.tags}")

    def print_group_weight(self, event=None):
        print(self.collections[self.current_collection_index].groups[self.current_group_index].weight)
