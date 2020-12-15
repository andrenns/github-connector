from pyArango.connection import *
from helper.youtrack import get_all_vcs_changes


def create_connection():
    conn = Connection(arangoURL='http://arangodb:8529/', username="root", password="root")
    return conn


def save_vcs_changes():
    vcs_changes = get_all_vcs_changes()
    conn = create_connection()
    db = conn["processDiscovery"]
    col = db["vcsChangesRaw"]

    for changes in vcs_changes:
        doc = col.createDocument()
        doc.set(changes)
        doc.save()
