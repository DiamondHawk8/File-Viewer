import os

# Hierarchy: Collection > Group > SmartImage

class SmartImage:
    def __init__(self, path, name, zoom_level = 1.0, panx = 0, pany = 0, series = "", index = 0, offset = None, weight = 1.0, tags = [], favorite = False ):
        self.path = path
        self.name = name
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
        self.weight = 1.0

        # Strings for assisting indexing
        self.tags = tags
        self.favorite = favorite

        #TODO potentially add a preconfig list that has the first 2 integers represent panx and y, then the 3rd represent a zoom etc.

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
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

    def modify(self, name=None, zoom_level=None, panx=None, pany=None, series = None, index = None, tags=None, favorite=None, weight=None):
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
        return (f"SmartImage(name={self.name}, path={self.path}, zoom_level={self.zoom_level}, "
            f"panx={self.panx}, pany={self.pany}, series={self.series}, index={self.index}, "
            f"offset={self.offset}, tags={self.tags}, favorite={self.favorite}, weight={self.weight})")

    

class Group:
    def __init__(self, folder_path, name, weight=1.0, favorite=False, images=None, subfolders=None):
        if images is None:
            images = []
        if subfolders is None:
            subfolders = {}
        self.folder_path = folder_path
        self.name = name  
        self.weight = weight 
        self.favorite = favorite 

        # List of SmartImage objects at the top level
        self.images = images  

        # Dictionary to store subfolder paths and their images
        self.subfolders = subfolders  

    def add_image(self, image, folder=None):
        """Add a SmartImage to the group. If a folder is specified, add to subfolder."""
        if isinstance(image, SmartImage):
            if folder is None:
                self.images.append(image)
            else:
                if folder not in self.subfolders:
                    self.subfolders[folder] = []
                self.subfolders[folder].append(image)

    def load_images(self, folder_path=None, parent_folder=None):
        """Recursively load images from the given folder path and nested subfolders."""

        # Default to object path if one is not provided
        if folder_path is None:
            folder_path = self.folder_path

        # Iterate through every item in the path
        for item in os.listdir(folder_path):
            # Joins the master path with the name of the current item, combining single path, which represents the full path to the item within the directory.
            item_path = os.path.join(folder_path, item)

            # If the item is a folder, recurse into it
            if os.path.isdir(item_path):
                self.load_images(item_path, folder=os.path.relpath(item_path, self.folder_path))
            
            # If the item is an image, add it to the appropriate list
            elif item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.add_image(SmartImage(item_path, item), folder=parent_folder)

    def __repr__(self):
        """String representation of the Group object for debugging."""
        return (f"Group(name={self.name}, folder_path={self.folder_path}, weight={self.weight}, "
                f"favorite={self.favorite}, images={len(self.images)}, subfolders={list(self.subfolders.keys())})")
    

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
                # Load images for each group
                group.load_images()  
                self.add_group(group)

    def __repr__(self):
        """String representation of the Collection object for debugging."""
        return (f"Collection(name={self.name}, base_folder_path={self.base_folder_path}, weight={self.weight}, "
                f"favorite={self.favorite}, groups={len(self.groups)})")