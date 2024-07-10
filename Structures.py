from PIL import Image, ImageTk, ImageSequence
import itertools
import os

# Hierarchy: Collection > Group > SmartImage

class SmartImage:
    def __init__(self, path, name, group, zoom_level=1.0, panx=0, pany=0, series="", index=0, offset=None, weight=1.0, tags=[], favorite=False):
        self.path = path
        self.name = name
        self.group = group  # Reference to the parent group
        self.default_zoom_level = zoom_level
        self.zoom_level = zoom_level
        self.default_panx = panx
        self.default_pany = pany
        self.panx = self.default_panx
        self.pany = self.default_pany
        
        # String representing a series of images that are related
        self.series = series

        # If the image is in a series, this is an index to represent the order the images go in
        self.index = index

        # Another SmartImage object that is an offset of it, EX: Translated version
        self.offset = offset

        # Rarity modifier for when true random draw is used 
        self.weight = weight

        # Strings for assisting indexing
        self.tags = tags
        self.favorite = favorite

        # A preconfig list that has the first 2 values represent panx and y, then the 3rd represent a zoom
        self.preconfig = []

    def add_tag(self, tags):
        for tag in tags.split(','):
            tag = tag.strip()
            tag = tag.lower()
            if tag and tag not in self.tags:
                self.tags.append(tag)

    def remove_tag(self, tags):
        for tag in tags.split(','):
            tag = tag.strip()
            tag = tag.lower()
            if tag in self.tags:
                self.tags.remove(tag)

    # Debug Only
    def print_tags(self):
        for tag in self.tags:
            print(tag)

    def set_zoom_level(self, zoom_level):
        self.default_zoom_level = zoom_level

    def set_pan(self, panx, pany):
        self.default_panx = panx
        self.default_pany = pany

    def reset_zoom_pan(self):
        self.zoom_level = self.default_zoom_level
        self.panx = self.default_panx
        self.pany = self.default_pany

    def modify(self, name=None, zoom_level=None, panx=None, pany=None, series=None, index=None, tags=None, favorite=None, weight=None):
        if name is not None:
            self.name = name
        if zoom_level is not None:
            self.set_zoom_level(zoom_level)
        if panx is not None and pany is not None:
            self.set_pan(panx, pany)
        if series is not None:
            self.series = series
        if index is not None:
            self.index = index
        if tags is not None:
            self.tags = tags
        if favorite is not None:
            self.favorite = favorite
        if weight is not None:
            self.weight = weight

    def toggle_favorite(self):
        self.favorite = not self.favorite

    def __repr__(self):
        return (f"SmartImage(name={self.name}, path={self.path}, group={self.group}, zoom_level={self.zoom_level}, "
                f"panx={self.panx}, pany={self.pany}, series={self.series}, index={self.index}, "
                f"offset={self.offset}, tags={self.tags}, favorite={self.favorite}, weight={self.weight})")


    

class Group:
    def __init__(self, folder_path, name, weight=1.0, favorite=False, images=None, parent=None, children=None, depth=0):
        if images is None:
            images = []
        if children is None:
            children = []
        self.folder_path = folder_path
        self.name = name  
        self.weight = weight 
        self.favorite = favorite

        # List of SmartImage objects at the top level
        self.images = images

        # Parent group reference
        self.parent = parent

        # List of child groups
        self.children = children

        # Depth of the group in the hierarchy (Integer)
        self.depth = depth

    def add_image(self, image):
        """Add a SmartImage to the group."""
        if isinstance(image, SmartImage):
            self.images.append(image)

    def add_child_group(self, child_group):
        """Add a child group to the group."""
        if isinstance(child_group, Group):
            child_group.parent = self
            child_group.depth = self.depth + 1
            self.children.append(child_group)

    def load_images(self, folder_path=None, parent_folder=None):
        """Recursively load images from the given folder path and nested subfolders."""

        # Default to object path if one is not provided
        if folder_path is None:
            folder_path = self.folder_path

        # Iterate through every item in the path
        for item in os.listdir(folder_path):
            # Joins the master path with the name of the current item, combining single path, which represents the full path to the item within the directory.
            item_path = os.path.join(folder_path, item)
            # print(f"Processing item: {item_path}")
            # If the item is a folder, create a child group and recurse into it
            if os.path.isdir(item_path):
                # print(f"Found directory: {item_path}")
                child_group = Group(item_path, item, parent=self, depth=self.depth + 1)
                self.add_child_group(child_group)
                child_group.load_images(item_path)

            # If the item is an image, add it to the appropriate list
            elif item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # print(f"Found image: {item_path}")
                if item.lower().endswith('.gif'):
                    with Image.open(item_path) as gif:
                        animation_speed = gif.info.get('duration', 100)  # Use a default value if 'duration' is missing
                    self.add_image(GifImage(item_path, item, group=self.name, animation_speed=animation_speed))
                else:
                    self.add_image(SmartImage(item_path, item, group=self.name))

    def __repr__(self):
        # String representation of the Group object for debugging.
        return (f"Group(name={self.name}, folder_path={self.folder_path}, weight={self.weight}, favorite={self.favorite}, "
                f"images={len(self.images)}, children={len(self.children)}, depth={self.depth})")



