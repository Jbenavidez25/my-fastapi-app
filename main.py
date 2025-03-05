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
        # Run Python script with input
        process = subprocess.run(
            ["python", "-c", request.script],
            input=request.stdin.encode(),
            capture_output=True,
            text=True
        )

        return {
            "output": process.stdout if process.returncode == 0 else process.stderr,
            "statusCode": process.returncode
        }

    except Exception as e:
        return {"output": str(e), "statusCode": 1}
