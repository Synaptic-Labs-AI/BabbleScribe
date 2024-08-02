#!/usr/bin/env python3
# src/babelscribe/main.py

import os
from dotenv import load_dotenv
from utils import load_config, ensure_folders_exist, save_results
from transcribe import process_audio_file
from summarize import summarize_text

def main():
    # Load environment variables
    load_dotenv()

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return

    # Ensure necessary folders exist
    ensure_folders_exist(config)

    # Get language input from user
    language = input("Enter the language code for all files (optional, press Enter to skip): ").strip() or None

    # Process audio files
    input_folder = config['input_folder']
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('.flac', '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.ogg', '.wav', '.webm')):
            print(f"Processing {file_name}...")
            try:
                # Transcribe audio
                transcription = process_audio_file(file_name, config, language)
                print("Transcription complete.")

                # Summarize transcription
                summary = summarize_text(transcription, config)
                print("Summary complete.")

                # Save results
                output_path = save_results(file_name, transcription, summary, config)
                print(f"Results saved to {output_path}")

            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")

    print("All files processed.")

if __name__ == "__main__":
    main()