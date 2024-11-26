import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import pandas as pd
import numpy as np

app = Flask(__name__, static_folder='static')

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color code."""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_colours(image_path):
    """
    Extracts dominant colors from an image and returns them with their respective percentages.

    Args:
        image_path (str): Path to the input image.

    Returns:
        list: A list of hex color codes with their percentages.
    """
    # Open the image
    image = Image.open(image_path)
    
    # Convert image to reduced palette
    reduced_image = image.convert("P", palette=Image.WEB)
    
    # Get the palette
    palette = reduced_image.getpalette()
    palette = [palette[i:i+3] for i in range(0, len(palette), 3)]
    
    # Get color counts
    colour_count = [[n, palette[m]] for n, m in reduced_image.getcolors()]
    
    # Create DataFrame
    df = pd.DataFrame(colour_count, columns=["count", "colour"]).sort_values(by="count", ascending=False)
    df["percentage"] = round((df["count"] / df["count"].sum()) * 100, 2)
    
    # Filter colors
    df = df[df["percentage"] >= 1.5]
    df = df.head(10) if len(df) > 10 else df
    
    # Convert to hex and create final list
    result = [
        {
            'hex': rgb_to_hex(row['colour']),
            'percentage': row['percentage']
        } 
        for _, row in df.iterrows()
    ]
    
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if file is present
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Check if file is allowed
    if file and allowed_file(file.filename):
        # Secure the filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract colors
            colors = get_colours(filepath)
            
            # Optional: Remove the uploaded file after processing
            os.remove(filepath)
            
            return jsonify(colors)
        except Exception as e:
            # Remove the file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)