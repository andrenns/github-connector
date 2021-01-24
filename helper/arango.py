from helper.youtrack import get_all_state_transitions
from arango import ArangoClient
from arango_orm import Database
from helper.enitites import StateTransition, Author, Issue, IssueHasStateTransition, AuthorDidStateTransition
import re
from arango.exceptions import DocumentInsertError
from helper.env_reader import ENV


def create_connection_db(db):
    client = ArangoClient(hosts=ENV['ARANGODB_HOST'])
    db = Database(client.db(db, username=ENV['ARANGODB_USER'], password=ENV['ARANGODB_PWD']))
    return db


def create_if_not_exists():
    db = create_connection_db(ENV['ARANGODB_DBNAME'])
    collections = [Author, Issue, StateTransition, IssueHasStateTransition, AuthorDidStateTransition]

    for col in collections:
        if not db.has_collection(col):
            db.create_collection(col)


def check_existence_save(db, doc, collection_class, has_filters=True, filter_name='', filter_value=''):
    try:
        db.add(doc)
        return doc
    except DocumentInsertError:
        if has_filters:
            doc = db.query(collection_class).filter(f'{filter_name}==@filter', filter=filter_value).first()
            return doc
        else:
            return True


def check_transition_values(transitions):
    if isinstance(transitions['added'], list) and not transitions['added']:
        if transitions['removed']:
            transitions['added'] = [{'$type': transitions['removed'][0]['$type'], 'name':'NONE'}]
    elif isinstance(transitions['removed'], list) and not transitions['removed']:
        if transitions['added']:
            transitions['removed'] = [{'$type': transitions['added'][0]['$type'], 'name':'NONE'}]
    elif not isinstance(transitions['added'], list) and not isinstance(transitions['removed'], list):
        transitions['added'] = [{'$type': 'NONE', 'name': 'NONE'}]
        transitions['removed'] = [{'$type': 'NONE', 'name': 'NONE'}]
    return transitions


def save_vcs_changes():
    create_if_not_exists()
    state_transitions = get_all_state_transitions()
    db = create_connection_db("processDiscovery")

    for transitions in state_transitions:
        transitions = check_transition_values(transitions)
        if transitions['added'][0]['$type'] == 'StateBundleElement' \
                or transitions['removed'][0]['$type'] == 'StateBundleElement':
            author = Author(name=transitions['author']['name'],
                            login=transitions['author']['login'],
                            type=transitions['author']['$type'],
                            id=transitions['author']['id']
                            )
            author = check_existence_save(db, author, Author, True, 'id', transitions['author']['id'])
            # save state_transition
            state_transition = StateTransition(
                            id=transitions['id'],
                            timestamp=transitions['timestamp'],
                            old_value=transitions['removed'][0]['name'],
                            new_value=transitions['added'][0]['name']
                            )
            state_transition = check_existence_save(db, state_transition, StateTransition, True, 'id', transitions['id'])
            # save author_did_state_transition
            author_did_state_transition = AuthorDidStateTransition(
                author_key=author._key,
                state_transition_key=state_transition._key,
            )
            check_existence_save(db, author_did_state_transition, AuthorDidStateTransition, False)
            issue = Issue(
                id_readable=transitions['target']['idReadable'],
                tittle=transitions['target']['summary'],
                id=transitions['target']['id'],
            )
            issue = check_existence_save(db, issue, Issue, True, 'id_readable', transitions['target']['idReadable'])

            # save author_did_state_transition
            issue_has_state_transition = IssueHasStateTransition(
                issue_key=issue._key,
                state_transition_key=state_transition._key,
            )
            check_existence_save(db, issue_has_state_transition, IssueHasStateTransition, False)
