import os
from config import FILE_CHAR_LIMIT

def get_file_content(working_directory, file_path):
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_dir, file_path))
    if full_path.startswith(base_dir) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(full_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        try:
            with open(full_path, "r") as f:
                truncated_file_content = f.read(FILE_CHAR_LIMIT + 1)
                if len(truncated_file_content) > FILE_CHAR_LIMIT:
                    return f'{truncated_file_content[:FILE_CHAR_LIMIT]}[...File "{file_path}" truncated at {FILE_CHAR_LIMIT} characters]'
                else:
                    return truncated_file_content
        except Exception as e:
            return f'Error: {e}'
        