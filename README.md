# BabbleScribe

BabbleScribe is an audio transcription tool that converts speech to text with high accuracy using the OpenAI whisper API. This repository contains the backend functionality for BabbleScribe.

## Features

- Audio file transcription using OpenAI's Whisper API
- Support for multiple audio formats (flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm)
- Organized file management with separate input, output, and transcription folders
- Markdown formatting for transcription output

## Dependencies

- Python 3.7+
- requests==2.31.0
- python-dotenv==0.19.1

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/babblescribe.git
   cd babblescribe
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Project Structure

```
babblescribe/
│
├── main.py
├── requirements.txt
├── .env
├── input/
├── output/
└── transcriptions/
```

- `main.py`: Contains the main transcription logic
- `input/`: Place audio files here for transcription
- `output/`: Processed audio files are moved here
- `transcriptions/`: Transcription results in markdown format are saved here

## Usage

1. Place your audio file(s) in the `input/` folder.

2. Run the transcription script:
   ```
   python main.py
   ```

3. Follow the prompts to enter the language code (optional) for the audio files.

4. The script will process all supported audio files in the `input/` folder, move them to the `output/` folder, and save markdown transcriptions in the `transcriptions/` folder.

## API Documentation

While BabbleScribe doesn't currently expose its own API, it interacts with the OpenAI Whisper API. Here's how the API is used in the project:

```python
def transcribe_audio(file_path, language=None):
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
```

This function sends a POST request to the Whisper API with the audio file and receives the transcription in response.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


Happy transcribing with BabbleScribe! If you encounter any issues or have suggestions for improvements, please open an issue on GitHub.🎙️📝
