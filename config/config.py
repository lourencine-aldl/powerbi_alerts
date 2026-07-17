import os
from dotenv import load_dotenv

load_dotenv()

#powerbi
TENANT_ID = os.getenv("PBI_TENANT_ID")
CLIENT_ID = os.getenv("PBI_CLIENT_ID")
CLIENT_SECRET = os.getenv("PBI_CLIENT_SECRET")

BASE_URL = "https://api.powerbi.com/v1.0/myorg"

#llm
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

#SMTP 
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)
EMAIL_TO = os.getenv("EMAIL_TO")
