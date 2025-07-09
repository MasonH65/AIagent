import os

def get_files_info(working_directory, directory=None):
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_dir, directory))
    dir_results = []
    if  full_path.startswith(base_dir) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(full_path) == False:
        return f'Error: "{directory}" is not a directory'
    else:
        try:
            dir_contents = os.listdir(full_path)
            for item in dir_contents:
                dir_results.append(f'- {item}: file_size={os.path.getsize(os.path.join(full_path, item))} bytes, is_dir={os.path.isdir(os.path.join(full_path, item))}')
        except Exception as e:
            return f'Error: {e}'
        return '\n'.join(dir_results)