import os
import subprocess

def run_python_file(working_directory, file_path):
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_dir, file_path))
    if os.path.commonpath([base_dir, full_path]) != base_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(full_path) == False:
        return f'Error: File "{file_path}" not found.'
    if full_path[-3:] != '.py':
        return f'Error: "{file_path}" is not a Python file.'
    try:
        process = subprocess.run(['python3', full_path], timeout=30, capture_output=True, cwd=base_dir, text=True)
        output = f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}'
        if process.stderr == '' and process.stdout == '':
            output = 'No output produced.'
        if process.returncode != 0:
            output += f'\nProcess exited with code {process.returncode}'
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"