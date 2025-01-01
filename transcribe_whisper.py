# Setup instructions for Windows
# pip install git+https://github.com/openai/whisper.git
# winget install "FFmpeg (Essentials Build)"

import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("base")  # Change "base" to other model sizes if needed
    print(f"Transcribing: {file_path}")
    result = model.transcribe(
        file_path,
        language="en",  # Force interpretation in English
    )
    
    # Print the transcription
    transcription = result["text"]
    print("\nTranscription:")
    print(transcription)

if __name__ == "__main__":
    audio_file = "recording.mkv"  # Replace with the actual full path to your file
    transcribe_audio(audio_file)
