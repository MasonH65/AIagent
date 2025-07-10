import os

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