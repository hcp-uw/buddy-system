from db.models import User
from asyncpg.connection import Connection

async def get_last_form_id(connection: Connection):
    return await connection.fetchval(
        f"SELECT id FROM forms ORDER BY created_at DESC LIMIT 1;"
    )

async def get_last_item_dict(connection: Connection):
    res = await connection.fetch(
        f"SELECT email_response_id, discord_response_id, name_response_id "
        f"FROM forms ORDER BY created_at DESC LIMIT 1;"
    )

    return {
        "Email": res[0].get('email_response_id'),
        "Discord": res[0].get('discord_response_id'),
        "Name": res[0].get('name_response_id')
    }

async def get_last_responses(connection: Connection):
    fid = await get_last_form_id(connection)
    res = await connection.fetch(
        f"SELECT u.name, u.email, u.discord "
        f"FROM form_responses fr "
        f"JOIN users u ON fr.user_email = u.email "
        f"WHERE fr.form_id = $1;",
        fid
    )

    return [User(email=x[1], name=x[0], discord=x[2]) for x in res]

async def get_last_n_pairings(connection: Connection, n: int):
    if n == 0:
        return []

    fids = await connection.fetch(
        f"SELECT id FROM forms ORDER BY created_at DESC LIMIT $1;",
        n
    )

    out = []
    for fid in fids:
        res = await connection.fetch(
            f"SELECT u1.name, u1.email, u1.discord, u2.name, u2.email, u2.discord "
            f"FROM pairings p "
            f"JOIN users u1 ON p.user1_email = u1.email "
            f"JOIN users u2 ON p.user2_email = u2.email "
            f"WHERE p.form_id = $1;",
            fid.get('id')
        )

        out.append([(User(email=x[1], name=x[0], discord=x[2]), User(email=x[4], name=x[3], discord=x[5])) for x in res])

    return out

async def get_all_prev_pairings(connection: Connection):
    num_prev = await connection.fetchval(
        f"SELECT COUNT(*) FROM forms;"
    )

    return await get_last_n_pairings(connection, num_prev)

async def get_last_pairing(connection: Connection):
    return await get_last_n_pairings(connection, 1)

async def write_form_id(connection: Connection, id: str, name: str, nameq: str, emailq: str, discordq: str):
    await connection.execute(
        f"INSERT INTO forms(id, name, email_response_id, discord_response_id, name_response_id) "
        f"VALUES ($1, $2, $3, $4, $5);",
        id, name, nameq, emailq, discordq
    )

async def write_responses(connection: Connection, responses: list[User]):
    fid = await get_last_form_id(connection)
    for person in responses:
        await connection.execute(
            f"INSERT INTO form_responses (form_id, user_email) "
            f"VALUES ($1, $2);",
            fid, person.email
        )

async def write_questions(connection: Connection, question_url: str, question2_url: str):
    await connection.execute(
        f"INSERT INTO questions (question_url, question_number) "
        f"VALUES ($1, 1), ($2, 2);", question_url, question2_url
    )

async def write_pairs(connection: Connection, pairs: list[tuple[User, User]], form_id: str):

    for pair in pairs:
        await connection.execute(
            f"INSERT INTO pairings (user1_email, user2_email, form_id) "
            f"VALUES ($1, $2, $3);",
            pair[0].email, pair[1].email, form_id
        )


async def get_user_by_email(connection: Connection, email: str):
    return await connection.fetchrow(
        f"SELECT * FROM users WHERE email = $1;",
        email
    )


async def create_user(connection: Connection, user: User):
    await connection.execute(
        f"INSERT INTO users (email, name, discord) "
        f"VALUES ($1, $2, $3);",
        user.email, user.name, user.discord
    )