-- ============================================================
-- Padel Pro - MySQL Seed Script
-- Generated from mock_data.json
-- Compatible with schema in backend/database.py
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------
-- Tables
-- ------------------------------------------------------------

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    avatar TEXT,
    level TEXT,
    position TEXT,
    dominant_hand TEXT,
    current_pair_id TEXT,
    points INTEGER DEFAULT 0,
    partner_name TEXT,
    phone TEXT,
    stats TEXT
);

DROP TABLE IF EXISTS pairs;
CREATE TABLE IF NOT EXISTS pairs (
    id VARCHAR(255) PRIMARY KEY,
    name TEXT NOT NULL,
    player1_id TEXT NOT NULL,
    player2_id TEXT NOT NULL,
    player1_name TEXT NOT NULL,
    player2_name TEXT NOT NULL,
    player1_avatar TEXT,
    player2_avatar TEXT,
    created_at TEXT,
    status TEXT NOT NULL,
    tournaments_disputed INTEGER,
    titles_won INTEGER
);

DROP TABLE IF EXISTS courts;
CREATE TABLE IF NOT EXISTS courts (
    id VARCHAR(255) PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    number INTEGER NOT NULL,
    status TEXT NOT NULL,
    current_match_id TEXT
);

DROP TABLE IF EXISTS tournaments;
CREATE TABLE IF NOT EXISTS tournaments (
    id VARCHAR(255) PRIMARY KEY,
    name TEXT NOT NULL,
    logo TEXT,
    description TEXT,
    category TEXT,
    level TEXT,
    location TEXT,
    start_date TEXT,
    end_date TEXT,
    status TEXT,
    format TEXT,
    max_pairs INTEGER,
    registered_pair_ids TEXT,
    registered_user_ids TEXT,
    rules TEXT,
    court_ids TEXT
);

DROP TABLE IF EXISTS matches;
CREATE TABLE IF NOT EXISTS matches (
    id VARCHAR(255) PRIMARY KEY,
    tournament_id TEXT,
    tournament_name TEXT,
    court_id TEXT,
    court_name TEXT NOT NULL,
    date_time TEXT NOT NULL,
    pair_a_id TEXT NOT NULL,
    pair_b_id TEXT NOT NULL,
    pair_a_name TEXT NOT NULL,
    pair_b_name TEXT NOT NULL,
    player_a1_id TEXT NOT NULL,
    player_a2_id TEXT NOT NULL,
    player_b1_id TEXT NOT NULL,
    player_b2_id TEXT NOT NULL,
    player_a1_name TEXT NOT NULL,
    player_a2_name TEXT NOT NULL,
    player_b1_name TEXT NOT NULL,
    player_b2_name TEXT NOT NULL,
    player_a1_avatar TEXT,
    player_a2_avatar TEXT,
    player_b1_avatar TEXT,
    player_b2_avatar TEXT,
    status TEXT NOT NULL,
    sets TEXT,
    current_game TEXT,
    current_set_index INTEGER,
    winner_pair_id TEXT,
    winner_team TEXT,
    start_time_ms INTEGER,
    elapsed_time_sec INTEGER NOT NULL,
    golden_point INTEGER NOT NULL,
    sets_to_win INTEGER NOT NULL,
    round_name TEXT
);

DROP TABLE IF EXISTS audit_logs;
CREATE TABLE IF NOT EXISTS audit_logs (
    id VARCHAR(255) PRIMARY KEY,
    admin_name TEXT NOT NULL,
    admin_email TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    details TEXT,
    timestamp TEXT NOT NULL
);

DROP TABLE IF EXISTS notifications;
CREATE TABLE IF NOT EXISTS notifications (
    id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT,
    timestamp TEXT NOT NULL,
    `read` INTEGER NOT NULL,
    `type` TEXT NOT NULL,
    link_id TEXT
);

