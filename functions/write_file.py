import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        if file_path:
            full_path = os.path.join(working_directory, file_path)
        else:
            full_path = working_directory
        working_directory_abs = os.path.abspath(working_directory)
        full_path_abs = os.path.abspath(full_path)
        if not os.path.commonpath([full_path_abs, working_directory_abs]) == working_directory_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        os.makedirs(os.path.dirname(full_path_abs),exist_ok=True)
        with open(full_path_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, overwriting pre-existing content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If it doesn't exist, it's created."),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written in the file."
            ),
        }
    ),
)