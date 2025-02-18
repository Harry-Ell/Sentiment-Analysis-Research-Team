import requests
import json
import time
from report_downloader2 import extract_filings_text

# Get the first file path by calling the function
cik = "0000320193"  # Apple Inc.'s CIK
first_file_path = extract_filings_text(cik, 'AAPL', 5)

if first_file_path:
    with open(first_file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    def make_api_call(file_content):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer <INSERT KEY>",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free", 
                "messages": [
                    {"role": "user", "content": f"Extract the exact text from the 'Risks' section of this file. Do not summarize, rephrase, or add any extra words—provide the content exactly as it appears:\n\n{file_content}"}
                ],
                "top_p": 0.99,
                "temperature": 0.63,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "repetition_penalty": 1,
                "top_k": 0,
            })
        )
        return response

    max_retries = 5
    retry_delay = 15  

    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries}...")
        response = make_api_call(file_content)
        if response.status_code == 429 or (response.status_code == 200 and 'error' in response.json() and response.json()['error']['code'] == 429) or (response.status_code == 200 and response.json().get('usage', {}).get('completion_tokens', 1) <= 0) or response.status_code != 200:
            print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            break

    if response.status_code == 200:
        response_json = response.json()
        if response_json.get('choices') and response_json['choices'][0]['message']['content']:
            print("API response:")
            print(response_json['choices'][0]['message']['content'])
        else:
            print("API response is empty or invalid.")
            print(response_json)
    else:
        print("Failed to get a valid response from the API.")
else:
    print("No file was saved.")