from helper.youtrack import get_all_vcs_changes, get_issue
from arango import ArangoClient
from arango_orm import Database
from helper.enitites import VcsChanges, Author, Target, Issue, IssueHasVcsChanges
import re


def create_connection_db(db):
    client = ArangoClient(hosts='http://arangodb:8529')
    db = Database(client.db(db, username='root', password='root'))
    return db


def create_if_not_exists():
    db = create_connection_db("processDiscovery")
    collections = [Author, Target, VcsChanges, Issue, IssueHasVcsChanges]

    for col in collections:
        if not db.has_collection(col):
            db.create_collection(col)


def save_vcs_changes():
    create_if_not_exists()
    vcs_changes = get_all_vcs_changes()
    db = create_connection_db("processDiscovery")

    for changes in vcs_changes:
        # save authors
        author = Author(name=changes['author']['name'],
                        login=changes['author']['login'],
                        type=changes['author']['$type']
                        )
        db.add(author)
        # save targets
        target = Target(text=changes['target']['text'],
                        id=changes['target']['id'],
                        type=changes['target']['$type']
                        )
        db.add(target)
        # save vcs_changes
        vcs_change = VcsChanges(
                        author_key=author._key,
                        id=changes['id'],
                        timestamp=changes['timestamp'],
                        target_key=target._key,
                        type=changes['$type']
                        )
        db.add(vcs_change)
        # get the issue id from the target text
        found_ids = re.findall(r"MSEDO-\d+", changes['target']['text'])
        # remove the duplicates
        issues_ids = list(set(found_ids))
        # get the issue from youtrack
        if issues_ids:
            for issue_id in issues_ids:
                issue_dict = get_issue(issue_id)
                if "error" in issue_dict:
                    # save issues with error
                    issue = Issue(
                        id_readable=issue_dict['error'],
                        tittle=issue_dict['error_description'],
                        id=issue_dict['error'],
                        type=issue_dict['error']
                    )
                else:
                    # save issues
                    issue = Issue(
                        id_readable=issue_dict['idReadable'],
                        tittle=issue_dict['summary'],
                        id=issue_dict['id'],
                        type=issue_dict['id']
                    )
                db.add(issue)
                # save relation between issues and changes
                issue_change = IssueHasVcsChanges(
                    issue_key=issue._key,
                    vcs_change_key=vcs_change._key
                )
                db.add(issue_change)
