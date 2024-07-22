
# Image Viewer Application

## Overview

The Image Viewer Application is a versatile and customizable tool designed to facilitate viewing, organizing, and managing images. It supports various image formats, including GIFs, and offers a range of features to enhance user interaction and experience.

## Features

- **Multi-Collection Support**: Load and manage multiple image collections.
- **Whitelist/Blacklist Filtering**: Include or exclude specific folders and their contents.
- **GIF Handling**: View and control GIF animations, including setting frame durations.
- **Zoom and Pan**: Adjust zoom levels and pan images for a better viewing experience.
- **Tag Management**: Add and remove tags for organizing images.
- **Favorite Images**: Mark and filter favorite images.
- **Group Management**: Navigate through groups and maintain state.
- **Session Management**: Save and load sessions for continued work.
- **Full-Screen Mode**: Experience images in full-screen mode for enhanced visibility.

## Getting Started

### Prerequisites

- Python 3.x
- `tkinter` library
- `Pillow` library

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/image-viewer-app.git
    cd image-viewer-app
    ```

2. **Install the required libraries**:
    ```sh
    pip install pillow
    ```

### Running the Application

1. **Run the main application**:
    ```sh
    python MainApp.py
    ```

2. **Using the application**:
   - Select a folder to load images.
   - Use the interface to navigate through images, manage collections, and apply filters.

## Usage

### Keybindings

- **Navigation**:
  - `Up Arrow`: Zoom in
  - `Down Arrow`: Zoom out
  - `Left Arrow`: Previous image
  - `Right Arrow`: Next image
  - `Ctrl + Shift + Tab`: Previous group
  - `Ctrl + Tab`: Next group
  - `Ctrl + d`: Toggle dialogs
  - `Ctrl + f`: Toggle favorite
  - `Ctrl + m`: Toggle wrap
  - `Ctrl + w`: Close group
  - `Ctrl + Shift + T`: Reopen group

- **Panning**:
  - `a`: Pan left
  - `d`: Pan right
  - `w`: Pan up
  - `s`: Pan down

- **GIF Control**:
  - `Space`: Pause/Resume GIF

- **Configuration Management**:
  - `Ctrl + r`: Reset to default configuration
  - `Ctrl + Shift + s`: Save default configuration
  - `Ctrl + s`: Save current configuration
  - `Ctrl + l`: Load configuration
  - `Ctrl + Shift + R`: Default reset

### UI Elements

- **TreeView**: Display folder structure and images.
- **Details Frame**: Show basic and advanced details of the current image.
- **Controls Frame**: Buttons for reset, save, and load configurations.
- **Tag Frame**: Manage tags for the current image or group.
- **Zoom/Pan Frame**: Adjust zoom and pan settings.
- **Group Frame**: Manage group details.
- **GIF Duration Frame**: Set and view GIF frame durations.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a pull request.

