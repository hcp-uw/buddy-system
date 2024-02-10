from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from constants import CLIENT_SECRETS_FILE, SCOPES, API_SERVICE_NAME, API_VERSION, NEW_FORM, NEW_QUESTIONS

def create_form(form_service, week_str):
    result = form_service.forms().create(body=NEW_FORM(week_str)).execute()

    question_setting = (
        form_service.forms()
        .batchUpdate(formId=result["formId"], body=NEW_QUESTIONS)
        .execute()
    )

    res = form_service.forms().get(formId=result["formId"]).execute()
    id = res["formId"]
    item_dict = { i["title"]: i["questionItem"]['question']['questionId'] for i in res["items"] }
    return id, item_dict