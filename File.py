from pathlib import Path

class File:
    from enum import Enum
    
    # Define an Enum for file types to ensure type consistency and clarity.
    class FileType(Enum):
        IMAGE = 'Image'
        VIDEO = 'Video'
        GIF = 'Gif'
        DOCUMENT = 'Document'

    def __init__(self, file_path, file_type: FileType):
        self.files_cache = {}  # Cache to store file data
        self.file_path = file_path
        self.file_name = Path(file_path).stem
        self.file_type = file_type
        self.tags = []
        self.groups = []
        self.comments = []
        self.last_modified = self.get_last_modified_time(file_path)
        self.size = self.get_file_size(file_path)

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def add_to_group(self, group_id):
        if group_id not in self.groups:
            self.groups.append(group_id)

    def remove_from_group(self, group_id):
        if group_id in self.groups:
            self.groups.remove(group_id)

    def add_comment(self, comment, position=None):
        self.comments.append((comment, position))

    def get_last_modified_time(self, path):
        return os.path.getmtime(path)

    def get_file_size(self, path):

        return os.path.getsize(path)

    def __repr__(self):
        # Representation of the File object for debugging and logging, shows path and type.
        return f"<File {self.file_path} Type={self.file_type}>"

