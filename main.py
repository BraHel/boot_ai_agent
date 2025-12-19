import os
from dotenv import load_dotenv
from config import MAX_ITERS
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
import argparse
import prompts

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def generate_content(client, messages, verbose, available_functions, system_prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is missing from the response.")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # 1) Append candidates to messages
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # 2) Check finished condition
    no_functions = not response.function_calls
    has_text = bool(response.text)

    if no_functions and has_text:
        return response.text  # done

    # 3) Otherwise, call tools and append tool responses
    if response.function_calls:
        function_response_list = []
        for function_call_part in response.function_calls:
            function_response = call_function(function_call_part, verbose)

            # validate and collect the tool response (like you did before)
            try:
                part = function_response.parts[0]
                func_resp = part.function_response
                if func_resp is None or func_resp.response is None:
                    raise Exception("Function call failed")
                if verbose:
                    print(f"-> {func_resp.response}")
                function_response_list.append(part)
            except Exception:
                raise Exception("Function call failed")

        if function_response_list:
            tool_message = types.Content(
                role="user",
                parts=function_response_list,
            )
            messages.append(tool_message)

    return None  # not done yet


def main():

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")
        return

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
    )

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    system_prompt = prompts.system_prompt

    # Now we can access `args.prompt`
    #chosen_message = args.prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    #response = client.models.generate_content(model=chosen_model, contents=messages)

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Exceeded maximum number of iterations ({MAX_ITERS}).")
            break

        try:
            final_response = generate_content(client,messages, args.verbose,available_functions,system_prompt)

            if final_response:
                print("Final response:")
                print(final_response)
                break    
            
        except Exception as e:
            print(f"Error in generate_content: {e}")
            return


if __name__ == "__main__":
    main()
