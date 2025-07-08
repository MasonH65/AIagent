import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: uv run main.py <prompt> <optional --verbose>")
    sys.exit(1)

prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
messages = [types.Content(role='user', parts=[types.Part(text=prompt)])]

def get_files_info(working_directory, directory=None):
    full_path = os.path.join(working_directory, directory)
    if os.path.abspath(directory) != full_path:
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if os.path.isdir(full_path) == False:
        raise Exception(f'Error: "{directory}" is not a directory')
    else:
        return (f'')

def main():
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
    print(response.text)
    if len(sys.argv) == 3:
        if sys.argv[2] == '--verbose':
            print(f'User prompt: {prompt}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
