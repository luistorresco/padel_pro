"""FastAPI dependencies."""

import os
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from domain.services.auth_service import AuthService
from infrastructure.container import container
from application.use_cases.auth import LoginUseCase, RegisterUseCase, GetCurrentUserUseCase
from application.use_cases.users import ListUsersUseCase, GetUserUseCase, CreateUserUseCase, UpdateUserUseCase, DeleteUserUseCase, UpdateUserPrivacyUseCase, ConvertGuestUseCase
from application.use_cases.tournaments import ListTournamentsUseCase, GetTournamentUseCase, GetTournamentFullUseCase, CreateTournamentUseCase, UpdateTournamentUseCase, DeleteTournamentUseCase, RegisterForTournamentUseCase
from application.use_cases.matches import ListMatchesUseCase, GetMatchUseCase, GetMatchPlayersUseCase, CreateMatchUseCase, UpdateMatchCourtUseCase, UpdateMatchDateTimeUseCase, UpdateMatchUseCase, FinishMatchUseCase, CreateMatchEventUseCase, DeleteMatchUseCase, GenerateBracketUseCase
from application.use_cases.pairs import ListPairsUseCase, GetPairUseCase, CreatePairUseCase, DeletePairUseCase
from application.use_cases.courts import ListCourtsUseCase, GetCourtUseCase, CreateCourtUseCase, UpdateCourtUseCase, DeleteCourtUseCase
from application.use_cases.notifications import ListNotificationsUseCase, CreateNotificationUseCase
from application.use_cases.audit_logs import ListAuditLogsUseCase, CreateAuditLogUseCase
from application.use_cases.stats import GetStatsUseCase
from application.use_cases.admin import RunMigrationsUseCase
from domain.services.privacy_service import PrivacyService
from domain.value_objects.privacy_settings import PrivacySettings

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "padel-pro-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
auth_service = AuthService(secret_key=JWT_SECRET_KEY)
privacy_service = PrivacyService()

login_uc = LoginUseCase(container.user_repo, container.role_repo, auth_service)
register_uc = RegisterUseCase(container.user_repo, auth_service)
get_current_user_uc = GetCurrentUserUseCase(container.user_repo, privacy_service)

list_users_uc = ListUsersUseCase(container.user_repo, privacy_service)
get_user_uc = GetUserUseCase(container.user_repo, privacy_service)
create_user_uc = CreateUserUseCase(container.user_repo, auth_service)
update_user_uc = UpdateUserUseCase(container.user_repo)
delete_user_uc = DeleteUserUseCase(container.user_repo)
update_user_privacy_uc = UpdateUserPrivacyUseCase(container.user_repo)
convert_guest_uc = ConvertGuestUseCase(container.user_repo, auth_service)

list_tournaments_uc = ListTournamentsUseCase(container.tournament_repo, container.match_repo)
get_tournament_uc = GetTournamentUseCase(container.tournament_repo, container.match_repo)
get_tournament_full_uc = GetTournamentFullUseCase(container.tournament_repo)
create_tournament_uc = CreateTournamentUseCase(container.tournament_repo)
update_tournament_uc = UpdateTournamentUseCase(container.tournament_repo)
delete_tournament_uc = DeleteTournamentUseCase(container.tournament_repo, container.match_repo)
register_for_tournament_uc = RegisterForTournamentUseCase(container.tournament_repo, container.match_repo)

list_matches_uc = ListMatchesUseCase(container.match_repo)
get_match_uc = GetMatchUseCase(container.match_repo)
get_match_players_uc = GetMatchPlayersUseCase(container.match_repo)
create_match_uc = CreateMatchUseCase(container.match_repo)
update_match_court_uc = UpdateMatchCourtUseCase(container.match_repo)
update_match_date_time_uc = UpdateMatchDateTimeUseCase(container.match_repo)
update_match_uc = UpdateMatchUseCase(container.match_repo)
finish_match_uc = FinishMatchUseCase(container.match_repo, container.user_repo, container.user_points_repo, container.pair_repo)
create_match_event_uc = CreateMatchEventUseCase(container.match_event_repo)
delete_match_uc = DeleteMatchUseCase(container.match_repo)
generate_bracket_uc = GenerateBracketUseCase(container.tournament_repo, container.match_repo, container.pair_repo)

list_pairs_uc = ListPairsUseCase(container.pair_repo)
get_pair_uc = GetPairUseCase(container.pair_repo)
create_pair_uc = CreatePairUseCase(container.pair_repo)
delete_pair_uc = DeletePairUseCase(container.pair_repo)

list_courts_uc = ListCourtsUseCase(container.court_repo)
get_court_uc = GetCourtUseCase(container.court_repo)
create_court_uc = CreateCourtUseCase(container.court_repo)
update_court_uc = UpdateCourtUseCase(container.court_repo)
delete_court_uc = DeleteCourtUseCase(container.court_repo)

list_notifications_uc = ListNotificationsUseCase(container.notification_repo)
create_notification_uc = CreateNotificationUseCase(container.notification_repo)

list_audit_logs_uc = ListAuditLogsUseCase(container.audit_log_repo)
create_audit_log_uc = CreateAuditLogUseCase(container.audit_log_repo)

get_stats_uc = GetStatsUseCase(container.engine)
run_migrations_uc = RunMigrationsUseCase(container.engine)


def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


def require_admin(payload: dict = Depends(get_current_user)):
    ADMIN_ROLES = {"ADMIN", "SUPER_ADMIN", "BUSINESS_ADMIN", "BUSINESS_MANAGER"}
    if payload.get("role") not in ADMIN_ROLES:
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload


def require_super_admin(payload: dict = Depends(get_current_user)):
    if payload.get("role") != "SUPER_ADMIN":
        raise HTTPException(status_code=403, detail="Super admin access required")
    return payload
