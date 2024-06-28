

class SmartImage:
    def __init__(self, path, zoom_level = 1.0, tags = [], ):
        self.path = path
        self.default_zoom_level = zoom_level
        self.zoom_level
        self.default_panx
        self.default_pany
        self.panx
        self.pany
        # Representation of what folder(s) the image is in
        self.group

        # Rarity modifier for when random draw is used 
        self.weight = 1.0

        self.tags = tags

class Group:
    def __init__(self, folder_path):
        self.folder_path = folder_path