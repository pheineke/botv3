import os
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import requests
from bs4 import BeautifulSoup
import os

class Mathe(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def mathedownloader(self, ctx):
        # Base URL
        base_url = "https://agag-jboehm.math.rptu.de/~boehm/lehre/24_MfI_KSS/"
        start_url = base_url + "start.html"
        log_file_path = './lib/data/mathe/download_log.txt'

        # Create a directory to save PDFs
        if not os.path.exists('./lib/data/mathe/pdfs'):
            os.makedirs('./lib/data/mathe/pdfs')

        # Load previously downloaded PDFs from the log file
        downloaded_pdfs = set()
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                downloaded_pdfs = set(line.strip() for line in log_file)

        # Request the start page
        response = requests.get(start_url)
        response.raise_for_status()

        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links ending with 'blattx.pdf'
        pdf_links = soup.find_all('a', href=True)
        new_downloads = []

        for link in pdf_links:
            href = link['href']
            if href.startswith('blatt') and href.endswith('.pdf'):
                if href not in downloaded_pdfs:
                    pdf_url = base_url + href
                    pdf_response = requests.get(pdf_url)
                    pdf_response.raise_for_status()
                    
                    # Save the PDF file
                    pdf_filename = os.path.join('./lib/data/mathe/pdfs', href)
                    await ctx.send()
                    with open(pdf_filename, 'wb') as pdf_file:
                        pdf_file.write(pdf_response.content)
                    print(f'Downloaded {href}')
                    
                    # Log the downloaded PDF
                    new_downloads.append(href)
                else:
                    print(f'Skipped {href} (already downloaded)')

        # Update the log file with new downloads
        if new_downloads:
            with open(log_file_path, 'a') as log_file:
                for pdf in new_downloads:
                    log_file.write(pdf + '\n')


async def setup(client):
    await client.add_cog(Mathe(client))