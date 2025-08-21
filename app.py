#!/usr/bin/env python3
"""
Ultra Simple TTS System using only gTTS
No FFmpeg, no pydub, no audio processing dependencies
"""

import os
import tempfile
import uuid
from datetime import datetime
import logging
import re
from io import BytesIO

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gtts import gTTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

class SimpleTTSManager:
    """Ultra simple TTS manager using only gTTS"""
    
    def __init__(self):
        # Available languages (gTTS supported)
        self.languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }
        
        # Simple voice options (using different TLDs)
        self.voices = {
            'default': {'lang': 'en', 'tld': 'com'},
            'british': {'lang': 'en', 'tld': 'co.uk'},
            'australian': {'lang': 'en', 'tld': 'com.au'},
            'canadian': {'lang': 'en', 'tld': 'ca'}
        }
        
        logger.info("Simple TTS Manager initialized")
    
    def clean_text(self, text):
        """Basic text cleaning"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Basic abbreviation expansion
        replacements = {
            "Dr.": "Doctor", "Mr.": "Mister", "Mrs.": "Missus",
            "vs.": "versus", "etc.": "etcetera"
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Ensure sentence ending
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def generate_speech(self, text, language='en', voice='default'):
        """Generate speech using gTTS - returns MP3 data"""
        try:
            # Clean text
            text = self.clean_text(text)
            logger.info(f"Generating speech: '{text[:50]}...'")
            
            # Get voice settings
            if voice in self.voices:
                lang = self.voices[voice]['lang']
                tld = self.voices[voice]['tld']
            else:
                lang = language if language in self.languages else 'en'
                tld = 'com'
            
            # Create TTS
            tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
            
            # Save to memory buffer
            buffer = BytesIO()
            tts.write_to_fp(buffer)
            buffer.seek(0)
            
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Speech generation failed: {e}")
            raise e

# Initialize manager
tts_manager = SimpleTTSManager()

@app.route('/', methods=['GET'])
def home():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "message": "Ultra Simple TTS is running",
        "service": "Google TTS (gTTS)",
        "languages": len(tts_manager.languages)
    })

@app.route('/api/tts/languages', methods=['GET'])
def get_languages():
    """Get available languages"""
    return jsonify({
        "languages": [
            {"code": code, "name": name} 
            for code, name in tts_manager.languages.items()
        ]
    })

@app.route('/api/tts/voices', methods=['GET'])
def get_voices():
    """Get available voices"""
    return jsonify({
        "voices": [
            {"id": voice_id, "name": voice_id.title(), "language": config['lang']}
            for voice_id, config in tts_manager.voices.items()
        ]
    })

@app.route('/api/tts/generate', methods=['POST'])
def generate_speech():
    """Generate speech - returns MP3 directly"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        if len(text) > 1000:
            return jsonify({"error": "Text too long (max 1000 characters)"}), 400
        
        # Get parameters
        language = data.get('language', 'en')
        voice = data.get('voice', 'default')
        
        logger.info(f"Request: lang={language}, voice={voice}")
        
        # Generate speech
        audio_data = tts_manager.generate_speech(
            text=text,
            language=language,
            voice=voice
        )
        
        # Create file
        audio_id = str(uuid.uuid4())
        filename = f"speech_{audio_id}.mp3"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        
        logger.info(f"Speech saved: {filename} ({len(audio_data)} bytes)")
        
        return jsonify({
            "success": True,
            "audio_id": audio_id,
            "filename": filename,
            "file_size": len(audio_data),
            "format": "mp3",
            "service": "Google TTS"
        })
        
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tts/download/<audio_id>')
def download_audio(audio_id):
    """Download audio file"""
    try:
        filename = f"speech_{audio_id}.mp3"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tts/stream/<audio_id>')
def stream_audio(audio_id):
    """Stream audio file"""
    try:
        filename = f"speech_{audio_id}.mp3"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(filepath, mimetype='audio/mpeg')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tts/test')
def test_service():
    """Test service"""
    try:
        test_audio = tts_manager.generate_speech("Testing, one, two, three.")
        return jsonify({
            "status": "working",
            "test_size": len(test_audio),
            "message": "TTS service is operational"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Ultra Simple TTS Server...")
    logger.info("No FFmpeg required!")
    
    # Quick test
    try:
        test_tts = gTTS(text="test", lang='en')
        logger.info("gTTS is working")
    except Exception as e:
        logger.error(f"gTTS test failed: {e}")
    
    # Start server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)