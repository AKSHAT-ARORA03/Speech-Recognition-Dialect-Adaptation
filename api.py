from flask import Flask, request, jsonify
from app.transcriber import transcribe_audio
from app.corrector import correct_transcript
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return '''
    <!doctype html>
    <html>
    <head><title>Upload Audio</title></head>
    <body>
      <h2>Upload an audio file</h2>
      <form method="POST" action="/transcribe" enctype="multipart/form-data">
        <input type="file" name="file" accept="audio/*" required>
        <br><br>
        <button type="submit">Transcribe</button>
      </form>
    </body>
    </html>
    '''

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio = request.files["file"]
    audio_path = "temp_audio"
    ext = audio.filename.split('.')[-1]
    raw_path = f"{audio_path}_raw.{ext}"
    wav_path = f"{audio_path}.wav"

    audio.save(raw_path)

    # Convert to wav using pydub
    try:
        audio_seg = AudioSegment.from_file(raw_path)
        audio_seg = audio_seg.set_channels(1).set_frame_rate(16000)
        audio_seg.export(wav_path, format="wav")
    except Exception as e:
        return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 400

    try:
        raw = transcribe_audio(wav_path)
        corrected = correct_transcript(raw)

        return jsonify({
            "raw_transcript": raw,
            "corrected_transcript": corrected
        })
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
    finally:
        # Clean up
        if os.path.exists(raw_path): os.remove(raw_path)
        if os.path.exists(wav_path): os.remove(wav_path)

if __name__ == "__main__":
    app.run(debug=True)
