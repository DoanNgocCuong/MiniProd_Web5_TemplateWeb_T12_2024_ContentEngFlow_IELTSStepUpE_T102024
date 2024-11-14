import json
import pandas as pd
import time
import openai
from openai import OpenAIError
import re
import os
import random
import requests
from pathlib import Path
from dotenv import load_dotenv
import sys
import io
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set console encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# Get and print API key (chỉ hiện 10 ký tự đầu và cuối)
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    masked_key = f"{api_key[:10]}...{api_key[-10:]}"
    print(f"API Key loaded: {masked_key}")
else:
    print("Warning: No API key found!")

# Replace with your actual OpenAI API key from env
openai.api_key = api_key
logger.debug(f"OpenAI API key loaded: {'*' * len(str(openai.api_key))}")

# Define upload and output folders
UPLOAD_FOLDER = Path(__file__).parent.parent / 'uploads'
OUTPUT_FOLDER = Path(__file__).parent.parent / 'output'
OUTPUT_AUDIO_FOLDER = OUTPUT_FOLDER / 'output_audio'  # Define audio output subfolder

logger.debug(f"Upload folder path: {UPLOAD_FOLDER}")
logger.debug(f"Output folder path: {OUTPUT_FOLDER}")

def process_conversation(order, base_prompt, inputs):
    responses = []
    response_times = []
    message_history = [{"role": "system", "content": base_prompt}]

    for user_input in inputs:
        if pd.isna(user_input) or user_input == '':
            logger.warning(f"Empty input for order {order}, skipping")
            responses.append('')
            response_times.append('')
            continue

        message_history.append({"role": "user", "content": str(user_input)})
        start_time = time.time()
        try_count = 0
        
        while try_count < 3:
            try:
                completion = openai.chat.completions.create(
                    model="gpt-4-turbo-preview",  # hoặc model phù hợp khác
                    messages=message_history,
                    temperature=0,
                    max_tokens=1500,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                end_time = time.time()
                response_content = completion.choices[0].message.content
                
                message_history.append({"role": "assistant", "content": response_content})
                responses.append(response_content)
                response_times.append(end_time - start_time)
                
                logger.debug(f"Order {order}, Input: '{user_input}', Response received in {end_time - start_time:.2f}s")
                break
                
            except Exception as e:
                try_count += 1
                if try_count >= 3:
                    responses.append("Request failed after 2 retries.")
                    response_times.append("-")
                    logger.error(f"Order {order}, Input: '{user_input}', Response: 'Request failed after 2 retries.'")
                else:
                    time.sleep(3)

    return responses, response_times, message_history

def process_initial_data():
    try:
        logger.info("Starting initial data processing")
        
        # Read input Excel file
        df_input = pd.read_excel(UPLOAD_FOLDER / 'data.xlsx')
        output_rows = []

        for index, row in df_input.iterrows():
            order = row['order']
            prompt = row['prompt']
            first_input = row.get('first', '')
            
            # Process conversation
            responses, response_times, _ = process_conversation(order, prompt, [first_input])
            
            # Create output row
            output_row = {
                'order': order,
                'User Input': first_input,
                'json': responses[0] if responses else '',
                'Response Time': response_times[0] if response_times else ''
            }
            output_rows.append(output_row)
            
            # Log for debugging
            logger.debug(f"Processed row - Order: {order}")
            logger.debug(f"Response: {responses[0] if responses else 'No response'}")

        # Create DataFrame
        df_output = pd.DataFrame(output_rows)
        
        # Ensure output directory exists
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        
        # Save to Excel
        output_path = OUTPUT_FOLDER / 'output_draft.xlsx'
        df_output.to_excel(output_path, index=False)
        
        logger.info(f"Output saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error in process_initial_data: {str(e)}", exc_info=True)
        raise

def process_story_data():
    try:
        logger.info("Starting story data processing")
        input_path = OUTPUT_FOLDER / 'output_draft.xlsx'
        df_input = pd.read_excel(input_path)
        story_output_rows = []

        for _, row in df_input.iterrows():
            order = row['order']
            logger.debug(f"Processing story data for order {order}")
            try:
                # Thêm kiểm tra và chuyển đổi kiểu dữ liệu
                json_data = row['json']
                if pd.isna(json_data):
                    logger.warning(f"Empty JSON for order {order}, skipping")
                    continue
                    
                # Chuyển đổi thành string nếu không phải
                if not isinstance(json_data, str):
                    logger.warning(f"Converting non-string JSON for order {order}")
                    json_data = str(json_data)
                
                data = json.loads(json_data)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON for order {row['order']}, skipping")
                continue
            except KeyError:
                logger.warning(f"Missing 'json' column for order {row['order']}, skipping")
                continue
            
            for situation in data:
                situation_en = situation['situation_en']
                situation_vn = situation['situation']
                for idx, convo in enumerate(situation['conversation']):
                    role = convo['role']
                    content = convo['content']
                    translation_en = convo['translation_en']
                    audio_name = f"https://smedia.stepup.edu.vn/ielts/chunking/listening/{order}/{role}.wav"
                    story_output_rows.append(["", "", "", "bot-left" if idx % 2 == 0 else "bot-right", translation_en, content, audio_name])

                summary_row = [order, situation_en, situation_vn, '', '', '', '']
                story_output_rows.append(summary_row)

        df_story = pd.DataFrame(story_output_rows, columns=['order', 'situation_en', 'situation', 'role', 'content', 'translation_en', 'audio_name'])
        output_path = OUTPUT_FOLDER / 'output_story.xlsx'
        df_story.to_excel(output_path, index=False)
        logger.info(f"Story data processing complete, saved to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error in process_story_data: {str(e)}", exc_info=True)
        raise

def remove_tags(text):
    return re.sub(r'<\/?r>', '', text)

def send_request(text, voice, order, role):
    try:
        logger.debug(f"Sending TTS request for order {order}, role {role}")
        url = 'http://103.253.20.13:25006/tts_to_audio'
        headers = {'Content-Type': 'application/json'}
        data = {
            "text": text,
            "speaker_wav": voice,
            "language": "en"
        }
        response = requests.post(url, headers=headers, json=data)
        
        # Save to output_story_audio folder only
        audio_dir = OUTPUT_AUDIO_FOLDER / str(order)
        audio_dir.mkdir(parents=True, exist_ok=True)
        output_file = audio_dir / f'{role}.wav'
        
        with open(output_file, 'wb') as f:
            f.write(response.content)
            
        logger.debug(f"Audio file saved: {output_file}")
    except Exception as e:
        logger.error(f"Error in send_request: {str(e)}", exc_info=True)
        raise

def generate_audio():
    try:
        logger.info("Starting audio generation")
        df_input = pd.read_excel(OUTPUT_FOLDER / 'output_draft.xlsx')
        
        for index, row in df_input.iterrows():
            order = row['order']
            logger.debug(f"Generating audio for order {order}")
            data = json.loads(row['json'])
            selected_voices = {}
            
            for convo in data[0]["conversation"]:
                role = convo["role"]
                if "female" in role and "female" not in selected_voices:
                    selected_voices["female"] = random.choice([
                        "claire1", "Elli", "Lily","xayah", "caitlyn", "ahri",
                        "Mimi","en-US-Neural2-H","murf_default"
                    ])
                elif "male" in role and "male" not in selected_voices:
                    selected_voices["male"] = random.choice([
                        "male", "Jeremy", "Adam", "Antoni","aloy_openai",
                        "en-US-Neural2-D","en-US-Neural2-J","en-US-Neural2-A","Sam"
                    ])
            
            for entry in data:
                for convo in entry["conversation"]:
                    role = convo["role"]
                    text = remove_tags(convo["translation_en"])
                    voice = selected_voices["female"] if "female" in role else selected_voices["male"]
                    send_request(text, voice, order, role)
        logger.info("Audio generation complete")
    except Exception as e:
        logger.error(f"Error in generate_audio: {str(e)}", exc_info=True)
        raise

def main():
    try:
        logger.info("Starting main process")
        # Ensure output directory exists
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        
        print("Processing initial data...")
        process_initial_data()
        
        print("\nProcessing story data...")
        output_story_path = process_story_data()
        
        print("\nGenerating audio files...")
        generate_audio()
        
        logger.info(f"Processing complete. Final output saved to: {output_story_path}")
        print(f"Processing complete. Final output saved to: {output_story_path}")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()