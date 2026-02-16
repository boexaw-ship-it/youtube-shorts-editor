#!/usr/bin/env python3
"""
YouTube Shorts AI Editor - Python Backend
Alternative implementation using Flask + MoviePy
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx import mirror_x, mirror_y, speedx
import google.generativeai as genai
import threading
import time

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'aac', 'm4a'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# Create directories
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


def cleanup_old_files():
    """Delete files older than 24 hours"""
    max_age = timedelta(hours=24)
    now = datetime.now()
    
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                file_age = now - datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_age > max_age:
                    try:
                        os.remove(filepath)
                        print(f"Deleted old file: {filename}")
                    except Exception as e:
                        print(f"Error deleting {filename}: {e}")


# Periodic cleanup (runs every hour)
def periodic_cleanup():
    while True:
        time.sleep(3600)  # 1 hour
        cleanup_old_files()

cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
cleanup_thread.start()


@app.route('/api/generate-script', methods=['POST'])
def generate_script():
    """Generate video script using Gemini AI"""
    try:
        data = request.json
        api_key = data.get('apiKey')
        topic = data.get('topic')
        
        if not api_key or not topic:
            return jsonify({'error': 'API Key and topic are required'}), 400
        
        # Configure Gemini AI
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Create a 30-45 second YouTube Shorts script about: {topic}. 

The script should be:
- In Myanmar (Burmese) language
- Engaging and trendy
- Include a strong hook in the first 3 seconds
- Have clear, conversational narration
- End with a call-to-action
- Keep it simple and easy to follow

Format the script with timing markers like [0-3s], [4-10s], etc."""
        
        response = model.generate_content(prompt)
        script_text = response.text
        
        return jsonify({
            'success': True,
            'script': script_text
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-video', methods=['POST'])
def upload_video():
    """Upload video file"""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({'error': 'Invalid file format'}), 400
        
        filename = secure_filename(f"{int(time.time())}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'path': filepath
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-audio', methods=['POST'])
def upload_audio():
    """Upload audio file"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
            return jsonify({'error': 'Invalid audio format'}), 400
        
        filename = secure_filename(f"{int(time.time())}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'path': filepath
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process-video', methods=['POST'])
def process_video():
    """Process video with all effects"""
    try:
        # Get parameters
        video_file = request.files.get('video')
        speed = float(request.form.get('speed', 1.0))
        mirror_h = request.form.get('mirrorH', 'false').lower() == 'true'
        mirror_v = request.form.get('mirrorV', 'false').lower() == 'true'
        blur = int(request.form.get('blur', 0))
        text_overlays = json.loads(request.form.get('textOverlays', '[]'))
        audio_file_path = request.form.get('audioFile')
        format_type = request.form.get('format', 'shorts')
        
        if not video_file:
            return jsonify({'error': 'No video file provided'}), 400
        
        # Save uploaded video
        video_filename = secure_filename(f"{int(time.time())}_{video_file.filename}")
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
        video_file.save(video_path)
        
        # Load video
        video = VideoFileClip(video_path)
        
        # Apply speed
        if speed != 1.0:
            video = video.fx(speedx, speed)
        
        # Apply mirror/flip
        if mirror_h:
            video = video.fx(mirror_x)
        if mirror_v:
            video = video.fx(mirror_y)
        
        # Resize to YouTube Shorts/TikTok format (9:16)
        if format_type in ['shorts', 'tiktok']:
            target_width = 1080
            target_height = 1920
            
            # Calculate scaling
            scale = min(target_width / video.w, target_height / video.h)
            new_width = int(video.w * scale)
            new_height = int(video.h * scale)
            
            video = video.resize((new_width, new_height))
            
            # Add padding if needed
            if new_width != target_width or new_height != target_height:
                video = video.on_color(
                    size=(target_width, target_height),
                    color=(0, 0, 0),
                    pos='center'
                )
        
        # Add text overlays
        clips = [video]
        for overlay in text_overlays:
            text = overlay['text']
            start_time = overlay['time']
            duration = 5  # Show for 5 seconds
            
            txt_clip = (TextClip(text, 
                                fontsize=48, 
                                color='white',
                                font='DejaVu-Sans-Bold',
                                stroke_color='black',
                                stroke_width=3)
                       .set_position('center')
                       .set_start(start_time)
                       .set_duration(duration))
            
            clips.append(txt_clip)
        
        # Composite video with overlays
        if len(clips) > 1:
            video = CompositeVideoClip(clips)
        
        # Add background audio
        if audio_file_path and os.path.exists(audio_file_path):
            audio = AudioFileClip(audio_file_path)
            
            # Mix with original audio
            if video.audio:
                from moviepy.audio.AudioClip import CompositeAudioClip
                audio = CompositeAudioClip([video.audio, audio])
            
            video = video.set_audio(audio)
        
        # Export
        output_filename = f"processed_{int(time.time())}.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30,
            preset='medium'
        )
        
        # Cleanup
        video.close()
        
        return jsonify({
            'success': True,
            'outputFile': output_filename,
            'downloadUrl': f'/download/{output_filename}'
        })
        
    except Exception as e:
        print(f"Processing error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download processed video"""
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'YouTube Shorts Editor API is running'
    })


if __name__ == '__main__':
    print("🚀 YouTube Shorts Editor Server (Python/Flask)")
    print("📹 Upload endpoint: http://localhost:5000/api/upload-video")
    print("🎬 Process endpoint: http://localhost:5000/api/process-video")
    print("🤖 Script generation: http://localhost:5000/api/generate-script")
    app.run(host='0.0.0.0', port=5000, debug=True)
