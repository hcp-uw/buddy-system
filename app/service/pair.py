from asyncpg import Connection
from db.crud import get_all_prev_pairings, write_pairs
from db.models import User


def does_pair_exist(u1: User, u2: User, prev_pairings: list[list[tuple[User, User]]]) -> bool:
    for prev_pairing in prev_pairings:
        for pair in prev_pairing:
            if u1 in pair and u2 in pair:
                return True

    return False


def pair(people: list[User], prev_pairs: list[list[tuple[User, User]]]) -> list[tuple[User, User]]:
    paired = set()

    if prev_pairs is None:
        prev_pairs = []

    out = []

    for i, u1 in enumerate(people):
        if u1 in paired:
            continue

        for u2 in people[i + 1:]:
            if u2 in paired:
                continue

            if not does_pair_exist(u1, u2, prev_pairs):
                out.append((u1, u2))
                paired.add(u1)
                paired.add(u2)
                break

    unpaired = list(filter(lambda x: x not in paired, people))

    return out, unpaired

async def save_pairs(connection: Connection, pairs: list[tuple[User, User]], form_id: str):
    await write_pairs(connection, pairs, form_id)

