import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.run_python_file import *
from functions.get_file_content import *
from functions.write_file import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_get_file_content,
        schema_write_file
    ]
)
available_functions_dict={
        "get_file_content":get_file_content,
        "write_file":write_file,
        "get_files_info":get_files_info,
        "run_python_file":run_python_file
    }

def main():
    parser = argparse.ArgumentParser(description="Process a user prompt with optional verbosity.")
    parser.add_argument("user_prompt", help="The user's prompt to process")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    user_prompt = args.user_prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    MAX_ITERATIONS = 20
    iteration=0
    success=False
    while iteration<MAX_ITERATIONS:
        try:
            iteration+=1
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )
            
            for c in response.candidates:
                messages.append(c.content)                

            if response.function_calls:
                from functions.call_function import call_function
                for function_call_part in response.function_calls:
                    function_call_result=call_function(function_call_part, args.verbose)
                    if function_call_result.parts[0].function_response.response and args.verbose:
                        print(f'User prompt: "{user_prompt}"')
                        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    elif not function_call_result.parts[0].function_response.response:
                        raise Exception("ERROR: No result reported.")
                    messages.append(types.Content(role="tool", parts=function_call_result.parts))
            else:
                print(response.text)
                success=True
                break
        except Exception as e:
            print(f"Error during iteration {iteration}: {e}")
            break
    if not success:
        print(f"{iteration} iterations out of a maximum of {MAX_ITERATIONS} were performed with no answer.")
        return None

if __name__ == "__main__":
    main()