class Collection:
    def __init__(self, base_folder_path, name, weight=1.0, favorite=False, groups=None):
        if groups is None:
            groups = []

        # Path to the base folder of the collection
        self.base_folder_path = base_folder_path  
        self.name = name  
        self.weight = weight  
        self.favorite = favorite
        self.groups = groups

    def add_group(self, group):
        """Add a Group to the collection."""
        if isinstance(group, Group):
            self.groups.append(group)

    def load_groups(self):
        """Load groups from the base folder path."""
        for folder_name in os.listdir(self.base_folder_path):
            folder_path = os.path.join(self.base_folder_path, folder_name)
            if os.path.isdir(folder_path):
                # Create a new Group for each subfolder in the base folder
                group = Group(folder_path, folder_name)
                # Load images and subfolders for each group
                group.load_images()  
                self.add_group(group)

    def __repr__(self):
        """String representation of the Collection object for debugging."""
        return (f"Collection(name={self.name}, base_folder_path={self.base_folder_path}, weight={self.weight}, "
                f"favorite={self.favorite}, groups={len(self.groups)})")


#TODO Gif class (inherits from smart image)

class GifImage(SmartImage):
    def __init__(self, path, name, group, zoom_level=1.0, panx=0, pany=0, series="", index=0, offset=None, weight=1.0, tags=[], favorite=False, animation_speed=100):
        super().__init__(path, name, group, zoom_level, panx, pany, series, index, offset, weight, tags, favorite)
        self.frames = []
        self.current_frame = 0
        self.animation = None
        self.animation_speed = animation_speed  # Speed in ms
        self.is_animated = True
        self.is_paused = False
        self.load_gif_frames()

    def load_gif_frames(self):
        try:
            with Image.open(self.path) as img:
                for i, frame in enumerate(ImageSequence.Iterator(img)):
                    frame_copy = frame.copy()
                    self.frames.append(frame_copy)
                    print(f"Loaded frame {i}")
            print(f"Total frames loaded: {len(self.frames)}")
        except Exception as e:
            print(f"Error loading GIF: {e}")

    def play(self, root, image_label):
        if self.is_animated and not self.is_paused:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            frame = self.frames[self.current_frame]
            
            # Apply zoom and pan to the current frame
            zoom_level = self.zoom_level
            panx = self.panx
            pany = self.pany

            screen_ratio = image_label.winfo_width() / image_label.winfo_height()
            image_ratio = frame.width / frame.height

            if image_ratio > screen_ratio:
                scale_factor = image_label.winfo_width() / frame.width
            else:
                scale_factor = image_label.winfo_height() / frame.height

            new_width = int(frame.width * scale_factor * zoom_level)
            new_height = int(frame.height * scale_factor * zoom_level)

            frame = frame.resize((new_width, new_height), Image.LANCZOS)
            result_image = Image.new("RGBA", (image_label.winfo_width(), image_label.winfo_height()), (0, 0, 0, 0))

            paste_x = (image_label.winfo_width() - new_width) // 2 + panx
            paste_y = (image_label.winfo_height() - new_height) // 2 + pany

            result_image.paste(frame, (paste_x, paste_y))

            img = ImageTk.PhotoImage(result_image)
            image_label.config(image=img)
            image_label.image = img

            self.animation = root.after(self.animation_speed, self.play, root, image_label)

    def pause(self):
        if self.animation:
            self.animation.after_cancel(self.animation)
            self.is_paused = True

    def resume(self, root, image_label):
        if self.is_paused:
            self.is_paused = False
            self.play(root, image_label)

    def stop(self):
        self.is_animated = False
        if self.animation:
            self.animation.after_cancel(self.animation)
            self.animation = None

    def set_animation_speed(self, speed):
        self.animation_speed = speed