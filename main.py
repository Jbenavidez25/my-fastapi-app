from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import re

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
            return {
                "output": result.stdout,
                "error": {
                    "message": "",
                    "line": -1  # -1 indicates no error
                }
            }
        else:
            # Error occurred, parse stderr to extract line number and error message
            error_output = result.stderr.strip()
            # Look for the line number in the Traceback (e.g., "File "<string>", line 2, in <module>")
            line_match = re.search(r'File "<string>", line (\d+)', error_output)
            line_number = int(line_match.group(1)) if line_match else -1

            # Extract the error message (e.g., "NameError: name 'x' is not defined")
            error_match = re.search(r"(?:Error|Exception): .*$", error_output, re.MULTILINE)
            if error_match:
                error_message = error_match.group(0)
            else:
                # Fallback: Use the last line if no error pattern is found
                error_lines = error_output.split('\n')
                error_message = error_lines[-1] if error_lines else "Unknown error occurred"

            return {
                "output": "",
                "error": {
                    "message": error_message,
                    "line": line_number
                }
            }
    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "error": {
                "message": "Execution timed out after 5 seconds",
                "line": -1
            }
        }
    except Exception as e:
        return {
            "output": "",
            "error": {
                "message": str(e),
                "line": -1
            }
        }
