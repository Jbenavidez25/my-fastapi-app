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
        # Ensure stdin is a string before encoding
        stdin_input = request.stdin if isinstance(request.stdin, str) else str(request.stdin)

        # Run Python script with input
        process = subprocess.run(
            ["python", "-c", request.script],
            input=stdin_input.encode("utf-8"),  # Convert to bytes correctly
            capture_output=True,
            text=True
        )

        # ✅ FIX: Ensure output is always a string
        output = process.stdout if process.returncode == 0 else process.stderr
        if isinstance(output, bytes):
            output = output.decode("utf-8")  # Decode if needed

        return {
            "output": output,
            "statusCode": process.returncode
        }

    except Exception as e:
        return {"output": str(e), "statusCode": 1}
