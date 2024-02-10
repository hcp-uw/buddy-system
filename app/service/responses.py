from db.models import User
from db.crud import get_last_form_id, get_last_item_dict, write_responses, get_last_responses, get_user_by_email, create_user
from constants import CLIENT_SECRETS_FILE, SCOPES, API_SERVICE_NAME, API_VERSION

def get_responses_raw(forms_service, form_id):
    http_res = forms_service.forms().responses().list(formId=form_id).execute()
    return http_res['responses'] if 'responses' in http_res else None


def parse_response(response, item_dict) -> User:
    answers = response['answers']

    qids = answers.keys()

    name = answers[item_dict['Name']]['textAnswers']['answers'][0]['value']
    email = answers[item_dict['Email']]['textAnswers']['answers'][0]['value']
    discord = answers[item_dict['Discord']]['textAnswers']['answers'][0]['value']

    return User(email=email, name=name, discord=discord)


def parse_responses(responses, item_dict):
    if not responses:
        return None

    people = [parse_response(x, item_dict) for x in responses]
    return people

def get_responses(forms_service, form_id, item_dict) -> list[User]:
    raw = get_responses_raw(forms_service, form_id)
    print(raw)
    return parse_responses(raw, item_dict)

async def save_responses(connection, forms_service, form_id, item_dict):
    responses = get_responses(forms_service, form_id, item_dict)

    for user in responses:
        email = user.email
        existed = await get_user_by_email(connection, email)
        if not existed:
            print(f"Creating user {email}")
            await create_user(connection, user)
            print(f"Created user {email}")


    await write_responses(connection, responses)
    return responses
