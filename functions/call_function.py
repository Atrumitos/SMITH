import os
from google.genai import types
from main import available_functions_dict

def call_function(function_call_part, verbose=False):
    function_name=function_call_part.name
    arguments=function_call_part.args.copy()
    arguments["working_directory"]='./calculator'
    try:
        if verbose==True:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")
        if function_name not in available_functions_dict:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
        function=available_functions_dict.get(function_name)
        function_result=function(**arguments)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
