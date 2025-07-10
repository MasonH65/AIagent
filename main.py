import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: uv run main.py <prompt> <optional --verbose>")
    sys.exit(1)

prompt = sys.argv[1]
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
messages = [types.Content(role='user', parts=[types.Part(text=prompt)])]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

functions = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'write_file': write_file,
    'run_python_file': run_python_file,
}

def call_function(function_call_part, verbose):
    args = function_call_part.args or {}
    args['working_directory'] = "./calculator"
    
    if verbose:
        print(f"Calling function: {function_call_part.name}({args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name in functions:
        function_to_call = functions[function_call_part.name]
        result = function_to_call(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
def main():
    verbose = False

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages, 
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[available_functions],
            ),
        )
    
    if len(sys.argv) == 3:
        if sys.argv[2] == '--verbose':
            print(f'User prompt: {prompt}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
            verbose = True

    if response.function_calls:
        for function_call_part in response.function_calls:
            try:
                result = call_function(function_call_part, verbose)
                if not result.parts or not hasattr(result.parts[0], 'function_response'):
                    raise Exception('Invalid function response structure')
                if verbose:
                    print(f"-> {result.parts[0].function_response.response}")
            except Exception as e:
                print(f'Error: {e}')

    else:
        print(response.text)

if __name__ == "__main__":
    main()
