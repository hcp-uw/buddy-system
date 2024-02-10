
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SECRET = os.getenv("EMAIL_SECRET")
EMAIL_ENDPOINT = os.getenv("EMAIL_ENDPOINT")

CLIENT_SECRETS_FILE = "./credentials.json"

# constants for Google API
SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly",
]
API_SERVICE_NAME = "forms"
API_VERSION = "v1"


# form templates
def NEW_FORM(date):
    return {
        "info": {
            "title": "Mock Interview Sign Up, " + date,
        }
    }


NEW_QUESTIONS = {
    "requests": [
        {
            "createItem": {
                "item": {
                    "title": "Name",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {
                    "index": 0
                }
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Email",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {
                    "index": 1
                }
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Discord",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {
                    "index": 2
                }
            }
        }
    ]
}
