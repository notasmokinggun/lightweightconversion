import tempfile, os
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from markitdown import MarkItDown

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert(file: UploadFile):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        result = MarkItDown().convert(tmp_path)
        return {"markdown": result.text_content}
    finally:
        os.unlink(tmp_path)
