def write_file(working_directory, file_path, content):
    import os

    #absolute working directory
    abs_working_directory = os.path.abspath(working_directory)

    #absolute file path
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    # Create the full path for the file        
    try:
        # Ensure the working directory exists
        os.makedirs(working_directory, exist_ok=True)

        # Ensure the directory for the file exists
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

    except Exception as e:
        return f"Error: {e}"

    
    try:
        # Check if we have write permission to the file or directory
        if os.path.exists(abs_file_path):
            if not os.access(abs_file_path, os.W_OK):
                return f'Error: No write permission for the file "{file_path}"'
        else:
            parent_dir = os.path.dirname(abs_file_path)
            if not os.access(parent_dir, os.W_OK):
                return f'Error: No write permission in the directory "{parent_dir}" to create the file "{file_path}"'
        
        # Write the content to the file
        with open(abs_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
