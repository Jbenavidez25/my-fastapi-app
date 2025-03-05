from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CodeRequest(BaseModel):
    script: str
    stdin: str = ""

@app.post("/execute")
async def execute_code(request: CodeRequest):
    try:
        # Print debugging info
        print(f"Received script: {request.script}")
        print(f"Received stdin: {request.stdin}")
        print(f"Type of stdin: {type(request.stdin)}")  # Check if it's already bytes
        
        # Ensure stdin is a string before encoding
        if isinstance(request.stdin, bytes):
            stdin_input = request.stdin.decode("utf-8")  # Convert bytes to string if needed
        else:
            stdin_input = request.stdin

        print(f"Processed stdin: {stdin_input}")

        # Run Python script with input
        process = subprocess.run(
            ["python", "-c", request.script],
            input=stdin_input.encode("utf-8"),  # Convert to bytes correctly
            capture_output=True,
            text=True
        )

        # ✅ FIX: Ensure output is always a string
        output = process.stdout if process.returncode == 0 else process.stderr

        print(f"Raw output type: {type(output)}")
        print(f"Raw output: {output}")

        return {
            "output": output,
            "statusCode": process.returncode
        }

    except Exception as e:
        return {"output": str(e), "statusCode": 1}
