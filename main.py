from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CodeRequest(BaseModel):
    script: str

@app.post("/execute")
def execute_code(request: CodeRequest):
    try:
        # Run the Python script as a subprocess and allow it to handle `input()`
        process = subprocess.Popen(
            ["python3", "-c", request.script],  # Run as inline Python script
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Capture output and errors
        stdout, stderr = process.communicate()

        return {
            "output": stdout,
            "error": stderr,
            "statusCode": process.returncode
        }

    except Exception as e:
        return {"error": str(e), "statusCode": 1}
