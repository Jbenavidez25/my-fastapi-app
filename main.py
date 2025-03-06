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
            input=request.stdin, text=True, 
            capture_output=True, timeout=5
        )
        return {"output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"output": "", "error": str(e)}
