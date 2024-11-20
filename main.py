import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI, Query, Body
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel
from pathlib import Path
app = FastAPI()

db_file = Path(__file__).parent / "names.txt"


def load_names() -> list[str]:
    if not db_file.is_file():
        return []
    with open(db_file) as file:
        return file.read().split("\n")


def save_names(names: list[str]):
    with open(db_file, "w") as file:
        file.write("\n".join(names))


class Item(BaseModel):
    name: str
    quantity: int


@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """
    Endpoint without parameters - returns a simple HTML website.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Homepage</title>
    </head>
    <body>
        <h1>Welcome to the FastAPI Server!</h1>
        <p>This is a simple HTML page served by FastAPI.</p>
    </body>
    </html>
    """
    return html_content


@app.get("/names", response_class=HTMLResponse)
async def get_homepage(name: Optional[str] = None):
    """
    Endpoint without parameters - returns a simple HTML website.
    """
    names = load_names()
    if name and name not in names:
        names.append(name)
        save_names(names)

    str_content = "\n".join(f"<li>{name}</li>" for name in names)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Names</title>
    </head>
    <body>
        <h1>These are all the students who signed already: </h1>
        <ol>
            {str_content}
        </ol>
    </body>
    </html>
    """
    return html_content


@app.get("/data")
async def get_data(id: int = Query(...), name: str = Query(...)):
    """
    Endpoint with query parameters - returns XML.
    """
    xml_content = f"""
    <response>
        <id>{id}</id>
        <name>{name}</name>
    </response>
    """
    return Response(content=xml_content, media_type="application/xml")


@app.post("/process", response_class=JSONResponse)
async def process_item(item: Item = Body(...)):
    """
    Endpoint with JSON body - returns JSON.
    """
    processed_data = {
        "message": "Item processed successfully",
        "item_name": item.name,
        "item_quantity": item.quantity,
        "data": {
            "hey": "hello",
            "value": 30,
            "true?": True,
            "null?": None,
        }
    }
    return processed_data


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 443
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
