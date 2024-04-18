from pathlib import Path
import os
import File  

class FileManager:
    def scan_directory(self, directory):
        # Scans the specified directory recursively and creates File objects for each found file.
        file_objects = []
        for file_path in Path(directory).rglob('*'):  # Using rglob to find all files recursively
            file_type = self.determine_file_type(file_path.suffix)  # Determine type based on file extension
            file_obj = File(file_path, file_type)
            file_objects.append(file_obj)
        return file_objects

    def determine_file_type(self, suffix):
        # Determines the type of the file based on the file extension.
        if suffix in ['.jpg', '.png', '.bmp']:
            return File.FileType.IMAGE
        elif suffix == '.mp4':
            return File.FileType.VIDEO
        elif suffix == '.gif':
            return File.FileType.GIF
        else:
            return File.FileType.DOCUMENT
    def get_media_files(self, directory):
        pass

    def get_comment_files(self, directory):
        pass
