from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from scripts.generate_text import generate_text
from scripts.generate_music import get_gradio_space_url
from scripts.generate_image import generate_image
from scripts.generate_video import get_gradio_space_url
from scripts.detect_content_type import detect_content_type
from scripts.context_processor import analyze_context, format_output
import os
import subprocess
import threading

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Define static folder path
STATIC_FOLDER = 'static/generated'
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Ensure static folder exists
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def home():
    """Serve the homepage."""
    return render_template('index.html')

@app.route('/static/generated/<path:filename>')
def serve_static(filename):
    """Serve static files from the generated folder."""
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

@app.route('/get-gradio-url', methods=['GET'])
def get_gradio_url():
    """
    Returns the Gradio space URL for embedding in an iframe.
    """
    gradio_url = "https://orderlymirror-text-to-video.hf.space"
    return jsonify({'gradio_url': gradio_url})

@app.route('/generate', methods=['POST'])
def generate():
    """
    Handle content generation requests.
    Automatically detects the content type and routes
    to the appropriate generation function.
    """
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # Detect content type
        media_type = detect_content_type(prompt)
        print(f"Detected media type: {media_type}")  # Debugging log

        # Generate content based on media type
        if media_type == 'text':
            context = analyze_context(prompt)
            raw_result = generate_text(prompt)
            formatted_result = format_output(raw_result, context)
            return jsonify({
                'result': formatted_result,
                'media_type': media_type,
                'context': context
            })

        elif media_type == 'music':
            return jsonify({'media_type': 'music'})


        elif media_type == 'image':
            filename = generate_image(prompt)
            file_url = f"{request.url_root}static/generated/{filename}"
            return jsonify({
                 'result': file_url,
                'media_type': media_type,
                'content_type': 'image/png'
                })
        elif media_type == 'video':
            return jsonify({'media_type': 'video'})
        else:
            return jsonify({'error': 'Unsupported content type'}), 400

    except Exception as e:
        # Log the error for debugging
        print(f"Error generating content: {e}")
        return jsonify({'error': f"Error generating content: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
