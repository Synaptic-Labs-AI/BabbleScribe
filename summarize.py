# src/babelscribe/summarize.py

import os
import requests
import json

def summarize_text(transcription: str, config: dict) -> str:
    """
    Summarize the given transcription using the OpenRouter API.
    
    Parameters:
    -----------
    transcription : str
        The transcribed text to be summarized.
    config : dict
        Configuration dictionary containing API settings.
    
    Returns:
    --------
    str
        The summarized text.
    
    Raises:
    -------
    Exception
        If there's an error in the API call or response processing.
    """
    url = config['openrouter_url']
    
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": config['your_site_url'],
        "X-Title": config['your_app_name'],
    }
    
    data = {
        "model": config['openrouter_model'],
        "messages": [
            {"role": "system", "content": config['summary_prompt']},
            {"role": "user", "content": transcription}
        ],
        "max_tokens": config['max_tokens'],
        "temperature": config['temperature'],
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        summary = result['choices'][0]['message']['content']
        return summary.strip()
    except requests.RequestException as e:
        raise Exception(f"API error: {str(e)}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise Exception(f"Error processing API response: {str(e)}")