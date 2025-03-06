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
        # Run Python script with input handling
        process = subprocess.Popen(
            ["python", "-c", request.script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send user input to the script
        stdout, stderr = process.communicate(input=request.stdin)

        return {
            "output": stdout if process.returncode == 0 else stderr,
            "statusCode": process.returncode
        }

    except Exception as e:
        return {"output": str(e), "statusCode": 1}
