import os

class SmartImage:
    def __init__(self, path, name, zoom_level = 1.0, panx = 0, pany = 0, tags = [], favorite = False ):
        self.path = path
        self.name = name
        self.default_zoom_level = zoom_level
        self.zoom_level
        self.default_panx = panx
        self.default_pany = pany
        self.panx = self.default_panx
        self.pany = self.default_pany
        
        # Rarity modifier for when true random draw is used 
        self.weight = 1.0
        self.tags = tags

        self.favorite = favorite

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def set_zoom_level(self, zoom_level):
        self.zoom_level = zoom_level

    def set_pan(self, panx, pany):
        self.default_panx = panx
        self.default_pany = pany
        

    def reset_zoom_pan(self):
        self.zoom_level = self.default_zoom_level
        self.panx = self.default_panx
        self.pany = self.default_pany

    def modify(self, name=None, zoom_level=None, panx=None, pany=None, tags=None, favorite=None, weight=None):
        if name is not None:
            self.name = name
        if zoom_level is not None:
            self.set_zoom_level(zoom_level)
        if panx is not None and pany is not None:
            self.set_pan(panx, pany)
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
                f"panx={self.panx}, pany={self.pany}, tags={self.tags}, favorite={self.favorite}, weight={self.weight})")
    

class Group:
    def __init__(self, folder_path, name, weight = 1.0, favorite = False, images = []):
        self.folder_path = folder_path

        self.name = name
        # Rarity modfier for when random groups are drawn
        self.weight = weight

        self.favorite = favorite

        self.images = images

    def add_image(self, image):
        if isinstance(image, SmartImage):
            image.group = self.name
            self.images.append(image)

    def remove_image(self, image):
        if image in self.images:
            image.group = None
            self.images.remove(image)

    def modify_group(self, name=None, weight=None, favorite=None):
        if name is not None:
            self.name = name
        if weight is not None:
            self.weight = weight
        if favorite is not None:
            self.favorite = favorite

    def find_image_by_name(self, name):
        return next((image for image in self.images if image.name == name), None)

    def find_images_by_tag(self, tag):
        return [image for image in self.images if tag in image.tags]

    def toggle_favorite(self):
        self.favorite = not self.favorite


    def load_images(self):
        # Load images inside the folder and makes them into 
        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(self.folder_path, filename)
                self.images.append(SmartImage(image_path))

    def __repr__(self):
        return f"Group(name={self.name}, folder_path={self.folder_path}, weight={self.weight}, favorite={self.favorite}, images={len(self.images)})"