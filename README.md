# Image Color Extractor

## Overview

Image Color Extractor is a Flask-based web application that allows users to upload images and extract their dominant colors. The application uses advanced color clustering techniques to identify and return the most significant colors in an uploaded image.

## Features

-  Upload images in PNG, JPG, JPEG, and GIF formats
-  Extract dominant colors using K-means clustering
-  Return colors with their percentage representation
-  Secure file handling with size and type restrictions
-  Fast and efficient color extraction

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/image-color-extractor.git
cd image-color-extractor
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- Flask
- Pillow (PIL)
- NumPy
- Scikit-learn
- Werkzeug

## Quick Start

1. Run the Flask application:
```bash
python main.py
```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload an image and see its dominant colors!

## Project Structure

```
image-color-extractor/
│
├── main.py           # Main Flask application
├── uploads/          # Temporary directory for uploaded files
├── static/           # Static files (CSS, JS)
├── templates/        # HTML templates
│   └── index.html    # Main page template
└── requirements.txt  # Project dependencies
```

## How It Works

The application uses K-means clustering to identify dominant colors:
1. Image is resized to improve processing speed
2. Pixels are converted to RGB color space
3. K-means algorithm clusters similar colors
4. Colors are sorted by their percentage representation
5. Top colors (>1.5% of image) are returned as hex codes

## API Endpoint

- **POST** `/upload`
  - Accepts image file
  - Returns JSON with color information
  - Example response:
    ```json
    [
      {"hex": "#123456", "percentage": 35.5},
      {"hex": "#789ABC", "percentage": 22.3}
    ]
    ```

## Limitations

- Maximum file size: 16 MB
- Supported formats: PNG, JPG, JPEG, GIF
- Up to 10 dominant colors returned

## Security

- Filename sanitization
- File type validation
- Temporary file cleanup