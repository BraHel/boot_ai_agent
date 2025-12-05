import os
from dotenv import load_dotenv
import argparse


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")
        
        return
    
    from google import genai
    from google.genai import types

    

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Now we can access `args.prompt`

    chosen_model = "gemini-2.5-flash"
    #chosen_message = args.prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(model=chosen_model, contents=messages)

    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is missing from the response.")
    
        return

    if args.verbose is True:
        print("User prompt: " + args.user_prompt)
        print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
        print("Response tokens: " + str(response.usage_metadata.candidates_token_count))

    print(response.text)
    
    #print("Hello from boot-ai-agent!")


if __name__ == "__main__":
    main()
