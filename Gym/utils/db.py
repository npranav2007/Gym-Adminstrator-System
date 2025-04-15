from sqlitedict import SqliteDict
import os

DB_PATH = 'instance/gym.sqlite'


def init_db():
    os.makedirs('instance', exist_ok=True)

    with SqliteDict(DB_PATH, autocommit=True) as db:
        if 'users' not in db:
            db['users'] = {}
        if 'customers' not in db:
            db['customers'] = {}
        if 'plans' not in db:
            db['plans'] = {}


def get_db():
    db = SqliteDict(DB_PATH, autocommit=False)

    if 'users' not in db:
        db['users'] = {}
    if 'customers' not in db:
        db['customers'] = {}
    if 'plans' not in db:
        db['plans'] = {}

    return db
