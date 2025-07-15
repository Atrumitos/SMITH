import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        if file_path:
            full_path = os.path.join(working_directory, file_path)
        else:
            full_path = working_directory
        working_directory_abs = os.path.abspath(working_directory)
        full_path_abs = os.path.abspath(full_path)
        if not os.path.commonpath([full_path_abs, working_directory_abs]) == working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_path_abs):
            return f'Error: File "{file_path}" not found.'
        elif not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        completed_process = subprocess.run(["python", full_path_abs] + args, cwd=working_directory_abs, timeout=30, capture_output=True)
        output=[]
        if completed_process.stdout:
            output.append(f"STDOUT: {completed_process.stdout.decode()}")
        if completed_process.stderr:
            output.append(f"STDERR: {completed_process.stderr.decode()}")
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not output:
            return "No output produced."
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python files, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file, relative to the working directory."),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of optional arguments to use when executing."),
            }
        ),
    )