import os
from config import char_limit
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        if file_path:
            full_path = os.path.join(working_directory, file_path)
        else:
            full_path = working_directory
        working_directory_abs = os.path.abspath(working_directory)
        full_path_abs = os.path.abspath(full_path)
        if not os.path.commonpath([full_path_abs, working_directory_abs]) == working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif  not os.path.isfile(full_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path_abs, 'r', encoding='utf-8') as f:
            file_content=f.read(char_limit+1)
            if len(file_content)>char_limit:
                return file_content[:char_limit] + f'\n[...File "{file_path}" truncated at {char_limit} characters]'
            return file_content
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file and returns its contents, truncated at 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        }
    ),
)