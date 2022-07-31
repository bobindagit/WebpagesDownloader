from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import weasyprint
import pdfkit
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup

import os
import logging
import json

logger = logging.getLogger('weasyprint')
logger.addHandler(logging.FileHandler('logs/weasyprint.log'))

# Creating folder for PDF files
if not os.path.exists('pdf'):
    os.makedirs('pdf')


app = FastAPI()


@app.post('/download_pdf_weasyprint')
def download_pdf_weasyprint(url: str, page_size: str, margin: int):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            # Removing pagebreak
            pagebreaks = soup.find_all(attrs={"class": "pagebreak"})
            for pagebreak in pagebreaks:
                pagebreak.replace_with('')
            
            filename = f'./pdf/weasyprint_{get_filename(url)}.pdf'
            style_string = generate_style_css(page_size, margin)
            weasyprint.HTML(string=soup.prettify()).write_pdf(filename, stylesheets=[weasyprint.CSS(string=style_string)])
        else:
            return 500
        return 200
    except Exception as exp:
        logger.error(exp)
        return exp


@app.post('/download_pdf_wkhtmltopdf')
async def download_pdf_wkhtmltopdf(url: str):
    try:
        filename = f'./pdf/wkhtmltopdf_{get_filename(url)}.pdf'
        pdfkit.from_url(url, filename)
        return 200
    except Exception as exp:
        logger.error(exp)
        return exp


@app.post('/download_pdf_selenium')
async def download_pdf_selenium(url: str):
    try:
        filename = f'./pdf/'
        
        options = ChromeOptions()
        chrome_prefs = {
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
            "download.open_pdf_in_system_reader": False,
            "profile.default_content_settings.popups": 0,
            "download.default_directory": filename,
        }
        options.add_experimental_option("prefs", chrome_prefs)
        
        driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
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


def generate_style_css(page_size: str, margin: int) -> str:
    return '@page {'\
                f'size: {page_size};'\
                f'margin: {margin}px;'\
            '}'


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
