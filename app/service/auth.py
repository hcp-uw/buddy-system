from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from constants import CLIENT_SECRETS_FILE, SCOPES, API_SERVICE_NAME, API_VERSION
import asyncio

def get_authorized_service_sync():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(authorization_prompt_message="")
    forms_service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

async def get_authorized_service():
    loop = asyncio.get_event_loop()
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = await loop.run_in_executor(None, flow.run_local_server)
    forms_service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
    return forms_service
