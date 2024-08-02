# src/babelscribe/utils.py

import os
import yaml
from datetime import datetime
from typing import Dict, Any, Union, Tuple, Optional

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load the configuration from the YAML file.
    
    Parameters:
    -----------
    config_path : str, optional
        Path to the configuration file (default is "config.yaml")
    
    Returns:
    --------
    Dict[str, Any]
        A dictionary containing the configuration settings
    
    Raises:
    -------
    FileNotFoundError
        If the configuration file is not found
    yaml.YAMLError
        If there's an error parsing the YAML file
    """
    try:
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing the configuration file: {e}")

def ensure_folders_exist(config: Dict[str, Any]) -> None:
    """
    Ensure that the required folders exist, creating them if necessary.
    
    Parameters:
    -----------
    config : Dict[str, Any]
        The configuration dictionary containing folder paths
    """
    for folder in [config['input_folder'], config['output_folder'], config['transcription_folder']]:
        os.makedirs(folder, exist_ok=True)

def save_results(file_name: str, transcription: str, summary: Optional[str], config: Dict[str, Any]) -> str:
    base_name = os.path.splitext(file_name)[0]
    output_file = f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    output_path = os.path.join(config['transcription_folder'], output_file)
    
    with open(output_path, 'w') as f:
        f.write(f"# Transcription and Summary of {file_name}\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Transcription\n\n")
        f.write(transcription)
        f.write("\n\n## Summary\n\n")
        if summary:
            f.write(summary)
        else:
            f.write("Summary generation failed.")

    return output_path