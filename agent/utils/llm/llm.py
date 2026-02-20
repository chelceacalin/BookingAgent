from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from ..tools import *
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.environ.get("LLM_MODEL", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
).bind_tools(tools)
