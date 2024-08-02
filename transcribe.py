# src/babelscribe/transcribe.py

import os
import requests
from typing import Optional

def transcribe_audio(file_path: str, config: dict, language: Optional[str] = None) -> str:
    """
    Transcribe an audio file using OpenAI's Whisper API.
    
    Parameters:
    -----------
    file_path : str
        Path to the audio file to be transcribed.
    config : dict
        Configuration dictionary containing API settings.
    language : str, optional
        Optional language code in ISO-639-1 format.
    
    Returns:
    --------
    str
        The transcribed text from the audio file.
    
    Raises:
    -------
    Exception
        If there's an error in the API call or file processing.
    """
    url = "https://api.openai.com/v1/audio/transcriptions"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    
    try:
        with open(file_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {
                "model": config['whisper_model'],
                "response_format": config['whisper_response_format']
            }
            
            if language:
                data["language"] = language
            
            response = requests.post(url, headers=headers, files=files, data=data)
        
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise Exception(f"API error: {str(e)}")
    except IOError as e:
        raise Exception(f"File error: {str(e)}")

def process_audio_file(file_name: str, config: dict, language: Optional[str] = None) -> str:
    input_path = os.path.join(config['input_folder'], file_name)
    output_path = os.path.join(config['output_folder'], file_name)
    
    try:
        # Transcribe audio
        transcription = transcribe_audio(input_path, config, language)
        
        # Move processed file to output folder
        os.rename(input_path, output_path)
        
        return transcription
    except Exception as e:
        raise Exception(f"Error processing {file_name}: {str(e)}")