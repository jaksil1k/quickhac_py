from dotenv import load_dotenv
import os

load_dotenv()

OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")
VS_ID = os.environ.get("VS_ID")
ASST_ID = os.environ.get("ASST_ID")
THREAD_ID = os.environ.get("THREAD_ID")
FILE_ID = os.environ.get("FILE_ID")
MSG_ID = os.environ.get("MSG_ID")
RUN_ID = os.environ.get("RUN_ID")
