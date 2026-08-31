"""Routers package."""

from presentation.routers import auth, users, pairs, tournaments, matches, courts, audit_logs, notifications, stats, admin

auth_router = auth.auth_router
users_router = users.users_router
pairs_router = pairs.pairs_router
tournaments_router = tournaments.tournaments_router
matches_router = matches.matches_router
courts_router = courts.courts_router
audit_logs_router = audit_logs.audit_logs_router
notifications_router = notifications.notifications_router
stats_router = stats.stats_router
admin_router = admin.admin_router
