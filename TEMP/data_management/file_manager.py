from pathlib import Path
import os
from TEMP.File import File  

class FileManager:
    def __init__(self):
        self.supported_file_types = {
            '.jpg': File.FileType.IMAGE,
            '.png': File.FileType.IMAGE,
            '.bmp': File.FileType.IMAGE,
            '.mp4': File.FileType.VIDEO,
            '.gif': File.FileType.GIF,
            '.doc': File.FileType.DOCUMENT,  # Assuming support for '.doc' as an example
            '.pdf': File.FileType.DOCUMENT  # Assuming support for '.pdf' as an example
        }

    def scan_directory(self, directory):
        """ Scans the specified directory recursively and creates File objects for each found file. """
        file_objects = []
        for file_path in Path(directory).rglob('*'):
            if file_path.is_file():  # Check if it is a file
                file_type = self.determine_file_type(file_path.suffix)
                if file_type:  # Ensure it's a supported file type
                    file_obj = File(file_path, file_type)
                    file_objects.append(file_obj)
                else:
                    print(f"Unsupported file type encountered: {file_path.suffix} for file {file_path}")
                    # raise ValueError(f"Unsupported file type encountered: {file_path.suffix} for file {file_path}")
        return file_objects

    def determine_file_type(self, suffix):
        """ Determines the type of the file based on the file extension. """
        return self.supported_file_types.get(suffix.lower(), None)  # Handle case sensitivity

    def get_media_files(self, directory):
        return [file for file in self.scan_directory(directory) if file.file_type in {File.FileType.IMAGE, File.FileType.VIDEO}]

    def get_comment_files(self, directory):
        pass
