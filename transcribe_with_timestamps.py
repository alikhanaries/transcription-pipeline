import os
import sys
import json
import subprocess
import whisper

# Allowed audio formats
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}
MAX_FILE_SIZE_MB = 100  # Max 100 MB per file

def validate_audio_file(file_path: str):
    """Check if file exists, format is allowed, and size is reasonable."""
    if not os.path.exists(file_path):
        raise FileNotFoundError("Audio file does not exist.")
    
    extension = os.path.splitext(file_path)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported format. Allowed: {ALLOWED_EXTENSIONS}")
    
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"File too large. Max allowed size is {MAX_FILE_SIZE_MB} MB.")

def normalize_audio(file_path: str) -> str:
    """Convert audio to mono WAV at 16kHz using ffmpeg."""
    normalized_file = "normalized_audio.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", file_path, "-ac", "1", "-ar", "16000", normalized_file
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return normalized_file

def transcribe_with_timestamps(file_path: str):
    """Transcribe audio and return JSON with segments and timestamps."""
    print("🔄 Loading Whisper model...")
    model = whisper.load_model("base")
    
    print("🎙 Normalizing audio...")
    normalized_file = normalize_audio(file_path)
    
    print("🎙 Transcribing audio with timestamps...")
    result = model.transcribe(normalized_file)
    
    segments_output = []
    for segment in result["segments"]:
        segments_output.append({
            "start": round(segment["start"], 2),
            "end": round(segment["end"], 2),
            "text": segment["text"].strip()
        })
    
    response = {
        "language": result.get("language"),
        "full_text": result["text"].strip(),
        "segments": segments_output
    }
    
    return response

def main():
    if len(sys.argv) != 2:
        print("Usage: python transcribe_with_timestamps.py <audio_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        validate_audio_file(file_path)
        output = transcribe_with_timestamps(file_path)
        print("\n✅ Transcription Complete:\n")
        print(json.dumps(output, indent=4))
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()