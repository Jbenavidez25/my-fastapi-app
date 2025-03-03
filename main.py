from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CodeRequest(BaseModel):
    script: str
    stdin: str = ""

@app.post("/execute")
def execute_code(request: CodeRequest):
    try:
        # Run the Python script and pass stdin
        result = subprocess.run(
            ["python", "-c", request.script],
            input=request.stdin,  # Pass user input
            text=True,
            capture_output=True
        )
        return {"output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}
