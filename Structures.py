from PIL import Image, ImageSequence

import os


class SmartImage:
    def __init__(self, path, name, group, default_zoom_level=1.0, default_panx=0, default_pany=0, series="", index=0,
                 offset=None, weight=1.0, tags=None, favorite=False, preconfig=None):
        if preconfig is None:
            preconfig = []
        if tags is None:
            tags = []
        self.path = path
        self.name = name
        self.group = group  # Reference to the parent group
        self.default_zoom_level = default_zoom_level
        self.zoom_level = default_zoom_level
        self.default_panx = default_panx
        self.default_pany = default_pany
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
        self.preconfig = preconfig

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

    def modify(self, name=None, zoom_level=None, panx=None, pany=None, series=None, index=None, tags=None,
               favorite=None, weight=None):
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
    def __init__(self, folder_path, name, weight=1.0, favorite=False, images=None, parent=None, depth=0):
        if images is None:
            images = []
        self.folder_path = folder_path
        self.name = name
        self.weight = weight
        self.favorite = favorite
        self.images = images
        self.parent = parent
        self.children = []
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

    def load_images(self, folder_path=None):
        """Recursively load images from the given folder path and nested subfolders."""
        if folder_path is None:
            folder_path = self.folder_path

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                child_group = Group(item_path, item, parent=self, depth=self.depth + 1)
                self.add_child_group(child_group)
                child_group.load_images(item_path)
            elif item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                if item.lower().endswith('.gif'):
                    with Image.open(item_path) as gif:
                        animation_speed = gif.info.get('duration', 100)  # Use a default value if 'duration' is missing
                    self.add_image(GifImage(item_path, item, group=self.name, animation_speed=animation_speed))
                else:
                    self.add_image(SmartImage(item_path, item, group=self.name))

    def __repr__(self):
        return (
            f"Group(name={self.name}, folder_path={self.folder_path}, weight={self.weight}, favorite={self.favorite}, "
            f"images={len(self.images)}, children={len(self.children)}, depth={self.depth})")


class Collection:
    def __init__(self, base_folder_path, name, weight=1.0, favorite=False, groups=None):
        if groups is None:
            groups = []
        self.base_folder_path = base_folder_path
        self.name = name
        self.weight = weight
        self.favorite = favorite
        self.groups = groups

    def add_group(self, group):
        """Add a Group to the collection."""
        if isinstance(group, Group):
            self.groups.append(group)

    def load_groups(self, whitelist=None, blacklist=None):
        """Load groups from the base folder path."""
        # print(f"Loading groups from {self.base_folder_path}")
        for folder_name in os.listdir(self.base_folder_path):
            folder_path = os.path.join(self.base_folder_path, folder_name)
            # print(f"Checking folder: {folder_path}")

            if os.path.isdir(folder_path):
                # print(f"Found directory: {folder_path}")

                # Check whitelist and blacklist
                if (whitelist and folder_name not in whitelist) or (blacklist and folder_name in blacklist):
                    print(f"Skipping folder {folder_name} due to whitelist/blacklist")
                    continue

                # Create a new Group for each subfolder in the base folder
                group = Group(folder_path, folder_name)
                # Load images and subfolders for each group
                group.load_images()
                self.add_group(group)
                self.add_child_groups(group)
                print(f"Group added: {folder_name} with {len(group.images)} images")

            #else:
            #print(f"Not a directory: {folder_path}")

    def add_child_groups(self, group):
        """Add child groups recursively."""
        for child_group in group.children:
            self.groups.append(child_group)
            self.add_child_groups(child_group)

    def __repr__(self):
        return (f"Collection(name={self.name}, base_folder_path={self.base_folder_path}, weight={self.weight}, "
                f"favorite={self.favorite}, groups={len(self.groups)})")


class GifImage(SmartImage):
    def __init__(self, path, name, group, default_zoom_level=1.0, default_panx=0, default_pany=0, series="", index=0,
                 offset=None, weight=1.0, tags=None, favorite=False, preconfig=None, durations=None, animation_speed=100):
        super().__init__(path, name, group, default_zoom_level, default_panx, default_pany, series, index, offset,
                         weight, tags, favorite, preconfig)
        if durations is None:
            durations = []
        if preconfig is None:
            preconfig = []
        if tags is None:
            tags = []
        self.frames = []
        self.durations = durations
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
                    duration = img.info.get('duration', 100)  # Default duration if not specified
                    self.durations.append(duration)
        except Exception as e:
            print(f"Error loading GIF: {e}")

    def play(self):
        self.is_animated = True

    def stop(self):
        self.is_animated = False

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def set_animation_speed(self, speed):
        self.animation_speed = speed

    def set_all_frame_durations(self, duration):
        self.durations = [duration] * len(self.frames)
        print(f"All frame durations set to {duration} ms")

    def increase_frame_durations(self, increment):
        self.durations = [d + increment for d in self.durations]
        print(f"Increased all frame durations by {increment} ms")

    def decrease_frame_durations(self, decrement):
        self.durations = [max(10, d - decrement) for d in self.durations]  # Ensure duration is at least 10 ms
        print(f"Decreased all frame durations by {decrement} ms")

    def get_next_frame_duration(self):
        duration = self.durations[self.current_frame]
        print(f"Next frame duration: {duration} ms for frame {self.current_frame}")
        return duration

    def resize_frames(self):
        # Resize all frames according to the current zoom level
        for i in range(len(self.frames)):
            frame = self.frames[i]
            zoom_level = self.zoom_level

            screen_ratio = self.screen_width / self.screen_height
            image_ratio = frame.width / frame.height

            if image_ratio > screen_ratio:
                scale_factor = self.screen_width / frame.width
            else:
                scale_factor = self.screen_height / frame.height

            new_width = int(frame.width * scale_factor * zoom_level)
            new_height = int(frame.height * scale_factor * zoom_level)

            self.frames[i] = frame.resize((new_width, new_height), Image.LANCZOS)