DROP TABLE IF EXISTS match_events;
CREATE TABLE IF NOT EXISTS match_events (
    id VARCHAR(255) PRIMARY KEY,
    match_id TEXT NOT NULL,
    set_number INTEGER NOT NULL,
    game_number INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    winning_pair_id TEXT NOT NULL,
    player_id TEXT,
    player_name TEXT,
    event_type TEXT NOT NULL,
    description TEXT,
    score_snapshot TEXT
);

DROP TABLE IF EXISTS gesture_config;
CREATE TABLE IF NOT EXISTS gesture_config (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    point_team_a_gesture TEXT NOT NULL,
    point_team_b_gesture TEXT NOT NULL,
    undo_gesture TEXT NOT NULL,
    cooldown_ms INTEGER NOT NULL,
    min_confidence REAL NOT NULL,
    required_hold_frames INTEGER NOT NULL,
    detection_zone TEXT,
    mode TEXT NOT NULL
);

DROP TABLE IF EXISTS users_auth;
CREATE TABLE IF NOT EXISTS users_auth (
    id VARCHAR(255) PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL
);

-- ------------------------------------------------------------
-- Seed Data
-- ------------------------------------------------------------

-- Users

INSERT INTO users (id, name, surname, username, email, role, avatar, level, position, dominant_hand, current_pair_id, points, partner_name, phone, stats) VALUES ('usr_carlos_admin', 'Carlos', 'Gómez', 'carlospadel', 'carlos@padelpro.app', 'ADMIN', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80', 'Avanzado', 'Revés (Izquierda)', 'Derecha', 'pair_galan_lebron', '1520', 'Juan Lebrón', '+34 612 345 678', '{"points_won":1842,"winners":312,"smashes":180,"smashes_won":142,"voleas_won":128,"bandejas":95,"viboras":64,"remates":110,"net_points_won":412,"touches":4210,"shots":3890,"serves":820,"first_serves":610,"second_serves":210,"aces":42,"double_faults":18,"break_points":94,"break_points_won":58,"recoveries":182,"globos":340,"devoluciones":680,"points_saved":88,"unforced_errors":187,"distance_km":94.3,"time_played_min":1420,"avg_speed_kmh":12.4,"moves_count":2840,"matches_played":24,"matches_won":17,"matches_lost":7,"sets_won":38,"sets_lost":21,"games_won":241,"games_lost":198}') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), surname = VALUES(surname), username = VALUES(username), email = VALUES(email), role = VALUES(role), avatar = VALUES(avatar), level = VALUES(level), position = VALUES(position), dominant_hand = VALUES(dominant_hand), current_pair_id = VALUES(current_pair_id), points = VALUES(points), partner_name = VALUES(partner_name), phone = VALUES(phone), stats = VALUES(stats);
INSERT INTO users (id, name, surname, username, email, role, avatar, level, position, dominant_hand, current_pair_id, points, partner_name, phone, stats) VALUES ('usr_ale_galan', 'Alejandro', 'Galán', 'alegalan', 'galan@padel.es', 'PLAYER', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80', 'Profesional', 'Revés (Izquierda)', 'Derecha', 'pair_galan_lebron', '1520', 'Juan Lebrón', NULL, '{"points_won":2100,"winners":410,"smashes":220,"smashes_won":190,"voleas_won":160,"bandejas":110,"viboras":85,"remates":130,"net_points_won":510,"touches":5100,"shots":4800,"serves":900,"first_serves":720,"second_serves":180,"aces":58,"double_faults":12,"break_points":110,"break_points_won":72,"recoveries":210,"globos":410,"devoluciones":780,"points_saved":102,"unforced_errors":140,"distance_km":112.5,"time_played_min":1600,"avg_speed_kmh":13.8,"moves_count":3400,"matches_played":28,"matches_won":22,"matches_lost":6,"sets_won":48,"sets_lost":18,"games_won":290,"games_lost":190}') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), surname = VALUES(surname), username = VALUES(username), email = VALUES(email), role = VALUES(role), avatar = VALUES(avatar), level = VALUES(level), position = VALUES(position), dominant_hand = VALUES(dominant_hand), current_pair_id = VALUES(current_pair_id), points = VALUES(points), partner_name = VALUES(partner_name), phone = VALUES(phone), stats = VALUES(stats);
INSERT INTO users (id, name, surname, username, email, role, avatar, level, position, dominant_hand, current_pair_id, points, partner_name, phone, stats) VALUES ('usr_juan_lebron', 'Juan', 'Lebrón', 'juanlebron', 'lebron@padel.es', 'PLAYER', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80', 'Profesional', 'Drive (Derecha)', 'Derecha', 'pair_galan_lebron', '1480', 'Alejandro Galán', NULL, '{"points_won":1980,"winners":380,"smashes":210,"smashes_won":175,"voleas_won":145,"bandejas":105,"viboras":78,"remates":118,"net_points_won":480,"touches":4900,"shots":4600,"serves":880,"first_serves":690,"second_serves":190,"aces":51,"double_faults":15,"break_points":104,"break_points_won":65,"recoveries":195,"globos":390,"devoluciones":740,"points_saved":95,"unforced_errors":155,"distance_km":108.2,"time_played_min":1550,"avg_speed_kmh":13.2,"moves_count":3200,"matches_played":28,"matches_won":22,"matches_lost":6,"sets_won":48,"sets_lost":18,"games_won":290,"games_lost":190}') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), surname = VALUES(surname), username = VALUES(username), email = VALUES(email), role = VALUES(role), avatar = VALUES(avatar), level = VALUES(level), position = VALUES(position), dominant_hand = VALUES(dominant_hand), current_pair_id = VALUES(current_pair_id), points = VALUES(points), partner_name = VALUES(partner_name), phone = VALUES(phone), stats = VALUES(stats);
INSERT INTO users (id, name, surname, username, email, role, avatar, level, position, dominant_hand, current_pair_id, points, partner_name, phone, stats) VALUES ('usr_agustin_tapia', 'Agustín', 'Tapia', 'agustapia', 'tapia@padel.ar', 'PLAYER', 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80', 'Profesional', 'Revés (Izquierda)', 'Derecha', 'pair_coello_tapia', '1410', 'Arturo Coello', NULL, '{"points_won":1890,"winners":395,"smashes":240,"smashes_won":205,"voleas_won":135,"bandejas":90,"viboras":92,"remates":140,"net_points_won":460,"touches":4700,"shots":4300,"serves":840,"first_serves":640,"second_serves":200,"aces":49,"double_faults":19,"break_points":98,"break_points_won":61,"recoveries":180,"globos":360,"devoluciones":710,"points_saved":88,"unforced_errors":168,"distance_km":102.0,"time_played_min":1480,"avg_speed_kmh":14.1,"moves_count":3100,"matches_played":26,"matches_won":19,"matches_lost":7,"sets_won":42,"sets_lost":20,"games_won":265,"games_lost":205}') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), surname = VALUES(surname), username = VALUES(username), email = VALUES(email), role = VALUES(role), avatar = VALUES(avatar), level = VALUES(level), position = VALUES(position), dominant_hand = VALUES(dominant_hand), current_pair_id = VALUES(current_pair_id), points = VALUES(points), partner_name = VALUES(partner_name), phone = VALUES(phone), stats = VALUES(stats);
INSERT INTO users (id, name, surname, username, email, role, avatar, level, position, dominant_hand, current_pair_id, points, partner_name, phone, stats) VALUES ('usr_arturo_coello', 'Arturo', 'Coello', 'acoello', 'coello@padel.es', 'PLAYER', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80', 'Profesional', 'Drive (Derecha)', 'Zurda', 'pair_coello_tapia', '1375', 'Agustín Tapia', NULL, '{"points_won":1820,"winners":370,"smashes":230,"smashes_won":195,"voleas_won":140,"bandejas":88,"viboras":80,"remates":135,"net_points_won":450,"touches":4500,"shots":4200,"serves":810,"first_serves":630,"second_serves":180,"aces":55,"double_faults":14,"break_points":92,"break_points_won":58,"recoveries":172,"globos":340,"devoluciones":690,"points_saved":82,"unforced_errors":160,"distance_km":99.4,"time_played_min":1420,"avg_speed_kmh":13.5,"moves_count":2950,"matches_played":26,"matches_won":19,"matches_lost":7,"sets_won":42,"sets_lost":20,"games_won":265,"games_lost":205}') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), surname = VALUES(surname), username = VALUES(username), email = VALUES(email), role = VALUES(role), avatar = VALUES(avatar), level = VALUES(level), position = VALUES(position), dominant_hand = VALUES(dominant_hand), current_pair_id = VALUES(current_pair_id), points = VALUES(points), partner_name = VALUES(partner_name), phone = VALUES(phone), stats = VALUES(stats);

-- Pairs

INSERT INTO pairs (id, name, player1_id, player2_id, player1_name, player2_name, player1_avatar, player2_avatar, created_at, status, tournaments_disputed, titles_won) VALUES ('pair_galan_lebron', 'Galán / Lebrón', 'usr_ale_galan', 'usr_juan_lebron', 'Alejandro Galán', 'Juan Lebrón', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80', '2025-01-15', 'ACTIVE', '12', '7') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id), player1_name = VALUES(player1_name), player2_name = VALUES(player2_name), player1_avatar = VALUES(player1_avatar), player2_avatar = VALUES(player2_avatar), created_at = VALUES(created_at), status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won);
INSERT INTO pairs (id, name, player1_id, player2_id, player1_name, player2_name, player1_avatar, player2_avatar, created_at, status, tournaments_disputed, titles_won) VALUES ('pair_coello_tapia', 'Coello / Tapia', 'usr_arturo_coello', 'usr_agustin_tapia', 'Arturo Coello', 'Agustín Tapia', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80', '2025-02-01', 'ACTIVE', '10', '5') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id), player1_name = VALUES(player1_name), player2_name = VALUES(player2_name), player1_avatar = VALUES(player1_avatar), player2_avatar = VALUES(player2_avatar), created_at = VALUES(created_at), status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won);
INSERT INTO pairs (id, name, player1_id, player2_id, player1_name, player2_name, player1_avatar, player2_avatar, created_at, status, tournaments_disputed, titles_won) VALUES ('pair_chingotto_navarro', 'Chingotto / Navarro', 'usr_chingotto', 'usr_paquito', 'Fede Chingotto', 'Paquito Navarro', 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=150&auto=format&fit=crop&q=80', '2025-03-10', 'ACTIVE', '8', '2') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id), player1_name = VALUES(player1_name), player2_name = VALUES(player2_name), player1_avatar = VALUES(player1_avatar), player2_avatar = VALUES(player2_avatar), created_at = VALUES(created_at), status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won);
INSERT INTO pairs (id, name, player1_id, player2_id, player1_name, player2_name, player1_avatar, player2_avatar, created_at, status, tournaments_disputed, titles_won) VALUES ('pair_stupaczuk_dinenno', 'Stupaczuk / Di Nenno', 'usr_stupa', 'usr_dinenno', 'Franco Stupaczuk', 'Martin Di Nenno', 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80', '2025-01-20', 'ACTIVE', '9', '3') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id), player1_name = VALUES(player1_name), player2_name = VALUES(player2_name), player1_avatar = VALUES(player1_avatar), player2_avatar = VALUES(player2_avatar), created_at = VALUES(created_at), status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won);

-- Courts

INSERT INTO courts (id, name, location, number, status, current_match_id) VALUES ('crt_central', 'Pista Central (Estadio)', 'Club Central', '1', 'OCCUPIED', 'match_live_01') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), location = VALUES(location), number = VALUES(number), status = VALUES(status), current_match_id = VALUES(current_match_id);
INSERT INTO courts (id, name, location, number, status, current_match_id) VALUES ('crt_2', 'Pista 2 Panorámica', 'Club Central', '2', 'AVAILABLE', NULL) ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), location = VALUES(location), number = VALUES(number), status = VALUES(status), current_match_id = VALUES(current_match_id);
INSERT INTO courts (id, name, location, number, status, current_match_id) VALUES ('crt_3', 'Pista 3 Cristal Norte', 'Anexo Norte', '3', 'AVAILABLE', NULL) ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), location = VALUES(location), number = VALUES(number), status = VALUES(status), current_match_id = VALUES(current_match_id);
INSERT INTO courts (id, name, location, number, status, current_match_id) VALUES ('crt_4', 'Pista 4 Cubierta', 'Anexo Sur', '4', 'AVAILABLE', NULL) ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), location = VALUES(location), number = VALUES(number), status = VALUES(status), current_match_id = VALUES(current_match_id);

-- Tournaments

INSERT INTO tournaments (id, name, logo, description, category, level, location, start_date, end_date, status, format, max_pairs, registered_pair_ids, registered_user_ids, rules, court_ids) VALUES ('tour_major_madrid', 'Premier Padel Major Madrid 2026', '🏆', 'El torneo oficial más prestigioso de la temporada con las mejores 16 parejas del circuito.', 'Masculino', 'Profesional', 'Wizink Center, Madrid', '2026-08-10', '2026-08-16', 'ACTIVE', 'Grupos + eliminación directa', '16', '["pair_galan_lebron","pair_coello_tapia","pair_chingotto_navarro","pair_stupaczuk_dinenno"]', '["usr_carlos_admin","usr_ale_galan","usr_juan_lebron","usr_agustin_tapia","usr_arturo_coello"]', '{"sets_to_win":2,"golden_point":true,"tie_break_at":6,"final_set_tie_break":true,"points_distribution":{"champion":1000,"runner_up":600,"semi_finals":360,"quarter_finals":180,"group_stage":90}}', '["crt_central","crt_2"]') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), logo = VALUES(logo), description = VALUES(description), category = VALUES(category), level = VALUES(level), location = VALUES(location), start_date = VALUES(start_date), end_date = VALUES(end_date), status = VALUES(status), format = VALUES(format), max_pairs = VALUES(max_pairs), registered_pair_ids = VALUES(registered_pair_ids), registered_user_ids = VALUES(registered_user_ids), rules = VALUES(rules), court_ids = VALUES(court_ids);
INSERT INTO tournaments (id, name, logo, description, category, level, location, start_date, end_date, status, format, max_pairs, registered_pair_ids, registered_user_ids, rules, court_ids) VALUES ('tour_open_barcelona', 'Copa Abierta Barcelona 2026', '🎾', 'Competición de categoría Mixto Abierto con fases de grupos intensas y eliminatorias.', 'Mixto', 'Avanzado', 'Real Club de Tenis Barcelona', '2026-09-01', '2026-09-05', 'REGISTRATION', 'Fase de grupos', '12', '["pair_chingotto_navarro","pair_stupaczuk_dinenno"]', '["usr_chingotto","usr_paquito","usr_stupa","usr_dinenno"]', '{"sets_to_win":2,"golden_point":true,"tie_break_at":6,"final_set_tie_break":true,"points_distribution":{"champion":500,"runner_up":300,"semi_finals":180,"quarter_finals":90,"group_stage":45}}', '["crt_3","crt_4"]') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), logo = VALUES(logo), description = VALUES(description), category = VALUES(category), level = VALUES(level), location = VALUES(location), start_date = VALUES(start_date), end_date = VALUES(end_date), status = VALUES(status), format = VALUES(format), max_pairs = VALUES(max_pairs), registered_pair_ids = VALUES(registered_pair_ids), registered_user_ids = VALUES(registered_user_ids), rules = VALUES(rules), court_ids = VALUES(court_ids);
INSERT INTO tournaments (id, name, logo, description, category, level, location, start_date, end_date, status, format, max_pairs, registered_pair_ids, registered_user_ids, rules, court_ids) VALUES ('tour_nocturno_sevilla', 'Torneo Nocturno Sevilla', '🌙', 'Edición nocturna exprés en formato Eliminación Directa.', 'Masculino', 'Principiante', 'Padel Club Sevilla', '2026-09-20', '2026-09-22', 'UPCOMING', 'Eliminación directa', '8', '["pair_coello_tapia"]', '["usr_arturo_coello","usr_agustin_tapia"]', '{"sets_to_win":2,"golden_point":false,"tie_break_at":6,"final_set_tie_break":true,"points_distribution":{"champion":250,"runner_up":150,"semi_finals":90,"quarter_finals":45,"group_stage":20}}', '["crt_2"]') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), logo = VALUES(logo), description = VALUES(description), category = VALUES(category), level = VALUES(level), location = VALUES(location), start_date = VALUES(start_date), end_date = VALUES(end_date), status = VALUES(status), format = VALUES(format), max_pairs = VALUES(max_pairs), registered_pair_ids = VALUES(registered_pair_ids), registered_user_ids = VALUES(registered_user_ids), rules = VALUES(rules), court_ids = VALUES(court_ids);

-- Matches

INSERT INTO matches (id, tournament_id, tournament_name, court_id, court_name, date_time, pair_a_id, pair_b_id, pair_a_name, pair_b_name, player_a1_id, player_a2_id, player_b1_id, player_b2_id, player_a1_name, player_a2_name, player_b1_name, player_b2_name, player_a1_avatar, player_a2_avatar, player_b1_avatar, player_b2_avatar, status, sets, current_game, current_set_index, winner_pair_id, winner_team, start_time_ms, elapsed_time_sec, golden_point, sets_to_win, round_name) VALUES ('match_live_01', 'tour_major_madrid', 'Premier Padel Major Madrid 2026', 'crt_central', 'Pista Central (Estadio)', '2026-08-08 11:30', 'pair_galan_lebron', 'pair_coello_tapia', 'Galán / Lebrón', 'Coello / Tapia', 'usr_ale_galan', 'usr_juan_lebron', 'usr_arturo_coello', 'usr_agustin_tapia', 'Alejandro Galán', 'Juan Lebrón', 'Arturo Coello', 'Agustín Tapia', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80', 'LIVE', '[{"team_a_games":6,"team_b_games":4,"is_tie_break":false,"winner":"A"},{"team_a_games":3,"team_b_games":6,"is_tie_break":false,"winner":"B"},{"team_a_games":3,"team_b_games":2,"is_tie_break":false}]', '{"team_a_points":"30","team_b_points":"15","server_team":"A","is_deuce":false}', '2', NULL, NULL, NULL, '5240', 1, '2', 'Gran Final') ON DUPLICATE KEY UPDATE id = VALUES(id), tournament_id = VALUES(tournament_id), tournament_name = VALUES(tournament_name), court_id = VALUES(court_id), court_name = VALUES(court_name), date_time = VALUES(date_time), pair_a_id = VALUES(pair_a_id), pair_b_id = VALUES(pair_b_id), pair_a_name = VALUES(pair_a_name), pair_b_name = VALUES(pair_b_name), player_a1_id = VALUES(player_a1_id), player_a2_id = VALUES(player_a2_id), player_b1_id = VALUES(player_b1_id), player_b2_id = VALUES(player_b2_id), player_a1_name = VALUES(player_a1_name), player_a2_name = VALUES(player_a2_name), player_b1_name = VALUES(player_b1_name), player_b2_name = VALUES(player_b2_name), player_a1_avatar = VALUES(player_a1_avatar), player_a2_avatar = VALUES(player_a2_avatar), player_b1_avatar = VALUES(player_b1_avatar), player_b2_avatar = VALUES(player_b2_avatar), status = VALUES(status), sets = VALUES(sets), current_game = VALUES(current_game), current_set_index = VALUES(current_set_index), winner_pair_id = VALUES(winner_pair_id), winner_team = VALUES(winner_team), start_time_ms = VALUES(start_time_ms), elapsed_time_sec = VALUES(elapsed_time_sec), golden_point = VALUES(golden_point), sets_to_win = VALUES(sets_to_win), round_name = VALUES(round_name);
INSERT INTO matches (id, tournament_id, tournament_name, court_id, court_name, date_time, pair_a_id, pair_b_id, pair_a_name, pair_b_name, player_a1_id, player_a2_id, player_b1_id, player_b2_id, player_a1_name, player_a2_name, player_b1_name, player_b2_name, player_a1_avatar, player_a2_avatar, player_b1_avatar, player_b2_avatar, status, sets, current_game, current_set_index, winner_pair_id, winner_team, start_time_ms, elapsed_time_sec, golden_point, sets_to_win, round_name) VALUES ('match_upcoming_02', 'tour_major_madrid', 'Premier Padel Major Madrid 2026', 'crt_2', 'Pista 2 Panorámica', '2026-08-08 18:30', 'pair_chingotto_navarro', 'pair_stupaczuk_dinenno', 'Chingotto / Navarro', 'Stupaczuk / Di Nenno', 'usr_chingotto', 'usr_paquito', 'usr_stupa', 'usr_dinenno', 'Fede Chingotto', 'Paquito Navarro', 'Franco Stupaczuk', 'Martin Di Nenno', 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80', 'UPCOMING', '[{"team_a_games":0,"team_b_games":0,"is_tie_break":false,"tie_break_points":{"team_a":0,"team_b":0}}]', '{"team_a_points":"0","team_b_points":"0","server_team":"A","is_deuce":false}', '0', NULL, NULL, NULL, '0', 1, '2', 'Cuartos de Final') ON DUPLICATE KEY UPDATE id = VALUES(id), tournament_id = VALUES(tournament_id), tournament_name = VALUES(tournament_name), court_id = VALUES(court_id), court_name = VALUES(court_name), date_time = VALUES(date_time), pair_a_id = VALUES(pair_a_id), pair_b_id = VALUES(pair_b_id), pair_a_name = VALUES(pair_a_name), pair_b_name = VALUES(pair_b_name), player_a1_id = VALUES(player_a1_id), player_a2_id = VALUES(player_a2_id), player_b1_id = VALUES(player_b1_id), player_b2_id = VALUES(player_b2_id), player_a1_name = VALUES(player_a1_name), player_a2_name = VALUES(player_a2_name), player_b1_name = VALUES(player_b1_name), player_b2_name = VALUES(player_b2_name), player_a1_avatar = VALUES(player_a1_avatar), player_a2_avatar = VALUES(player_a2_avatar), player_b1_avatar = VALUES(player_b1_avatar), player_b2_avatar = VALUES(player_b2_avatar), status = VALUES(status), sets = VALUES(sets), current_game = VALUES(current_game), current_set_index = VALUES(current_set_index), winner_pair_id = VALUES(winner_pair_id), winner_team = VALUES(winner_team), start_time_ms = VALUES(start_time_ms), elapsed_time_sec = VALUES(elapsed_time_sec), golden_point = VALUES(golden_point), sets_to_win = VALUES(sets_to_win), round_name = VALUES(round_name);

-- Audit Logs

INSERT INTO audit_logs (id, admin_name, admin_email, action, target, details, timestamp) VALUES ('audit_01', 'Carlos Gómez', 'carlos@padelpro.app', 'MODIFICACION_PARTIDO', 'Partido #match_live_01', 'Pista actualizada de Pista 2 a Pista Central por retransmisión televisiva', '2026-08-08 11:15:00') ON DUPLICATE KEY UPDATE id = VALUES(id), admin_name = VALUES(admin_name), admin_email = VALUES(admin_email), action = VALUES(action), target = VALUES(target), details = VALUES(details), timestamp = VALUES(timestamp);
INSERT INTO audit_logs (id, admin_name, admin_email, action, target, details, timestamp) VALUES ('audit_02', 'Carlos Gómez', 'carlos@padelpro.app', 'APROBACION_INSCRIPCION', 'Pareja Coello/Tapia', 'Inscripción confirmada para Premier Padel Major Madrid', '2026-08-08 10:00:00') ON DUPLICATE KEY UPDATE id = VALUES(id), admin_name = VALUES(admin_name), admin_email = VALUES(admin_email), action = VALUES(action), target = VALUES(target), details = VALUES(details), timestamp = VALUES(timestamp);
INSERT INTO audit_logs (id, admin_name, admin_email, action, target, details, timestamp) VALUES ('audit_03', 'Sistema Automático', 'system@padelpro.app', 'REGLAS_TORNEO', 'Copa Abierta Barcelona', 'Modo Punto de Oro activado para todos los partidos de fase de grupos', '2026-08-07 18:30:00') ON DUPLICATE KEY UPDATE id = VALUES(id), admin_name = VALUES(admin_name), admin_email = VALUES(admin_email), action = VALUES(action), target = VALUES(target), details = VALUES(details), timestamp = VALUES(timestamp);

-- Notifications

INSERT INTO notifications (id, title, body, timestamp, `read`, `type`, link_id) VALUES ('notif_1', '🔴 ¡Partido en Vivo Activo!', 'Gran Final: Galán / Lebrón vs Coello / Tapia se está disputando en Pista Central.', 'Hace 5 min', 0, 'MATCH', 'match_live_01') ON DUPLICATE KEY UPDATE id = VALUES(id), title = VALUES(title), body = VALUES(body), timestamp = VALUES(timestamp), `read` = VALUES(`read`), `type` = VALUES(`type`), link_id = VALUES(link_id);
INSERT INTO notifications (id, title, body, timestamp, `read`, `type`, link_id) VALUES ('notif_2', '🎾 Horario de tu próximo partido', 'Atención: Tu partido de Cuartos de Final se jugará hoy a las 18:30 h en Pista 2.', 'Hace 1 hora', 0, 'MATCH', 'match_upcoming_02') ON DUPLICATE KEY UPDATE id = VALUES(id), title = VALUES(title), body = VALUES(body), timestamp = VALUES(timestamp), `read` = VALUES(`read`), `type` = VALUES(`type`), link_id = VALUES(link_id);
INSERT INTO notifications (id, title, body, timestamp, `read`, `type`, link_id) VALUES ('notif_3', '🏆 Inscripciones Abiertas', 'Se ha abierto la inscripción para la Copa Abierta Barcelona 2026.', 'Ayer', 1, 'TOURNAMENT', 'tour_open_barcelona') ON DUPLICATE KEY UPDATE id = VALUES(id), title = VALUES(title), body = VALUES(body), timestamp = VALUES(timestamp), `read` = VALUES(`read`), `type` = VALUES(`type`), link_id = VALUES(link_id);

-- Gesture Configuration

INSERT INTO gesture_config (id, point_team_a_gesture, point_team_b_gesture, undo_gesture, cooldown_ms, min_confidence, required_hold_frames, detection_zone, mode) VALUES (1, 'ROCK', 'CALL', 'THUMB_DOWN', '500', '0.8', '15', '{"enabled":true,"x_min":0,"y_min":0,"x_max":640,"y_max":480}', 'ONE_HAND') ON DUPLICATE KEY UPDATE id = VALUES(id), point_team_a_gesture = VALUES(point_team_a_gesture), point_team_b_gesture = VALUES(point_team_b_gesture), undo_gesture = VALUES(undo_gesture), cooldown_ms = VALUES(cooldown_ms), min_confidence = VALUES(min_confidence), required_hold_frames = VALUES(required_hold_frames), detection_zone = VALUES(detection_zone), mode = VALUES(mode);

-- Users Auth (bcrypt hashed passwords)

INSERT INTO users_auth (id, email, hashed_password, role) VALUES ('usr_carlos_admin', 'admin@padelpro.app', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeY5XzL8x0e5wQ7K2', 'ADMIN') ON DUPLICATE KEY UPDATE id = VALUES(id), email = VALUES(email), hashed_password = VALUES(hashed_password), role = VALUES(role);

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- Seed completed successfully
-- ============================================================
