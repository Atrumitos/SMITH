import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    try:
        if directory:
            full_path = os.path.join(working_directory, directory)
        else:
            full_path = working_directory
        working_directory_abs = os.path.abspath(working_directory)
        full_path_abs = os.path.abspath(full_path)
        if not os.path.commonpath([full_path_abs, working_directory_abs]) == working_directory_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif  not os.path.isdir(full_path_abs):
            return f'Error: "{directory}" is not a directory'
        files_info = []
        for entry in sorted(os.listdir(full_path_abs)):
            entry_path = os.path.join(full_path_abs, entry)
            is_dir = os.path.isdir(entry_path)
            file_size = os.path.getsize(entry_path) if not is_dir else 128
            files_info.append(f" - {entry}: file_size={file_size}, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        }
    ),
)