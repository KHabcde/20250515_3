import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test if the OPENAI_API_KEY is loaded
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print("Environment variable loaded successfully.")
else:
    print("Failed to load environment variable.")
