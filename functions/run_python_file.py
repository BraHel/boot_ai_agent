def run_python_file(working_directory, file_path, args=[]):
    import subprocess
    import os

    # Construct the full path to the Python file
    full_path = os.path.join(working_directory, file_path)

    if os.path.commonpath([os.path.abspath(full_path), os.path.abspath(working_directory)]) != os.path.abspath(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if os.path.isfile(full_path) is False:
        return f'Error: File "{file_path}" not found.'

    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'



    # Prepare the command to run the Python file
    command = ['python', file_path] + args


    # Execute the command
    completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_directory)

    stdout = completed_process.stdout or ""
    stderr = completed_process.stderr or ""

    if not stdout and not stderr:
        return "No output produced"
    
    result = f"STDOUT:{stdout}"
    result += f"\nSTDERR:{stderr}"

    # Return the output and error messages
    if completed_process.returncode != 0:
        result += f"\nProcess exited with code {completed_process.returncode}"
    
    return result