import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")
PORT = os.environ.get("MAIL_PORT", 465)
