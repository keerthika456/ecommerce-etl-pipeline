from dotenv import load_dotenv  #from dotenv import load_dotenv python-dotenv is a lightweight Python library that loads environment variables from a .env file into a program’s environment. It helps developers manage configuration data, such as API keys or database credentials, without hard-coding them in source code. 
#Read variables from .env file.
import os #os helps Python interact with:environment variables, folders, files, operating system
from urllib.parse import quote_plus #This handles special characters in passwords.
load_dotenv() #This tells Python:“Open .env file and load all values.”
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
FILE_PATH = os.getenv("FILE_PATH")

CONNECTION_STRING = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)