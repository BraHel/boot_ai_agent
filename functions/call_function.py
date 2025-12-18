import ast
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    arguments = function_call_part.args

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
           return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    arguments_copy = arguments.copy()

    # --- Start of the simplified argument handling ---

    # First, ensure our default working_directory is always set.
    # The assignment explicitly requires './calculator'.
    arguments_copy["working_directory"] = "./calculator"

    # Now, handle the LLM's 'directory' argument if it exists for these functions,
    # as it often conflicts with our intended 'working_directory'.
    # We remove it because 'working_directory' is already set above.
    if function_name in ["run_python_file", "get_file_content", "write_file", "get_files_info"]:
        if "directory" in arguments_copy:
            del arguments_copy["directory"]

    # Specific path cleaning for 'file_path' for functions that process files
    if function_name in ["run_python_file", "get_file_content", "write_file"]:
        if "file_path" in arguments_copy:
            # This ensures the file_path is just the filename relative to the working_directory
            path_parts = arguments_copy["file_path"].split('/')
            arguments_copy["file_path"] = path_parts[-1]

    # --- End of the simplified argument handling ---

    func = function_map[function_name]
    return types.Content(
       role="tool",
       parts=[
           types.Part.from_function_response(
               name=function_name,
               response={"result": func(**arguments_copy)},
           )
       ],
   )