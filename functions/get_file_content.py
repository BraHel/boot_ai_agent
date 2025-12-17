from google.genai import types

def get_file_content(working_directory, file_path):
    import os
    from functions.get_config_values import get_config_values

    target_file_path = os.path.join(working_directory, file_path)

    config = get_config_values()
    
    if os.path.commonpath([os.path.abspath(target_file_path), os.path.abspath(working_directory)]) != os.path.abspath(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
    
    if os.path.isfile(target_file_path) is False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file_path, 'r') as file:
            content = file.read()
            if len(content) > config["FILE_CONTENT_CHAR_LIMIT"]:
                content = content[:config["FILE_CONTENT_CHAR_LIMIT"]] + "[...File "+str(file_path)+" truncated at 10000 characters]"
            return content
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file from the specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory from which to read a file.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read.",
            ),
        },
    ),
)