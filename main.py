import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Process a user prompt with optional verbosity.")
    parser.add_argument("user_prompt", help="The user's prompt to process")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    user_prompt = args.user_prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if args.verbose:
        print(f'User prompt: "{user_prompt}"')
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)

if __name__ == "__main__":
    main()
