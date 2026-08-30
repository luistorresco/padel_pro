-- ============================================================
-- Padel Pro - MySQL Seed Script
-- Source: backend/mock_data.json
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------
-- Table: users
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `surname` VARCHAR(100) DEFAULT NULL,
  `username` VARCHAR(100) NOT NULL,
  `email` VARCHAR(255) DEFAULT NULL,
  `avatar` TEXT DEFAULT NULL,
  `account_type` ENUM('GUEST','USER') NOT NULL DEFAULT 'GUEST',
  `status` ENUM('ACTIVE','INACTIVE','BLOCKED') NOT NULL DEFAULT 'ACTIVE',
  `invited_by` VARCHAR(255) DEFAULT NULL,
  `invitation_code` VARCHAR(100) DEFAULT NULL,
  `converted_at` DATETIME DEFAULT NULL,
  `level` VARCHAR(50) DEFAULT NULL,
  `position` VARCHAR(50) DEFAULT NULL,
  `dominant_hand` ENUM('RIGHT','LEFT','BOTH') DEFAULT NULL,
  `points` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users_username` (`username`),
  UNIQUE KEY `uk_users_email` (`email`),
  UNIQUE KEY `uk_users_invitation_code` (`invitation_code`),
  INDEX `idx_users_invited_by` (`invited_by`),
  INDEX `idx_users_account_type` (`account_type`),
  INDEX `idx_users_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `users` (`id`, `name`, `surname`, `username`, `email`, `avatar`, `account_type`, `status`, `level`, `position`, `dominant_hand`, `points`) VALUES ('usr_carlos_admin', 'Carlos', 'Gómez', 'carlospadel', 'carlos@padelpro.app', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80', 'USER', 'ACTIVE', 'Avanzado', 'Revés (Izquierda)', 'RIGHT', '1520') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), surname = VALUES(surname), username = VALUES(username), email = VALUES(email), avatar = VALUES(avatar), level = VALUES(level), position = VALUES(position), dominant_hand = VALUES(dominant_hand), points = VALUES(points);
INSERT INTO `users` (`id`, `name`, `surname`, `username`, `email`, `avatar`, `account_type`, `status`, `level`, `position`, `dominant_hand`, `points`) VALUES ('usr_1787371091916', 'luis', 'torres', 'lucho', 'lucho@gmail.com', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', 'USER', 'ACTIVE', 'Intermedio', 'Drive (Derecha)', NULL, '0') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), surname = VALUES(surname), username = VALUES(username), email = VALUES(email), avatar = VALUES(avatar), level = VALUES(level), position = VALUES(position), dominant_hand = VALUES(dominant_hand), points = VALUES(points);

-- ------------------------------------------------------------
-- Table: users_auth
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `users_auth`;
CREATE TABLE IF NOT EXISTS `users_auth` (
  `user_id` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `hashed_password` VARCHAR(255) DEFAULT NULL,
  `last_login` DATETIME DEFAULT NULL,
  `email_verified_at` DATETIME DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `uk_users_auth_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `users_auth` (`user_id`, `email`, `hashed_password`) VALUES ('usr_carlos_admin', 'admin@padelpro.app', '$2b$12$8Z0bgAQi.WEuwZ5bJ4wqfuqElKuyofx4/WupEitolw9w2hodwxXQS') ON DUPLICATE KEY UPDATE user_id = VALUES(user_id), email = VALUES(email), hashed_password = VALUES(hashed_password);

-- ------------------------------------------------------------
-- Table: roles
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `description` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_roles_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `roles` (`name`, `description`) VALUES ('USER', 'Usuario normal de la aplicación'), ('BUSINESS_ADMIN', 'Administrador de un negocio'), ('BUSINESS_MANAGER', 'Administrador o manager de un negocio'), ('SUPER_ADMIN', 'Administrador general de la plataforma') ON DUPLICATE KEY UPDATE name = VALUES(name);

-- ------------------------------------------------------------
-- Table: user_roles
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `user_roles`;
CREATE TABLE IF NOT EXISTS `user_roles` (
  `user_id` VARCHAR(255) NOT NULL,
  `role_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `role_id`),
  INDEX `idx_user_roles_role` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES ('usr_carlos_admin', (SELECT id FROM roles WHERE name = 'ADMIN')) ON DUPLICATE KEY UPDATE user_id = VALUES(user_id), role_id = VALUES(role_id);

-- ------------------------------------------------------------
-- Table: pairs
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `pairs`;
CREATE TABLE IF NOT EXISTS `pairs` (
  `id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(150) DEFAULT NULL,
  `player1_id` VARCHAR(255) NOT NULL,
  `player2_id` VARCHAR(255) NOT NULL,
  `created_by` VARCHAR(255) NOT NULL,
  `status` ENUM('ACTIVE','INACTIVE') NOT NULL DEFAULT 'ACTIVE',
  `tournaments_disputed` INT NOT NULL DEFAULT 0,
  `titles_won` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `idx_pairs_player1` (`player1_id`),
  INDEX `idx_pairs_player2` (`player2_id`),
  INDEX `idx_pairs_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `pairs` (`id`, `name`, `player1_id`, `player2_id`, `created_by`, `status`, `tournaments_disputed`, `titles_won`) VALUES ('pair_galan_lebron', 'Galán / Lebrón', 'usr_ale_galan', 'usr_juan_lebron', 'usr_ale_galan', 'ACTIVE', '12', '7') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id), created_by = VALUES(created_by), status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won);
INSERT INTO `pairs` (`id`, `name`, `player1_id`, `player2_id`, `created_by`, `status`, `tournaments_disputed`, `titles_won`) VALUES ('pair_coello_tapia', 'Coello / Tapia', 'usr_arturo_coello', 'usr_agustin_tapia', 'usr_arturo_coello', 'ACTIVE', '10', '5') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id), created_by = VALUES(created_by), status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won);
INSERT INTO `pairs` (`id`, `name`, `player1_id`, `player2_id`, `created_by`, `status`, `tournaments_disputed`, `titles_won`) VALUES ('pair_chingotto_navarro', 'Chingotto / Navarro', 'usr_chingotto', 'usr_paquito', 'usr_chingotto', 'ACTIVE', '8', '2') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id), created_by = VALUES(created_by), status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won);
INSERT INTO `pairs` (`id`, `name`, `player1_id`, `player2_id`, `created_by`, `status`, `tournaments_disputed`, `titles_won`) VALUES ('pair_stupaczuk_dinenno', 'Stupaczuk / Di Nenno', 'usr_stupa', 'usr_dinenno', 'usr_stupa', 'ACTIVE', '9', '3') ON DUPLICATE KEY UPDATE id = VALUES(id), name = VALUES(name), player1_id = VALUES(player1_id), player2_id = VALUES(player2_id), created_by = VALUES(created_by), status = VALUES(status), tournaments_disputed = VALUES(tournaments_disputed), titles_won = VALUES(titles_won);

