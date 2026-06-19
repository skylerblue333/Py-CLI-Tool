"""
Py-CLI-Tool: API backend for CLI configuration management
"""
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Py-CLI-Tool", version="3.0.0")

configs = {}
class Config(BaseModel):
    key: str
    value: str

@app.put("/api/v1/config")
def set_config(c: Config):
    configs[c.key] = c.value
    return {"status": "saved", "key": c.key}

@app.get("/api/v1/config/{key}")
def get_config(key: str):
    if key not in configs:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": configs[key]}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "Py-CLI-Tool", "timestamp": int(time.time())}
