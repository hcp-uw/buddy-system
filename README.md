# Project to pair people together for a week

## Requirements

- Python 3.6
- A virtual environment with the packages defined in `requirements.txt`
- A PostgreSQL database with the schema defined in `app/db/schema.sql`
- An .env file with the following variables:
    - DB_USER
    - DB_PASSWORD
    - DB_PORT
    - DB_HOST
    - DB_NAME
    - EMAIL_SECRET
    - EMAIL_ENDPOINT
- Credentials for a Google Api project with the scopes defined in `app/constants.py:SCOPES`. The credentials should be stored in a file called `credentials.json` in the root directory of the project.


## How to use

### Launch the shell
```bash
python3 app/cli/admin-client.py
```

### Reference





| Command | Description |
| --- | --- |
| `last-form-id` | Prints the id of the last form saved to the database |
| `assign` | Assign partners for all the responses of the last posted form |
| `release` | Release pairings and send emails |
| `new-form` | Create a new signup form |
| `login` | Connect to DB and authenticate with Google (as app owner) |
| `exit` | Exit the shell |
| `auth` | Authenticate with Google |
| `up` | Connect to the DB |
| `down` | Disconnect from the DB |
| `debug` | Enable debugging (print exception messages) |
| `silent` | Silence debugging (do not print exception messages) |

