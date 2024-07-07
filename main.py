import os
import requests
import shutil
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")

# Define folder paths
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
TRANSCRIPTION_FOLDER = "transcriptions"

def ensure_folders_exist():
    """Ensure that the required folders exist."""
    for folder in [INPUT_FOLDER, OUTPUT_FOLDER, TRANSCRIPTION_FOLDER]:
        os.makedirs(folder, exist_ok=True)

def transcribe_audio(file_path, language=None):
    """
    Transcribe an audio file using OpenAI's Whisper API.
    
    :param file_path: Path to the audio file
    :param language: Optional language code in ISO-639-1 format
    :return: Transcription text
    """
    url = "https://api.openai.com/v1/audio/transcriptions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    with open(file_path, "rb") as audio_file:
        files = {"file": audio_file}
        data = {
            "model": "whisper-1",
            "response_format": "text"
        }
        
        if language:
            data["language"] = language
        
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def process_audio_file(file_name, language=None):
    """
    Process a single audio file: transcribe, move to output, and save transcription.
    
    :param file_name: Name of the audio file in the input folder
    :param language: Optional language code in ISO-639-1 format
    """
    input_path = os.path.join(INPUT_FOLDER, file_name)
    output_path = os.path.join(OUTPUT_FOLDER, file_name)
    
    try:
        # Transcribe audio
        transcription = transcribe_audio(input_path, language)
        
        # Move processed file to output folder
        shutil.move(input_path, output_path)
        
        # Save transcription as markdown
        base_name = os.path.splitext(file_name)[0]
        transcript_file_name = f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        transcript_path = os.path.join(TRANSCRIPTION_FOLDER, transcript_file_name)
        
        with open(transcript_path, "w") as f:
            f.write(f"# Transcription of {file_name}\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Content\n\n")
            f.write(transcription)
        
        print(f"Processed {file_name}. Transcription saved to {transcript_path}")
    
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

def main():
    ensure_folders_exist()
    
    language = input("Enter the language code for all files (optional, press Enter to skip): ")
    
    for file_name in os.listdir(INPUT_FOLDER):
        if file_name.lower().endswith(('.flac', '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.ogg', '.wav', '.webm')):
            process_audio_file(file_name, language if language else None)
        else:
            print(f"Skipping {file_name}: not a supported audio format")

if __name__ == "__main__":
    main()