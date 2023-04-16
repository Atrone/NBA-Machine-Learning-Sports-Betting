from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

def read_text_file(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/", response_class=HTMLResponse)
async def display_text_file():
    file_path = r"C:\Users\antho\PycharmProjects\nba_fantasy_trone\NBA-Machine-Learning-Sports-Betting\output.txt"  # Replace with the path to your text file
    content = read_text_file(file_path)
    html_content = f"<html><body><pre>{content}</pre></body></html>"
    return HTMLResponse(content=html_content, status_code=200)
