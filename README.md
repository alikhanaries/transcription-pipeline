# Transcription Pipeline

## Overview
This project implements a simple transcription pipeline in Python. It accepts audio files (WAV, MP3, M4A), transcribes the spoken language into text, and provides timestamps for each segment. The pipeline is designed to be simple, reliable, and easy to integrate into other systems or applications. It focuses on engineering decisions and robustness rather than training any models from scratch.

---

## Key Features
- Accepts common audio formats: WAV, MP3, M4A
- Transcribes speech to text using the open-source **Whisper** model
- Returns structured JSON output including segment-level timestamps
- Handles long audio files via chunking (optional for scalability)
- Validates file type and size before processing
- Easily extendable into a REST API for concurrent uploads

---

## Design Decisions

### 1. Choice of Transcription Engine
I used the **Whisper** model by OpenAI because it:
- Provides high transcription accuracy
- Supports multiple languages
- Is open-source and can run locally, reducing costs
- Supports timestamps natively, which is required for segment-level output

### 2. Handling Different Audio Formats
- The system accepts WAV, MP3, and M4A audio files.
- All audio files are converted to **mono WAV at 16 kHz** using ffmpeg to normalize the input.
- This ensures consistent input quality and improves transcription accuracy.
- Unsupported formats trigger a clear error message.

### 3. Segment Timestamps
- Whisper provides timestamps for each segment of audio.
- The pipeline returns structured JSON including start and end times for each segment.
- This makes it easy to generate subtitles or align text with audio in downstream applications.

### 4. Handling Long Audio Files
- Large audio files can be split into smaller chunks for transcription.
- Each chunk is processed separately and then merged to form a full transcription.
- This prevents memory issues and allows parallel processing if scaled.

### 5. Error Handling and Retries
- The pipeline checks for invalid formats, missing files, and oversized audio.
- Failed transcriptions can be retried automatically or flagged for the user to retry manually.

### 6. Concurrent Uploads
- The pipeline can be extended into a **REST API** using FastAPI.
- Concurrent uploads can be handled with a job queue and background workers.
- This ensures multiple users can submit audio files simultaneously without errors.

### 7. Storage
- Audio files and transcripts can be stored in cloud storage (like AWS S3) or local storage.
- Transcripts are saved in structured JSON format, making them easy to use in other applications.

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt

### 2. Run the transcription script

#### For a single file:

python transcribe_with_timestamps.py sample_audio/test_1.mp3


#### For processing all files in the folder (if batch mode is enabled in the script):

python transcribe_with_timestamps.py


### 3. Expected JSON OUTPUT
{
    "language": "en",
    "full_text": "Hello everyone. Welcome to the demo.",
    "segments": [
        {
            "start": 0.0,
            "end": 3.42,
            "text": "Hello everyone."
        },
        {
            "start": 3.42,
            "end": 6.10,
            "text": "Welcome to the demo."
        }
    ]
}


### 4. PROJECT STRUCTURE

transcription-pipeline/
│
├── transcribe_with_timestamps.py   # Main transcription script
├── requirements.txt                # Python dependencies
├── README.md                       # Project explanation and design decisions
├── sample_audio/                   # Sample short audio files for testing
│   ├── test_1.mp3
│   ├── test_2.mp3
│   └── demo_audio.wav
└── .gitignore                      # Ignore __pycache__, uploads, normalized audio