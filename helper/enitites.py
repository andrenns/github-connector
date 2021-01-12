
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

    vcs_changes = relationship(__name__+".VcsChange", '_key', target_field='author_key')

    def __str__(self):
        return "<Author(" + self.name + ")>"


class Target(Collection):
    __collection__ = 'target'
    _index = [{'type': 'hash', 'fields': ['id'], 'unique': True}]

    text = String(required=True)
    id = String(required=True, allow_none=False)
    type = String(required=True)

    vcs_changes = relationship(__name__+".VcsChange", '_key', target_field='target_key')

    def __str__(self):
        return "<Target(" + self.text + ")>"


class VcsChanges(Collection):
    __collection__ = 'vcsChanges'
    _index = [{'type': 'hash', 'fields': ['id'], 'unique': True}]

    _allow_extra_fields = False

    author_key = String()
    id = String(required=True, allow_none=False)
    timestamp = Integer(required=True)
    target_key = String()
    type = String(required=True)

    author = relationship(Author, 'author_key', cache=False)
    target = relationship(Target, 'target_key', cache=False)

    def __str__(self):
        return "<VcsChange({} - {} - {})>".format(self.id, self.timestamp, self.type)


class Issue(Collection):
    __collection__ = 'issue'
    _index = [{'type': 'hash', 'fields': ['id_readable'], 'unique': True}]

    _allow_extra_fields = False

    id_readable = String(required=True, allow_none=False)
    tittle = String(required=True)
    id = String(required=True)
    type = String(required=True)

    def __str__(self):
        return "<Issue({} - {})>".format(self.id_readable, self.tittle)


class IssueHasVcsChanges(Collection):
    __collection__ = 'issue_has_vcsChanges'
    _index = [{'type': 'hash', 'fields': ['issue_key', 'vcs_change_key'], 'unique': True}]

    _allow_extra_fields = False

    issue_key = String(allow_none=False)
    vcs_change_key = String(allow_none=False)

    issue = relationship(Issue, 'issue_key', cache=False)
    vcs_change = relationship(VcsChanges, 'vcs_change_key', cache=False)

    def __str__(self):
        return "<IssueHasVcsChange({} - {})>".format(self.issue_key, self.vcs_change_key)
