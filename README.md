# Simple Text-to-Speech System

A lightweight web-based Text-to-Speech system using Google's gTTS (Google Text-to-Speech) service.

## Features

- Web-based interface for easy text input
- Multiple language support (English, Spanish, French, German, etc.)
- Different voice options (US, UK, Australian, Canadian accents)
- Real-time speech generation
- Audio download functionality
- No heavy dependencies or model downloads required

## Technologies Used

- **Backend**: Python Flask with gTTS
- **Frontend**: HTML, CSS, JavaScript
- **TTS Service**: Google Text-to-Speech API

## Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection (required for Google TTS service)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/simple-tts-system.git
cd simple-tts-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Start the Backend Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

### Access the Web Interface

**Option 1: Direct file opening**
- Open `index.html` in your web browser

**Option 2: HTTP server (recommended)**
```bash
python -m http.server 8000
```
Then visit: `http://localhost:8000`

### Using the System

1. Enter text in the input field
2. Select language and voice options
3. Click "Generate Speech"
4. Play the generated audio or download it

## API Endpoints

- `GET /` - Health check
- `GET /api/tts/languages` - Get available languages
- `GET /api/tts/voices` - Get available voices
- `POST /api/tts/generate` - Generate speech from text
- `GET /api/tts/download/<audio_id>` - Download audio file
- `GET /api/tts/stream/<audio_id>` - Stream audio file

### Example API Request

```bash
curl -X POST http://localhost:5000/api/tts/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "language": "en", "voice": "default"}'
```

## Supported Languages

- English (en) - US, UK, Australian, Canadian accents
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- Arabic (ar)
- Hindi (hi)

## Configuration

The system uses environment variables for configuration:

- `PORT` - Server port (default: 5000)
- `DEBUG` - Debug mode (default: False)

## Limitations

- Requires internet connection for speech generation
- Text length limited to 1000 characters per request
- Audio output format is MP3
- Speed control not available (limitation of gTTS)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Google Text-to-Speech (gTTS) for the TTS engine
- Flask for the web framework
- Contributors and testers

## Troubleshooting

### Common Issues

**Server won't start:**
- Check if port 5000 is already in use
- Verify all dependencies are installed
- Check internet connection

**No audio generated:**
- Verify internet connection
- Check server logs for errors
- Try with shorter text

**Frontend can't connect:**
- Ensure backend server is running
- Check for CORS issues
- Try using HTTP server instead of file:// protocol

