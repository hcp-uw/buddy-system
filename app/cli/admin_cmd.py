from db.models import User
from service.responses import save_responses
from service.forms import create_form
from service.pair import pair, save_pairs, get_all_prev_pairings
from service.send import send, generate_emails
from db.crud import get_last_form_id, get_last_item_dict, write_form_id, get_last_pairing
from service.auth import get_authorized_service
from util import printc, get_week_str

from dotenv import load_dotenv
from random import random
import asyncio

async def last_form_id(state):
    res = await get_last_form_id(state.db_connection)
    print(res)
    return res

async def new_signup_form(state):
    week_str = get_week_str()
    id, item_dict = create_form(state.forms_service, week_str)

    await write_form_id(state.db_connection, id, week_str,
        item_dict["Name"], item_dict["Email"], item_dict["Discord"])

async def assign_pairings(state):
    fid = await get_last_form_id(state.db_connection)
    item_dict = await get_last_item_dict(state.db_connection)
    responses = await save_responses(state.db_connection, state.forms_service, fid, item_dict)
    if not responses:
        printc("No responses found", "yellow")
        return []

    printc("Responses:", "green")
    for response in responses:
        printc(response, "blue")

    printc("Previous pairings:", "green")
    previous_pairs = await get_all_prev_pairings(state.db_connection)
    for pairs in previous_pairs:
        printc(pairs, "blue")
    pairs, unpaired = pair(responses, previous_pairs)
    if unpaired:
        printc("Unpaired people:", "red")
        for person in unpaired:
            printc(person, "yellow")
    await save_pairs(state.db_connection, pairs, fid)
    return pairs

async def release_pairings(state):
    # pairs, = await get_last_pairing(state.db_connection)
    pairs = [(User(email="test1", name="test1", discord="test1"), User(email="test2", name="test2", discord="test2"))]
    if len(pairs) == 0:
        printc("No pairs found", "yellow")
        return

    plink_1 = input("\tEnter the link to the first problem: ")
    plink_2 = input("\tEnter the link to the second problem: ")
    message = input("\tEnter a message to send about the problems: ")

    printc("Enter resources. Press enter when finished", "yellow")
    resources = []
    while True:
        name = input("\tEnter the name of the resource: ")
        if not name:
            break
        link = input("\tEnter the link to the resource: ")
        resources.append((name, link))

    emails = generate_emails(pairs, plink_1, plink_2, message, resources)
    # for email, content in generate_emails(pairs, plink_1, plink_2, message, resources).items():
    printc("Emails:", "green")
    for email, content in emails.items():
        printc(f"To: {email}\nContent: {content}", "blue")
        # send(email, content)

async def login(state):
    await state.startup_db_connection()
    await state.authenticate()

async def quit(state):
    await state.shutdown_db_connection()
    asyncio.get_event_loop().stop()
    exit(1)