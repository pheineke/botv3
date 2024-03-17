import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

from dotenv import load_dotenv
import praw,os

load_dotenv()

class Reddit():
    def __init__(self):
        self.reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"), \
                        client_secret=os.getenv("CLIENT_SECRET"), \
                        user_agent=os.getenv("USER_AGENT")) 
                        #username=genv("USERNAME1"), \
                        #password=genv("PASSWD"))
        self.cache = []

        self.create_log()

    def create_log(self):
        if not(os.path.exists('reddit_logger.log')):
            with open('reddit_logger.log', 'w') as file:
                file.write('a\nb\nc')

    def get_submission(self):
        # submission = self.reddit.subreddit("ich_iel").random()
        # submission_url = submission.url

        with open('reddit_logger.log', 'r') as file:
            cache = [line.strip('\n') for line in file.readlines()]

        print(cache)


r = Reddit()
r.get_submission()