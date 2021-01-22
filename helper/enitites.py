
from arango_orm.fields import String, Date, Integer, Boolean
from arango_orm import Collection, Relation, Graph, GraphConnection
from arango_orm.references import relationship


class Author(Collection):
    __collection__ = 'author'
    _index = [{'type': 'hash', 'fields': ['id'], 'unique':True}]

    name = String(required=True, allow_none=False)
    login = String(required=True)
    type = String(required=True)
    id = String(required=True)

    def __str__(self):
        return "<Author(" + self.name + ")>"


class StateTransition(Collection):
    __collection__ = 'state_transition'
    _index = [{'type': 'hash', 'fields': ['id'], 'unique': True}]

    _allow_extra_fields = False

    id = String(required=True, allow_none=False)
    timestamp = Integer(required=True)
    old_value = String(required=True)
    new_value = String(required=True)

    def __str__(self):
        return "<StateTransition({} - {} - {})>".format(self.id, self.timestamp, self.type)


class AuthorDidStateTransition(Collection):
    __collection__ = 'author_did_state_transition'
    _index = [{'type': 'hash', 'fields': ['author_key', 'state_transition_key'], 'unique': True}]

    _allow_extra_fields = False

    author_key = String()
    state_transition_key = String()

    author = relationship(Author, 'author_key', cache=False)
    state_transition = relationship(StateTransition, 'state_transition_key', cache=False)

    def __str__(self):
        return "<AuthorDidStateTransition({} - {})>".format(self.author_key, self.state_transition_key)


class Issue(Collection):
    __collection__ = 'issue'
    _index = [{'type': 'hash', 'fields': ['id_readable'], 'unique': True}]

    _allow_extra_fields = False

    id_readable = String(required=True, allow_none=False)
    tittle = String(required=True)
    id = String(required=True)

    def __str__(self):
        return "<Issue({} - {})>".format(self.id_readable, self.tittle)


class IssueHasStateTransition(Collection):
    __collection__ = 'issue_has_state_transition'
    _index = [{'type': 'hash', 'fields': ['issue_key', 'state_transition_key'], 'unique': True}]

    _allow_extra_fields = False

    issue_key = String(allow_none=False)
    state_transition_key = String(allow_none=False)

    issue = relationship(Issue, 'issue_key', cache=False)
    state_transition = relationship(StateTransition, 'state_transition_key', cache=False)

    def __str__(self):
        return "<IssueHasStateTransition({} - {})>".format(self.issue_key, self.state_transition_key)
