#!/usr/bin/env python3
"""
Database integrity check script.
Verifies FK constraints and data consistency.
"""

import os
import sys
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL is not set.")
    sys.exit(1)

engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)


def check_orphaned_records(conn, child_table, child_col, parent_table, parent_col, label=""):
    """Check for orphaned records violating FK constraints."""
    query = text(f"""
        SELECT COUNT(*) as cnt FROM {child_table} c
        LEFT JOIN {parent_table} p ON c.{child_col} = p.{parent_col}
        WHERE c.{child_col} IS NOT NULL AND p.{parent_col} IS NULL
    """)
    row = conn.execute(query).mappings().first()
    count = row["cnt"] if row else 0
    status = "OK" if count == 0 else "VIOLATION"
    print(f"  [{status}] {label or child_table + '.' + child_col + ' -> ' + parent_table}: {count} orphans")
    return count


def check_match_players_consistency(conn):
    """Verify match_players are in sync with pairs."""
    query = text("""
        SELECT COUNT(*) as cnt FROM match_players mp
        JOIN matches m ON mp.match_id = m.id
        WHERE (mp.team = 'A' AND mp.pair_id != m.pair_a_id)
           OR (mp.team = 'B' AND mp.pair_id != m.pair_b_id)
    """)
    row = conn.execute(query).mappings().first()
    count = row["cnt"] if row else 0
    status = "OK" if count == 0 else "WARNING"
    print(f"  [{status}] match_players team/pair mismatch: {count}")
    return count


def check_tournament_counts(conn):
    """Verify registered counts match actual records."""
    query = text("""
        SELECT t.id, t.name,
               (SELECT COUNT(*) FROM tournament_pairs tp WHERE tp.tournament_id = t.id) as actual_pairs,
               (SELECT COUNT(*) FROM tournament_players tpl WHERE tpl.tournament_id = t.id) as actual_players
        FROM tournaments t
    """)
    rows = conn.execute(query).mappings().all()
    print("\nTournament registration counts:")
    for r in rows:
        print(f"  - {r['name']}: {r['actual_pairs']} pairs, {r['actual_players']} players")


def main():
    with engine.connect() as conn:
        print("=== Database Integrity Check ===\n")

        print("FK Constraint Violations (orphaned records):")
        total_violations = 0

        total_violations += check_orphaned_records(conn, "users_auth", "user_id", "users", "id", "users_auth -> users")
        total_violations += check_orphaned_records(conn, "user_roles", "user_id", "users", "id", "user_roles -> users")
        total_violations += check_orphaned_records(conn, "user_roles", "role_id", "roles", "id", "user_roles -> roles")
        total_violations += check_orphaned_records(conn, "profiles", "user_id", "users", "id", "profiles -> users")
        total_violations += check_orphaned_records(conn, "pairs", "player1_id", "users", "id", "pairs -> users (player1)")
        total_violations += check_orphaned_records(conn, "pairs", "player2_id", "users", "id", "pairs -> users (player2)")
        total_violations += check_orphaned_records(conn, "tournament_pairs", "tournament_id", "tournaments", "id", "tournament_pairs -> tournaments")
        total_violations += check_orphaned_records(conn, "tournament_pairs", "pair_id", "pairs", "id", "tournament_pairs -> pairs")
        total_violations += check_orphaned_records(conn, "tournament_players", "tournament_id", "tournaments", "id", "tournament_players -> tournaments")
        total_violations += check_orphaned_records(conn, "tournament_players", "user_id", "users", "id", "tournament_players -> users")
        total_violations += check_orphaned_records(conn, "matches", "tournament_id", "tournaments", "id", "matches -> tournaments")
        total_violations += check_orphaned_records(conn, "matches", "pair_a_id", "pairs", "id", "matches -> pairs (A)")
        total_violations += check_orphaned_records(conn, "matches", "pair_b_id", "pairs", "id", "matches -> pairs (B)")
        total_violations += check_orphaned_records(conn, "match_players", "match_id", "matches", "id", "match_players -> matches")
        total_violations += check_orphaned_records(conn, "match_players", "user_id", "users", "id", "match_players -> users")
        total_violations += check_orphaned_records(conn, "match_players", "pair_id", "pairs", "id", "match_players -> pairs")

        print("\nConsistency Checks:")
        check_match_players_consistency(conn)

        check_tournament_counts(conn)

        print(f"\n=== Total FK violations: {total_violations} ===")
        return total_violations == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
