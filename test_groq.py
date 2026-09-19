import os                       # Standard library module for os related tasks
from dotenv import load_dotenv  # Function from dotenv package to load variables from .env
from groq import Groq           # Class from groq package to interact with Groq's API


# Load variables from .env
load_dotenv()            

# Create Groq API client object
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Get available models
models = client.models.list()

for model in models.data:
    print(model.id)