import os
from google.genai import types

def write_file(working_directory, file_path, content):
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_dir, file_path))
    if os.path.commonpath([base_dir, full_path]) != base_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to specified file and creates it if it does not exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to write to files from, relative to the working directory. If not provided, write to files files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that was written to the file"
            )
        },
    ),
)