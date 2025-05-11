from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the Mongo URI from the environment
uri = os.getenv("MONGO_DB_URL")

# Connect to MongoDB
client = MongoClient(uri, tls=True)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection failed:", e)
