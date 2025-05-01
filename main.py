from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CodeRequest(BaseModel):
    script: str
    stdin: str  # New: Accept multiple lines of input

@app.post("/execute")
async def execute_code(request: CodeRequest):
    try:
        # Run the script and pass input dynamically
        result = subprocess.run(
            ["python", "-c", request.script], 
            input=request.stdin, 
            text=True, 
            capture_output=True, 
            timeout=5
        )
        if result.returncode == 0:
            # Successful execution, return the output
            return {"output": result.stdout, "error": ""}
        else:
            # Error occurred, extract only the error message from stderr
            error_lines = result.stderr.strip().split('\n')
            error_message = error_lines[-1]  # The last line is typically the error (e.g., "NameError: name 'x' is not defined")
            return {"output": "", "error": error_message}
    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Execution timed out after 5 seconds"}
    except Exception as e:
        return {"output": "", "error": str(e)}
