from fastapi import FastAPI
from pydantic import BaseModel
import sys
import io

app = FastAPI()

class CodeRequest(BaseModel):
    script: str
    stdin: str

@app.post("/execute")
def execute_code(request: CodeRequest):
    # Split user inputs into a list
    user_inputs = request.stdin.split("\n")

    # Detect numbers and convert them
    for i in range(len(user_inputs)):
        if user_inputs[i].replace(".", "", 1).isdigit():
            user_inputs[i] = eval(user_inputs[i])  # Convert automatically to int or float

    # Replace input() calls with user-provided values
    script = request.script
    for value in user_inputs:
        script = script.replace("input()", str(value), 1)

    # Capture output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(script)
        output = sys.stdout.getvalue()
    except Exception as e:
        output = f"Error: {str(e)}"
    sys.stdout = old_stdout

    return {"output": output}

