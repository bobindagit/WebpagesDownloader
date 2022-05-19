
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pdfkit
import os
import logging


logger = logging.getLogger('PDF_DOWNLOADER')

# Creating folder for PDF files
if not os.path.exists('pdf'):
    os.makedirs('pdf')


app = FastAPI()


class PDFDownloader(BaseModel):
    url: str


@app.post('/download_pdf')
async def download_pdf(url: str):
    try:
        pdfkit.from_url(url, f'pdf/{get_filename(url)}.pdf')
        return 200
    except Exception as exp:
        logger.error(exp)
        return exp
        

def get_filename(url: str) -> str:
    url_parts = url.split('/')
    # For filename we need last part
    for i in range(len(url_parts) - 1, 0, -1):
        current_part = url_parts[i]
        if current_part:
            return current_part

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
