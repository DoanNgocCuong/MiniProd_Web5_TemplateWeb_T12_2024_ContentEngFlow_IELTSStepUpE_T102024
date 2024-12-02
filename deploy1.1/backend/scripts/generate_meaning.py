import subprocess
import os
import re
import json
import time
import pandas as pd
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import sys
import logging
import requests

# Set console output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

UPLOAD_FOLDER = Path(__file__).parent.parent / 'uploads'
OUTPUT_FOLDER = Path(__file__).parent.parent / 'output'  # Define output folder
OUTPUT_MEANING_FOLDER = OUTPUT_FOLDER / 'output_audio'  # Define output subfolder for meaning exercises
data = pd.read_excel(UPLOAD_FOLDER / 'data.xlsx')

# Create an empty list to store the output data
output_data = []

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def save_audio_file(text, order):
    try:
        # Log the input parameters
        logger.info(f"Attempting to save audio for text: {text}, order: {order}")
        
        # Tạo thư mục con theo số thứ tự
        order_folder = OUTPUT_MEANING_FOLDER / str(order)
        logger.info(f"Creating folder at: {order_folder}")
        order_folder.mkdir(parents=True, exist_ok=True)
        
        # Đường dẫn file output
        output_file = order_folder / 'choose_answer.mp3'
        logger.info(f"Output file will be saved at: {output_file}")
        
        # Use requests instead of curl
        url = "http://103.253.20.13:25010/api/text-to-speech"
        headers = {"Content-Type": "application/json"}
        data = {
            "text": text,
            "voice": "en-CA-ClaraNeural",
            "speed": 1
        }
        
        logger.info(f"Sending request to: {url}")
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            # Save the audio content to file
            with open(output_file, 'wb') as f:
                f.write(response.content)
            logger.info(f"Audio file successfully saved at: {output_file}")
            logger.info(f"File size: {output_file.stat().st_size} bytes")
        else:
            logger.error(f"Failed to get audio. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            
    except Exception as e:
        logger.error(f"Error saving audio file for order {order}: {str(e)}", exc_info=True)
        raise

# Loop through each row in the Excel file
for index, row in data.iterrows():
    prompt = row['prompt_meaning']
    message = row['vocabulary']
    order = row['order']
    stt_week = row['week']  # Get the week value
    start_time = time.time()    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=2500,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=1,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ]
        )
        
        response_content = response.choices[0].message.content
        end_time = time.time()
        print(response_content)
        
        # Parse the JSON response content
        response_json = json.loads(response_content)
        
        # Extract the 'question', 'answer', and 'explain' fields
        question = response_json.get("question", "").strip()
        answer = response_json.get("answer", "").strip()
        explain = response_json.get("explain", "").strip()
        
        # Generate the audio URL using the order value
        # audio_url = f"https://smedia.stepup.edu.vn/ielts/chunking/listening/{order}/choose_answer.mp3"
        # Muốn update thành:
        audio_url = f"https://smedia.stepup.edu.vn/ielts/chunking/listening/week_{stt_week}/{order}/choose_answer.mp3"
        
        # Append the output to the list
        output_data.append({
            "id": f"vs_choose_answer_question_{order}",
            "vocabulary_id": f"vocab_{order}",
            "title": "CHỌN ĐÁP ÁN",
            "order": "4",
            "progress": "TRẮC NGHIỆM",
            "question": question,
            "answer": answer,
            "audio": audio_url,
            "feedback_1": explain
        })

        # Prepare the output directory for saving the audio file
        if not os.path.exists(OUTPUT_MEANING_FOLDER):
            os.makedirs(OUTPUT_MEANING_FOLDER)

        # Save the audio file
        save_audio_file(question, order)
    except Exception as e:
        print(f"Error processing row {index}: {e}")

# Convert the output list to a DataFrame and save it to an Excel file
output_df = pd.DataFrame(output_data)
output_df.to_excel(f'{OUTPUT_FOLDER}/output_meaning.xlsx', index=False)