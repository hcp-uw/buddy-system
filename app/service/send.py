import requests
from db.models import User
from db.crud import get_last_pairing, write_questions
from util import get_week_str
from constants import EMAIL_SECRET, EMAIL_ENDPOINT

def email(recip: User, partner: User, problem_link: str, resources: list[tuple[str, str]], message) -> str:
    resources = "\n".join([f"<li><a href='{x[1]}'>{x[0]}</a></li>" for x in resources])
    return (
        f"<html>"
        f"<body>"
        f"<p>Hi {recip.name},</p>"
        f"<p>This week you will be partnered with {partner.name}, and you will be interviewing them on <a href='{problem_link}'>{problem_link}</a>. Please reach out to them and schedule a time to meet.</p>"
        f"<p>Email: {partner.email}</p>"
        f"<p>Discord: {partner.discord}</p>"
        f"<p>"
            f"{message}"
        f"</p>"
        f"<p>"
            f"Here are some resources:"
        f"<ul>"
        f"{resources}"
        f"</ul>"
        f"<p>Best,</p>"
        f"<p>SWECC Leadership</p>"
        f"</body>"
        f"</html>"
    )



def generate_emails(pairs: list[tuple[User, User]], plink_1, plink_2, message, resources) -> dict[str, str]:
    out = {}

    for pair in pairs:
        out[pair[0].email] = email(pair[0], pair[1], plink_1, resources, message)
        out[pair[1].email] = email(pair[1], pair[0], plink_2, resources, message)
    return out


def send(email: str, content: str):
    """
    to, from, subject, content
    """
    body = {
        "to": email,
        "secret": EMAIL_SECRET,
        "subject": "OSIMP Partner " + get_week_str(),
        "content": content,
    }

    content_type = "application/json"

    res = requests.post(EMAIL_ENDPOINT, json=body, headers={"Content-Type": content_type})

    if res.status_code != 200:
        print(f"[ERROR]: {res.status_code} {res.text}")
        return False

    return True




