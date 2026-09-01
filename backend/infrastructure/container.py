"""Dependency injection container."""

from infrastructure.database import engine
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_court_repository import SQLAlchemyCourtRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_pair_repository import SQLAlchemyPairRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_tournament_repository import SQLAlchemyTournamentRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_match_repository import SQLAlchemyMatchRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_match_event_repository import SQLAlchemyMatchEventRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_notification_repository import SQLAlchemyNotificationRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_audit_log_repository import SQLAlchemyAuditLogRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_user_points_repository import SQLAlchemyUserPointsRepository


class Container:
    def __init__(self):
        self._user_repo = None
        self._role_repo = None
        self._court_repo = None
        self._pair_repo = None
        self._tournament_repo = None
        self._match_repo = None
        self._match_event_repo = None
        self._notification_repo = None
        self._audit_log_repo = None
        self._user_points_repo = None

    @property
    def user_repo(self):
        if self._user_repo is None:
            self._user_repo = SQLAlchemyUserRepository(engine)
        return self._user_repo

    @property
    def role_repo(self):
        if self._role_repo is None:
            self._role_repo = SQLAlchemyRoleRepository(engine)
        return self._role_repo

    @property
    def court_repo(self):
        if self._court_repo is None:
            self._court_repo = SQLAlchemyCourtRepository(engine)
        return self._court_repo

    @property
    def pair_repo(self):
        if self._pair_repo is None:
            self._pair_repo = SQLAlchemyPairRepository(engine)
        return self._pair_repo

    @property
    def tournament_repo(self):
        if self._tournament_repo is None:
            self._tournament_repo = SQLAlchemyTournamentRepository(engine)
        return self._tournament_repo

    @property
    def match_repo(self):
        if self._match_repo is None:
            self._match_repo = SQLAlchemyMatchRepository(engine)
        return self._match_repo

    @property
    def match_event_repo(self):
        if self._match_event_repo is None:
            self._match_event_repo = SQLAlchemyMatchEventRepository(engine)
        return self._match_event_repo

    @property
    def notification_repo(self):
        if self._notification_repo is None:
            self._notification_repo = SQLAlchemyNotificationRepository(engine)
        return self._notification_repo

    @property
    def audit_log_repo(self):
        if self._audit_log_repo is None:
            self._audit_log_repo = SQLAlchemyAuditLogRepository(engine)
        return self._audit_log_repo

    @property
    def user_points_repo(self):
        if self._user_points_repo is None:
            self._user_points_repo = SQLAlchemyUserPointsRepository(engine)
        return self._user_points_repo


container = Container()
