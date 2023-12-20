# Pixel-Editor


A small Python app inspired by Piskel that allows the user to create pixel art.     

## Features:
- **Pixel Art Creation**: provides tools for layer-based pixel art, allowing users to create detailed and intricate images. Transparency is fully supported.
- **Customizable Canvas Size**: users can set the dimensions of the canvas at any point, allowing for design flexibility
- **Color Palette Management**: allows users to customize and manage color palettes, making it easier to work with consistent color schemes, along with an eyedropper tool to quickly pick colors from the canvas.
- **Export Options**: supports exporting images in various formats, including GIF, PNG, and more.
- **Keyboard Shortcuts**: includes keyboard shortcuts for common actions, enhancing workflow efficiency.
- **Brush and Eraser Tools**: includes basic drawing tools such as brushes and erasers to help users create and refine their pixel art.
- **Line and rectangle tools**: allows for simple drawing of pixel lines and rectangles
- **Undo and Redo**: has basic undo/redo functionality
- **User-Friendly Interface**: straightforward and intuitive interface, making it accessible to users with varying levels of experience in pixel art creation.
- **Texture import**: allows users to import other textures in different formats, like JPG and PNG.

## Dependencies
The backend part of this application is based on the Pillow library. It provides fairly powerful image processing capabilities and most pixel operations here are based on a Pillow implementation.   

The fronend was made using Tkinter. ***TODO***

Why not use Tkinter's default pixel operations? The idea was to provide a backend API that can then be used in conjunction with any GUI library.

## Usage
#### Installing dependencies

#### Running the app
***TODO***

## Gallery

## Contributors
Project contributors:
- Vlad Chira - Pillow backend implementation
- ***TODO***
- ***TODO***

## Encountered problems & solutions
#### Backend
- **Slow pixel operations**. Initially a lot of operations with pixels, like painting with the brush, or filling with the bucket tool were very slow at larger scales, up to the point they were completely unusable. The fix was to no longer try to reinvent the wheel by manually setting pixels one at a time, but to take advantage of already existing fast pixel operations in the library.
- **Laggy mouse movement & discontinuous brush strokes**. The program can only be run at a certain framerate. Between the frames, no information about the mouse position is given. That is a huge problem for rapid brush movements, because the distance the brush moves inbetween frames is larger than the radius of the brush, leaving spaces in the brush stroke even if the user never released the mouse button. The fix was to check whether the mouse position was pressed in both the previous and the current frame, and if so, linearly interpolate between the two positions and draw extra brush strokes to fill in the gaps.
- **Previews**. The line and rectangle tools need a preview while holding down the mouse button and dragging. When releasing the mouse, the preview must end and the line or rectangle must be drawn to the canvas. This was quite a challenge to implement, the final solution we went for is for the canvas to hold a special, hidden preview layer that is always drawn on top of the others. Most of the times it is completely transparent, but it can be used for previews.

***TODO***