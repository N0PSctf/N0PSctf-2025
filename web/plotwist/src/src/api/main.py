# main.asgi.py
import os
import re
import subprocess

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.routing import APIRouter

from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Route
from starlette.applications import Starlette

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = FastAPI()

class Letter(BaseModel):
    letter: str

regex = r"^[0-9 ?$]+$"

# GET routes

@app.get("/api")
async def read_root():
    return {"message": "Hum.. What are you exactly looking for here x)?"}

@app.get("/api/lordhttp")
async def read_root():
    return {"msg": "Hello from the other side, Lord HTTP"}

@app.get("/api/noopsy")
async def read_root():
    return {"msg": "Got a secret, can you keep it? Well this one, I'll save it in the secret_flag.txt file ^.^"}


# POST routes

@app.post("/api/lordhttp")
async def send_lordhttp(letter: Letter):
    return {"msg": f"Letter received by Lord HTTP: {letter.letter}"}


@app.post("/api/noopsy")
async def send_noopsy(letter: Letter):
    content = letter.letter
    print(content)

    message = '''Money
        It’s a crime 💸
        Talk in dollars or digits, or don’t even try 💁‍♀️
        Money
        So they say 💰
        Is the root of all evil today 😈
        Got a question? I’ll answer you away 💬✨'''

    match =  re.fullmatch(regex, content)

    if not match:
        return {"error": message}

    command = match.group()

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return {"msg": result.stdout}
        else:
            return {"msg": f"{result.stderr}"}
    
    except Exception as e:
        return {"msg": f"Error: {str(e)}"}
