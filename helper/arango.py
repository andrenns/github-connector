from helper.youtrack import get_all_vcs_changes
from arango import ArangoClient
from arango_orm import Database
from helper.enitites import VcsChanges, Author, Target


def create_connection_db(db):
    client = ArangoClient(hosts='http://arangodb:8529')
    db = Database(client.db(db, username='root', password='root'))
    return db


def create_if_not_exists():
    db = create_connection_db("processDiscovery")
    collections = [Author, Target, VcsChanges]

    for col in collections:
        if not db.has_collection(col):
            db.create_collection(col)


def save_vcs_changes():
    create_if_not_exists()
    vcs_changes = get_all_vcs_changes()
    db = create_connection_db("processDiscovery")

    for changes in vcs_changes:
        author = Author(name=changes['author']['name'],
                        login=changes['author']['login'],
                        type=changes['author']['$type']
                        )
        db.add(author)
        target = Target(text=changes['target']['text'],
                        id=changes['target']['id'],
                        type=changes['target']['$type']
                        )
        db.add(target)
        doc = VcsChanges(author_key=author._key,
                         id=changes['id'],
                         timestamp=changes['timestamp'],
                         target_key=target._key,
                         type=changes['$type']
                         )
        db.add(doc)
