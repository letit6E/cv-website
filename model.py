from pathlib import Path
import shutil
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

from config import SQLITE_DATABASE_NAME, SQLITE_DATABASE_BACKUP_NAME

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    position = db.Column(db.String(512), nullable=False)
    text = db.Column(db.String(2048), nullable=False)


def db_init():
    guestbook_init = []

    # Check if db file already exists. If so, backup it
    db_file = Path(SQLITE_DATABASE_NAME)
    if db_file.is_file():
        shutil.copyfile(SQLITE_DATABASE_NAME, SQLITE_DATABASE_BACKUP_NAME)

    # Init DB
    db.session.commit()  # https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
    db.drop_all()
    db.create_all()

    # Create TestOne questions
    print("Create Guestbook")
    for g in guestbook_init:
        gb = Post(name=g['name'], position=g['position'], text=g['text'])
        db.session.add(gb)
        db.session.commit()
