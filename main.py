from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import weasyprint
import requests
from bs4 import BeautifulSoup

import os
import logging


logger = logging.getLogger('weasyprint')
logger.addHandler(logging.FileHandler('logs/weasyprint.log'))

# Creating folder for PDF files
if not os.path.exists('pdf'):
    os.makedirs('pdf')


app = FastAPI()


class PDFDownloader(BaseModel):
    url: str


@app.post('/download_pdf')
def download_pdf(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            # Removing pagebreak
            pagebreaks = soup.find_all(attrs={"class": "pagebreak"})
            for pagebreak in pagebreaks:
                pagebreak.replace_with('')
            weasyprint.HTML(string=soup.prettify()).write_pdf(f'pdf/{get_filename(url)}.pdf', stylesheets=[weasyprint.CSS('style.css')])
        else:
            return 500
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