-- ------------------------------------------------------------
-- Table: courts
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `courts`;
CREATE TABLE IF NOT EXISTS `courts` (
  `id` VARCHAR(255) NOT NULL,
  `business_id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(150) NOT NULL,
  `location` TEXT DEFAULT NULL,
  `number` INT DEFAULT NULL,
  `status` ENUM('AVAILABLE','OCCUPIED','MAINTENANCE','INACTIVE') NOT NULL DEFAULT 'AVAILABLE',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `idx_courts_business` (`business_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `courts` (`id`, `business_id`, `name`, `location`, `number`, `status`) VALUES ('crt_central', 'biz_default', 'Pista Central (Estadio)', 'Club Central', '1', 'OCCUPIED') ON DUPLICATE KEY UPDATE id = VALUES(id), business_id = VALUES(business_id), name = VALUES(name), location = VALUES(location), number = VALUES(number), status = VALUES(status);
INSERT INTO `courts` (`id`, `business_id`, `name`, `location`, `number`, `status`) VALUES ('crt_2', 'biz_default', 'Pista 2 Panorámica', 'Club Central', '2', 'AVAILABLE') ON DUPLICATE KEY UPDATE id = VALUES(id), business_id = VALUES(business_id), name = VALUES(name), location = VALUES(location), number = VALUES(number), status = VALUES(status);
INSERT INTO `courts` (`id`, `business_id`, `name`, `location`, `number`, `status`) VALUES ('crt_3', 'biz_default', 'Pista 3 Cristal Norte', 'Anexo Norte', '3', 'AVAILABLE') ON DUPLICATE KEY UPDATE id = VALUES(id), business_id = VALUES(business_id), name = VALUES(name), location = VALUES(location), number = VALUES(number), status = VALUES(status);
INSERT INTO `courts` (`id`, `business_id`, `name`, `location`, `number`, `status`) VALUES ('crt_4', 'biz_default', 'Pista 4 Cubierta', 'Anexo Sur', '4', 'AVAILABLE') ON DUPLICATE KEY UPDATE id = VALUES(id), business_id = VALUES(business_id), name = VALUES(name), location = VALUES(location), number = VALUES(number), status = VALUES(status);

-- ------------------------------------------------------------
-- Table: tournaments
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `tournaments`;
CREATE TABLE IF NOT EXISTS `tournaments` (
  `id` VARCHAR(255) NOT NULL,
  `business_id` VARCHAR(255) DEFAULT NULL,
  `created_by` VARCHAR(255) NOT NULL,
  `name` VARCHAR(200) NOT NULL,
  `logo` TEXT DEFAULT NULL,
  `description` TEXT DEFAULT NULL,
  `category` VARCHAR(100) DEFAULT NULL,
  `level` VARCHAR(100) DEFAULT NULL,
  `location` TEXT DEFAULT NULL,
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME DEFAULT NULL,
  `format` VARCHAR(100) DEFAULT NULL,
  `max_pairs` INT DEFAULT NULL,
  `status` ENUM('DRAFT','OPEN','IN_PROGRESS','FINISHED','CANCELLED') NOT NULL DEFAULT 'DRAFT',
  `visibility` ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PRIVATE',
  `rules` JSON DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_tournaments_business` (`business_id`),
  INDEX `idx_tournaments_created_by` (`created_by`),
  INDEX `idx_tournaments_status` (`status`),
  INDEX `idx_tournaments_visibility` (`visibility`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `tournaments` (`id`, `business_id`, `created_by`, `name`, `logo`, `description`, `category`, `level`, `location`, `start_date`, `end_date`, `status`, `format`, `max_pairs`, `visibility`, `rules`) VALUES ('tour_major_madrid', 'biz_default', 'usr_carlos_admin', 'Premier Padel Major Madrid 2026', '🏆', 'El torneo oficial más prestigioso de la temporada con las mejores 16 parejas del circuito.', 'Masculino', 'Profesional', 'Wizink Center, Madrid', '2026-08-10', '2026-08-16', 'IN_PROGRESS', 'Grupos + eliminación directa', '16', 'PRIVATE', '{"sets_to_win": 2, "golden_point": true, "tie_break_at": 6, "final_set_tie_break": true, "points_distribution": {"champion": 1000, "runner_up": 600, "semi_finals": 360, "quarter_finals": 180, "group_stage": 90}}') ON DUPLICATE KEY UPDATE id = VALUES(id), business_id = VALUES(business_id), created_by = VALUES(created_by), name = VALUES(name), logo = VALUES(logo), description = VALUES(description), category = VALUES(category), level = VALUES(level), location = VALUES(location), start_date = VALUES(start_date), end_date = VALUES(end_date), status = VALUES(status), format = VALUES(format), max_pairs = VALUES(max_pairs), visibility = VALUES(visibility), rules = VALUES(rules);
INSERT INTO `tournaments` (`id`, `business_id`, `created_by`, `name`, `logo`, `description`, `category`, `level`, `location`, `start_date`, `end_date`, `status`, `format`, `max_pairs`, `visibility`, `rules`) VALUES ('tour_open_barcelona', 'biz_default', 'usr_carlos_admin', 'Copa Abierta Barcelona 2026', '🎾', 'Competición de categoría Mixto Abierto con fases de grupos intensas y eliminatorias.', 'Mixto', 'Avanzado', 'Real Club de Tenis Barcelona', '2026-09-01', '2026-09-05', 'OPEN', 'Fase de grupos', '12', 'PRIVATE', '{"sets_to_win": 2, "golden_point": true, "tie_break_at": 6, "final_set_tie_break": true, "points_distribution": {"champion": 500, "runner_up": 300, "semi_finals": 180, "quarter_finals": 90, "group_stage": 45}}') ON DUPLICATE KEY UPDATE id = VALUES(id), business_id = VALUES(business_id), created_by = VALUES(created_by), name = VALUES(name), logo = VALUES(logo), description = VALUES(description), category = VALUES(category), level = VALUES(level), location = VALUES(location), start_date = VALUES(start_date), end_date = VALUES(end_date), status = VALUES(status), format = VALUES(format), max_pairs = VALUES(max_pairs), visibility = VALUES(visibility), rules = VALUES(rules);
INSERT INTO `tournaments` (`id`, `business_id`, `created_by`, `name`, `logo`, `description`, `category`, `level`, `location`, `start_date`, `end_date`, `status`, `format`, `max_pairs`, `visibility`, `rules`) VALUES ('tour_nocturno_sevilla', 'biz_default', 'usr_carlos_admin', 'Torneo Nocturno Sevilla', '🌙', 'Edición nocturna exprés en formato Eliminación Directa.', 'Masculino', 'Principiante', 'Padel Club Sevilla', '2026-09-20', '2026-09-22', 'DRAFT', 'Eliminación directa', '8', 'PRIVATE', '{"sets_to_win": 2, "golden_point": false, "tie_break_at": 6, "final_set_tie_break": true, "points_distribution": {"champion": 250, "runner_up": 150, "semi_finals": 90, "quarter_finals": 45, "group_stage": 20}}') ON DUPLICATE KEY UPDATE id = VALUES(id), business_id = VALUES(business_id), created_by = VALUES(created_by), name = VALUES(name), logo = VALUES(logo), description = VALUES(description), category = VALUES(category), level = VALUES(level), location = VALUES(location), start_date = VALUES(start_date), end_date = VALUES(end_date), status = VALUES(status), format = VALUES(format), max_pairs = VALUES(max_pairs), visibility = VALUES(visibility), rules = VALUES(rules);

-- ------------------------------------------------------------
-- Table: matches
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `matches`;
CREATE TABLE IF NOT EXISTS `matches` (
  `id` VARCHAR(255) NOT NULL,
  `tournament_id` VARCHAR(255) DEFAULT NULL,
  `round_id` VARCHAR(255) DEFAULT NULL,
  `business_id` VARCHAR(255) DEFAULT NULL,
  `court_id` VARCHAR(255) DEFAULT NULL,
  `created_by` VARCHAR(255) NOT NULL,
  `pair_a_id` VARCHAR(255) DEFAULT NULL,
  `pair_b_id` VARCHAR(255) DEFAULT NULL,
  `date_time` DATETIME DEFAULT NULL,
  `status` ENUM('SCHEDULED','IN_PROGRESS','FINISHED','CANCELLED') NOT NULL DEFAULT 'SCHEDULED',
  `visibility` ENUM('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PRIVATE',
  `sets` JSON DEFAULT NULL,
  `current_set_index` INT NOT NULL DEFAULT 0,
  `winner_pair_id` VARCHAR(255) DEFAULT NULL,
  `winner_team` ENUM('A','B') DEFAULT NULL,
  `start_time_ms` BIGINT DEFAULT NULL,
  `elapsed_time_sec` INT NOT NULL DEFAULT 0,
  `golden_point` TINYINT(1) NOT NULL DEFAULT 0,
  `sets_to_win` INT NOT NULL DEFAULT 2,
  `round_name` VARCHAR(100) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_matches_tournament` (`tournament_id`),
  INDEX `idx_matches_round` (`round_id`),
  INDEX `idx_matches_business` (`business_id`),
  INDEX `idx_matches_court` (`court_id`),
  INDEX `idx_matches_created_by` (`created_by`),
  INDEX `idx_matches_pair_a` (`pair_a_id`),
  INDEX `idx_matches_pair_b` (`pair_b_id`),
  INDEX `idx_matches_winner_pair` (`winner_pair_id`),
  INDEX `idx_matches_status` (`status`),
  INDEX `idx_matches_date_time` (`date_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `matches` (`id`, `tournament_id`, `court_id`, `date_time`, `pair_a_id`, `pair_b_id`, `status`, `sets`, `current_set_index`, `winner_pair_id`, `winner_team`, `start_time_ms`, `elapsed_time_sec`, `golden_point`, `sets_to_win`, `round_name`, `created_by`) VALUES ('match_live_01', 'tour_major_madrid', 'crt_central', '2026-08-08 11:30', 'pair_galan_lebron', 'pair_coello_tapia', 'IN_PROGRESS', '[{"team_a_games": 6, "team_b_games": 4, "is_tie_break": false, "winner": "A"}, {"team_a_games": 3, "team_b_games": 6, "is_tie_break": false, "winner": "B"}, {"team_a_games": 3, "team_b_games": 2, "is_tie_break": false}]', '2', NULL, NULL, NULL, '5240', '1', '2', 'Gran Final', 'usr_carlos_admin') ON DUPLICATE KEY UPDATE id = VALUES(id), tournament_id = VALUES(tournament_id), court_id = VALUES(court_id), date_time = VALUES(date_time), pair_a_id = VALUES(pair_a_id), pair_b_id = VALUES(pair_b_id), status = VALUES(status), sets = VALUES(sets), current_set_index = VALUES(current_set_index), winner_pair_id = VALUES(winner_pair_id), winner_team = VALUES(winner_team), start_time_ms = VALUES(start_time_ms), elapsed_time_sec = VALUES(elapsed_time_sec), golden_point = VALUES(golden_point), sets_to_win = VALUES(sets_to_win), round_name = VALUES(round_name), created_by = VALUES(created_by);
INSERT INTO `matches` (`id`, `tournament_id`, `court_id`, `date_time`, `pair_a_id`, `pair_b_id`, `status`, `sets`, `current_set_index`, `winner_pair_id`, `winner_team`, `start_time_ms`, `elapsed_time_sec`, `golden_point`, `sets_to_win`, `round_name`, `created_by`) VALUES ('match_upcoming_02', 'tour_major_madrid', 'crt_2', '2026-08-08 18:30', 'pair_chingotto_navarro', 'pair_stupaczuk_dinenno', 'SCHEDULED', '[{"team_a_games": 0, "team_b_games": 0, "is_tie_break": false, "tie_break_points": {"team_a": 0, "team_b": 0}}]', '0', NULL, NULL, NULL, '0', '1', '2', 'Cuartos de Final', 'usr_carlos_admin') ON DUPLICATE KEY UPDATE id = VALUES(id), tournament_id = VALUES(tournament_id), court_id = VALUES(court_id), date_time = VALUES(date_time), pair_a_id = VALUES(pair_a_id), pair_b_id = VALUES(pair_b_id), status = VALUES(status), sets = VALUES(sets), current_set_index = VALUES(current_set_index), winner_pair_id = VALUES(winner_pair_id), winner_team = VALUES(winner_team), start_time_ms = VALUES(start_time_ms), elapsed_time_sec = VALUES(elapsed_time_sec), golden_point = VALUES(golden_point), sets_to_win = VALUES(sets_to_win), round_name = VALUES(round_name), created_by = VALUES(created_by);

-- ------------------------------------------------------------
-- Table: match_events
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `match_events`;
CREATE TABLE IF NOT EXISTS `match_events` (
  `id` VARCHAR(255) NOT NULL,
  `match_id` VARCHAR(255) NOT NULL,
  `set_number` INT NOT NULL,
  `game_number` INT DEFAULT NULL,
  `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `winning_pair_id` VARCHAR(255) DEFAULT NULL,
  `player_id` VARCHAR(255) DEFAULT NULL,
  `event_type` VARCHAR(100) NOT NULL,
  `description` TEXT DEFAULT NULL,
  `score_snapshot` JSON DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `idx_match_events_match` (`match_id`),
  INDEX `idx_match_events_player` (`player_id`),
  INDEX `idx_match_events_pair` (`winning_pair_id`),
  INDEX `idx_match_events_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Table: gesture_config
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `gesture_config`;
CREATE TABLE IF NOT EXISTS `gesture_config` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `business_id` VARCHAR(255) NOT NULL,
  `point_team_a_gesture` TEXT DEFAULT NULL,
  `point_team_b_gesture` TEXT DEFAULT NULL,
  `undo_gesture` TEXT DEFAULT NULL,
  `cooldown_ms` INT NOT NULL DEFAULT 1000,
  `min_confidence` DOUBLE NOT NULL DEFAULT 0.80,
  `required_hold_frames` INT NOT NULL DEFAULT 10,
  `detection_zone` TEXT DEFAULT NULL,
  `mode` TEXT DEFAULT NULL,
  `pause_timer_gesture` TEXT DEFAULT NULL,
  `resume_timer_gesture` TEXT DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_gesture_business` (`business_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `gesture_config` (`business_id`, `point_team_a_gesture`, `point_team_b_gesture`, `undo_gesture`, `cooldown_ms`, `min_confidence`, `required_hold_frames`, `detection_zone`, `mode`, `pause_timer_gesture`, `resume_timer_gesture`) VALUES ('biz_default', 'OPEN_PALM', 'FIST', 'THUMB_DOWN', '500', '0.8', '15', '{"enabled": true, "x_min": 0, "y_min": 0, "x_max": 640, "y_max": 480}', 'ONE_HAND', 'HORIZONTAL_PALM', 'THUMB_UP') ON DUPLICATE KEY UPDATE business_id = VALUES(business_id), point_team_a_gesture = VALUES(point_team_a_gesture), point_team_b_gesture = VALUES(point_team_b_gesture), undo_gesture = VALUES(undo_gesture), cooldown_ms = VALUES(cooldown_ms), min_confidence = VALUES(min_confidence), required_hold_frames = VALUES(required_hold_frames), detection_zone = VALUES(detection_zone), mode = VALUES(mode), pause_timer_gesture = VALUES(pause_timer_gesture), resume_timer_gesture = VALUES(resume_timer_gesture);

-- ------------------------------------------------------------
-- Table: notifications
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE IF NOT EXISTS `notifications` (
  `id` VARCHAR(255) NOT NULL,
  `user_id` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `body` TEXT DEFAULT NULL,
  `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `read_status` TINYINT(1) NOT NULL DEFAULT 0,
  `type` VARCHAR(100) DEFAULT NULL,
  `link_id` VARCHAR(255) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `idx_notifications_user` (`user_id`),
  INDEX `idx_notifications_read` (`read_status`),
  INDEX `idx_notifications_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `notifications` (`id`, `user_id`, `title`, `body`, `timestamp`, `read_status`, `type`, `link_id`) VALUES ('notif_1', 'usr_carlos_admin', '🔴 ¡Partido en Vivo Activo!', 'Gran Final: Galán / Lebrón vs Coello / Tapia se está disputando en Pista Central.', 'Hace 5 min', '0', 'MATCH', 'match_live_01') ON DUPLICATE KEY UPDATE id = VALUES(id), user_id = VALUES(user_id), title = VALUES(title), body = VALUES(body), timestamp = VALUES(timestamp), read_status = VALUES(read_status), type = VALUES(type), link_id = VALUES(link_id);
INSERT INTO `notifications` (`id`, `user_id`, `title`, `body`, `timestamp`, `read_status`, `type`, `link_id`) VALUES ('notif_2', 'usr_carlos_admin', '🎾 Horario de tu próximo partido', 'Atención: Tu partido de Cuartos de Final se jugará hoy a las 18:30 h en Pista 2.', 'Hace 1 hora', '0', 'MATCH', 'match_upcoming_02') ON DUPLICATE KEY UPDATE id = VALUES(id), user_id = VALUES(user_id), title = VALUES(title), body = VALUES(body), timestamp = VALUES(timestamp), read_status = VALUES(read_status), type = VALUES(type), link_id = VALUES(link_id);
INSERT INTO `notifications` (`id`, `user_id`, `title`, `body`, `timestamp`, `read_status`, `type`, `link_id`) VALUES ('notif_3', 'usr_carlos_admin', '🏆 Inscripciones Abiertas', 'Se ha abierto la inscripción para la Copa Abierta Barcelona 2026.', 'Ayer', '1', 'TOURNAMENT', 'tour_open_barcelona') ON DUPLICATE KEY UPDATE id = VALUES(id), user_id = VALUES(user_id), title = VALUES(title), body = VALUES(body), timestamp = VALUES(timestamp), read_status = VALUES(read_status), type = VALUES(type), link_id = VALUES(link_id);

-- ------------------------------------------------------------
-- Table: audit_logs
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE IF NOT EXISTS `audit_logs` (
  `id` VARCHAR(255) NOT NULL,
  `business_id` VARCHAR(255) DEFAULT NULL,
  `user_id` VARCHAR(255) DEFAULT NULL,
  `action` VARCHAR(100) NOT NULL,
  `target_type` VARCHAR(100) NOT NULL,
  `target_id` VARCHAR(255) NOT NULL,
  `details` JSON DEFAULT NULL,
  `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `idx_audit_business` (`business_id`),
  INDEX `idx_audit_user` (`user_id`),
  INDEX `idx_audit_target` (`target_type`, `target_id`),
  INDEX `idx_audit_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `audit_logs` (`id`, `action`, `target_type`, `target_id`, `details`, `timestamp`) VALUES ('audit_01', 'MODIFICACION_PARTIDO', 'match', 'match_live_01', 'Pista actualizada de Pista 2 a Pista Central por retransmisión televisiva', '2026-08-08 11:15:00') ON DUPLICATE KEY UPDATE id = VALUES(id), action = VALUES(action), target_type = VALUES(target_type), target_id = VALUES(target_id), details = VALUES(details), timestamp = VALUES(timestamp);
INSERT INTO `audit_logs` (`id`, `action`, `target_type`, `target_id`, `details`, `timestamp`) VALUES ('audit_02', 'APROBACION_INSCRIPCION', 'pair', 'pair_coello_tapia', 'Inscripción confirmada para Premier Padel Major Madrid', '2026-08-08 10:00:00') ON DUPLICATE KEY UPDATE id = VALUES(id), action = VALUES(action), target_type = VALUES(target_type), target_id = VALUES(target_id), details = VALUES(details), timestamp = VALUES(timestamp);
INSERT INTO `audit_logs` (`id`, `action`, `target_type`, `target_id`, `details`, `timestamp`) VALUES ('audit_03', 'REGLAS_TORNEO', 'tournament', 'tour_open_barcelona', 'Modo Punto de Oro activado para todos los partidos de fase de grupos', '2026-08-07 18:30:00') ON DUPLICATE KEY UPDATE id = VALUES(id), action = VALUES(action), target_type = VALUES(target_type), target_id = VALUES(target_id), details = VALUES(details), timestamp = VALUES(timestamp);

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- Seed completed successfully
-- ============================================================
