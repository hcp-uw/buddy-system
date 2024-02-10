from service.auth import get_authorized_service
from cli.admin_cmd import last_form_id, new_signup_form, assign_pairings, release_pairings, login, quit
from util import printc

from dotenv import load_dotenv
from random import random

import asyncio
import time
import asyncpg
import os
import signal

load_dotenv()

class State:
    def __init__(self):
        self.db_connection = None
        self.forms_service = None
        self.show_exceptions = False

    async def startup_db_connection(self):
        self.db_connection = await asyncpg.connect(
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME"),
            host = os.getenv("DB_HOST")
        )
        printc("Database connection established", "green")

    async def shutdown_db_connection(self):
        if self.db_connection:
            await self.db_connection.close()
            printc("Database connection closed", "green")
        else:
            printc("No database connection to close", "yellow")

    async def authenticate(self):
        self.forms_service = await get_authorized_service()
        printc("Authenticated", "green")

    async def debug_mode(self):
        self.show_exceptions = not self.show_exceptions

    async def silent_mode(self):
        self.show_exceptions = False


# Define a signal handler function
def ctrl_c(signum, frame):
    state = "."
    n = 50
    for i in range(n):
        printc(state, ["red", "green", "yellow", "blue"][i % 4])
        if i < random() * n:
            state += "." * (i % 3)
        else:
            state = state[:-1]

        time.sleep(0.01)

    printc("CTRL-C received. Exiting...", "yellow")
    asyncio.get_event_loop().stop()
    exit()

async def main():
    signal.signal(signal.SIGINT, ctrl_c)
    state = State()


    commands = {
        "last-form-id": last_form_id,
        "assign": assign_pairings,
        "release": release_pairings,
        "new-form": new_signup_form,
        "login": login,
        "exit": quit,
        "auth": state.authenticate,
        "up": state.startup_db_connection,
        "down": state.shutdown_db_connection,
        "debug": state.debug_mode,
        "silent": state.silent_mode
    }

    printc("Welcome to the OSIMP Admin Client", "yellow")
    invalid_command = lambda: printc("Invalid command", "red")
    while True:
        printc("Enter a command:", "cyan", end=" ")
        command = input()
        try:
            await commands.get(command, invalid_command)(state)
        except Exception as e:
            if state.show_exceptions:
                printc(f"Exception: \n\n{str(e)}", "red")
            else:
                printc("Failed. Use 'debug' to see the exception", "red")

if __name__ == "__main__":
    asyncio.run(main())