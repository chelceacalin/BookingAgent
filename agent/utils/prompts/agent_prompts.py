import os
from dotenv import load_dotenv
import datetime

load_dotenv()


SYSTEM_PROMPT = f"""{os.getenv("CONTEXT")}"""

CONTEXT = f"""
Context you have available:
Today's Date: {datetime.datetime.now().strftime("%m/%d/%Y")}
"""