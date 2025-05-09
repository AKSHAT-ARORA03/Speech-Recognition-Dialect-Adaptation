import whisper
from app.corrector import correct_transcript  # Assuming this is your error correction function

# Load the Whisper model (you can use a larger model for more accuracy, like "large" or "xlarge")
model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    # Perform transcription using Whisper
    print("Transcribing audio...")
    result = model.transcribe(audio_path)
    
    # Extract raw transcription text
    transcript = result["text"]
    
    # Apply error correction to improve transcript quality
    print("Applying error correction...")
    corrected_transcript = correct_transcript(transcript)
    
    # Return the corrected transcript
    return corrected_transcript

# Example usage:
# transcribe_audio("path/to/audio_file.mp3")
