from helper.youtrack import get_all_state_transitions
from arango import ArangoClient
from arango_orm import Database
from helper.enitites import StateTransition, Author, Issue, IssueHasStateTransition, AuthorDidStateTransition, \
    AnalysisResult
from arango.exceptions import DocumentInsertError
from helper.env_reader import ENV


def create_connection_db(db):
    client = ArangoClient(hosts=ENV['ARANGODB_HOST'])
    db = Database(client.db(db, username=ENV['ARANGODB_USER'], password=ENV['ARANGODB_PWD']))
    return db


DB = create_connection_db(ENV['ARANGODB_DBNAME'])


def create_if_not_exists():
    collections = [Author, Issue, StateTransition, IssueHasStateTransition, AuthorDidStateTransition, AnalysisResult]

    for col in collections:
        if not DB.has_collection(col):
            DB.create_collection(col)


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
            transitions['added'] = [{'$type': transitions['removed'][0]['$type'], 'name': 'NONE'}]
    elif isinstance(transitions['removed'], list) and not transitions['removed']:
        if transitions['added']:
            transitions['removed'] = [{'$type': transitions['added'][0]['$type'], 'name': 'NONE'}]
    elif not isinstance(transitions['added'], list) and not isinstance(transitions['removed'], list):
        transitions['added'] = [{'$type': 'NONE', 'name': 'NONE'}]
        transitions['removed'] = [{'$type': 'NONE', 'name': 'NONE'}]
    return transitions


def save_vcs_changes():
    create_if_not_exists()
    state_transitions = get_all_state_transitions()

    for transitions in state_transitions:
        transitions = check_transition_values(transitions)
        if transitions['added'][0]['$type'] == 'StateBundleElement' \
                or transitions['removed'][0]['$type'] == 'StateBundleElement':
            author = Author(name=transitions['author']['name'],
                            login=transitions['author']['login'],
                            type=transitions['author']['$type'],
                            id=transitions['author']['id']
                            )
            author = check_existence_save(DB, author, Author, True, 'id', transitions['author']['id'])
            # save state_transition
            state_transition = StateTransition(
                id=transitions['id'],
                timestamp=transitions['timestamp'],
                old_value=transitions['removed'][0]['name'],
                new_value=transitions['added'][0]['name']
            )
            state_transition = check_existence_save(DB, state_transition, StateTransition, True, 'id',
                                                    transitions['id'])
            # save author_did_state_transition
            author_did_state_transition = AuthorDidStateTransition(
                author_key=author._key,
                state_transition_key=state_transition._key,
            )
            check_existence_save(DB, author_did_state_transition, AuthorDidStateTransition, False)
            issue = Issue(
                id_readable=transitions['target']['idReadable'],
                tittle=transitions['target']['summary'],
                id=transitions['target']['id'],
            )
            issue = check_existence_save(DB, issue, Issue, True, 'id_readable', transitions['target']['idReadable'])

            # save author_did_state_transition
            issue_has_state_transition = IssueHasStateTransition(
                issue_key=issue._key,
                state_transition_key=state_transition._key,
            )
            check_existence_save(DB, issue_has_state_transition, IssueHasStateTransition, False)


def get_stored_data():
    cursor = DB.aql.execute('FOR i in issue \
                FOR it in issue_has_state_transition \
                FILTER i._key == it.issue_key \
                    FOR t in state_transition \
                    FILTER t._key == it.state_transition_key \
                        FOR at in author_did_state_transition \
                        FILTER at.state_transition_key == t._key \
                            FOR a in author \
                            FILTER a._key == at.author_key \
                            RETURN {\'issue_id\' :i.id_readable, \'timestamp\':DATE_ISO8601(t.timestamp), \'old_value\'\
                            :t.old_value, \'new_value\': t.new_value, \'author_name\':a.name}')
    return [doc for doc in cursor]


def save_analysis_results(data_used_file_name, analysis_result_file_name, timestamp):
    create_if_not_exists()
    analysis_result = AnalysisResult(
        data_file_name=data_used_file_name,
        analysis_result_file_name=analysis_result_file_name,
        timestamp=timestamp
        )
    check_existence_save(DB, analysis_result, AnalysisResult, False)
