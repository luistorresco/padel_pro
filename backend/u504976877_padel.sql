-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 30-08-2026 a las 19:56:55
-- Versión del servidor: 11.8.8-MariaDB-log
-- Versión de PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `u504976877_padel`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `audit_logs`
--

CREATE TABLE `audit_logs` (
  `id` varchar(255) NOT NULL,
  `admin_name` text NOT NULL,
  `admin_email` text NOT NULL,
  `action` text NOT NULL,
  `target` text NOT NULL,
  `details` text DEFAULT NULL,
  `timestamp` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `audit_logs`
--

INSERT INTO `audit_logs` (`id`, `admin_name`, `admin_email`, `action`, `target`, `details`, `timestamp`) VALUES
('audit_01', 'Carlos Gómez', 'carlos@padelpro.app', 'MODIFICACION_PARTIDO', 'Partido #match_live_01', 'Pista actualizada de Pista 2 a Pista Central por retransmisión televisiva', '2026-08-08 11:15:00'),
('audit_02', 'Carlos Gómez', 'carlos@padelpro.app', 'APROBACION_INSCRIPCION', 'Pareja Coello/Tapia', 'Inscripción confirmada para Premier Padel Major Madrid', '2026-08-08 10:00:00'),
('audit_03', 'Sistema Automático', 'system@padelpro.app', 'REGLAS_TORNEO', 'Copa Abierta Barcelona', 'Modo Punto de Oro activado para todos los partidos de fase de grupos', '2026-08-07 18:30:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `businesses`
--

CREATE TABLE `businesses` (
  `id` varchar(255) NOT NULL,
  `name` varchar(200) NOT NULL,
  `logo` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `location` text DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_by` varchar(255) NOT NULL,
  `status` enum('ACTIVE','INACTIVE') NOT NULL DEFAULT 'ACTIVE',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `business_users`
--

CREATE TABLE `business_users` (
  `business_id` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `role` enum('OWNER','ADMIN','MANAGER') NOT NULL DEFAULT 'MANAGER',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `courts`
--

CREATE TABLE `courts` (
  `id` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `location` text NOT NULL,
  `number` int(11) NOT NULL,
  `status` text NOT NULL,
  `current_match_id` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `courts`
--

INSERT INTO `courts` (`id`, `name`, `location`, `number`, `status`, `current_match_id`) VALUES
('crt_2', 'Pista 2 Panorámica', 'Club Central', 2, 'AVAILABLE', NULL),
('crt_3', 'Pista 3 Cristal Norte', 'Anexo Norte', 3, 'AVAILABLE', NULL),
('crt_4', 'Pista 4 Cubierta', 'Anexo Sur', 4, 'AVAILABLE', NULL),
('crt_central', 'Pista Central (Estadio)', 'Club Central', 1, 'OCCUPIED', 'match_live_01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gesture_config`
--

CREATE TABLE `gesture_config` (
  `id` int(11) NOT NULL CHECK (`id` = 1),
  `point_team_a_gesture` text NOT NULL,
  `point_team_b_gesture` text NOT NULL,
  `undo_gesture` text NOT NULL,
  `cooldown_ms` int(11) NOT NULL,
  `min_confidence` double NOT NULL,
  `required_hold_frames` int(11) NOT NULL,
  `detection_zone` text DEFAULT NULL,
  `mode` text NOT NULL,
  `pause_timer_gesture` text NOT NULL DEFAULT '',
  `resume_timer_gesture` text NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `gesture_config`
--

INSERT INTO `gesture_config` (`id`, `point_team_a_gesture`, `point_team_b_gesture`, `undo_gesture`, `cooldown_ms`, `min_confidence`, `required_hold_frames`, `detection_zone`, `mode`, `pause_timer_gesture`, `resume_timer_gesture`) VALUES
(1, 'ROCK', 'CALL', 'THUMB_DOWN', 500, 0.8, 15, '{\"enabled\": true, \"x_min\": 0, \"y_min\": 0, \"x_max\": 640, \"y_max\": 480}', 'ONE_HAND', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matches`
--

CREATE TABLE `matches` (
  `id` varchar(255) NOT NULL,
  `tournament_id` text DEFAULT NULL,
  `tournament_name` text DEFAULT NULL,
  `court_id` text DEFAULT NULL,
  `court_name` text NOT NULL,
  `date_time` text NOT NULL,
  `pair_a_id` text NOT NULL,
  `pair_b_id` text NOT NULL,
  `pair_a_name` text NOT NULL,
  `pair_b_name` text NOT NULL,
  `player_a1_id` text NOT NULL,
  `player_a2_id` text NOT NULL,
  `player_b1_id` text NOT NULL,
  `player_b2_id` text NOT NULL,
  `player_a1_name` text NOT NULL,
  `player_a2_name` text NOT NULL,
  `player_b1_name` text NOT NULL,
  `player_b2_name` text NOT NULL,
  `player_a1_avatar` text DEFAULT NULL,
  `player_a2_avatar` text DEFAULT NULL,
  `player_b1_avatar` text DEFAULT NULL,
  `player_b2_avatar` text DEFAULT NULL,
  `status` text NOT NULL,
  `sets` text DEFAULT NULL,
  `current_game` text DEFAULT NULL,
  `current_set_index` int(11) DEFAULT NULL,
  `winner_pair_id` text DEFAULT NULL,
  `winner_team` text DEFAULT NULL,
  `start_time_ms` int(11) DEFAULT NULL,
  `elapsed_time_sec` int(11) NOT NULL,
  `golden_point` int(11) NOT NULL,
  `sets_to_win` int(11) NOT NULL,
  `round_name` text DEFAULT NULL,
  `round_id` varchar(255) DEFAULT NULL,
  `business_id` varchar(255) DEFAULT NULL,
  `visibility` enum('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PRIVATE',
  `deleted_at` datetime DEFAULT NULL,
  `created_by` varchar(255) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `matches`
--

INSERT INTO `matches` (`id`, `tournament_id`, `tournament_name`, `court_id`, `court_name`, `date_time`, `pair_a_id`, `pair_b_id`, `pair_a_name`, `pair_b_name`, `player_a1_id`, `player_a2_id`, `player_b1_id`, `player_b2_id`, `player_a1_name`, `player_a2_name`, `player_b1_name`, `player_b2_name`, `player_a1_avatar`, `player_a2_avatar`, `player_b1_avatar`, `player_b2_avatar`, `status`, `sets`, `current_game`, `current_set_index`, `winner_pair_id`, `winner_team`, `start_time_ms`, `elapsed_time_sec`, `golden_point`, `sets_to_win`, `round_name`, `round_id`, `business_id`, `visibility`, `deleted_at`, `created_by`) VALUES
('match_1787717933638', NULL, NULL, 'crt_2', 'Pista 2 Panorámica', '2026-08-25T23:18', 'pair_1787699331943', 'pair_1787699340031', 'ochoa / jimenez', 'torres / lopez', '', '', '', '', '', '', '', '', NULL, NULL, NULL, NULL, 'FINISHED', '[{\"teamAGames\": 4, \"teamBGames\": 6, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"B\"}, {\"teamAGames\": 6, \"teamBGames\": 0, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"A\"}, {\"teamAGames\": 6, \"teamBGames\": 0, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"A\"}]', '{\"teamAPoints\": \"0\", \"teamBPoints\": \"0\", \"serverTeam\": \"A\", \"isDeuce\": false}', 2, 'pair_1787699331943', NULL, NULL, 0, 0, 2, NULL, NULL, NULL, 'PRIVATE', NULL, ''),
('match_1787720688776', NULL, NULL, 'crt_2', 'Pista 2 Panorámica', '2026-08-26T00:04', 'pair_1787699331943', 'pair_1787699340031', 'ochoa / jimenez', 'torres / lopez', '', '', '', '', '', '', '', '', NULL, NULL, NULL, NULL, 'FINISHED', '[{\"teamAGames\": 6, \"teamBGames\": 2, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"A\"}, {\"teamAGames\": 6, \"teamBGames\": 0, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"A\"}]', '{\"teamAPoints\": \"0\", \"teamBPoints\": \"0\", \"serverTeam\": \"A\", \"isDeuce\": false}', 1, 'pair_1787699331943', NULL, NULL, 29, 0, 2, NULL, NULL, NULL, 'PRIVATE', NULL, ''),
('match_1787723625046', NULL, NULL, 'crt_4', 'Pista 4 Cubierta', '2026-08-26T00:53', 'pair_1787699331943', 'pair_1787699340031', 'ochoa / jimenez', 'torres / lopez', '', '', '', '', '', '', '', '', NULL, NULL, NULL, NULL, 'FINISHED', '[{\"teamAGames\": 6, \"teamBGames\": 0, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"A\"}, {\"teamAGames\": 6, \"teamBGames\": 0, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"A\"}]', '{\"teamAPoints\": \"0\", \"teamBPoints\": \"0\", \"serverTeam\": \"A\", \"isDeuce\": false}', 1, 'pair_1787699331943', NULL, NULL, 14, 0, 2, NULL, NULL, NULL, 'PRIVATE', NULL, ''),
('match_1787750047902', NULL, NULL, 'crt_3', 'Pista 3 Cristal Norte', '2026-08-26T08:14', 'pair_1787699331943', 'pair_1787699340031', 'ochoa / jimenez', 'torres / lopez', '', '', '', '', '', '', '', '', NULL, NULL, NULL, NULL, 'FINISHED', '[{\"teamAGames\": 6, \"teamBGames\": 0, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"A\"}, {\"teamAGames\": 0, \"teamBGames\": 6, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"B\"}, {\"teamAGames\": 0, \"teamBGames\": 6, \"isTieBreak\": false, \"tieBreakPoints\": {\"teamA\": 0, \"teamB\": 0}, \"winner\": \"B\"}]', '{\"teamAPoints\": \"0\", \"teamBPoints\": \"0\", \"serverTeam\": \"A\", \"isDeuce\": false}', 2, 'pair_1787699340031', NULL, NULL, 0, 0, 2, NULL, NULL, NULL, 'PRIVATE', NULL, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `match_events`
--

CREATE TABLE `match_events` (
  `id` varchar(255) NOT NULL,
  `match_id` text NOT NULL,
  `set_number` int(11) NOT NULL,
  `game_number` int(11) NOT NULL,
  `timestamp` text NOT NULL,
  `winning_pair_id` text NOT NULL,
  `player_id` text DEFAULT NULL,
  `player_name` text DEFAULT NULL,
  `event_type` text NOT NULL,
  `description` text DEFAULT NULL,
  `score_snapshot` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `match_events`
--

INSERT INTO `match_events` (`id`, `match_id`, `set_number`, `game_number`, `timestamp`, `winning_pair_id`, `player_id`, `player_name`, `event_type`, `description`, `score_snapshot`) VALUES
('evt_1787699993818_ad09g', 'match_live_01', 0, 0, '06:19:53 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787699997140_ze6r7', 'match_live_01', 0, 0, '06:19:57 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 15-15]'),
('evt_1787700656712_2sv8z', 'match_live_01', 0, 0, '06:30:56 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787700710093_j5rz9', 'match_live_01', 0, 0, '06:31:50 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787700870087_qx018', 'match_live_01', 0, 0, '06:34:30 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787700886353_67ufc', 'match_live_01', 0, 0, '06:34:46 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 [Pts: 30-0]'),
('evt_1787700904832_udmvf', 'match_live_01', 0, 0, '06:35:04 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787700922172_giy9l', 'match_live_01', 0, 0, '06:35:22 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 [Pts: 40-15]'),
('evt_1787700969873_vgt92', 'match_live_01', 0, 0, '06:36:09 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 [Pts: 40-15]'),
('evt_1787700995640_9fthq', 'match_live_01', 0, 0, '06:36:35 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 [Pts: 40-30]'),
('evt_1787701015687_aw7vp', 'match_live_01', 0, 0, '06:36:55 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 1-0 [Pts: 0-0]'),
('evt_1787701050173_39dks', 'match_live_01', 0, 0, '06:37:30 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 1-0 [Pts: 15-0]'),
('evt_1787701066024_xnper', 'match_live_01', 0, 0, '06:37:46 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 1-0 [Pts: 30-0]'),
('evt_1787701087577_wjsh3', 'match_live_01', 0, 0, '06:38:07 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 1-0 [Pts: 40-0]'),
('evt_1787701114361_xtu7w', 'match_live_01', 0, 0, '06:38:34 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 [Pts: 0-0]'),
('evt_1787701142964_9brzu', 'match_live_01', 0, 0, '06:39:02 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 [Pts: 0-15]'),
('evt_1787701156879_5ljqy', 'match_live_01', 0, 0, '06:39:16 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 [Pts: 15-15]'),
('evt_1787701169666_1les2', 'match_live_01', 0, 0, '06:39:29 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 [Pts: 30-15]'),
('evt_1787701211848_4t0rn', 'match_live_01', 0, 0, '06:40:11 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 [Pts: 30-30]'),
('evt_1787701239339_c412j', 'match_live_01', 0, 0, '06:40:39 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 [Pts: 30-40]'),
('evt_1787701263661_ysqk3', 'match_live_01', 0, 0, '06:41:03 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: 0-0]'),
('evt_1787701305959_rtips', 'match_live_01', 0, 0, '06:41:45 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: 15-0]'),
('evt_1787701320193_jbhks', 'match_live_01', 0, 0, '06:42:00 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: 30-0]'),
('evt_1787701337792_icchv', 'match_live_01', 0, 0, '06:42:17 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: 30-15]'),
('evt_1787701385159_1c9ih', 'match_live_01', 0, 0, '06:43:05 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: 30-30]'),
('evt_1787701410527_po0d6', 'match_live_01', 0, 0, '06:43:30 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: 30-30]'),
('evt_1787701412806_ihohp', 'match_live_01', 0, 0, '06:43:32 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: 40-30]'),
('evt_1787701434444_5bx6o', 'match_live_01', 0, 0, '06:43:54 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: 40-40]'),
('evt_1787701457146_2l658', 'match_live_01', 0, 0, '06:44:17 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-1 [Pts: AD-40]'),
('evt_1787701461243_7afu6', 'match_live_01', 0, 0, '06:44:21 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-1 [Pts: 0-0]'),
('evt_1787701506528_f6vuk', 'match_live_01', 0, 0, '06:45:06 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-1 [Pts: 0-15]'),
('evt_1787701527042_3c1dt', 'match_live_01', 0, 0, '06:45:27 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-1 [Pts: 15-15]'),
('evt_1787701554616_l4fzf', 'match_live_01', 0, 0, '06:45:54 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-1 [Pts: 15-30]'),
('evt_1787701573127_fp9t2', 'match_live_01', 0, 0, '06:46:13 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-1 [Pts: 15-40]'),
('evt_1787701581942_66wfs', 'match_live_01', 0, 0, '06:46:21 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-2 [Pts: 0-0]'),
('evt_1787701635301_s30q5', 'match_live_01', 0, 0, '06:47:15 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-2 [Pts: 15-0]'),
('evt_1787701664536_carpf', 'match_live_01', 0, 0, '06:47:44 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-2 [Pts: 15-15]'),
('evt_1787701688013_z049l', 'match_live_01', 0, 0, '06:48:08 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-2 [Pts: 30-15]'),
('evt_1787701708728_oqn4r', 'match_live_01', 0, 0, '06:48:28 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-2 [Pts: 40-15]'),
('evt_1787701738318_wh4ko', 'match_live_01', 0, 0, '06:48:58 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-2 [Pts: 0-0]'),
('evt_1787701755329_lovgc', 'match_live_01', 0, 0, '06:49:15 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-2 [Pts: 0-15]'),
('evt_1787701768031_abqgj', 'match_live_01', 0, 0, '06:49:28 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-2 [Pts: 0-30]'),
('evt_1787701801882_stjk7', 'match_live_01', 0, 0, '06:50:01 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-2 [Pts: 0-40]'),
('evt_1787701827189_boyvc', 'match_live_01', 0, 0, '06:50:27 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-3 [Pts: 0-0]'),
('evt_1787701858904_iij4n', 'match_live_01', 0, 0, '06:50:58 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-3 [Pts: 15-0]'),
('evt_1787701877896_8a771', 'match_live_01', 0, 0, '06:51:17 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-3 [Pts: 30-0]'),
('evt_1787701900538_zh7kv', 'match_live_01', 0, 0, '06:51:40 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-3 [Pts: 40-0]'),
('evt_1787701925929_jrdhj', 'match_live_01', 0, 0, '06:52:05 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-3 [Pts: 0-0]'),
('evt_1787701983558_wsoy7', 'match_live_01', 0, 0, '06:53:03 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-3 [Pts: 0-15]'),
('evt_1787702007789_wi91j', 'match_live_01', 0, 0, '06:53:27 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-3 [Pts: 15-15]'),
('evt_1787702048779_7pzlw', 'match_live_01', 0, 0, '06:54:08 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-3 [Pts: 15-30]'),
('evt_1787702061346_2fvff', 'match_live_01', 0, 0, '06:54:21 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-3 [Pts: 30-30]'),
('evt_1787702083994_5a1d3', 'match_live_01', 0, 0, '06:54:43 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-3 [Pts: 40-30]'),
('evt_1787702101914_hiijp', 'match_live_01', 0, 0, '06:55:01 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-3 [Pts: 40-40]'),
('evt_1787702126137_xieet', 'match_live_01', 0, 0, '06:55:26 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-3 [Pts: AD-40]'),
('evt_1787702127891_wg5e2', 'match_live_01', 0, 0, '06:55:27 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 0-0]'),
('evt_1787702177635_fa2re', 'match_live_01', 0, 0, '06:56:17 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 0-0]'),
('evt_1787702223601_3m4ul', 'match_live_01', 0, 0, '06:57:03 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 15-0]'),
('evt_1787702250252_0t7cq', 'match_live_01', 0, 0, '06:57:30 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 15-15]'),
('evt_1787702266069_1svqc', 'match_live_01', 0, 0, '06:57:46 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 30-15]'),
('evt_1787702289004_r7xc8', 'match_live_01', 0, 0, '06:58:09 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 30-30]'),
('evt_1787702310271_469su', 'match_live_01', 0, 0, '06:58:30 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 40-30]'),
('evt_1787702327455_navyz', 'match_live_01', 0, 0, '06:58:47 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 0-0]'),
('evt_1787702345909_i6i5c', 'match_live_01', 0, 0, '06:59:05 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 0-15]'),
('evt_1787702359997_yx0kl', 'match_live_01', 0, 0, '06:59:19 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 0-30]'),
('evt_1787702388154_dpm6i', 'match_live_01', 0, 0, '06:59:48 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 0-30]'),
('evt_1787702391478_o6ymn', 'match_live_01', 0, 0, '06:59:51 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 0-40]'),
('evt_1787702406466_3cqt5', 'match_live_01', 0, 0, '07:00:06 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 15-40]'),
('evt_1787702432686_0l2du', 'match_live_01', 0, 0, '07:00:32 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 30-40]'),
('evt_1787702450052_lljei', 'match_live_01', 0, 0, '07:00:50 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 40-40]'),
('evt_1787702468439_e2yul', 'match_live_01', 0, 0, '07:01:08 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: AD-40]'),
('evt_1787702471324_hu2nm', 'match_live_01', 0, 0, '07:01:11 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 2-0 [Pts: 0-0]'),
('evt_1787702515960_fafy0', 'match_live_01', 0, 0, '07:01:55 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 2-0 [Pts: 15-0]'),
('evt_1787702547095_lgoqa', 'match_live_01', 0, 0, '07:02:27 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 2-0 [Pts: 15-15]'),
('evt_1787702578839_3ip35', 'match_live_01', 0, 0, '07:02:58 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 2-0 [Pts: 15-15]'),
('evt_1787702582443_rd635', 'match_live_01', 0, 0, '07:03:02 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 2-0 [Pts: 15-30]'),
('evt_1787702611641_trr34', 'match_live_01', 0, 0, '07:03:31 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 2-0 [Pts: 30-15]'),
('evt_1787702615603_aha9b', 'match_live_01', 0, 0, '07:03:35 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 2-0 [Pts: 30-30]'),
('evt_1787702637695_1cdqx', 'match_live_01', 0, 0, '07:03:57 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 2-0 [Pts: 40-30]'),
('evt_1787702660299_t8odu', 'match_live_01', 0, 0, '07:04:20 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 0-0]'),
('evt_1787702664538_81fd1', 'match_live_01', 0, 0, '07:04:24 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 0-0]'),
('evt_1787702671788_p6s3f', 'match_live_01', 0, 0, '07:04:31 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 0-0]'),
('evt_1787702675833_f2pb9', 'match_live_01', 0, 0, '07:04:35 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 0-15]'),
('evt_1787702678491_urbel', 'match_live_01', 0, 0, '07:04:38 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 0-30]'),
('evt_1787702707551_l4oy9', 'match_live_01', 0, 0, '07:05:07 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 0-0]'),
('evt_1787702711091_903ho', 'match_live_01', 0, 0, '07:05:11 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 0-15]'),
('evt_1787702743525_invce', 'match_live_01', 0, 0, '07:05:43 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 15-15]'),
('evt_1787702761154_nq6x9', 'match_live_01', 0, 0, '07:06:01 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 15-15]'),
('evt_1787702761880_pj6zj', 'match_live_01', 0, 0, '07:06:01 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 30-15]'),
('evt_1787702789251_e2tkz', 'match_live_01', 0, 0, '07:06:29 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 30-30]'),
('evt_1787702815460_95g0g', 'match_live_01', 0, 0, '07:06:55 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 30-40]'),
('evt_1787702836339_lsm6t', 'match_live_01', 0, 0, '07:07:16 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 40-40]'),
('evt_1787702851686_uibf4', 'match_live_01', 0, 0, '07:07:31 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-0 [Pts: 40-AD]'),
('evt_1787702852894_ulwgf', 'match_live_01', 0, 0, '07:07:32 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 0-0]'),
('evt_1787702858157_lrbs5', 'match_live_01', 0, 0, '07:07:38 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 0-0]'),
('evt_1787702860778_kkm81', 'match_live_01', 0, 0, '07:07:40 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 0-15]'),
('evt_1787702899483_6ew1i', 'match_live_01', 0, 0, '07:08:19 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 15-0]'),
('evt_1787702930044_ebkp1', 'match_live_01', 0, 0, '07:08:50 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 30-0]'),
('evt_1787702945631_6w1z4', 'match_live_01', 0, 0, '07:09:05 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 40-0]'),
('evt_1787702945911_xer95', 'match_live_01', 0, 0, '07:09:05 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 0-0]'),
('evt_1787702986638_xt4s2', 'match_live_01', 0, 0, '07:09:46 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 15-0]'),
('evt_1787703007619_tw1in', 'match_live_01', 0, 0, '07:10:07 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 0-0]'),
('evt_1787703007710_nambp', 'match_live_01', 0, 0, '07:10:07 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 15-0]'),
('evt_1787703008525_o7xez', 'match_live_01', 0, 0, '07:10:08 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 30-0]'),
('evt_1787703025944_hhzs1', 'match_live_01', 0, 0, '07:10:25 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 30-15]'),
('evt_1787703040777_fq4eb', 'match_live_01', 0, 0, '07:10:40 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 40-15]'),
('evt_1787703081348_9wylx', 'match_live_01', 0, 0, '07:11:21 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 0-0]'),
('evt_1787703089462_gmmju', 'match_live_01', 0, 0, '07:11:29 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 0-0]'),
('evt_1787703094949_2ehn2', 'match_live_01', 0, 0, '07:11:34 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 0-0]'),
('evt_1787703096072_6iovu', 'match_live_01', 0, 0, '07:11:36 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 15-0]'),
('evt_1787703130611_0tg46', 'match_live_01', 0, 0, '07:12:10 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 0-15]'),
('evt_1787703151163_fqoqg', 'match_live_01', 0, 0, '07:12:31 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 15-15]'),
('evt_1787703168883_4knqx', 'match_live_01', 0, 0, '07:12:48 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 15-30]'),
('evt_1787703187918_bi765', 'match_live_01', 0, 0, '07:13:07 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 15-40]'),
('evt_1787703214333_eqh9p', 'match_live_01', 0, 0, '07:13:34 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-2 [Pts: 0-0]'),
('evt_1787703250665_jsv79', 'match_live_01', 0, 0, '07:14:10 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-2 [Pts: 0-15]'),
('evt_1787703271656_nuv9g', 'match_live_01', 0, 0, '07:14:31 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-2 [Pts: 0-30]'),
('evt_1787703289950_d4p3c', 'match_live_01', 0, 0, '07:14:49 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-2 [Pts: 15-30]'),
('evt_1787703290048_vkeu4', 'match_live_01', 0, 0, '07:14:50 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-2 [Pts: 30-30]'),
('evt_1787703301422_yzfy9', 'match_live_01', 0, 0, '07:15:01 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-2 [Pts: 15-40]'),
('evt_1787703319556_o10nq', 'match_live_01', 0, 0, '07:15:19 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 0-0]'),
('evt_1787703353252_8iekz', 'match_live_01', 0, 0, '07:15:53 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 0-15]'),
('evt_1787703399583_0x32p', 'match_live_01', 0, 0, '07:16:39 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 0-15]'),
('evt_1787703400553_ut82x', 'match_live_01', 0, 0, '07:16:40 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 15-15]'),
('evt_1787703414038_civ4r', 'match_live_01', 0, 0, '07:16:54 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 15-15]'),
('evt_1787703429858_qgp3e', 'match_live_01', 0, 0, '07:17:09 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 15-30]'),
('evt_1787703457759_nylgm', 'match_live_01', 0, 0, '07:17:37 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 30-30]'),
('evt_1787703486564_t15b0', 'match_live_01', 0, 0, '07:18:06 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 30-40]'),
('evt_1787703509441_dqc9i', 'match_live_01', 0, 0, '07:18:29 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: 40-40]'),
('evt_1787703562401_1pyc7', 'match_live_01', 0, 0, '07:19:22 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: AD-40]'),
('evt_1787703563568_06jsv', 'match_live_01', 0, 0, '07:19:23 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 0-0]'),
('evt_1787703571521_8y18g', 'match_live_01', 0, 0, '07:19:31 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: AD-40]'),
('evt_1787703572298_5qnbt', 'match_live_01', 0, 0, '07:19:32 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: AD-40]'),
('evt_1787703572951_mh8kh', 'match_live_01', 0, 0, '07:19:32 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 0-0]'),
('evt_1787703577078_q1n0m', 'match_live_01', 0, 0, '07:19:37 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: AD-40]'),
('evt_1787703577902_xem1j', 'match_live_01', 0, 0, '07:19:37 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: AD-40]'),
('evt_1787703578581_otz7o', 'match_live_01', 0, 0, '07:19:38 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 0-0]'),
('evt_1787703583336_i0cin', 'match_live_01', 0, 0, '07:19:43 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 5-3 [Pts: AD-40]'),
('evt_1787703585965_a9bzj', 'match_live_01', 0, 0, '07:19:45 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 0-0]'),
('evt_1787703586148_1b9qu', 'match_live_01', 0, 0, '07:19:46 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 15-0]'),
('evt_1787703702674_9nixy', 'match_live_01', 0, 0, '07:21:42 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 0-15]'),
('evt_1787703738158_asn6t', 'match_live_01', 0, 0, '07:22:18 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 0-30]'),
('evt_1787703755175_4kq28', 'match_live_01', 0, 0, '07:22:35 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 15-30]'),
('evt_1787703779627_5r8ao', 'match_live_01', 0, 0, '07:22:59 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 30-30]'),
('evt_1787703810388_eto4u', 'match_live_01', 0, 0, '07:23:30 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 30-30]'),
('evt_1787703812135_c3zcl', 'match_live_01', 0, 0, '07:23:32 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-0 [Pts: 30-40]'),
('evt_1787703831440_tvx8b', 'match_live_01', 0, 0, '07:23:51 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 0-0]'),
('evt_1787703853641_zo8k8', 'match_live_01', 0, 0, '07:24:13 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 0-15]'),
('evt_1787703894573_2vc4j', 'match_live_01', 0, 0, '07:24:54 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 15-15]'),
('evt_1787703897678_44y2q', 'match_live_01', 0, 0, '07:24:57 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 15-30]'),
('evt_1787703931533_hnyav', 'match_live_01', 0, 0, '07:25:31 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 30-15]'),
('evt_1787703933044_vvbv3', 'match_live_01', 0, 0, '07:25:33 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 30-30]'),
('evt_1787703972987_jooc5', 'match_live_01', 0, 0, '07:26:12 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 30-15]'),
('evt_1787704017023_h0jq9', 'match_live_01', 0, 0, '07:26:57 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 0-15]'),
('evt_1787704018404_dtyhq', 'match_live_01', 0, 0, '07:26:58 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 15-15]'),
('evt_1787704102997_15wtc', 'match_live_01', 0, 0, '07:28:22 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 15-0]'),
('evt_1787704104629_q79b4', 'match_live_01', 0, 0, '07:28:24 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 15-15]'),
('evt_1787704132039_6aywh', 'match_live_01', 0, 0, '07:28:52 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 30-15]'),
('evt_1787704168841_e3j4c', 'match_live_01', 0, 0, '07:29:28 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 30-30]'),
('evt_1787704180894_o60nb', 'match_live_01', 0, 0, '07:29:40 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 40-30]'),
('evt_1787704202049_ysccw', 'match_live_01', 0, 0, '07:30:02 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 40-40]'),
('evt_1787704213024_atkdc', 'match_live_01', 0, 0, '07:30:13 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-1 [Pts: 40-AD]'),
('evt_1787704213142_zr3zs', 'match_live_01', 0, 0, '07:30:13 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-2 [Pts: 0-0]'),
('evt_1787704221510_2crh4', 'match_live_01', 0, 0, '07:30:21 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-2 [Pts: 0-0]'),
('evt_1787704257660_pklnq', 'match_live_01', 0, 0, '07:30:57 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-2 [Pts: 0-15]'),
('evt_1787704258227_zvm5u', 'match_live_01', 0, 0, '07:30:58 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-2 [Pts: 0-30]'),
('evt_1787704275004_z0at3', 'match_live_01', 0, 0, '07:31:15 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-2 [Pts: 0-40]'),
('evt_1787704300967_qcxis', 'match_live_01', 0, 0, '07:31:40 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-2 [Pts: 15-40]'),
('evt_1787704327535_6klpp', 'match_live_01', 0, 0, '07:32:07 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 0-0]'),
('evt_1787704331756_rdri9', 'match_live_01', 0, 0, '07:32:11 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 0-0]'),
('evt_1787704335533_h602z', 'match_live_01', 0, 0, '07:32:15 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 0-0]'),
('evt_1787704337420_4x66y', 'match_live_01', 0, 0, '07:32:17 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 0-15]'),
('evt_1787704356716_7ldep', 'match_live_01', 0, 0, '07:32:36 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 15-15]'),
('evt_1787704385896_x0y30', 'match_live_01', 0, 0, '07:33:05 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 30-15]'),
('evt_1787704401079_76pol', 'match_live_01', 0, 0, '07:33:21 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 40-15]'),
('evt_1787704434032_vywbs', 'match_live_01', 0, 0, '07:33:54 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 40-30]'),
('evt_1787704496999_c10em', 'match_live_01', 0, 0, '07:34:56 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: 40-40]'),
('evt_1787704523056_wcdsl', 'match_live_01', 0, 0, '07:35:23 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 0-3 [Pts: AD-40]'),
('evt_1787704524826_zdvef', 'match_live_01', 0, 0, '07:35:24 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: 0-0]'),
('evt_1787704550735_y84wf', 'match_live_01', 0, 0, '07:35:50 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: 0-15]'),
('evt_1787704573650_ykwas', 'match_live_01', 0, 0, '07:36:13 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: 15-15]'),
('evt_1787704609412_vfnzt', 'match_live_01', 0, 0, '07:36:49 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: 15-30]'),
('evt_1787704634452_hulnd', 'match_live_01', 0, 0, '07:37:14 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: 30-30]'),
('evt_1787704659024_znc3h', 'match_live_01', 0, 0, '07:37:39 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: 15-40]'),
('evt_1787704680628_krk6p', 'match_live_01', 0, 0, '07:38:00 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: 30-40]'),
('evt_1787704681219_m8322', 'match_live_01', 0, 0, '07:38:01 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: 40-40]'),
('evt_1787704724842_xzh0g', 'match_live_01', 0, 0, '07:38:44 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 1-3 [Pts: AD-40]'),
('evt_1787704725693_4u3nw', 'match_live_01', 0, 0, '07:38:45 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 2-3 [Pts: 0-0]'),
('evt_1787704763349_llooz', 'match_live_01', 0, 0, '07:39:23 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 2-3 [Pts: 0-15]'),
('evt_1787704771757_lbnyc', 'match_live_01', 0, 0, '07:39:31 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 2-3 [Pts: 15-15]'),
('evt_1787704771853_xm4ql', 'match_live_01', 0, 0, '07:39:31 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 2-3 [Pts: 30-15]'),
('evt_1787704826327_amr96', 'match_live_01', 0, 0, '07:40:26 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 2-3 [Pts: 15-30]'),
('evt_1787704828217_2smxv', 'match_live_01', 0, 0, '07:40:28 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 2-3 [Pts: 15-40]'),
('evt_1787704877307_2o0fk', 'match_live_01', 0, 0, '07:41:17 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 2-3 [Pts: 30-30]'),
('evt_1787704877959_nq7uz', 'match_live_01', 0, 0, '07:41:17 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 2-3 [Pts: 40-30]'),
('evt_1787704907180_82k1w', 'match_live_01', 0, 0, '07:41:47 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 3-3 [Pts: 0-0]'),
('evt_1787704940941_a7axs', 'match_live_01', 0, 0, '07:42:20 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 3-3 [Pts: 15-0]'),
('evt_1787704960547_fszpq', 'match_live_01', 0, 0, '07:42:40 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 3-3 [Pts: 30-0]'),
('evt_1787704985714_lbf71', 'match_live_01', 0, 0, '07:43:05 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 3-3 [Pts: 40-0]'),
('evt_1787705024458_qmu3o', 'match_live_01', 0, 0, '07:43:44 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-3 [Pts: 0-0]'),
('evt_1787705045953_t9g2z', 'match_live_01', 0, 0, '07:44:05 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-3 [Pts: 15-0]'),
('evt_1787705086029_vl8k7', 'match_live_01', 0, 0, '07:44:46 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-3 [Pts: 15-15]'),
('evt_1787705091215_nnhc3', 'match_live_01', 0, 0, '07:44:51 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-3 [Pts: 30-15]'),
('evt_1787705118365_gxt1r', 'match_live_01', 0, 0, '07:45:18 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-3 [Pts: 30-30]'),
('evt_1787705162665_elktd', 'match_live_01', 0, 0, '07:46:02 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-3 [Pts: 30-40]'),
('evt_1787705199726_v53xs', 'match_live_01', 0, 0, '07:46:39 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-4 [Pts: 0-0]'),
('evt_1787705250774_1eqzz', 'match_live_01', 0, 0, '07:47:30 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-4 [Pts: 15-0]'),
('evt_1787705251388_a08tm', 'match_live_01', 0, 0, '07:47:31 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-4 [Pts: 30-0]'),
('evt_1787705276194_9ggka', 'match_live_01', 0, 0, '07:47:56 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-4 [Pts: 30-15]'),
('evt_1787705295164_a5jig', 'match_live_01', 0, 0, '07:48:15 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-4 [Pts: 40-15]'),
('evt_1787705321202_8j3hx', 'match_live_01', 0, 0, '07:48:41 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 4-4 [Pts: 40-15]'),
('evt_1787705322033_7kprb', 'match_live_01', 0, 0, '07:48:42 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 5-4 [Pts: 0-0]'),
('evt_1787705328841_iy1cc', 'match_live_01', 0, 0, '07:48:48 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 5-4 [Pts: 0-0]'),
('evt_1787705356014_cn137', 'match_live_01', 0, 0, '07:49:16 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 5-4 [Pts: 15-0]'),
('evt_1787705400857_vkcwe', 'match_live_01', 0, 0, '07:50:00 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 5-4 [Pts: 30-0]'),
('evt_1787705432188_2pyrq', 'match_live_01', 0, 0, '07:50:32 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 5-4 [Pts: 40-0]'),
('evt_1787705457660_fifnk', 'match_live_01', 0, 0, '07:50:57 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 6-4 | S4: 0-0 [Pts: 0-0]'),
('evt_1787705516464_0lwr4', 'match_live_01', 0, 0, '07:51:56 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 6-4 | S4: 0-0 [Pts: 15-0]'),
('evt_1787705518380_8yrm1', 'match_live_01', 0, 0, '07:51:58 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 6-4 | S4: 0-0 [Pts: 15-15]'),
('evt_1787705543389_qhhq9', 'match_live_01', 0, 0, '07:52:23 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 6-4 | S4: 0-0 [Pts: 15-30]'),
('evt_1787705577590_rmm8t', 'match_live_01', 0, 0, '07:52:57 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 6-4 | S4: 0-0 [Pts: 30-30]'),
('evt_1787705629452_x705x', 'match_live_01', 0, 0, '07:53:49 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 6-4 | S4: 0-0 [Pts: 40-30]'),
('evt_1787705631030_ww24d', 'match_live_01', 0, 0, '07:53:51 p.m.', 'B', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 6-4 | S4: 0-0 [Pts: 40-40]'),
('evt_1787705662328_wy7hi', 'match_live_01', 0, 0, '07:54:22 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-3 | S2: 6-3 | S3: 6-4 | S4: 1-0 [Pts: 0-0]'),
('evt_1787708833758_7bn55', 'match_1787708807671', 0, 0, '20:47:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787708835123_39q16', 'match_1787708807671', 0, 0, '20:47:15', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-0]'),
('evt_1787708839900_qah50', 'match_1787708807671', 0, 0, '20:47:19', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787708846812_gizqm', 'match_1787708807671', 0, 0, '20:47:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708853725_3j79f', 'match_1787708807671', 0, 0, '20:47:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708856228_u0dlj', 'match_1787708807671', 0, 0, '20:47:36', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708857428_hle1j', 'match_1787708807671', 0, 0, '20:47:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 30-15]'),
('evt_1787708858262_1kvbb', 'match_1787708807671', 0, 0, '20:47:38', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708859109_zw1wn', 'match_1787708807671', 0, 0, '20:47:39', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 30-40]'),
('evt_1787708859932_xp3c2', 'match_1787708807671', 0, 0, '20:47:39', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708860613_33fwa', 'match_1787708807671', 0, 0, '20:47:40', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: AD-40]'),
('evt_1787708861532_r0316', 'match_1787708807671', 0, 0, '20:47:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708863220_mwmk5', 'match_1787708807671', 0, 0, '20:47:43', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 40-AD]'),
('evt_1787708866710_c6ua3', 'match_1787708807671', 0, 0, '20:47:46', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708867806_npq34', 'match_1787708807671', 0, 0, '20:47:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708869404_53vq6', 'match_1787708807671', 0, 0, '20:47:49', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 | S2: 0-0 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708870245_l34ag', 'match_1787708807671', 0, 0, '20:47:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 | S2: 0-0 | S3: 0-0 [Pts: 30-15]'),
('evt_1787708871070_sxxq7', 'match_1787708807671', 0, 0, '20:47:51', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 | S2: 0-0 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708871886_ep3kg', 'match_1787708807671', 0, 0, '20:47:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 | S2: 0-0 | S3: 0-0 [Pts: 40-30]'),
('evt_1787708873044_dsuf1', 'match_1787708807671', 0, 0, '20:47:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708874167_ds6a6', 'match_1787708807671', 0, 0, '20:47:54', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708874956_3w0mk', 'match_1787708807671', 0, 0, '20:47:54', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708875804_0tzf9', 'match_1787708807671', 0, 0, '20:47:55', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 30-15]'),
('evt_1787708876766_cm6h8', 'match_1787708807671', 0, 0, '20:47:56', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708877581_lcv83', 'match_1787708807671', 0, 0, '20:47:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 40-30]'),
('evt_1787708878284_iij16', 'match_1787708807671', 0, 0, '20:47:58', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708879068_sj8xt', 'match_1787708807671', 0, 0, '20:47:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: AD-40]'),
('evt_1787708880285_qz7qz', 'match_1787708807671', 0, 0, '20:48:00', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708881364_76kwn', 'match_1787708807671', 0, 0, '20:48:01', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: AD-40]'),
('evt_1787708882164_65f02', 'match_1787708807671', 0, 0, '20:48:02', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708883164_b28c8', 'match_1787708807671', 0, 0, '20:48:03', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: AD-40]'),
('evt_1787708884300_7smj9', 'match_1787708807671', 0, 0, '20:48:04', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708885590_balex', 'match_1787708807671', 0, 0, '20:48:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: AD-40]'),
('evt_1787708886374_b0w7n', 'match_1787708807671', 0, 0, '20:48:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708887589_6k8vu', 'match_1787708807671', 0, 0, '20:48:07', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 40-AD]'),
('evt_1787708888581_al2gu', 'match_1787708807671', 0, 0, '20:48:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708889446_zztwl', 'match_1787708807671', 0, 0, '20:48:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 | S2: 0-0 | S3: 0-0 [Pts: AD-40]'),
('evt_1787708890388_i6nb6', 'match_1787708807671', 0, 0, '20:48:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708891595_92ikk', 'match_1787708807671', 0, 0, '20:48:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708892325_yexm9', 'match_1787708807671', 0, 0, '20:48:12', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708892998_dj03r', 'match_1787708807671', 0, 0, '20:48:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 15-30]'),
('evt_1787708893734_9u93t', 'match_1787708807671', 0, 0, '20:48:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708894421_dthno', 'match_1787708807671', 0, 0, '20:48:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 30-40]'),
('evt_1787708895181_6u8j1', 'match_1787708807671', 0, 0, '20:48:15', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708896189_9hi79', 'match_1787708807671', 0, 0, '20:48:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 40-AD]'),
('evt_1787708896710_xbad7', 'match_1787708807671', 0, 0, '20:48:16', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708897309_d4rcj', 'match_1787708807671', 0, 0, '20:48:17', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: AD-40]'),
('evt_1787708898542_3v418', 'match_1787708807671', 0, 0, '20:48:18', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708898852_jqeem', 'match_1787708807671', 0, 0, '20:48:18', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 | S2: 0-0 | S3: 0-0 [Pts: 40-AD]'),
('evt_1787708899437_0e5tz', 'match_1787708807671', 0, 0, '20:48:19', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-2 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708900213_dpfic', 'match_1787708807671', 0, 0, '20:48:20', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-2 | S2: 0-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708900941_8swvn', 'match_1787708807671', 0, 0, '20:48:20', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-2 | S2: 0-0 | S3: 0-0 [Pts: 0-30]'),
('evt_1787708901492_ef85s', 'match_1787708807671', 0, 0, '20:48:21', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-2 | S2: 0-0 | S3: 0-0 [Pts: 0-40]'),
('evt_1787708901765_629zs', 'match_1787708807671', 0, 0, '20:48:21', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-3 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708901981_r4ryb', 'match_1787708807671', 0, 0, '20:48:21', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-3 | S2: 0-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708902268_htpzo', 'match_1787708807671', 0, 0, '20:48:22', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-3 | S2: 0-0 | S3: 0-0 [Pts: 0-30]'),
('evt_1787708902493_2cmrn', 'match_1787708807671', 0, 0, '20:48:22', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-3 | S2: 0-0 | S3: 0-0 [Pts: 0-40]'),
('evt_1787708902693_5fw76', 'match_1787708807671', 0, 0, '20:48:22', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-4 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708902909_tvbwk', 'match_1787708807671', 0, 0, '20:48:22', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-4 | S2: 0-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708903124_efspy', 'match_1787708807671', 0, 0, '20:48:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-4 | S2: 0-0 | S3: 0-0 [Pts: 0-30]'),
('evt_1787708903316_r9r9k', 'match_1787708807671', 0, 0, '20:48:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-4 | S2: 0-0 | S3: 0-0 [Pts: 0-40]'),
('evt_1787708903518_67emc', 'match_1787708807671', 0, 0, '20:48:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-5 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708903710_wdeig', 'match_1787708807671', 0, 0, '20:48:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-5 | S2: 0-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708903925_0n0lv', 'match_1787708807671', 0, 0, '20:48:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-5 | S2: 0-0 | S3: 0-0 [Pts: 0-30]'),
('evt_1787708904133_a93ig', 'match_1787708807671', 0, 0, '20:48:24', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-5 | S2: 0-0 | S3: 0-0 [Pts: 0-40]'),
('evt_1787708904966_fyx2m', 'match_1787708807671', 0, 0, '20:48:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-5 | S2: 0-0 | S3: 0-0 [Pts: 15-40]'),
('evt_1787708905172_jihae', 'match_1787708807671', 0, 0, '20:48:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-5 | S2: 0-0 | S3: 0-0 [Pts: 30-40]'),
('evt_1787708905389_nofe1', 'match_1787708807671', 0, 0, '20:48:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-5 | S2: 0-0 | S3: 0-0 [Pts: 40-40]'),
('evt_1787708905612_19sdo', 'match_1787708807671', 0, 0, '20:48:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-5 | S2: 0-0 | S3: 0-0 [Pts: AD-40]'),
('evt_1787708905828_as42z', 'match_1787708807671', 0, 0, '20:48:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-5 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708906037_ypvr6', 'match_1787708807671', 0, 0, '20:48:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-5 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708906236_fc3mu', 'match_1787708807671', 0, 0, '20:48:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-5 | S2: 0-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787708907054_gebch', 'match_1787708807671', 0, 0, '20:48:27', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-5 | S2: 0-0 | S3: 0-0 [Pts: 30-15]'),
('evt_1787708907269_vcvxr', 'match_1787708807671', 0, 0, '20:48:27', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-5 | S2: 0-0 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708907486_kel38', 'match_1787708807671', 0, 0, '20:48:27', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-5 | S2: 0-0 | S3: 0-0 [Pts: 30-40]'),
('evt_1787708907686_drwy0', 'match_1787708807671', 0, 0, '20:48:27', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708907902_82jzv', 'match_1787708807671', 0, 0, '20:48:27', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 0-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708908804_obvc3', 'match_1787708807671', 0, 0, '20:48:28', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 0-0 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708909036_7z3fp', 'match_1787708807671', 0, 0, '20:48:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 0-0 | S3: 0-0 [Pts: 30-15]');
INSERT INTO `match_events` (`id`, `match_id`, `set_number`, `game_number`, `timestamp`, `winning_pair_id`, `player_id`, `player_name`, `event_type`, `description`, `score_snapshot`) VALUES
('evt_1787708909260_jb49y', 'match_1787708807671', 0, 0, '20:48:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 0-0 | S3: 0-0 [Pts: 40-15]'),
('evt_1787708909460_zvgdp', 'match_1787708807671', 0, 0, '20:48:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 1-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708909663_3j978', 'match_1787708807671', 0, 0, '20:48:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 1-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708909862_unova', 'match_1787708807671', 0, 0, '20:48:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 1-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787708910102_div3z', 'match_1787708807671', 0, 0, '20:48:30', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 1-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787708910366_i4q4u', 'match_1787708807671', 0, 0, '20:48:30', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 2-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708911013_ibb7o', 'match_1787708807671', 0, 0, '20:48:31', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 2-0 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708911229_aeh7m', 'match_1787708807671', 0, 0, '20:48:31', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 2-0 | S3: 0-0 [Pts: 0-30]'),
('evt_1787708911445_gltat', 'match_1787708807671', 0, 0, '20:48:31', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 2-0 | S3: 0-0 [Pts: 0-40]'),
('evt_1787708911647_181e0', 'match_1787708807671', 0, 0, '20:48:31', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 2-1 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708911861_of3hk', 'match_1787708807671', 0, 0, '20:48:31', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 2-1 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708912061_twq71', 'match_1787708807671', 0, 0, '20:48:32', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 2-1 | S3: 0-0 [Pts: 0-30]'),
('evt_1787708912781_skijx', 'match_1787708807671', 0, 0, '20:48:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 2-1 | S3: 0-0 [Pts: 15-30]'),
('evt_1787708912989_sjy4m', 'match_1787708807671', 0, 0, '20:48:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 2-1 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708913204_vtzob', 'match_1787708807671', 0, 0, '20:48:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 2-1 | S3: 0-0 [Pts: 40-30]'),
('evt_1787708913437_dp73r', 'match_1787708807671', 0, 0, '20:48:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 3-1 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708913637_jfi6r', 'match_1787708807671', 0, 0, '20:48:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 3-1 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708914157_w5l53', 'match_1787708807671', 0, 0, '20:48:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 3-1 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708914366_a50n0', 'match_1787708807671', 0, 0, '20:48:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 3-1 | S3: 0-0 [Pts: 15-30]'),
('evt_1787708914580_elj52', 'match_1787708807671', 0, 0, '20:48:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 3-1 | S3: 0-0 [Pts: 15-40]'),
('evt_1787708914782_c56w5', 'match_1787708807671', 0, 0, '20:48:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 3-2 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708914997_hludt', 'match_1787708807671', 0, 0, '20:48:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 3-2 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708915212_n39o7', 'match_1787708807671', 0, 0, '20:48:35', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 3-2 | S3: 0-0 [Pts: 0-30]'),
('evt_1787708915863_jldo2', 'match_1787708807671', 0, 0, '20:48:35', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 3-2 | S3: 0-0 [Pts: 15-30]'),
('evt_1787708916096_hwjf0', 'match_1787708807671', 0, 0, '20:48:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 3-2 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708916311_0dam5', 'match_1787708807671', 0, 0, '20:48:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 3-2 | S3: 0-0 [Pts: 40-30]'),
('evt_1787708916532_5l2zf', 'match_1787708807671', 0, 0, '20:48:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 4-2 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708916748_2fis9', 'match_1787708807671', 0, 0, '20:48:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 4-2 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708916964_ybe2d', 'match_1787708807671', 0, 0, '20:48:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 4-2 | S3: 0-0 [Pts: 30-0]'),
('evt_1787708917558_9r9l7', 'match_1787708807671', 0, 0, '20:48:37', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 4-2 | S3: 0-0 [Pts: 30-15]'),
('evt_1787708917950_gv85e', 'match_1787708807671', 0, 0, '20:48:37', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 4-2 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708918188_yy4u9', 'match_1787708807671', 0, 0, '20:48:38', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 4-2 | S3: 0-0 [Pts: 30-40]'),
('evt_1787708918412_jkjse', 'match_1787708807671', 0, 0, '20:48:38', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 4-3 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708918620_imy7s', 'match_1787708807671', 0, 0, '20:48:38', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 4-3 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708919348_cir85', 'match_1787708807671', 0, 0, '20:48:39', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 4-3 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708919580_q3zlt', 'match_1787708807671', 0, 0, '20:48:39', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 4-3 | S3: 0-0 [Pts: 30-15]'),
('evt_1787708919796_q05v0', 'match_1787708807671', 0, 0, '20:48:39', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 4-3 | S3: 0-0 [Pts: 40-15]'),
('evt_1787708920013_3ex83', 'match_1787708807671', 0, 0, '20:48:40', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 5-3 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708920237_kl97s', 'match_1787708807671', 0, 0, '20:48:40', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 5-3 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708920877_jkbyn', 'match_1787708807671', 0, 0, '20:48:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 5-3 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708921101_np08x', 'match_1787708807671', 0, 0, '20:48:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 5-3 | S3: 0-0 [Pts: 15-30]'),
('evt_1787708921317_mfjbs', 'match_1787708807671', 0, 0, '20:48:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 5-3 | S3: 0-0 [Pts: 15-40]'),
('evt_1787708921516_u6efg', 'match_1787708807671', 0, 0, '20:48:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 5-4 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708921733_9oagf', 'match_1787708807671', 0, 0, '20:48:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 5-4 | S3: 0-0 [Pts: 0-15]'),
('evt_1787708922006_otgxw', 'match_1787708807671', 0, 0, '20:48:42', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 5-4 | S3: 0-0 [Pts: 0-30]'),
('evt_1787708922639_1v9ey', 'match_1787708807671', 0, 0, '20:48:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 5-4 | S3: 0-0 [Pts: 15-30]'),
('evt_1787708922860_0yrsm', 'match_1787708807671', 0, 0, '20:48:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 5-4 | S3: 0-0 [Pts: 30-30]'),
('evt_1787708923076_xrmto', 'match_1787708807671', 0, 0, '20:48:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 5-4 | S3: 0-0 [Pts: 40-30]'),
('evt_1787708923292_v9l80', 'match_1787708807671', 0, 0, '20:48:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-0 [Pts: 0-0]'),
('evt_1787708923508_7a5x5', 'match_1787708807671', 0, 0, '20:48:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-0 [Pts: 15-0]'),
('evt_1787708924110_veac0', 'match_1787708807671', 0, 0, '20:48:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-0 [Pts: 15-15]'),
('evt_1787708924350_6ewm5', 'match_1787708807671', 0, 0, '20:48:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-0 [Pts: 15-30]'),
('evt_1787708924566_p2nai', 'match_1787708807671', 0, 0, '20:48:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-0 [Pts: 15-40]'),
('evt_1787708924782_u5brw', 'match_1787708807671', 0, 0, '20:48:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-1 [Pts: 0-0]'),
('evt_1787708925013_m8yzh', 'match_1787708807671', 0, 0, '20:48:45', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-1 [Pts: 0-15]'),
('evt_1787708925221_jgjhq', 'match_1787708807671', 0, 0, '20:48:45', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-1 [Pts: 0-30]'),
('evt_1787708925878_kcmbt', 'match_1787708807671', 0, 0, '20:48:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-1 [Pts: 15-30]'),
('evt_1787708926117_b5mnh', 'match_1787708807671', 0, 0, '20:48:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-1 [Pts: 30-30]'),
('evt_1787708926324_3akd0', 'match_1787708807671', 0, 0, '20:48:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 0-1 [Pts: 40-30]'),
('evt_1787708926551_t24zc', 'match_1787708807671', 0, 0, '20:48:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 1-1 [Pts: 0-0]'),
('evt_1787708926756_6jf5k', 'match_1787708807671', 0, 0, '20:48:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 1-1 [Pts: 15-0]'),
('evt_1787708926974_z7qe6', 'match_1787708807671', 0, 0, '20:48:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 1-1 [Pts: 30-0]'),
('evt_1787708927196_koamu', 'match_1787708807671', 0, 0, '20:48:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 1-1 [Pts: 40-0]'),
('evt_1787708927404_0quex', 'match_1787708807671', 0, 0, '20:48:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 2-1 [Pts: 0-0]'),
('evt_1787708927613_0w9ty', 'match_1787708807671', 0, 0, '20:48:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 2-1 [Pts: 15-0]'),
('evt_1787708927829_gyy5d', 'match_1787708807671', 0, 0, '20:48:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 2-1 [Pts: 30-0]'),
('evt_1787708928085_kk14y', 'match_1787708807671', 0, 0, '20:48:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 2-1 [Pts: 40-0]'),
('evt_1787708928300_9h58l', 'match_1787708807671', 0, 0, '20:48:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 3-1 [Pts: 0-0]'),
('evt_1787708928526_z3v95', 'match_1787708807671', 0, 0, '20:48:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 3-1 [Pts: 15-0]'),
('evt_1787708929254_yf19d', 'match_1787708807671', 0, 0, '20:48:49', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 3-1 [Pts: 15-15]'),
('evt_1787708929500_c5my6', 'match_1787708807671', 0, 0, '20:48:49', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 3-1 [Pts: 15-30]'),
('evt_1787708930164_s22fd', 'match_1787708807671', 0, 0, '20:48:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 3-1 [Pts: 30-30]'),
('evt_1787708930415_uluk5', 'match_1787708807671', 0, 0, '20:48:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 3-1 [Pts: 40-30]'),
('evt_1787708930636_okwkb', 'match_1787708807671', 0, 0, '20:48:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 4-1 [Pts: 0-0]'),
('evt_1787708930902_kcnnr', 'match_1787708807671', 0, 0, '20:48:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 4-1 [Pts: 15-0]'),
('evt_1787708931462_kykbw', 'match_1787708807671', 0, 0, '20:48:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 4-1 [Pts: 30-0]'),
('evt_1787708932000_5395q', 'match_1787708807671', 0, 0, '20:48:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 4-1 [Pts: 40-0]'),
('evt_1787708932484_3p66i', 'match_1787708807671', 0, 0, '20:48:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 5-1 [Pts: 0-0]'),
('evt_1787708933230_o8uxo', 'match_1787708807671', 0, 0, '20:48:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 5-1 [Pts: 15-0]'),
('evt_1787708933484_w0z81', 'match_1787708807671', 0, 0, '20:48:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 5-1 [Pts: 30-0]'),
('evt_1787708933697_5z9uo', 'match_1787708807671', 0, 0, '20:48:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 5-1 [Pts: 40-0]'),
('evt_1787708933928_sagwh', 'match_1787708807671', 0, 0, '20:48:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 6-1 [Pts: 0-0]'),
('evt_1787708934199_jp3c8', 'match_1787708807671', 0, 0, '20:48:54', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-6 | S2: 6-4 | S3: 6-1 [Pts: 15-0]'),
('evt_1787709042222_0bx5g', 'match_1787708807671', 0, 0, '20:50:42', 'A', NULL, NULL, 'WINNER', 'ochoa / jimenez gana punto (WINNER)', 'S1: 3-6 | S2: 6-4 | S3: 6-1 [Pts: 15-0]'),
('evt_1787709730239_zdndt', 'match_1787700526113', 0, 0, '09:02:10 p.m.', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', ' [Pts: 15-0]'),
('evt_1787716358119_9d1y1', 'match_1787716319484', 0, 0, '22:52:38', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787716358805_6d3jm', 'match_1787716319484', 0, 0, '22:52:38', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787716362960_o4hyu', 'match_1787716319484', 0, 0, '22:52:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787716363522_7ss5a', 'match_1787716319484', 0, 0, '22:52:43', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 30-30]'),
('evt_1787716364267_e4c3d', 'match_1787716319484', 0, 0, '22:52:44', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 40-30]'),
('evt_1787716364762_jd0q1', 'match_1787716319484', 0, 0, '22:52:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 40-40]'),
('evt_1787716365300_h826w', 'match_1787716319484', 0, 0, '22:52:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: AD-40]'),
('evt_1787716365730_6f6ol', 'match_1787716319484', 0, 0, '22:52:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 0-0]'),
('evt_1787716365938_qyitd', 'match_1787716319484', 0, 0, '22:52:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 15-0]'),
('evt_1787716366154_6vifh', 'match_1787716319484', 0, 0, '22:52:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-0]'),
('evt_1787716366353_c6uv0', 'match_1787716319484', 0, 0, '22:52:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 40-0]'),
('evt_1787716366655_mdi4u', 'match_1787716319484', 0, 0, '22:52:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 0-0]'),
('evt_1787716367084_x9pj4', 'match_1787716319484', 0, 0, '22:52:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 0-15]'),
('evt_1787716367309_amuz5', 'match_1787716319484', 0, 0, '22:52:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 0-30]'),
('evt_1787716367527_d93kg', 'match_1787716319484', 0, 0, '22:52:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 0-40]'),
('evt_1787716367713_qs3dz', 'match_1787716319484', 0, 0, '22:52:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-0]'),
('evt_1787716367939_ib0ml', 'match_1787716319484', 0, 0, '22:52:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-15]'),
('evt_1787716368538_1erfk', 'match_1787716319484', 0, 0, '22:52:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 15-15]'),
('evt_1787716368756_1va4o', 'match_1787716319484', 0, 0, '22:52:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 30-15]'),
('evt_1787716368957_48so6', 'match_1787716319484', 0, 0, '22:52:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 40-15]'),
('evt_1787716369168_p7wao', 'match_1787716319484', 0, 0, '22:52:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 0-0]'),
('evt_1787716369371_jrwan', 'match_1787716319484', 0, 0, '22:52:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 15-0]'),
('evt_1787716369846_py6nj', 'match_1787716319484', 0, 0, '22:52:49', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 15-15]'),
('evt_1787716370063_pk6mh', 'match_1787716319484', 0, 0, '22:52:50', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 15-30]'),
('evt_1787716370265_ashao', 'match_1787716319484', 0, 0, '22:52:50', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 15-40]'),
('evt_1787716370466_sghbc', 'match_1787716319484', 0, 0, '22:52:50', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-2 [Pts: 0-0]'),
('evt_1787716370659_lmhn6', 'match_1787716319484', 0, 0, '22:52:50', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-2 [Pts: 0-15]'),
('evt_1787716370876_ipjbr', 'match_1787716319484', 0, 0, '22:52:50', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-2 [Pts: 0-30]'),
('evt_1787716371014_l30rz', 'match_1787716319484', 0, 0, '22:52:51', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-2 [Pts: 0-40]'),
('evt_1787716371708_agnzj', 'match_1787716319484', 0, 0, '22:52:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 15-40]'),
('evt_1787716371923_66ggv', 'match_1787716319484', 0, 0, '22:52:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 30-40]'),
('evt_1787716372125_h3c8n', 'match_1787716319484', 0, 0, '22:52:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 40-40]'),
('evt_1787716372325_qja4d', 'match_1787716319484', 0, 0, '22:52:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: AD-40]'),
('evt_1787716372527_a99k9', 'match_1787716319484', 0, 0, '22:52:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 0-0]'),
('evt_1787716372740_dpfaf', 'match_1787716319484', 0, 0, '22:52:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 15-0]'),
('evt_1787716372946_wpmda', 'match_1787716319484', 0, 0, '22:52:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 30-0]'),
('evt_1787716373155_olrwf', 'match_1787716319484', 0, 0, '22:52:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 40-0]'),
('evt_1787716373364_h28z5', 'match_1787716319484', 0, 0, '22:52:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 0-0]'),
('evt_1787716373581_ewi0v', 'match_1787716319484', 0, 0, '22:52:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 15-0]'),
('evt_1787716373831_9xugj', 'match_1787716319484', 0, 0, '22:52:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 30-0]'),
('evt_1787716374055_4p2ba', 'match_1787716319484', 0, 0, '22:52:54', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 40-0]'),
('evt_1787716374282_bqcpe', 'match_1787716319484', 0, 0, '22:52:54', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 0-0]'),
('evt_1787716374545_xsk08', 'match_1787716319484', 0, 0, '22:52:54', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 15-0]'),
('evt_1787716374819_q1kfr', 'match_1787716319484', 0, 0, '22:52:54', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 30-0]'),
('evt_1787716375037_wofcs', 'match_1787716319484', 0, 0, '22:52:55', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 40-0]'),
('evt_1787716375253_uoael', 'match_1787716319484', 0, 0, '22:52:55', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 0-0]'),
('evt_1787716375470_nep7a', 'match_1787716319484', 0, 0, '22:52:55', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 15-0]'),
('evt_1787716375678_trmzk', 'match_1787716319484', 0, 0, '22:52:55', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 30-0]'),
('evt_1787716375880_nze08', 'match_1787716319484', 0, 0, '22:52:55', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 40-0]'),
('evt_1787716376122_r6ehr', 'match_1787716319484', 0, 0, '22:52:56', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 0-0]'),
('evt_1787716376323_3xl2e', 'match_1787716319484', 0, 0, '22:52:56', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 15-0]'),
('evt_1787716376513_50ym6', 'match_1787716319484', 0, 0, '22:52:56', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 30-0]'),
('evt_1787716376724_d1oxy', 'match_1787716319484', 0, 0, '22:52:56', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 40-0]'),
('evt_1787716376915_pi5c6', 'match_1787716319484', 0, 0, '22:52:56', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 0-0]'),
('evt_1787716377131_d521x', 'match_1787716319484', 0, 0, '22:52:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 15-0]'),
('evt_1787716377364_u04yr', 'match_1787716319484', 0, 0, '22:52:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 30-0]'),
('evt_1787716377558_el9qg', 'match_1787716319484', 0, 0, '22:52:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 40-0]'),
('evt_1787716377775_5o9oz', 'match_1787716319484', 0, 0, '22:52:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 0-0]'),
('evt_1787716377992_z4fsn', 'match_1787716319484', 0, 0, '22:52:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 15-0]'),
('evt_1787716378192_vmgkp', 'match_1787716319484', 0, 0, '22:52:58', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 30-0]'),
('evt_1787716378369_y21fz', 'match_1787716319484', 0, 0, '22:52:58', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 40-0]'),
('evt_1787716378578_wel38', 'match_1787716319484', 0, 0, '22:52:58', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 0-0]'),
('evt_1787716378818_73e70', 'match_1787716319484', 0, 0, '22:52:58', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 15-0]'),
('evt_1787716379033_r3smh', 'match_1787716319484', 0, 0, '22:52:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 30-0]'),
('evt_1787716379251_0vk9n', 'match_1787716319484', 0, 0, '22:52:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 40-0]'),
('evt_1787716379466_gwwti', 'match_1787716319484', 0, 0, '22:52:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 0-0]'),
('evt_1787716379668_ux2tk', 'match_1787716319484', 0, 0, '22:52:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 15-0]'),
('evt_1787716379878_g4bgz', 'match_1787716319484', 0, 0, '22:52:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 30-0]'),
('evt_1787716380140_sga5r', 'match_1787716319484', 0, 0, '22:53:00', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 15-0]'),
('evt_1787716438438_jtzc3', 'match_1787716319484', 0, 0, '22:53:58', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 15-15]'),
('evt_1787716438661_f5c5i', 'match_1787716319484', 0, 0, '22:53:58', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 15-30]'),
('evt_1787716438877_mbens', 'match_1787716319484', 0, 0, '22:53:58', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 15-40]'),
('evt_1787716439085_0pn47', 'match_1787716319484', 0, 0, '22:53:59', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-1 [Pts: 0-0]'),
('evt_1787716439301_5twxf', 'match_1787716319484', 0, 0, '22:53:59', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-1 [Pts: 0-15]'),
('evt_1787716439527_21yas', 'match_1787716319484', 0, 0, '22:53:59', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-1 [Pts: 0-30]'),
('evt_1787716439750_t2ele', 'match_1787716319484', 0, 0, '22:53:59', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-1 [Pts: 0-40]'),
('evt_1787716439974_6p1iq', 'match_1787716319484', 0, 0, '22:53:59', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-2 [Pts: 0-0]'),
('evt_1787716440191_llj9e', 'match_1787716319484', 0, 0, '22:54:00', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-2 [Pts: 0-15]'),
('evt_1787716440408_cjs54', 'match_1787716319484', 0, 0, '22:54:00', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-2 [Pts: 0-30]'),
('evt_1787716440622_ih7ii', 'match_1787716319484', 0, 0, '22:54:00', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-2 [Pts: 0-40]'),
('evt_1787716440823_hw58x', 'match_1787716319484', 0, 0, '22:54:00', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-3 [Pts: 0-0]'),
('evt_1787716441091_51ho3', 'match_1787716319484', 0, 0, '22:54:01', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-3 [Pts: 0-15]'),
('evt_1787716441343_euc29', 'match_1787716319484', 0, 0, '22:54:01', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-3 [Pts: 0-30]'),
('evt_1787716441560_a80hw', 'match_1787716319484', 0, 0, '22:54:01', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-3 [Pts: 0-40]'),
('evt_1787716441767_vq8wz', 'match_1787716319484', 0, 0, '22:54:01', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-4 [Pts: 0-0]'),
('evt_1787716441991_gybpf', 'match_1787716319484', 0, 0, '22:54:01', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-4 [Pts: 0-15]'),
('evt_1787716442207_1n8h7', 'match_1787716319484', 0, 0, '22:54:02', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-4 [Pts: 0-30]'),
('evt_1787716442416_wm165', 'match_1787716319484', 0, 0, '22:54:02', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-4 [Pts: 0-40]'),
('evt_1787716442655_529ix', 'match_1787716319484', 0, 0, '22:54:02', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-5 [Pts: 0-0]'),
('evt_1787716442881_zq6mu', 'match_1787716319484', 0, 0, '22:54:02', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-5 [Pts: 0-15]'),
('evt_1787716443104_aha09', 'match_1787716319484', 0, 0, '22:54:03', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-5 [Pts: 0-30]'),
('evt_1787716443313_bpiuv', 'match_1787716319484', 0, 0, '22:54:03', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-5 [Pts: 0-40]'),
('evt_1787716444440_xssf9', 'match_1787716319484', 0, 0, '22:54:04', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-5 [Pts: 15-40]'),
('evt_1787716444665_pnr1y', 'match_1787716319484', 0, 0, '22:54:04', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-5 [Pts: 30-40]'),
('evt_1787716445057_wnsxm', 'match_1787716319484', 0, 0, '22:54:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-5 [Pts: 40-40]'),
('evt_1787716445281_mcbxe', 'match_1787716319484', 0, 0, '22:54:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-5 [Pts: AD-40]'),
('evt_1787716445564_ck7f9', 'match_1787716319484', 0, 0, '22:54:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-1 [Pts: 15-0]'),
('evt_1787716446012_8pp3z', 'match_1787716319484', 0, 0, '22:54:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-1 [Pts: 30-0]'),
('evt_1787716446242_3lg1d', 'match_1787716319484', 0, 0, '22:54:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-3 [Pts: 15-0]'),
('evt_1787716446443_gdxci', 'match_1787716319484', 0, 0, '22:54:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-4 [Pts: 15-0]'),
('evt_1787716446674_kfwka', 'match_1787716319484', 0, 0, '22:54:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-4 [Pts: 30-0]'),
('evt_1787716446922_6fvxc', 'match_1787716319484', 0, 0, '22:54:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-4 [Pts: 40-0]'),
('evt_1787716447154_jucvw', 'match_1787716319484', 0, 0, '22:54:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 7-4 [Pts: 0-0]'),
('evt_1787716447386_a91vt', 'match_1787716319484', 0, 0, '22:54:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 7-4 [Pts: 15-0]'),
('evt_1787716447618_6lv2q', 'match_1787716319484', 0, 0, '22:54:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 7-4 [Pts: 15-0]'),
('evt_1787716448035_0veoq', 'match_1787716319484', 0, 0, '22:54:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 7-4 [Pts: 30-0]'),
('evt_1787716448292_lotzt', 'match_1787716319484', 0, 0, '22:54:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 7-4 [Pts: 40-0]'),
('evt_1787716448532_gmyqc', 'match_1787716319484', 0, 0, '22:54:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 8-4 [Pts: 0-0]'),
('evt_1787716448771_o63rx', 'match_1787716319484', 0, 0, '22:54:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 8-4 [Pts: 15-0]'),
('evt_1787716449013_9xlv0', 'match_1787716319484', 0, 0, '22:54:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 8-4 [Pts: 15-0]'),
('evt_1787716449246_rl6yf', 'match_1787716319484', 0, 0, '22:54:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 8-4 [Pts: 30-0]'),
('evt_1787716450325_ovhrl', 'match_1787716319484', 0, 0, '22:54:10', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-4 [Pts: 30-15]'),
('evt_1787716450540_64hdj', 'match_1787716319484', 0, 0, '22:54:10', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-4 [Pts: 30-30]'),
('evt_1787716450756_luul4', 'match_1787716319484', 0, 0, '22:54:10', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-4 [Pts: 30-40]'),
('evt_1787716450973_qiucb', 'match_1787716319484', 0, 0, '22:54:10', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-5 [Pts: 0-0]'),
('evt_1787716451190_p7mk0', 'match_1787716319484', 0, 0, '22:54:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-5 [Pts: 0-15]'),
('evt_1787716451412_t8un6', 'match_1787716319484', 0, 0, '22:54:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-5 [Pts: 0-30]'),
('evt_1787716451654_s70hb', 'match_1787716319484', 0, 0, '22:54:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-5 [Pts: 0-15]'),
('evt_1787716451878_vp3tx', 'match_1787716319484', 0, 0, '22:54:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-5 [Pts: 0-30]'),
('evt_1787716452102_5j0l1', 'match_1787716319484', 0, 0, '22:54:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-5 [Pts: 0-40]'),
('evt_1787716452333_7okfj', 'match_1787716319484', 0, 0, '22:54:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-6 [Pts: 0-0]'),
('evt_1787716452549_xejqk', 'match_1787716319484', 0, 0, '22:54:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-6 [Pts: 0-15]'),
('evt_1787716452766_0parh', 'match_1787716319484', 0, 0, '22:54:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-6 [Pts: 0-30]'),
('evt_1787716452989_7jwi8', 'match_1787716319484', 0, 0, '22:54:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-6 [Pts: 0-15]'),
('evt_1787716453197_rfbhs', 'match_1787716319484', 0, 0, '22:54:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-6 [Pts: 0-30]'),
('evt_1787716453446_jax19', 'match_1787716319484', 0, 0, '22:54:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-6 [Pts: 0-40]'),
('evt_1787716453677_rbwpc', 'match_1787716319484', 0, 0, '22:54:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-7 [Pts: 0-0]'),
('evt_1787716453917_bg0rf', 'match_1787716319484', 0, 0, '22:54:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-7 [Pts: 0-15]'),
('evt_1787716454133_5guh1', 'match_1787716319484', 0, 0, '22:54:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-7 [Pts: 0-30]'),
('evt_1787716454383_giktk', 'match_1787716319484', 0, 0, '22:54:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-7 [Pts: 0-40]'),
('evt_1787716454598_sct42', 'match_1787716319484', 0, 0, '22:54:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-8 [Pts: 0-0]'),
('evt_1787716454847_jc0jg', 'match_1787716319484', 0, 0, '22:54:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-8 [Pts: 0-15]'),
('evt_1787716455128_9lx2p', 'match_1787716319484', 0, 0, '22:54:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-8 [Pts: 0-30]'),
('evt_1787716455382_zykdy', 'match_1787716319484', 0, 0, '22:54:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-8 [Pts: 0-40]'),
('evt_1787716455599_gao9i', 'match_1787716319484', 0, 0, '22:54:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-9 [Pts: 0-0]'),
('evt_1787716455824_667q6', 'match_1787716319484', 0, 0, '22:54:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-9 [Pts: 0-15]'),
('evt_1787716456039_i1nbi', 'match_1787716319484', 0, 0, '22:54:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-9 [Pts: 0-30]'),
('evt_1787716456256_hslza', 'match_1787716319484', 0, 0, '22:54:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-9 [Pts: 0-40]'),
('evt_1787716456472_fwv3a', 'match_1787716319484', 0, 0, '22:54:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-0 [Pts: 0-0]'),
('evt_1787716456703_o1en1', 'match_1787716319484', 0, 0, '22:54:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-0 [Pts: 0-15]'),
('evt_1787716456912_cfe41', 'match_1787716319484', 0, 0, '22:54:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-0 [Pts: 0-30]'),
('evt_1787716457160_a3z2t', 'match_1787716319484', 0, 0, '22:54:17', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-0 [Pts: 0-40]'),
('evt_1787716457392_knzha', 'match_1787716319484', 0, 0, '22:54:17', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-1 [Pts: 0-0]'),
('evt_1787716457648_9msx9', 'match_1787716319484', 0, 0, '22:54:17', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-1 [Pts: 0-15]'),
('evt_1787716457897_rq1ze', 'match_1787716319484', 0, 0, '22:54:17', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-1 [Pts: 0-30]'),
('evt_1787716458209_edaei', 'match_1787716319484', 0, 0, '22:54:18', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-1 [Pts: 0-40]'),
('evt_1787716458497_bk9p7', 'match_1787716319484', 0, 0, '22:54:18', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-2 [Pts: 0-0]'),
('evt_1787716458728_ufaao', 'match_1787716319484', 0, 0, '22:54:18', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-2 [Pts: 0-15]'),
('evt_1787716458946_ua18d', 'match_1787716319484', 0, 0, '22:54:18', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-2 [Pts: 0-30]'),
('evt_1787716459170_eo592', 'match_1787716319484', 0, 0, '22:54:19', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-2 [Pts: 0-40]'),
('evt_1787716459400_asc63', 'match_1787716319484', 0, 0, '22:54:19', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-3 [Pts: 0-0]'),
('evt_1787716459602_7ix09', 'match_1787716319484', 0, 0, '22:54:19', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-3 [Pts: 0-15]'),
('evt_1787716459833_o1jea', 'match_1787716319484', 0, 0, '22:54:19', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-3 [Pts: 0-30]'),
('evt_1787716460050_7bokc', 'match_1787716319484', 0, 0, '22:54:20', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-3 [Pts: 0-40]'),
('evt_1787716460265_fu9uw', 'match_1787716319484', 0, 0, '22:54:20', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-4 [Pts: 0-0]'),
('evt_1787716460491_laz7d', 'match_1787716319484', 0, 0, '22:54:20', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-4 [Pts: 0-15]'),
('evt_1787716460705_7mwhm', 'match_1787716319484', 0, 0, '22:54:20', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-4 [Pts: 0-30]'),
('evt_1787716460930_6tawh', 'match_1787716319484', 0, 0, '22:54:20', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-4 [Pts: 0-40]'),
('evt_1787716461145_z28ab', 'match_1787716319484', 0, 0, '22:54:21', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-5 [Pts: 0-0]'),
('evt_1787716461369_94qi8', 'match_1787716319484', 0, 0, '22:54:21', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-5 [Pts: 0-15]'),
('evt_1787716461594_u4k9c', 'match_1787716319484', 0, 0, '22:54:21', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-5 [Pts: 0-30]'),
('evt_1787716461829_1sp6i', 'match_1787716319484', 0, 0, '22:54:21', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-5 [Pts: 0-40]'),
('evt_1787716462034_bdeb6', 'match_1787716319484', 0, 0, '22:54:22', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-6 [Pts: 0-0]'),
('evt_1787716462252_uxfzz', 'match_1787716319484', 0, 0, '22:54:22', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-6 [Pts: 0-15]'),
('evt_1787716462492_41wfz', 'match_1787716319484', 0, 0, '22:54:22', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-6 [Pts: 0-15]'),
('evt_1787716462796_b21v9', 'match_1787716319484', 0, 0, '22:54:22', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-6 [Pts: 0-30]'),
('evt_1787716463027_t14xd', 'match_1787716319484', 0, 0, '22:54:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-6 [Pts: 0-40]'),
('evt_1787716463266_q8xvv', 'match_1787716319484', 0, 0, '22:54:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-7 [Pts: 0-0]'),
('evt_1787716463523_h9ydp', 'match_1787716319484', 0, 0, '22:54:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-7 [Pts: 0-15]'),
('evt_1787716463757_lfq3j', 'match_1787716319484', 0, 0, '22:54:23', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-7 [Pts: 0-15]'),
('evt_1787716464068_3km85', 'match_1787716319484', 0, 0, '22:54:24', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-7 [Pts: 0-30]'),
('evt_1787716467773_0f6n7', 'match_1787716319484', 0, 0, '22:54:27', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-7 [Pts: 0-40]'),
('evt_1787716468300_8pz9q', 'match_1787716319484', 0, 0, '22:54:28', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 8-10 | S3: 0-8 [Pts: 0-0]'),
('evt_1787717944984_iiczv', 'match_1787717933638', 0, 0, '23:19:04', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787717946375_eyis2', 'match_1787717933638', 0, 0, '23:19:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787717947494_lub8t', 'match_1787717933638', 0, 0, '23:19:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787717947774_w1fd9', 'match_1787717933638', 0, 0, '23:19:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 40-15]'),
('evt_1787717947982_32b6r', 'match_1787717933638', 0, 0, '23:19:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 0-0]'),
('evt_1787717948181_r8j92', 'match_1787717933638', 0, 0, '23:19:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 15-0]'),
('evt_1787717948406_5fhrh', 'match_1787717933638', 0, 0, '23:19:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-0]'),
('evt_1787717948598_gyamc', 'match_1787717933638', 0, 0, '23:19:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 40-0]'),
('evt_1787717948806_ezyuf', 'match_1787717933638', 0, 0, '23:19:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 0-0]'),
('evt_1787717949015_rte63', 'match_1787717933638', 0, 0, '23:19:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 15-0]'),
('evt_1787717949246_4w4o9', 'match_1787717933638', 0, 0, '23:19:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 30-0]'),
('evt_1787717949463_mg4ue', 'match_1787717933638', 0, 0, '23:19:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 40-0]'),
('evt_1787717949749_oqj20', 'match_1787717933638', 0, 0, '23:19:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 0-0]'),
('evt_1787717949982_pm7d6', 'match_1787717933638', 0, 0, '23:19:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 15-0]'),
('evt_1787717950197_hsddr', 'match_1787717933638', 0, 0, '23:19:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 30-0]'),
('evt_1787717950406_v9ema', 'match_1787717933638', 0, 0, '23:19:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 40-0]'),
('evt_1787717950645_1rn4t', 'match_1787717933638', 0, 0, '23:19:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 0-0]'),
('evt_1787717950885_rjszg', 'match_1787717933638', 0, 0, '23:19:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 15-0]'),
('evt_1787717951478_rvfoq', 'match_1787717933638', 0, 0, '23:19:11', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 30-0]'),
('evt_1787717952358_hqjsk', 'match_1787717933638', 0, 0, '23:19:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-0 [Pts: 30-15]'),
('evt_1787717952559_unhsx', 'match_1787717933638', 0, 0, '23:19:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-0 [Pts: 30-30]'),
('evt_1787717952782_fegke', 'match_1787717933638', 0, 0, '23:19:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-0 [Pts: 30-40]'),
('evt_1787717952981_n8gky', 'match_1787717933638', 0, 0, '23:19:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 0-0]'),
('evt_1787717953191_u4m48', 'match_1787717933638', 0, 0, '23:19:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 0-15]'),
('evt_1787717953391_mp15h', 'match_1787717933638', 0, 0, '23:19:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 0-30]'),
('evt_1787717953598_vefw5', 'match_1787717933638', 0, 0, '23:19:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 0-40]'),
('evt_1787717953909_75kek', 'match_1787717933638', 0, 0, '23:19:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-0]'),
('evt_1787717954114_3zdep', 'match_1787717933638', 0, 0, '23:19:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-15]'),
('evt_1787717954318_7nnuj', 'match_1787717933638', 0, 0, '23:19:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-30]'),
('evt_1787717954527_xm7oy', 'match_1787717933638', 0, 0, '23:19:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-40]'),
('evt_1787717954798_wvb22', 'match_1787717933638', 0, 0, '23:19:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-3 [Pts: 0-0]'),
('evt_1787717955014_m8npf', 'match_1787717933638', 0, 0, '23:19:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-3 [Pts: 0-15]'),
('evt_1787717955246_okwjj', 'match_1787717933638', 0, 0, '23:19:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-3 [Pts: 0-30]'),
('evt_1787717955454_likmz', 'match_1787717933638', 0, 0, '23:19:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-3 [Pts: 0-40]'),
('evt_1787717955663_4soi8', 'match_1787717933638', 0, 0, '23:19:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-4 [Pts: 0-0]'),
('evt_1787717955878_goe4f', 'match_1787717933638', 0, 0, '23:19:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-4 [Pts: 0-15]'),
('evt_1787717956085_y1uc7', 'match_1787717933638', 0, 0, '23:19:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-4 [Pts: 0-30]'),
('evt_1787717956301_jji3t', 'match_1787717933638', 0, 0, '23:19:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-4 [Pts: 0-40]'),
('evt_1787717956510_rofa6', 'match_1787717933638', 0, 0, '23:19:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-5 [Pts: 0-0]'),
('evt_1787717956725_cgn61', 'match_1787717933638', 0, 0, '23:19:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-5 [Pts: 0-15]'),
('evt_1787717956934_deu6p', 'match_1787717933638', 0, 0, '23:19:16', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-5 [Pts: 0-30]'),
('evt_1787717957150_mmsug', 'match_1787717933638', 0, 0, '23:19:17', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-5 [Pts: 0-40]');
INSERT INTO `match_events` (`id`, `match_id`, `set_number`, `game_number`, `timestamp`, `winning_pair_id`, `player_id`, `player_name`, `event_type`, `description`, `score_snapshot`) VALUES
('evt_1787717957335_t36o6', 'match_1787717933638', 0, 0, '23:19:17', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-6 | S2: 0-0 [Pts: 0-0]'),
('evt_1787717957615_xuoin', 'match_1787717933638', 0, 0, '23:19:17', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-6 | S2: 0-0 [Pts: 0-15]'),
('evt_1787717958742_s98w8', 'match_1787717933638', 0, 0, '23:19:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 0-0 [Pts: 15-15]'),
('evt_1787717958958_x3tiu', 'match_1787717933638', 0, 0, '23:19:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 0-0 [Pts: 30-15]'),
('evt_1787717959150_n3utb', 'match_1787717933638', 0, 0, '23:19:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 0-0 [Pts: 40-15]'),
('evt_1787717959390_e5uli', 'match_1787717933638', 0, 0, '23:19:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 1-0 [Pts: 0-0]'),
('evt_1787717959598_lwi2v', 'match_1787717933638', 0, 0, '23:19:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 1-0 [Pts: 15-0]'),
('evt_1787717959814_ns613', 'match_1787717933638', 0, 0, '23:19:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 1-0 [Pts: 30-0]'),
('evt_1787717960031_js8us', 'match_1787717933638', 0, 0, '23:19:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 1-0 [Pts: 40-0]'),
('evt_1787717960246_u7ygc', 'match_1787717933638', 0, 0, '23:19:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 2-0 [Pts: 0-0]'),
('evt_1787717960461_oscr9', 'match_1787717933638', 0, 0, '23:19:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 2-0 [Pts: 15-0]'),
('evt_1787717960678_4b3t9', 'match_1787717933638', 0, 0, '23:19:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 2-0 [Pts: 30-0]'),
('evt_1787717960895_soo2y', 'match_1787717933638', 0, 0, '23:19:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 2-0 [Pts: 40-0]'),
('evt_1787717961110_134n2', 'match_1787717933638', 0, 0, '23:19:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 3-0 [Pts: 0-0]'),
('evt_1787717961319_ubdhv', 'match_1787717933638', 0, 0, '23:19:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 3-0 [Pts: 15-0]'),
('evt_1787717961542_nrqd0', 'match_1787717933638', 0, 0, '23:19:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 3-0 [Pts: 30-0]'),
('evt_1787717961743_g4zcb', 'match_1787717933638', 0, 0, '23:19:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 3-0 [Pts: 40-0]'),
('evt_1787717961959_uus40', 'match_1787717933638', 0, 0, '23:19:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 4-0 [Pts: 0-0]'),
('evt_1787717962190_tdh3w', 'match_1787717933638', 0, 0, '23:19:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 4-0 [Pts: 15-0]'),
('evt_1787717962406_86ee5', 'match_1787717933638', 0, 0, '23:19:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 4-0 [Pts: 30-0]'),
('evt_1787717962646_6oxs2', 'match_1787717933638', 0, 0, '23:19:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 4-0 [Pts: 40-0]'),
('evt_1787717962862_huzvi', 'match_1787717933638', 0, 0, '23:19:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 5-0 [Pts: 0-0]'),
('evt_1787717963079_urf5d', 'match_1787717933638', 0, 0, '23:19:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 5-0 [Pts: 15-0]'),
('evt_1787717963648_58frv', 'match_1787717933638', 0, 0, '23:19:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 5-0 [Pts: 30-0]'),
('evt_1787717964118_gqo9z', 'match_1787717933638', 0, 0, '23:19:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 5-0 [Pts: 40-0]'),
('evt_1787717964526_36gm1', 'match_1787717933638', 0, 0, '23:19:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787717966558_e0izu', 'match_1787717933638', 0, 0, '23:19:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787717966870_zymbc', 'match_1787717933638', 0, 0, '23:19:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787717967103_ucwvl', 'match_1787717933638', 0, 0, '23:19:27', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787717967319_5hqcb', 'match_1787717933638', 0, 0, '23:19:27', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 1-0 [Pts: 0-0]'),
('evt_1787717967583_e49fx', 'match_1787717933638', 0, 0, '23:19:27', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 1-0 [Pts: 15-0]'),
('evt_1787717967896_qbvcy', 'match_1787717933638', 0, 0, '23:19:27', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 1-0 [Pts: 30-0]'),
('evt_1787717968110_etmv1', 'match_1787717933638', 0, 0, '23:19:28', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 1-0 [Pts: 40-0]'),
('evt_1787717968328_qz0z5', 'match_1787717933638', 0, 0, '23:19:28', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 2-0 [Pts: 0-0]'),
('evt_1787717968542_pjysy', 'match_1787717933638', 0, 0, '23:19:28', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 2-0 [Pts: 15-0]'),
('evt_1787717968814_4usf5', 'match_1787717933638', 0, 0, '23:19:28', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 2-0 [Pts: 30-0]'),
('evt_1787717969134_2i6h5', 'match_1787717933638', 0, 0, '23:19:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 2-0 [Pts: 40-0]'),
('evt_1787717969366_ivn6t', 'match_1787717933638', 0, 0, '23:19:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 3-0 [Pts: 0-0]'),
('evt_1787717969662_tj4iu', 'match_1787717933638', 0, 0, '23:19:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 3-0 [Pts: 15-0]'),
('evt_1787717969991_4e6dw', 'match_1787717933638', 0, 0, '23:19:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 3-0 [Pts: 30-0]'),
('evt_1787717970375_e3m8m', 'match_1787717933638', 0, 0, '23:19:30', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 3-0 [Pts: 40-0]'),
('evt_1787717970682_kvyxe', 'match_1787717933638', 0, 0, '23:19:30', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 4-0 [Pts: 0-0]'),
('evt_1787717970913_b9x6i', 'match_1787717933638', 0, 0, '23:19:30', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 4-0 [Pts: 15-0]'),
('evt_1787717971166_uvm81', 'match_1787717933638', 0, 0, '23:19:31', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 4-0 [Pts: 30-0]'),
('evt_1787717971391_a57jq', 'match_1787717933638', 0, 0, '23:19:31', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 4-0 [Pts: 40-0]'),
('evt_1787717971623_gl1ge', 'match_1787717933638', 0, 0, '23:19:31', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 5-0 [Pts: 0-0]'),
('evt_1787717971863_lf991', 'match_1787717933638', 0, 0, '23:19:31', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 5-0 [Pts: 15-0]'),
('evt_1787717972111_nic3b', 'match_1787717933638', 0, 0, '23:19:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 5-0 [Pts: 30-0]'),
('evt_1787717972398_v6xf7', 'match_1787717933638', 0, 0, '23:19:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 5-0 [Pts: 40-0]'),
('evt_1787717972743_e335j', 'match_1787717933638', 0, 0, '23:19:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-6 | S2: 6-0 | S3: 6-0 [Pts: 0-0]'),
('evt_1787718100805_kb41b', 'match_1787718088212', 0, 0, '23:21:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 0-15]'),
('evt_1787718101846_eo97a', 'match_1787718088212', 0, 0, '23:21:41', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787718102084_o9k1r', 'match_1787718088212', 0, 0, '23:21:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787718102781_2zs03', 'match_1787718088212', 0, 0, '23:21:42', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 30-30]'),
('evt_1787718103035_7o79u', 'match_1787718088212', 0, 0, '23:21:43', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 30-40]'),
('evt_1787718103235_g4yo2', 'match_1787718088212', 0, 0, '23:21:43', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-0]'),
('evt_1787718103436_t6pvz', 'match_1787718088212', 0, 0, '23:21:43', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-15]'),
('evt_1787718103668_pt6on', 'match_1787718088212', 0, 0, '23:21:43', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-30]'),
('evt_1787718103867_jn4ay', 'match_1787718088212', 0, 0, '23:21:43', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-40]'),
('evt_1787718104076_qisjv', 'match_1787718088212', 0, 0, '23:21:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-2 [Pts: 0-0]'),
('evt_1787718104284_yoeey', 'match_1787718088212', 0, 0, '23:21:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-2 [Pts: 0-15]'),
('evt_1787718104500_5cfzz', 'match_1787718088212', 0, 0, '23:21:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-2 [Pts: 0-30]'),
('evt_1787718104699_a83xp', 'match_1787718088212', 0, 0, '23:21:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-2 [Pts: 0-40]'),
('evt_1787718104906_r3mo8', 'match_1787718088212', 0, 0, '23:21:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-3 [Pts: 0-0]'),
('evt_1787718105115_tfn4l', 'match_1787718088212', 0, 0, '23:21:45', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-3 [Pts: 0-15]'),
('evt_1787718105698_rbnqr', 'match_1787718088212', 0, 0, '23:21:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-3 [Pts: 15-15]'),
('evt_1787718106219_ftsht', 'match_1787718088212', 0, 0, '23:21:46', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-3 [Pts: 15-30]'),
('evt_1787718106442_3a4x1', 'match_1787718088212', 0, 0, '23:21:46', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-3 [Pts: 15-40]'),
('evt_1787718106659_dqpro', 'match_1787718088212', 0, 0, '23:21:46', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-4 [Pts: 0-0]'),
('evt_1787718106852_i5hqq', 'match_1787718088212', 0, 0, '23:21:46', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-4 [Pts: 0-15]'),
('evt_1787718107107_hsjdy', 'match_1787718088212', 0, 0, '23:21:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-4 [Pts: 0-30]'),
('evt_1787718107298_irola', 'match_1787718088212', 0, 0, '23:21:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-4 [Pts: 0-40]'),
('evt_1787718107507_mp4o6', 'match_1787718088212', 0, 0, '23:21:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-5 [Pts: 0-0]'),
('evt_1787718107714_q6ybq', 'match_1787718088212', 0, 0, '23:21:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-5 [Pts: 0-15]'),
('evt_1787718107923_via8j', 'match_1787718088212', 0, 0, '23:21:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-5 [Pts: 0-30]'),
('evt_1787718108137_57k4m', 'match_1787718088212', 0, 0, '23:21:48', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-5 [Pts: 0-40]'),
('evt_1787718108353_vf5ir', 'match_1787718088212', 0, 0, '23:21:48', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 0-0 [Pts: 0-0]'),
('evt_1787718108560_hxelm', 'match_1787718088212', 0, 0, '23:21:48', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 0-0 [Pts: 0-15]'),
('evt_1787718109330_0po5f', 'match_1787718088212', 0, 0, '23:21:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 0-0 [Pts: 15-15]'),
('evt_1787718109569_doabc', 'match_1787718088212', 0, 0, '23:21:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 0-0 [Pts: 30-15]'),
('evt_1787718109759_1ktut', 'match_1787718088212', 0, 0, '23:21:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 0-0 [Pts: 40-15]'),
('evt_1787718109976_rupln', 'match_1787718088212', 0, 0, '23:21:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 1-0 [Pts: 0-0]'),
('evt_1787718110185_fzma6', 'match_1787718088212', 0, 0, '23:21:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 1-0 [Pts: 15-0]'),
('evt_1787718110392_0hkgq', 'match_1787718088212', 0, 0, '23:21:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 1-0 [Pts: 30-0]'),
('evt_1787718110607_llbv7', 'match_1787718088212', 0, 0, '23:21:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 1-0 [Pts: 40-0]'),
('evt_1787718110816_sbz02', 'match_1787718088212', 0, 0, '23:21:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 2-0 [Pts: 0-0]'),
('evt_1787718111024_j1way', 'match_1787718088212', 0, 0, '23:21:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 2-0 [Pts: 15-0]'),
('evt_1787718111239_z89t1', 'match_1787718088212', 0, 0, '23:21:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 2-0 [Pts: 30-0]'),
('evt_1787718111455_7ch7v', 'match_1787718088212', 0, 0, '23:21:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 2-0 [Pts: 40-0]'),
('evt_1787718111671_lpmow', 'match_1787718088212', 0, 0, '23:21:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 3-0 [Pts: 0-0]'),
('evt_1787718111895_wx86y', 'match_1787718088212', 0, 0, '23:21:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 3-0 [Pts: 15-0]'),
('evt_1787718112146_iire0', 'match_1787718088212', 0, 0, '23:21:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-6 | S2: 3-0 [Pts: 30-0]'),
('evt_1787718112646_88dwe', 'match_1787718088212', 0, 0, '23:21:52', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-0 [Pts: 30-15]'),
('evt_1787718112872_mnn8c', 'match_1787718088212', 0, 0, '23:21:52', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-0 [Pts: 30-30]'),
('evt_1787718113095_senuj', 'match_1787718088212', 0, 0, '23:21:53', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-0 [Pts: 30-40]'),
('evt_1787718113287_mus9e', 'match_1787718088212', 0, 0, '23:21:53', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-1 [Pts: 0-0]'),
('evt_1787718113495_lzadf', 'match_1787718088212', 0, 0, '23:21:53', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-1 [Pts: 0-15]'),
('evt_1787718113703_epgbl', 'match_1787718088212', 0, 0, '23:21:53', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-1 [Pts: 0-30]'),
('evt_1787718113926_zqj0b', 'match_1787718088212', 0, 0, '23:21:53', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-1 [Pts: 0-40]'),
('evt_1787718114126_4t3ip', 'match_1787718088212', 0, 0, '23:21:54', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-2 [Pts: 0-0]'),
('evt_1787718114343_c5yan', 'match_1787718088212', 0, 0, '23:21:54', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-2 [Pts: 0-15]'),
('evt_1787718114549_n63he', 'match_1787718088212', 0, 0, '23:21:54', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-2 [Pts: 0-30]'),
('evt_1787718114757_5cg2o', 'match_1787718088212', 0, 0, '23:21:54', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-2 [Pts: 0-40]'),
('evt_1787718114965_u6zyq', 'match_1787718088212', 0, 0, '23:21:54', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-3 [Pts: 0-0]'),
('evt_1787718115183_ku6s2', 'match_1787718088212', 0, 0, '23:21:55', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-3 [Pts: 0-15]'),
('evt_1787718115389_vje8x', 'match_1787718088212', 0, 0, '23:21:55', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-3 [Pts: 0-30]'),
('evt_1787718115616_qzaq0', 'match_1787718088212', 0, 0, '23:21:55', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-3 [Pts: 0-40]'),
('evt_1787718115823_dcx8k', 'match_1787718088212', 0, 0, '23:21:55', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-4 [Pts: 0-0]'),
('evt_1787718116037_q110l', 'match_1787718088212', 0, 0, '23:21:56', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-4 [Pts: 0-15]'),
('evt_1787718116262_xif22', 'match_1787718088212', 0, 0, '23:21:56', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-4 [Pts: 0-30]'),
('evt_1787718116478_rsmct', 'match_1787718088212', 0, 0, '23:21:56', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-4 [Pts: 0-40]'),
('evt_1787718116694_tx9az', 'match_1787718088212', 0, 0, '23:21:56', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-5 [Pts: 0-0]'),
('evt_1787718116916_pycsx', 'match_1787718088212', 0, 0, '23:21:56', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-5 [Pts: 0-15]'),
('evt_1787718117132_k3f8s', 'match_1787718088212', 0, 0, '23:21:57', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-5 [Pts: 0-30]'),
('evt_1787718117341_1knxr', 'match_1787718088212', 0, 0, '23:21:57', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-5 [Pts: 0-40]'),
('evt_1787718117629_sf0js', 'match_1787718088212', 0, 0, '23:21:57', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-6 | S2: 3-6 [Pts: 0-0]'),
('evt_1787719742888_tgm6o', 'match_1787719723180', 0, 0, '23:49:02', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787719744435_haijs', 'match_1787719723180', 0, 0, '23:49:04', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787719745386_xh0no', 'match_1787719723180', 0, 0, '23:49:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787719745835_3emyv', 'match_1787719723180', 0, 0, '23:49:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 40-15]'),
('evt_1787719746058_lgcco', 'match_1787719723180', 0, 0, '23:49:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 0-0]'),
('evt_1787719746651_mjpwb', 'match_1787719723180', 0, 0, '23:49:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-0 [Pts: 0-15]'),
('evt_1787719746874_giak7', 'match_1787719723180', 0, 0, '23:49:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-0 [Pts: 0-30]'),
('evt_1787719748106_se4p7', 'match_1787719723180', 0, 0, '23:49:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 15-30]'),
('evt_1787719748353_xyhbp', 'match_1787719723180', 0, 0, '23:49:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-30]'),
('evt_1787719748586_gn5p8', 'match_1787719723180', 0, 0, '23:49:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 40-30]'),
('evt_1787719748842_lvgxo', 'match_1787719723180', 0, 0, '23:49:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 0-0]'),
('evt_1787719749058_ppu5f', 'match_1787719723180', 0, 0, '23:49:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 15-0]'),
('evt_1787719749337_fxm3w', 'match_1787719723180', 0, 0, '23:49:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 30-0]'),
('evt_1787719750410_7tau4', 'match_1787719723180', 0, 0, '23:49:10', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 30-15]'),
('evt_1787719750618_zjrdq', 'match_1787719723180', 0, 0, '23:49:10', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 30-30]'),
('evt_1787719750875_0wnrh', 'match_1787719723180', 0, 0, '23:49:10', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 30-40]'),
('evt_1787719751097_gu2ht', 'match_1787719723180', 0, 0, '23:49:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-0]'),
('evt_1787719751305_po5kj', 'match_1787719723180', 0, 0, '23:49:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-15]'),
('evt_1787719751505_r90sf', 'match_1787719723180', 0, 0, '23:49:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-30]'),
('evt_1787719751705_lmvox', 'match_1787719723180', 0, 0, '23:49:11', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-40]'),
('evt_1787719752296_n8bjm', 'match_1787719723180', 0, 0, '23:49:12', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 15-40]'),
('evt_1787719752520_4gfe6', 'match_1787719723180', 0, 0, '23:49:12', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 30-40]'),
('evt_1787719752705_oo8c1', 'match_1787719723180', 0, 0, '23:49:12', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 40-40]'),
('evt_1787719752927_6l7x8', 'match_1787719723180', 0, 0, '23:49:12', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: AD-40]'),
('evt_1787719753136_vu5ql', 'match_1787719723180', 0, 0, '23:49:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 0-0]'),
('evt_1787719753368_c39sv', 'match_1787719723180', 0, 0, '23:49:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 15-0]'),
('evt_1787719753608_kkla9', 'match_1787719723180', 0, 0, '23:49:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 30-0]'),
('evt_1787719753848_08j5v', 'match_1787719723180', 0, 0, '23:49:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 40-0]'),
('evt_1787719754064_vclvx', 'match_1787719723180', 0, 0, '23:49:14', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-1 [Pts: 0-0]'),
('evt_1787719754385_vk729', 'match_1787719723180', 0, 0, '23:49:14', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-1 [Pts: 15-0]'),
('evt_1787719754959_wsbag', 'match_1787719723180', 0, 0, '23:49:14', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 15-15]'),
('evt_1787719755175_065x1', 'match_1787719723180', 0, 0, '23:49:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 15-30]'),
('evt_1787719755383_an8yq', 'match_1787719723180', 0, 0, '23:49:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 15-40]'),
('evt_1787719755599_logpg', 'match_1787719723180', 0, 0, '23:49:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-0]'),
('evt_1787719755823_iw39t', 'match_1787719723180', 0, 0, '23:49:15', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-15]'),
('evt_1787719756736_u4nuy', 'match_1787719723180', 0, 0, '23:49:16', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 15-15]'),
('evt_1787719756990_ulu9k', 'match_1787719723180', 0, 0, '23:49:16', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 30-15]'),
('evt_1787719757215_axdts', 'match_1787719723180', 0, 0, '23:49:17', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 40-15]'),
('evt_1787719757472_kew16', 'match_1787719723180', 0, 0, '23:49:17', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 0-0]'),
('evt_1787719757711_6ersx', 'match_1787719723180', 0, 0, '23:49:17', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 15-0]'),
('evt_1787719757936_ejoz3', 'match_1787719723180', 0, 0, '23:49:17', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 30-0]'),
('evt_1787719758142_3yvhq', 'match_1787719723180', 0, 0, '23:49:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 40-0]'),
('evt_1787719758390_mq3d7', 'match_1787719723180', 0, 0, '23:49:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 0-0]'),
('evt_1787719758606_0fglf', 'match_1787719723180', 0, 0, '23:49:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 15-0]'),
('evt_1787719759118_byn0u', 'match_1787719723180', 0, 0, '23:49:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 30-0]'),
('evt_1787719759358_fkwie', 'match_1787719723180', 0, 0, '23:49:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 40-0]'),
('evt_1787719759654_vgdxd', 'match_1787719723180', 0, 0, '23:49:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 0-0]'),
('evt_1787719759999_x9yjl', 'match_1787719723180', 0, 0, '23:49:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 15-0]'),
('evt_1787719760271_cdwbw', 'match_1787719723180', 0, 0, '23:49:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 30-0]'),
('evt_1787719760673_vj54o', 'match_1787719723180', 0, 0, '23:49:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 40-0]'),
('evt_1787719764335_ng0v4', 'match_1787719723180', 0, 0, '23:49:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 0-0]'),
('evt_1787719764958_t7urt', 'match_1787719723180', 0, 0, '23:49:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 15-0]'),
('evt_1787719765191_4zg2s', 'match_1787719723180', 0, 0, '23:49:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 30-0]'),
('evt_1787719765471_hgxla', 'match_1787719723180', 0, 0, '23:49:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 40-0]'),
('evt_1787719766046_vwm12', 'match_1787719723180', 0, 0, '23:49:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 0-0]'),
('evt_1787719766549_ndwup', 'match_1787719723180', 0, 0, '23:49:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 15-0]'),
('evt_1787719766790_893la', 'match_1787719723180', 0, 0, '23:49:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 30-0]'),
('evt_1787719767012_uyvso', 'match_1787719723180', 0, 0, '23:49:27', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 40-0]'),
('evt_1787719767229_m0g5l', 'match_1787719723180', 0, 0, '23:49:27', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 0-0]'),
('evt_1787719767901_vkx9o', 'match_1787719723180', 0, 0, '23:49:27', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 15-0]'),
('evt_1787719768919_iylyy', 'match_1787719723180', 0, 0, '23:49:28', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 15-15]'),
('evt_1787719769124_lozn2', 'match_1787719723180', 0, 0, '23:49:29', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 15-30]'),
('evt_1787719769333_ztgry', 'match_1787719723180', 0, 0, '23:49:29', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 15-40]'),
('evt_1787719770246_togox', 'match_1787719723180', 0, 0, '23:49:30', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-1 [Pts: 0-0]'),
('evt_1787719770468_g4fgk', 'match_1787719723180', 0, 0, '23:49:30', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-1 [Pts: 0-15]'),
('evt_1787719770652_upvrq', 'match_1787719723180', 0, 0, '23:49:30', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-1 [Pts: 0-30]'),
('evt_1787719771458_l3cmt', 'match_1787719723180', 0, 0, '23:49:31', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-1 [Pts: 15-30]'),
('evt_1787719771690_y6u4b', 'match_1787719723180', 0, 0, '23:49:31', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-1 [Pts: 30-30]'),
('evt_1787719771916_xnego', 'match_1787719723180', 0, 0, '23:49:31', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-1 [Pts: 40-30]'),
('evt_1787719772133_28q56', 'match_1787719723180', 0, 0, '23:49:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-1 [Pts: 0-0]'),
('evt_1787719772411_ubnxd', 'match_1787719723180', 0, 0, '23:49:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-1 [Pts: 15-0]'),
('evt_1787719772732_qybh9', 'match_1787719723180', 0, 0, '23:49:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-1 [Pts: 30-0]'),
('evt_1787719772963_5dtqp', 'match_1787719723180', 0, 0, '23:49:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-1 [Pts: 40-0]'),
('evt_1787719773210_lox60', 'match_1787719723180', 0, 0, '23:49:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-1 [Pts: 0-0]'),
('evt_1787720531892_npknw', 'match_1787720522428', 0, 0, '00:02:11', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787720532740_3ls41', 'match_1787720522428', 0, 0, '00:02:12', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787720533370_hjsly', 'match_1787720522428', 0, 0, '00:02:13', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787720533891_q7kf2', 'match_1787720522428', 0, 0, '00:02:13', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-30]'),
('evt_1787720534401_hastz', 'match_1787720522428', 0, 0, '00:02:14', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 40-30]'),
('evt_1787720534601_ggj86', 'match_1787720522428', 0, 0, '00:02:14', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-0 [Pts: 0-0]'),
('evt_1787720534802_nh3ne', 'match_1787720522428', 0, 0, '00:02:14', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-0 [Pts: 15-0]'),
('evt_1787720535051_gr5k1', 'match_1787720522428', 0, 0, '00:02:15', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-0 [Pts: 30-0]'),
('evt_1787720535874_h0svx', 'match_1787720522428', 0, 0, '00:02:15', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-15]'),
('evt_1787720536140_14e1o', 'match_1787720522428', 0, 0, '00:02:16', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-30]'),
('evt_1787720536346_o70o5', 'match_1787720522428', 0, 0, '00:02:16', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-40]'),
('evt_1787720536597_bzwn4', 'match_1787720522428', 0, 0, '00:02:16', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 [Pts: 0-0]'),
('evt_1787720537386_l779h', 'match_1787720522428', 0, 0, '00:02:17', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 [Pts: 15-0]'),
('evt_1787720537611_b0e2f', 'match_1787720522428', 0, 0, '00:02:17', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 [Pts: 30-0]'),
('evt_1787720537811_b3mor', 'match_1787720522428', 0, 0, '00:02:17', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 [Pts: 40-0]'),
('evt_1787720538018_zpigg', 'match_1787720522428', 0, 0, '00:02:18', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-0]'),
('evt_1787720538210_mm0nk', 'match_1787720522428', 0, 0, '00:02:18', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 15-0]'),
('evt_1787720538410_ozsg5', 'match_1787720522428', 0, 0, '00:02:18', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 30-0]'),
('evt_1787720538842_m8bpm', 'match_1787720522428', 0, 0, '00:02:18', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 40-0]'),
('evt_1787720539075_ev9jp', 'match_1787720522428', 0, 0, '00:02:19', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 0-0]'),
('evt_1787720539385_4uy14', 'match_1787720522428', 0, 0, '00:02:19', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 15-0]'),
('evt_1787720539626_1k6a2', 'match_1787720522428', 0, 0, '00:02:19', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 30-0]'),
('evt_1787720539834_tiu3e', 'match_1787720522428', 0, 0, '00:02:19', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 40-0]'),
('evt_1787720540050_2eyci', 'match_1787720522428', 0, 0, '00:02:20', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 0-0]'),
('evt_1787720540266_gitbe', 'match_1787720522428', 0, 0, '00:02:20', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 15-0]'),
('evt_1787720541257_7g7y6', 'match_1787720522428', 0, 0, '00:02:21', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-1 [Pts: 15-15]'),
('evt_1787720541451_hxblb', 'match_1787720522428', 0, 0, '00:02:21', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-1 [Pts: 15-30]'),
('evt_1787720541652_rkvgt', 'match_1787720522428', 0, 0, '00:02:21', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-1 [Pts: 15-40]'),
('evt_1787720541858_4fozv', 'match_1787720522428', 0, 0, '00:02:21', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 0-0]'),
('evt_1787720542074_tuz7i', 'match_1787720522428', 0, 0, '00:02:22', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 0-15]'),
('evt_1787720542836_fj9gh', 'match_1787720522428', 0, 0, '00:02:22', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 15-15]'),
('evt_1787720543050_kt3rf', 'match_1787720522428', 0, 0, '00:02:23', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 30-15]'),
('evt_1787720543266_5ol6v', 'match_1787720522428', 0, 0, '00:02:23', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 40-15]'),
('evt_1787720543482_ncoza', 'match_1787720522428', 0, 0, '00:02:23', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 5-2 [Pts: 0-0]'),
('evt_1787720543697_kat4y', 'match_1787720522428', 0, 0, '00:02:23', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 5-2 [Pts: 15-0]'),
('evt_1787720543937_18hr9', 'match_1787720522428', 0, 0, '00:02:23', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 5-2 [Pts: 30-0]'),
('evt_1787720544137_ykjaq', 'match_1787720522428', 0, 0, '00:02:24', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 5-2 [Pts: 40-0]'),
('evt_1787720544355_qfwde', 'match_1787720522428', 0, 0, '00:02:24', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 0-0]'),
('evt_1787720544620_uw7tu', 'match_1787720522428', 0, 0, '00:02:24', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 15-0]'),
('evt_1787720545356_5td4o', 'match_1787720522428', 0, 0, '00:02:25', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 15-15]'),
('evt_1787720545562_6nuik', 'match_1787720522428', 0, 0, '00:02:25', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 15-30]'),
('evt_1787720545771_6k5tr', 'match_1787720522428', 0, 0, '00:02:25', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 15-40]'),
('evt_1787720545978_a0p2r', 'match_1787720522428', 0, 0, '00:02:25', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-1 [Pts: 0-0]'),
('evt_1787720546196_x6a4z', 'match_1787720522428', 0, 0, '00:02:26', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-1 [Pts: 0-15]'),
('evt_1787720546403_9iikd', 'match_1787720522428', 0, 0, '00:02:26', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-1 [Pts: 0-30]'),
('evt_1787720546619_gdgja', 'match_1787720522428', 0, 0, '00:02:26', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-1 [Pts: 0-40]'),
('evt_1787720546875_rembj', 'match_1787720522428', 0, 0, '00:02:26', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-2 [Pts: 0-0]'),
('evt_1787720547833_l2nbh', 'match_1787720522428', 0, 0, '00:02:27', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 0-2 [Pts: 15-0]'),
('evt_1787720548083_wigv7', 'match_1787720522428', 0, 0, '00:02:28', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 0-2 [Pts: 30-0]'),
('evt_1787720548284_k2220', 'match_1787720522428', 0, 0, '00:02:28', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 0-2 [Pts: 40-0]'),
('evt_1787720548506_6wgq5', 'match_1787720522428', 0, 0, '00:02:28', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 1-2 [Pts: 0-0]'),
('evt_1787720548738_7l5az', 'match_1787720522428', 0, 0, '00:02:28', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 1-2 [Pts: 15-0]'),
('evt_1787720548945_lk7ci', 'match_1787720522428', 0, 0, '00:02:28', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 1-2 [Pts: 30-0]'),
('evt_1787720549235_1ppch', 'match_1787720522428', 0, 0, '00:02:29', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 1-2 [Pts: 40-0]'),
('evt_1787720549435_umc3a', 'match_1787720522428', 0, 0, '00:02:29', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 2-2 [Pts: 0-0]'),
('evt_1787720549954_atfx6', 'match_1787720522428', 0, 0, '00:02:29', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-2 [Pts: 0-15]'),
('evt_1787720550185_o87oz', 'match_1787720522428', 0, 0, '00:02:30', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-2 [Pts: 0-30]'),
('evt_1787720551218_x6vmi', 'match_1787720522428', 0, 0, '00:02:31', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 2-2 [Pts: 15-30]'),
('evt_1787720551451_iyhyg', 'match_1787720522428', 0, 0, '00:02:31', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 2-2 [Pts: 30-30]'),
('evt_1787720551667_xbvcj', 'match_1787720522428', 0, 0, '00:02:31', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 2-2 [Pts: 40-30]'),
('evt_1787720551899_3p7y7', 'match_1787720522428', 0, 0, '00:02:31', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 3-2 [Pts: 0-0]'),
('evt_1787720552164_hzvhd', 'match_1787720522428', 0, 0, '00:02:32', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 3-2 [Pts: 15-0]'),
('evt_1787720552413_1ydcx', 'match_1787720522428', 0, 0, '00:02:32', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 3-2 [Pts: 30-0]'),
('evt_1787720552643_mf8q7', 'match_1787720522428', 0, 0, '00:02:32', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 3-2 [Pts: 40-0]'),
('evt_1787720552875_zwxe2', 'match_1787720522428', 0, 0, '00:02:32', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-2 [Pts: 0-0]'),
('evt_1787720553082_749m6', 'match_1787720522428', 0, 0, '00:02:33', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-2 [Pts: 15-0]'),
('evt_1787720553300_2u654', 'match_1787720522428', 0, 0, '00:02:33', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-2 [Pts: 30-0]'),
('evt_1787720553514_2oj3c', 'match_1787720522428', 0, 0, '00:02:33', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 4-2 [Pts: 40-0]'),
('evt_1787720553755_5f1xo', 'match_1787720522428', 0, 0, '00:02:33', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 5-2 [Pts: 0-0]'),
('evt_1787720554018_h1ocq', 'match_1787720522428', 0, 0, '00:02:34', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 5-2 [Pts: 15-0]'),
('evt_1787720554684_kwb32', 'match_1787720522428', 0, 0, '00:02:34', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-2 [Pts: 15-15]'),
('evt_1787720554923_kbr09', 'match_1787720522428', 0, 0, '00:02:34', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-2 [Pts: 15-30]'),
('evt_1787720555163_0ljyz', 'match_1787720522428', 0, 0, '00:02:35', 'B', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-2 [Pts: 15-40]'),
('evt_1787720556299_6plfn', 'match_1787720522428', 0, 0, '00:02:36', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 5-2 [Pts: 30-40]'),
('evt_1787720556652_mqb6o', 'match_1787720522428', 0, 0, '00:02:36', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 5-2 [Pts: 40-40]'),
('evt_1787720556907_yj5hu', 'match_1787720522428', 0, 0, '00:02:36', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 5-2 [Pts: AD-40]'),
('evt_1787720557139_q2zd2', 'match_1787720522428', 0, 0, '00:02:37', 'A', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-2 | S2: 6-2 [Pts: 0-0]'),
('evt_1787720629958_9s6mk', 'match_1787718088212', 0, 0, '00:03:49', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720630208_9w05g', 'match_1787718088212', 0, 0, '00:03:50', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720630406_3vnj8', 'match_1787718088212', 0, 0, '00:03:50', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 0-0 | S2: 0-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720630670_9itbo', 'match_1787718088212', 0, 0, '00:03:50', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 1-0 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720630894_qe8rj', 'match_1787718088212', 0, 0, '00:03:50', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 1-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720631134_42s0u', 'match_1787718088212', 0, 0, '00:03:51', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 1-0 | S2: 0-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720631462_4pm1j', 'match_1787718088212', 0, 0, '00:03:51', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 1-0 | S2: 0-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720631725_hsmyg', 'match_1787718088212', 0, 0, '00:03:51', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720631940_7z4bz', 'match_1787718088212', 0, 0, '00:03:51', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720632180_kus8a', 'match_1787718088212', 0, 0, '00:03:52', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 | S2: 0-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720632420_ofggi', 'match_1787718088212', 0, 0, '00:03:52', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 2-0 | S2: 0-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720632652_bcr1d', 'match_1787718088212', 0, 0, '00:03:52', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-0 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720632883_hmq80', 'match_1787718088212', 0, 0, '00:03:52', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720633107_n0mby', 'match_1787718088212', 0, 0, '00:03:53', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-0 | S2: 0-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720633333_9rwbs', 'match_1787718088212', 0, 0, '00:03:53', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 3-0 | S2: 0-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720633550_fb267', 'match_1787718088212', 0, 0, '00:03:53', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-0 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720633765_7kzbh', 'match_1787718088212', 0, 0, '00:03:53', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720633996_d8gk5', 'match_1787718088212', 0, 0, '00:03:53', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-0 | S2: 0-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720634203_11xai', 'match_1787718088212', 0, 0, '00:03:54', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 4-0 | S2: 0-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720634412_5g8mh', 'match_1787718088212', 0, 0, '00:03:54', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-0 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720634611_ojccg', 'match_1787718088212', 0, 0, '00:03:54', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720634826_aed7n', 'match_1787718088212', 0, 0, '00:03:54', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-0 | S2: 0-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720635042_tvtut', 'match_1787718088212', 0, 0, '00:03:55', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 5-0 | S2: 0-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720635250_nniwy', 'match_1787718088212', 0, 0, '00:03:55', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 0-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720635466_27wkr', 'match_1787718088212', 0, 0, '00:03:55', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 0-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720635682_ppjwq', 'match_1787718088212', 0, 0, '00:03:55', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 0-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720635890_rzml7', 'match_1787718088212', 0, 0, '00:03:55', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 0-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720636099_gcbxe', 'match_1787718088212', 0, 0, '00:03:56', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 1-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720636331_cf75o', 'match_1787718088212', 0, 0, '00:03:56', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 1-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720636554_xqg6g', 'match_1787718088212', 0, 0, '00:03:56', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 1-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720636779_oj3i0', 'match_1787718088212', 0, 0, '00:03:56', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 1-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720637000_1pcal', 'match_1787718088212', 0, 0, '00:03:57', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 2-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720637218_i3owi', 'match_1787718088212', 0, 0, '00:03:57', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 2-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720637433_qqbpn', 'match_1787718088212', 0, 0, '00:03:57', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 2-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720637649_3j2fe', 'match_1787718088212', 0, 0, '00:03:57', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 2-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720637874_amd4h', 'match_1787718088212', 0, 0, '00:03:57', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 3-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720638105_ltnvq', 'match_1787718088212', 0, 0, '00:03:58', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 3-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720638329_lx81y', 'match_1787718088212', 0, 0, '00:03:58', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 3-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720638560_gon2o', 'match_1787718088212', 0, 0, '00:03:58', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 3-0 | S3: 0-0 [Pts: 40-0]');
INSERT INTO `match_events` (`id`, `match_id`, `set_number`, `game_number`, `timestamp`, `winning_pair_id`, `player_id`, `player_name`, `event_type`, `description`, `score_snapshot`) VALUES
('evt_1787720638799_bipoc', 'match_1787718088212', 0, 0, '00:03:58', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 4-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720639032_crbxx', 'match_1787718088212', 0, 0, '00:03:59', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 4-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720639256_h67qy', 'match_1787718088212', 0, 0, '00:03:59', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 4-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720639465_mo9f6', 'match_1787718088212', 0, 0, '00:03:59', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 4-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720639696_n4y9i', 'match_1787718088212', 0, 0, '00:03:59', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 5-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720639928_yw9kb', 'match_1787718088212', 0, 0, '00:03:59', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 5-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720640144_iuili', 'match_1787718088212', 0, 0, '00:04:00', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 5-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720640387_h7hfo', 'match_1787718088212', 0, 0, '00:04:00', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 5-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720640607_h0na0', 'match_1787718088212', 0, 0, '00:04:00', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 0-0 [Pts: 0-0]'),
('evt_1787720640889_32uwp', 'match_1787718088212', 0, 0, '00:04:00', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 0-0 [Pts: 15-0]'),
('evt_1787720641271_5sxrn', 'match_1787718088212', 0, 0, '00:04:01', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 0-0 [Pts: 30-0]'),
('evt_1787720641487_ygo3t', 'match_1787718088212', 0, 0, '00:04:01', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 0-0 [Pts: 40-0]'),
('evt_1787720641688_zgaip', 'match_1787718088212', 0, 0, '00:04:01', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 1-0 [Pts: 0-0]'),
('evt_1787720641911_k29wv', 'match_1787718088212', 0, 0, '00:04:01', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 1-0 [Pts: 15-0]'),
('evt_1787720642126_7jgfg', 'match_1787718088212', 0, 0, '00:04:02', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 1-0 [Pts: 30-0]'),
('evt_1787720642398_5xtwz', 'match_1787718088212', 0, 0, '00:04:02', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 1-0 [Pts: 40-0]'),
('evt_1787720642607_cbl6b', 'match_1787718088212', 0, 0, '00:04:02', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 2-0 [Pts: 0-0]'),
('evt_1787720642814_iuix3', 'match_1787718088212', 0, 0, '00:04:02', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 2-0 [Pts: 15-0]'),
('evt_1787720643030_opoxf', 'match_1787718088212', 0, 0, '00:04:03', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 2-0 [Pts: 30-0]'),
('evt_1787720643237_gzoua', 'match_1787718088212', 0, 0, '00:04:03', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 2-0 [Pts: 40-0]'),
('evt_1787720643454_6xb18', 'match_1787718088212', 0, 0, '00:04:03', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 3-0 [Pts: 0-0]'),
('evt_1787720643701_xqoan', 'match_1787718088212', 0, 0, '00:04:03', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 3-0 [Pts: 15-0]'),
('evt_1787720643950_roiwn', 'match_1787718088212', 0, 0, '00:04:03', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 3-0 [Pts: 30-0]'),
('evt_1787720644197_ehqr4', 'match_1787718088212', 0, 0, '00:04:04', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 3-0 [Pts: 40-0]'),
('evt_1787720644436_lzxyj', 'match_1787718088212', 0, 0, '00:04:04', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 4-0 [Pts: 0-0]'),
('evt_1787720644668_kuqfn', 'match_1787718088212', 0, 0, '00:04:04', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 4-0 [Pts: 15-0]'),
('evt_1787720644908_kcoa2', 'match_1787718088212', 0, 0, '00:04:04', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 4-0 [Pts: 30-0]'),
('evt_1787720645165_ac7pw', 'match_1787718088212', 0, 0, '00:04:05', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 4-0 [Pts: 40-0]'),
('evt_1787720645397_69b8v', 'match_1787718088212', 0, 0, '00:04:05', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 5-0 [Pts: 0-0]'),
('evt_1787720646052_1fq22', 'match_1787718088212', 0, 0, '00:04:06', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 5-0 [Pts: 15-0]'),
('evt_1787720646397_zqlpq', 'match_1787718088212', 0, 0, '00:04:06', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 5-0 [Pts: 30-0]'),
('evt_1787720646612_o1pn9', 'match_1787718088212', 0, 0, '00:04:06', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 5-0 [Pts: 40-0]'),
('evt_1787720647100_u6bxs', 'match_1787718088212', 0, 0, '00:04:07', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 0-0 [Pts: 0-0]'),
('evt_1787720647947_t1ohk', 'match_1787718088212', 0, 0, '00:04:07', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 0-0 [Pts: 15-0]'),
('evt_1787720648218_dpyxt', 'match_1787718088212', 0, 0, '00:04:08', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 0-0 [Pts: 30-0]'),
('evt_1787720648419_99s93', 'match_1787718088212', 0, 0, '00:04:08', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 0-0 [Pts: 40-0]'),
('evt_1787720648627_ho5v0', 'match_1787718088212', 0, 0, '00:04:08', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 1-0 [Pts: 0-0]'),
('evt_1787720648844_8yyyf', 'match_1787718088212', 0, 0, '00:04:08', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 1-0 [Pts: 15-0]'),
('evt_1787720649034_ntb28', 'match_1787718088212', 0, 0, '00:04:09', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 1-0 [Pts: 30-0]'),
('evt_1787720649243_oulz5', 'match_1787718088212', 0, 0, '00:04:09', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 1-0 [Pts: 40-0]'),
('evt_1787720649451_k5ier', 'match_1787718088212', 0, 0, '00:04:09', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 2-0 [Pts: 0-0]'),
('evt_1787720649650_jbiwe', 'match_1787718088212', 0, 0, '00:04:09', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 2-0 [Pts: 15-0]'),
('evt_1787720649858_lpkho', 'match_1787718088212', 0, 0, '00:04:09', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 2-0 [Pts: 30-0]'),
('evt_1787720650090_9p9ba', 'match_1787718088212', 0, 0, '00:04:10', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 2-0 [Pts: 40-0]'),
('evt_1787720650313_08f2p', 'match_1787718088212', 0, 0, '00:04:10', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 3-0 [Pts: 0-0]'),
('evt_1787720650553_uaqog', 'match_1787718088212', 0, 0, '00:04:10', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 3-0 [Pts: 15-0]'),
('evt_1787720650785_tj1pb', 'match_1787718088212', 0, 0, '00:04:10', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 3-0 [Pts: 30-0]'),
('evt_1787720651009_ikgnb', 'match_1787718088212', 0, 0, '00:04:11', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 3-0 [Pts: 40-0]'),
('evt_1787720651217_lwyni', 'match_1787718088212', 0, 0, '00:04:11', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 4-0 [Pts: 0-0]'),
('evt_1787720651441_xcl8u', 'match_1787718088212', 0, 0, '00:04:11', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 4-0 [Pts: 15-0]'),
('evt_1787720651673_oq05v', 'match_1787718088212', 0, 0, '00:04:11', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 4-0 [Pts: 30-0]'),
('evt_1787720651922_bg2ml', 'match_1787718088212', 0, 0, '00:04:11', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 4-0 [Pts: 40-0]'),
('evt_1787720652130_82r4f', 'match_1787718088212', 0, 0, '00:04:12', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 5-0 [Pts: 0-0]'),
('evt_1787720652352_2h756', 'match_1787718088212', 0, 0, '00:04:12', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 5-0 [Pts: 15-0]'),
('evt_1787720652576_jtfrc', 'match_1787718088212', 0, 0, '00:04:12', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 5-0 [Pts: 30-0]'),
('evt_1787720652816_h3t3e', 'match_1787718088212', 0, 0, '00:04:12', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 5-0 [Pts: 40-0]'),
('evt_1787720653296_gsoa4', 'match_1787718088212', 0, 0, '00:04:13', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 6-0 | S5: 0-0 [Pts: 0-0]'),
('evt_1787720653536_q2kg6', 'match_1787718088212', 0, 0, '00:04:13', 'A', NULL, NULL, 'POINT', 'undefined gana punto (POINT)', 'S1: 6-0 | S2: 6-0 | S3: 6-0 | S4: 6-0 | S5: 0-0 [Pts: 15-0]'),
('evt_1787720699041_id1yy', 'match_1787720688776', 0, 0, '00:04:59', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 0-15]'),
('evt_1787720700056_fmd5s', 'match_1787720688776', 0, 0, '00:05:00', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787720700944_ltdk5', 'match_1787720688776', 0, 0, '00:05:00', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-30]'),
('evt_1787720701249_v1j4t', 'match_1787720688776', 0, 0, '00:05:01', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-40]'),
('evt_1787720703055_bel0t', 'match_1787720688776', 0, 0, '00:05:03', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-40]'),
('evt_1787720703687_xqb01', 'match_1787720688776', 0, 0, '00:05:03', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-0]'),
('evt_1787720705102_5z00s', 'match_1787720688776', 0, 0, '00:05:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 15-0]'),
('evt_1787720705334_ad8gk', 'match_1787720688776', 0, 0, '00:05:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 30-0]'),
('evt_1787720705557_qrzlb', 'match_1787720688776', 0, 0, '00:05:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 40-0]'),
('evt_1787720706054_f8txo', 'match_1787720688776', 0, 0, '00:05:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 40-15]'),
('evt_1787720706279_u0p76', 'match_1787720688776', 0, 0, '00:05:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 40-30]'),
('evt_1787720706486_nop0t', 'match_1787720688776', 0, 0, '00:05:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 40-40]'),
('evt_1787720706718_hl4r8', 'match_1787720688776', 0, 0, '00:05:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 40-AD]'),
('evt_1787720706927_o91fg', 'match_1787720688776', 0, 0, '00:05:06', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-2 [Pts: 0-0]'),
('evt_1787720707767_1vs01', 'match_1787720688776', 0, 0, '00:05:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-2 [Pts: 15-0]'),
('evt_1787720707981_vsfr4', 'match_1787720688776', 0, 0, '00:05:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-2 [Pts: 30-0]'),
('evt_1787720708181_8h4qr', 'match_1787720688776', 0, 0, '00:05:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-2 [Pts: 40-0]'),
('evt_1787720708405_x3yss', 'match_1787720688776', 0, 0, '00:05:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-2 [Pts: 0-0]'),
('evt_1787720708790_fsdbg', 'match_1787720688776', 0, 0, '00:05:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-2 [Pts: 15-0]'),
('evt_1787720709109_s5nuw', 'match_1787720688776', 0, 0, '00:05:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-2 [Pts: 30-0]'),
('evt_1787720709581_m0sto', 'match_1787720688776', 0, 0, '00:05:09', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-2 [Pts: 30-15]'),
('evt_1787720709812_0ws47', 'match_1787720688776', 0, 0, '00:05:09', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-2 [Pts: 30-30]'),
('evt_1787720710036_90fj4', 'match_1787720688776', 0, 0, '00:05:10', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-2 [Pts: 30-40]'),
('evt_1787720710700_q2sop', 'match_1787720688776', 0, 0, '00:05:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-2 [Pts: 40-40]'),
('evt_1787720710979_091xm', 'match_1787720688776', 0, 0, '00:05:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-2 [Pts: AD-40]'),
('evt_1787720711925_2oh8q', 'match_1787720688776', 0, 0, '00:05:11', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-2 [Pts: 0-0]'),
('evt_1787720712804_0r3fu', 'match_1787720688776', 0, 0, '00:05:12', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-2 [Pts: 15-0]'),
('evt_1787720713036_l5ovv', 'match_1787720688776', 0, 0, '00:05:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-2 [Pts: 30-0]'),
('evt_1787720713244_lsjnj', 'match_1787720688776', 0, 0, '00:05:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-2 [Pts: 40-0]'),
('evt_1787720713491_at0fv', 'match_1787720688776', 0, 0, '00:05:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 0-0]'),
('evt_1787720713754_y6s8b', 'match_1787720688776', 0, 0, '00:05:13', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 15-0]'),
('evt_1787720718587_bxv3q', 'match_1787720688776', 0, 0, '00:05:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 30-0]'),
('evt_1787720718802_mzwys', 'match_1787720688776', 0, 0, '00:05:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 40-0]'),
('evt_1787720719002_ai9nh', 'match_1787720688776', 0, 0, '00:05:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 0-0]'),
('evt_1787720719210_or3x8', 'match_1787720688776', 0, 0, '00:05:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 15-0]'),
('evt_1787720719411_8po7r', 'match_1787720688776', 0, 0, '00:05:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 30-0]'),
('evt_1787720719617_zp36r', 'match_1787720688776', 0, 0, '00:05:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 40-0]'),
('evt_1787720719829_jsaro', 'match_1787720688776', 0, 0, '00:05:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 0-0]'),
('evt_1787720720034_1fnim', 'match_1787720688776', 0, 0, '00:05:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 15-0]'),
('evt_1787720720248_2laux', 'match_1787720688776', 0, 0, '00:05:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 30-0]'),
('evt_1787720720449_em7y3', 'match_1787720688776', 0, 0, '00:05:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 40-0]'),
('evt_1787720720658_335a1', 'match_1787720688776', 0, 0, '00:05:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 0-0]'),
('evt_1787720720866_c1ggz', 'match_1787720688776', 0, 0, '00:05:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 15-0]'),
('evt_1787720721073_4qghm', 'match_1787720688776', 0, 0, '00:05:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 30-0]'),
('evt_1787720721288_4tfya', 'match_1787720688776', 0, 0, '00:05:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 40-0]'),
('evt_1787720721496_pr86h', 'match_1787720688776', 0, 0, '00:05:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 0-0]'),
('evt_1787720721721_avwzf', 'match_1787720688776', 0, 0, '00:05:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 15-0]'),
('evt_1787720721928_3xp5d', 'match_1787720688776', 0, 0, '00:05:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 30-0]'),
('evt_1787720722152_j2wjk', 'match_1787720688776', 0, 0, '00:05:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 40-0]'),
('evt_1787720722391_49rk0', 'match_1787720688776', 0, 0, '00:05:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 0-0]'),
('evt_1787720722674_rl8m2', 'match_1787720688776', 0, 0, '00:05:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 15-0]'),
('evt_1787720722911_vpaia', 'match_1787720688776', 0, 0, '00:05:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 30-0]'),
('evt_1787720723295_7g376', 'match_1787720688776', 0, 0, '00:05:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 40-0]'),
('evt_1787720723536_lnpwg', 'match_1787720688776', 0, 0, '00:05:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 0-0]'),
('evt_1787720723743_x4kyw', 'match_1787720688776', 0, 0, '00:05:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 15-0]'),
('evt_1787720723958_rx1dl', 'match_1787720688776', 0, 0, '00:05:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 30-0]'),
('evt_1787720724177_ia85n', 'match_1787720688776', 0, 0, '00:05:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 40-0]'),
('evt_1787720724391_6acjw', 'match_1787720688776', 0, 0, '00:05:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 0-0]'),
('evt_1787720724617_3gkxo', 'match_1787720688776', 0, 0, '00:05:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 15-0]'),
('evt_1787720724831_r3v7x', 'match_1787720688776', 0, 0, '00:05:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 30-0]'),
('evt_1787720725096_p5eqm', 'match_1787720688776', 0, 0, '00:05:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 40-0]'),
('evt_1787720725323_elh24', 'match_1787720688776', 0, 0, '00:05:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 0-0]'),
('evt_1787720725552_yz3ur', 'match_1787720688776', 0, 0, '00:05:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 15-0]'),
('evt_1787720725775_hysjt', 'match_1787720688776', 0, 0, '00:05:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 30-0]'),
('evt_1787720725999_37x8z', 'match_1787720688776', 0, 0, '00:05:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 40-0]'),
('evt_1787720726222_g1ygq', 'match_1787720688776', 0, 0, '00:05:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 0-0]'),
('evt_1787721389674_wf29y', 'match_1787721367330', 0, 0, '00:16:29', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787721390065_uxesu', 'match_1787721367330', 0, 0, '00:16:30', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787721390641_l506o', 'match_1787721367330', 0, 0, '00:16:30', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787721390992_fzl29', 'match_1787721367330', 0, 0, '00:16:30', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 30-30]'),
('evt_1787721391496_cy9w1', 'match_1787721367330', 0, 0, '00:16:31', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 40-30]'),
('evt_1787721392791_dfmxk', 'match_1787721367330', 0, 0, '00:16:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 0-0]'),
('evt_1787721393002_efsls', 'match_1787721367330', 0, 0, '00:16:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 15-0]'),
('evt_1787721393200_bbmrd', 'match_1787721367330', 0, 0, '00:16:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-0]'),
('evt_1787721393416_xznws', 'match_1787721367330', 0, 0, '00:16:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 40-0]'),
('evt_1787721393632_9lg22', 'match_1787721367330', 0, 0, '00:16:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 0-0]'),
('evt_1787721393839_rm0bh', 'match_1787721367330', 0, 0, '00:16:33', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 15-0]'),
('evt_1787721394256_vb17f', 'match_1787721367330', 0, 0, '00:16:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 15-15]'),
('evt_1787721394448_qj6tv', 'match_1787721367330', 0, 0, '00:16:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 15-30]'),
('evt_1787721394655_rr6ya', 'match_1787721367330', 0, 0, '00:16:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-0 [Pts: 15-40]'),
('evt_1787721394848_6lxz5', 'match_1787721367330', 0, 0, '00:16:34', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-0]'),
('evt_1787721395065_630nr', 'match_1787721367330', 0, 0, '00:16:35', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-15]'),
('evt_1787721395256_ec1yh', 'match_1787721367330', 0, 0, '00:16:35', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 2-1 [Pts: 0-30]'),
('evt_1787721395825_594nz', 'match_1787721367330', 0, 0, '00:16:35', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 15-30]'),
('evt_1787721396056_atuv1', 'match_1787721367330', 0, 0, '00:16:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 30-30]'),
('evt_1787721396256_dh6ve', 'match_1787721367330', 0, 0, '00:16:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 40-30]'),
('evt_1787721396463_8u2ym', 'match_1787721367330', 0, 0, '00:16:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 0-0]'),
('evt_1787721396671_gmcxi', 'match_1787721367330', 0, 0, '00:16:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 15-0]'),
('evt_1787721396886_tsme5', 'match_1787721367330', 0, 0, '00:16:36', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 30-0]'),
('evt_1787721397102_8wfol', 'match_1787721367330', 0, 0, '00:16:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 40-0]'),
('evt_1787721397320_j151c', 'match_1787721367330', 0, 0, '00:16:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-1 [Pts: 0-0]'),
('evt_1787721397527_9kqrq', 'match_1787721367330', 0, 0, '00:16:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-1 [Pts: 15-0]'),
('evt_1787721397744_0cqke', 'match_1787721367330', 0, 0, '00:16:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-1 [Pts: 30-0]'),
('evt_1787721398560_rppmv', 'match_1787721367330', 0, 0, '00:16:38', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 30-15]'),
('evt_1787721398766_qmsct', 'match_1787721367330', 0, 0, '00:16:38', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 30-30]'),
('evt_1787721398959_1z9vh', 'match_1787721367330', 0, 0, '00:16:38', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-1 [Pts: 30-40]'),
('evt_1787721399167_1eg5y', 'match_1787721367330', 0, 0, '00:16:39', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-0]'),
('evt_1787721399398_hdosn', 'match_1787721367330', 0, 0, '00:16:39', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-15]'),
('evt_1787721399606_jema1', 'match_1787721367330', 0, 0, '00:16:39', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-30]'),
('evt_1787721399830_otx2v', 'match_1787721367330', 0, 0, '00:16:39', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-2 [Pts: 0-40]'),
('evt_1787721400069_ia5s7', 'match_1787721367330', 0, 0, '00:16:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-3 [Pts: 0-0]'),
('evt_1787721400311_pmxpt', 'match_1787721367330', 0, 0, '00:16:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 4-3 [Pts: 0-15]'),
('evt_1787721400813_zaj4m', 'match_1787721367330', 0, 0, '00:16:40', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-3 [Pts: 15-15]'),
('evt_1787721401159_lqzew', 'match_1787721367330', 0, 0, '00:16:41', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-3 [Pts: 30-15]'),
('evt_1787721401390_1weih', 'match_1787721367330', 0, 0, '00:16:41', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-3 [Pts: 40-15]'),
('evt_1787721401605_dp1pe', 'match_1787721367330', 0, 0, '00:16:41', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-3 [Pts: 0-0]'),
('evt_1787721401814_uwcn1', 'match_1787721367330', 0, 0, '00:16:41', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-3 [Pts: 15-0]'),
('evt_1787721402022_z2q51', 'match_1787721367330', 0, 0, '00:16:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-3 [Pts: 30-0]'),
('evt_1787721402239_qvqep', 'match_1787721367330', 0, 0, '00:16:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-3 [Pts: 40-0]'),
('evt_1787721402455_vbgb8', 'match_1787721367330', 0, 0, '00:16:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 0-0]'),
('evt_1787721402671_efikm', 'match_1787721367330', 0, 0, '00:16:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 15-0]'),
('evt_1787721402878_6dyr5', 'match_1787721367330', 0, 0, '00:16:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 30-0]'),
('evt_1787721403109_yc6ni', 'match_1787721367330', 0, 0, '00:16:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 0-0 [Pts: 40-0]'),
('evt_1787721403325_rl0b1', 'match_1787721367330', 0, 0, '00:16:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 0-0]'),
('evt_1787721403551_inri0', 'match_1787721367330', 0, 0, '00:16:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 15-0]'),
('evt_1787721403796_e21lf', 'match_1787721367330', 0, 0, '00:16:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 30-0]'),
('evt_1787721404598_8ubjk', 'match_1787721367330', 0, 0, '00:16:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 30-15]'),
('evt_1787721404813_0t66d', 'match_1787721367330', 0, 0, '00:16:44', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 30-30]'),
('evt_1787721405028_erx5d', 'match_1787721367330', 0, 0, '00:16:45', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-3 | S2: 1-0 [Pts: 30-40]'),
('evt_1787721405245_t32az', 'match_1787721367330', 0, 0, '00:16:45', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-3 | S2: 1-1 [Pts: 0-0]'),
('evt_1787721405860_q0dyl', 'match_1787721367330', 0, 0, '00:16:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 1-1 [Pts: 15-0]'),
('evt_1787721406084_jri2r', 'match_1787721367330', 0, 0, '00:16:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 1-1 [Pts: 30-0]'),
('evt_1787721406301_n6e2u', 'match_1787721367330', 0, 0, '00:16:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 1-1 [Pts: 40-0]'),
('evt_1787721406534_77d8g', 'match_1787721367330', 0, 0, '00:16:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 2-1 [Pts: 0-0]'),
('evt_1787721406750_ro5bd', 'match_1787721367330', 0, 0, '00:16:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 2-1 [Pts: 15-0]'),
('evt_1787721406981_g3nny', 'match_1787721367330', 0, 0, '00:16:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 2-1 [Pts: 30-0]'),
('evt_1787721407198_1v2jp', 'match_1787721367330', 0, 0, '00:16:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 2-1 [Pts: 40-0]'),
('evt_1787721407413_if4ua', 'match_1787721367330', 0, 0, '00:16:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 0-0]'),
('evt_1787721407631_anekq', 'match_1787721367330', 0, 0, '00:16:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 15-0]'),
('evt_1787721407869_ko3rd', 'match_1787721367330', 0, 0, '00:16:47', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 30-0]'),
('evt_1787721408124_thot0', 'match_1787721367330', 0, 0, '00:16:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 3-1 [Pts: 40-0]'),
('evt_1787721408349_r5b00', 'match_1787721367330', 0, 0, '00:16:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 0-0]'),
('evt_1787721408572_sj1x6', 'match_1787721367330', 0, 0, '00:16:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 15-0]'),
('evt_1787721408799_d0563', 'match_1787721367330', 0, 0, '00:16:48', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 30-0]'),
('evt_1787721409028_zwn2i', 'match_1787721367330', 0, 0, '00:16:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 4-1 [Pts: 40-0]'),
('evt_1787721409251_no12s', 'match_1787721367330', 0, 0, '00:16:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 0-0]'),
('evt_1787721409476_3hjlu', 'match_1787721367330', 0, 0, '00:16:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 15-0]'),
('evt_1787721409702_m0l7v', 'match_1787721367330', 0, 0, '00:16:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 30-0]'),
('evt_1787721409939_21szt', 'match_1787721367330', 0, 0, '00:16:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 5-1 [Pts: 40-0]'),
('evt_1787721410363_1hn1d', 'match_1787721367330', 0, 0, '00:16:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-3 | S2: 6-1 [Pts: 0-0]'),
('evt_1787721907011_tyawf', 'match_1787721895941', 0, 0, '00:25:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787721907564_dksn3', 'match_1787721895941', 0, 0, '00:25:07', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787721908052_j2d27', 'match_1787721895941', 0, 0, '00:25:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787721908812_1b740', 'match_1787721895941', 0, 0, '00:25:08', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 30-30]'),
('evt_1787721909044_wc95s', 'match_1787721895941', 0, 0, '00:25:09', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 30-40]'),
('evt_1787721909251_163mm', 'match_1787721895941', 0, 0, '00:25:09', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-0]'),
('evt_1787721909458_9spl4', 'match_1787721895941', 0, 0, '00:25:09', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-15]'),
('evt_1787721909676_t4wlm', 'match_1787721895941', 0, 0, '00:25:09', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-30]'),
('evt_1787721909970_pusnc', 'match_1787721895941', 0, 0, '00:25:09', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-40]'),
('evt_1787721910547_z8jdj', 'match_1787721895941', 0, 0, '00:25:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 15-40]'),
('evt_1787721910788_2pgd1', 'match_1787721895941', 0, 0, '00:25:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 30-40]'),
('evt_1787721910995_mx7zg', 'match_1787721895941', 0, 0, '00:25:10', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 40-40]'),
('evt_1787721911235_njfih', 'match_1787721895941', 0, 0, '00:25:11', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: AD-40]'),
('evt_1787721911460_46rfc', 'match_1787721895941', 0, 0, '00:25:11', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 [Pts: 0-0]'),
('evt_1787721911788_an8tm', 'match_1787721895941', 0, 0, '00:25:11', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 [Pts: 15-0]'),
('evt_1787721912676_1w2ay', 'match_1787721895941', 0, 0, '00:25:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 [Pts: 15-15]'),
('evt_1787721912900_tx3gx', 'match_1787721895941', 0, 0, '00:25:12', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 [Pts: 15-30]'),
('evt_1787721913116_hsn0n', 'match_1787721895941', 0, 0, '00:25:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-1 [Pts: 15-40]'),
('evt_1787721913339_1vvzx', 'match_1787721895941', 0, 0, '00:25:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-2 [Pts: 0-0]'),
('evt_1787721913571_kuouc', 'match_1787721895941', 0, 0, '00:25:13', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-2 [Pts: 0-15]'),
('evt_1787721914307_fsi6u', 'match_1787721895941', 0, 0, '00:25:14', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-2 [Pts: 15-15]'),
('evt_1787721914531_3f6cu', 'match_1787721895941', 0, 0, '00:25:14', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-2 [Pts: 30-15]'),
('evt_1787721914749_fhxji', 'match_1787721895941', 0, 0, '00:25:14', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-2 [Pts: 40-15]'),
('evt_1787721914971_rqpi8', 'match_1787721895941', 0, 0, '00:25:14', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-2 [Pts: 0-0]'),
('evt_1787721915187_6eqlg', 'match_1787721895941', 0, 0, '00:25:15', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-2 [Pts: 15-0]'),
('evt_1787721916483_dz6cb', 'match_1787721895941', 0, 0, '00:25:16', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-2 [Pts: 30-0]'),
('evt_1787721916877_9v2xf', 'match_1787721895941', 0, 0, '00:25:16', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-2 [Pts: 40-0]'),
('evt_1787721917164_xa42v', 'match_1787721895941', 0, 0, '00:25:17', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 0-0]'),
('evt_1787721917419_xqhw5', 'match_1787721895941', 0, 0, '00:25:17', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 15-0]'),
('evt_1787721917701_a0j8d', 'match_1787721895941', 0, 0, '00:25:17', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 30-0]'),
('evt_1787721918363_tys6l', 'match_1787721895941', 0, 0, '00:25:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-2 [Pts: 40-0]'),
('evt_1787721918677_go19z', 'match_1787721895941', 0, 0, '00:25:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 0-0]'),
('evt_1787721918876_zhq14', 'match_1787721895941', 0, 0, '00:25:18', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 15-0]'),
('evt_1787721919108_0t0q6', 'match_1787721895941', 0, 0, '00:25:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 30-0]'),
('evt_1787721919343_rugkz', 'match_1787721895941', 0, 0, '00:25:19', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-2 [Pts: 40-0]'),
('evt_1787721920043_kvgfr', 'match_1787721895941', 0, 0, '00:25:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 0-0]'),
('evt_1787721920315_m0wnv', 'match_1787721895941', 0, 0, '00:25:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 15-0]'),
('evt_1787721920603_9a518', 'match_1787721895941', 0, 0, '00:25:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 30-0]'),
('evt_1787721920836_uuve3', 'match_1787721895941', 0, 0, '00:25:20', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-2 [Pts: 40-0]'),
('evt_1787721921076_t3c5z', 'match_1787721895941', 0, 0, '00:25:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 0-0]'),
('evt_1787721921323_gf0sm', 'match_1787721895941', 0, 0, '00:25:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 15-0]'),
('evt_1787721921557_wsh7j', 'match_1787721895941', 0, 0, '00:25:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 30-0]'),
('evt_1787721921773_yf48r', 'match_1787721895941', 0, 0, '00:25:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 0-0 [Pts: 40-0]'),
('evt_1787721921988_1k4r7', 'match_1787721895941', 0, 0, '00:25:21', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 0-0]'),
('evt_1787721922227_ox0yv', 'match_1787721895941', 0, 0, '00:25:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 15-0]'),
('evt_1787721922438_dim6k', 'match_1787721895941', 0, 0, '00:25:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 30-0]'),
('evt_1787721922683_28hia', 'match_1787721895941', 0, 0, '00:25:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 1-0 [Pts: 40-0]'),
('evt_1787721922916_9aekh', 'match_1787721895941', 0, 0, '00:25:22', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 0-0]'),
('evt_1787721923155_ja3q5', 'match_1787721895941', 0, 0, '00:25:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 15-0]'),
('evt_1787721923388_pu645', 'match_1787721895941', 0, 0, '00:25:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 30-0]'),
('evt_1787721923611_u51aa', 'match_1787721895941', 0, 0, '00:25:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 2-0 [Pts: 40-0]'),
('evt_1787721923859_l571v', 'match_1787721895941', 0, 0, '00:25:23', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 0-0]'),
('evt_1787721924091_6kpz8', 'match_1787721895941', 0, 0, '00:25:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 15-0]'),
('evt_1787721924332_o3u2v', 'match_1787721895941', 0, 0, '00:25:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 30-0]'),
('evt_1787721924556_h5urf', 'match_1787721895941', 0, 0, '00:25:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 3-0 [Pts: 40-0]'),
('evt_1787721924772_a11iy', 'match_1787721895941', 0, 0, '00:25:24', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 0-0]'),
('evt_1787721925005_d360p', 'match_1787721895941', 0, 0, '00:25:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 15-0]'),
('evt_1787721925235_eifkb', 'match_1787721895941', 0, 0, '00:25:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 30-0]'),
('evt_1787721925459_239ip', 'match_1787721895941', 0, 0, '00:25:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 4-0 [Pts: 40-0]'),
('evt_1787721925702_jpbdj', 'match_1787721895941', 0, 0, '00:25:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 0-0]'),
('evt_1787721925940_w7und', 'match_1787721895941', 0, 0, '00:25:25', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 15-0]'),
('evt_1787721926173_qod1t', 'match_1787721895941', 0, 0, '00:25:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 30-0]'),
('evt_1787721926412_vi8p8', 'match_1787721895941', 0, 0, '00:25:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 5-0 [Pts: 40-0]'),
('evt_1787721926637_66chh', 'match_1787721895941', 0, 0, '00:25:26', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-2 | S2: 6-0 [Pts: 0-0]'),
('evt_1787722832166_n39so', 'match_1787722823111', 0, 0, '00:40:32', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787722833189_z3mmh', 'match_1787722823111', 0, 0, '00:40:33', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787722833588_aixvi', 'match_1787722823111', 0, 0, '00:40:33', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-30]'),
('evt_1787722833788_c18aj', 'match_1787722823111', 0, 0, '00:40:33', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-40]'),
('evt_1787722834229_8k71d', 'match_1787722823111', 0, 0, '00:40:34', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-40]'),
('evt_1787722834541_0p339', 'match_1787722823111', 0, 0, '00:40:34', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 40-40]'),
('evt_1787722835436_chahp', 'match_1787722823111', 0, 0, '00:40:35', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 40-AD]'),
('evt_1787722835652_cxiaa', 'match_1787722823111', 0, 0, '00:40:35', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-0]'),
('evt_1787722835862_9weh5', 'match_1787722823111', 0, 0, '00:40:35', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-15]'),
('evt_1787722836100_33441', 'match_1787722823111', 0, 0, '00:40:36', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-1 [Pts: 0-30]'),
('evt_1787722837003_uhqvc', 'match_1787722823111', 0, 0, '00:40:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 15-30]'),
('evt_1787722837228_vv078', 'match_1787722823111', 0, 0, '00:40:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 30-30]'),
('evt_1787722837419_nx0kj', 'match_1787722823111', 0, 0, '00:40:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-1 [Pts: 40-30]'),
('evt_1787722837630_832h8', 'match_1787722823111', 0, 0, '00:40:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 [Pts: 0-0]'),
('evt_1787722837851_nl24a', 'match_1787722823111', 0, 0, '00:40:37', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 [Pts: 15-0]'),
('evt_1787722838044_9wle4', 'match_1787722823111', 0, 0, '00:40:38', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 [Pts: 30-0]'),
('evt_1787722838252_1ntxi', 'match_1787722823111', 0, 0, '00:40:38', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-1 [Pts: 40-0]'),
('evt_1787722838468_7kift', 'match_1787722823111', 0, 0, '00:40:38', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 0-0]'),
('evt_1787722838667_f5sj0', 'match_1787722823111', 0, 0, '00:40:38', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 15-0]'),
('evt_1787722838884_wfyfh', 'match_1787722823111', 0, 0, '00:40:38', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 30-0]'),
('evt_1787722839100_dqvvh', 'match_1787722823111', 0, 0, '00:40:39', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-1 [Pts: 40-0]'),
('evt_1787722839300_o9jvz', 'match_1787722823111', 0, 0, '00:40:39', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 0-0]'),
('evt_1787722839515_smhew', 'match_1787722823111', 0, 0, '00:40:39', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-1 [Pts: 15-0]'),
('evt_1787722839915_jrghi', 'match_1787722823111', 0, 0, '00:40:39', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 15-15]'),
('evt_1787722840130_qnd8u', 'match_1787722823111', 0, 0, '00:40:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 15-30]'),
('evt_1787722840332_w4dr9', 'match_1787722823111', 0, 0, '00:40:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-1 [Pts: 15-40]'),
('evt_1787722840531_sf8u4', 'match_1787722823111', 0, 0, '00:40:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-2 [Pts: 0-0]'),
('evt_1787722840746_pcn0p', 'match_1787722823111', 0, 0, '00:40:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-2 [Pts: 0-15]'),
('evt_1787722840948_1oe5e', 'match_1787722823111', 0, 0, '00:40:40', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-2 [Pts: 0-30]'),
('evt_1787722841162_0pelw', 'match_1787722823111', 0, 0, '00:40:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-2 [Pts: 0-40]'),
('evt_1787722841388_cbw3o', 'match_1787722823111', 0, 0, '00:40:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-3 [Pts: 0-0]'),
('evt_1787722841604_oxdwl', 'match_1787722823111', 0, 0, '00:40:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-3 [Pts: 0-15]'),
('evt_1787722841819_7lft7', 'match_1787722823111', 0, 0, '00:40:41', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-3 [Pts: 0-30]'),
('evt_1787722842036_n4zka', 'match_1787722823111', 0, 0, '00:40:42', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-3 [Pts: 0-40]'),
('evt_1787722842250_wel5x', 'match_1787722823111', 0, 0, '00:40:42', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 3-4 [Pts: 0-0]'),
('evt_1787722842699_ne96b', 'match_1787722823111', 0, 0, '00:40:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-4 [Pts: 15-0]'),
('evt_1787722842907_8gy9y', 'match_1787722823111', 0, 0, '00:40:42', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-4 [Pts: 30-0]'),
('evt_1787722843113_4rpwb', 'match_1787722823111', 0, 0, '00:40:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-4 [Pts: 40-0]'),
('evt_1787722843330_wdp0n', 'match_1787722823111', 0, 0, '00:40:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-4 [Pts: 0-0]'),
('evt_1787722843547_1x8x9', 'match_1787722823111', 0, 0, '00:40:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-4 [Pts: 15-0]'),
('evt_1787722843763_7ts0x', 'match_1787722823111', 0, 0, '00:40:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-4 [Pts: 30-0]'),
('evt_1787722843978_emydb', 'match_1787722823111', 0, 0, '00:40:43', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-4 [Pts: 40-0]'),
('evt_1787722844210_wh3zs', 'match_1787722823111', 0, 0, '00:40:44', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-4 [Pts: 0-0]'),
('evt_1787722844442_8re7t', 'match_1787722823111', 0, 0, '00:40:44', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-4 [Pts: 15-0]'),
('evt_1787722844650_g91b5', 'match_1787722823111', 0, 0, '00:40:44', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-4 [Pts: 30-0]'),
('evt_1787722844866_83ym1', 'match_1787722823111', 0, 0, '00:40:44', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-4 [Pts: 40-0]'),
('evt_1787722845099_wa9mw', 'match_1787722823111', 0, 0, '00:40:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 0-0 [Pts: 0-0]');
INSERT INTO `match_events` (`id`, `match_id`, `set_number`, `game_number`, `timestamp`, `winning_pair_id`, `player_id`, `player_name`, `event_type`, `description`, `score_snapshot`) VALUES
('evt_1787722845331_u3mr1', 'match_1787722823111', 0, 0, '00:40:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 0-0 [Pts: 15-0]'),
('evt_1787722845555_utmxq', 'match_1787722823111', 0, 0, '00:40:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 0-0 [Pts: 30-0]'),
('evt_1787722845786_f07k7', 'match_1787722823111', 0, 0, '00:40:45', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 0-0 [Pts: 40-0]'),
('evt_1787722846018_bfejz', 'match_1787722823111', 0, 0, '00:40:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 1-0 [Pts: 0-0]'),
('evt_1787722846243_mdn97', 'match_1787722823111', 0, 0, '00:40:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 1-0 [Pts: 15-0]'),
('evt_1787722846451_h8fh8', 'match_1787722823111', 0, 0, '00:40:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 1-0 [Pts: 30-0]'),
('evt_1787722846657_1d34l', 'match_1787722823111', 0, 0, '00:40:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 1-0 [Pts: 40-0]'),
('evt_1787722846890_y41tr', 'match_1787722823111', 0, 0, '00:40:46', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 2-0 [Pts: 0-0]'),
('evt_1787722847338_3gmy6', 'match_1787722823111', 0, 0, '00:40:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-4 | S2: 2-0 [Pts: 0-15]'),
('evt_1787722847562_nfm41', 'match_1787722823111', 0, 0, '00:40:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-4 | S2: 2-0 [Pts: 0-30]'),
('evt_1787722847779_lucfs', 'match_1787722823111', 0, 0, '00:40:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-4 | S2: 2-0 [Pts: 0-40]'),
('evt_1787722847979_xc5na', 'match_1787722823111', 0, 0, '00:40:47', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-4 | S2: 2-1 [Pts: 0-0]'),
('evt_1787722848218_6pi7d', 'match_1787722823111', 0, 0, '00:40:48', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-4 | S2: 2-1 [Pts: 0-15]'),
('evt_1787722848434_az1v5', 'match_1787722823111', 0, 0, '00:40:48', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-4 | S2: 2-1 [Pts: 0-30]'),
('evt_1787722848634_9gcw4', 'match_1787722823111', 0, 0, '00:40:48', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-4 | S2: 2-1 [Pts: 0-40]'),
('evt_1787722849442_ftfuf', 'match_1787722823111', 0, 0, '00:40:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 2-1 [Pts: 15-40]'),
('evt_1787722849667_ah725', 'match_1787722823111', 0, 0, '00:40:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 2-1 [Pts: 30-40]'),
('evt_1787722849900_hu5h4', 'match_1787722823111', 0, 0, '00:40:49', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 2-1 [Pts: 40-40]'),
('evt_1787722850145_7vydr', 'match_1787722823111', 0, 0, '00:40:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 2-1 [Pts: AD-40]'),
('evt_1787722850396_lvqh0', 'match_1787722823111', 0, 0, '00:40:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 3-1 [Pts: 0-0]'),
('evt_1787722850641_yx7p3', 'match_1787722823111', 0, 0, '00:40:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 3-1 [Pts: 15-0]'),
('evt_1787722850858_okcx8', 'match_1787722823111', 0, 0, '00:40:50', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 3-1 [Pts: 30-0]'),
('evt_1787722851098_mvhjm', 'match_1787722823111', 0, 0, '00:40:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 3-1 [Pts: 40-0]'),
('evt_1787722851337_o0zmt', 'match_1787722823111', 0, 0, '00:40:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 4-1 [Pts: 0-0]'),
('evt_1787722851593_lba5r', 'match_1787722823111', 0, 0, '00:40:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 4-1 [Pts: 15-0]'),
('evt_1787722851843_l0j39', 'match_1787722823111', 0, 0, '00:40:51', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 4-1 [Pts: 30-0]'),
('evt_1787722852075_wh19w', 'match_1787722823111', 0, 0, '00:40:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 4-1 [Pts: 40-0]'),
('evt_1787722852306_et2gi', 'match_1787722823111', 0, 0, '00:40:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 5-1 [Pts: 0-0]'),
('evt_1787722852546_1cwol', 'match_1787722823111', 0, 0, '00:40:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 5-1 [Pts: 15-0]'),
('evt_1787722852800_4qqfx', 'match_1787722823111', 0, 0, '00:40:52', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 5-1 [Pts: 30-0]'),
('evt_1787722853049_ihw3n', 'match_1787722823111', 0, 0, '00:40:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 5-1 [Pts: 40-0]'),
('evt_1787722853290_hv851', 'match_1787722823111', 0, 0, '00:40:53', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-4 | S2: 6-1 [Pts: 0-0]'),
('evt_1787723636260_5k9tj', 'match_1787723625046', 0, 0, '00:53:56', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787723637091_uxfmh', 'match_1787723625046', 0, 0, '00:53:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-0]'),
('evt_1787723637314_nf5dz', 'match_1787723625046', 0, 0, '00:53:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 40-0]'),
('evt_1787723637530_c2wb7', 'match_1787723625046', 0, 0, '00:53:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 0-0]'),
('evt_1787723637730_toyra', 'match_1787723625046', 0, 0, '00:53:57', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 15-0]'),
('evt_1787723638250_zce2q', 'match_1787723625046', 0, 0, '00:53:58', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-0 [Pts: 15-15]'),
('evt_1787723638562_gns28', 'match_1787723625046', 0, 0, '00:53:58', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 1-0 [Pts: 15-30]'),
('evt_1787723639097_9v04k', 'match_1787723625046', 0, 0, '00:53:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-30]'),
('evt_1787723639443_ez3sn', 'match_1787723625046', 0, 0, '00:53:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 40-30]'),
('evt_1787723639690_pbt6j', 'match_1787723625046', 0, 0, '00:53:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 0-0]'),
('evt_1787723639915_2rcbo', 'match_1787723625046', 0, 0, '00:53:59', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 15-0]'),
('evt_1787723640153_y1qkf', 'match_1787723625046', 0, 0, '00:54:00', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 30-0]'),
('evt_1787723640378_isn8x', 'match_1787723625046', 0, 0, '00:54:00', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 40-0]'),
('evt_1787723640618_xb8un', 'match_1787723625046', 0, 0, '00:54:00', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 0-0]'),
('evt_1787723640833_4z2qx', 'match_1787723625046', 0, 0, '00:54:00', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 15-0]'),
('evt_1787723641057_kczou', 'match_1787723625046', 0, 0, '00:54:01', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 30-0]'),
('evt_1787723641265_q75bu', 'match_1787723625046', 0, 0, '00:54:01', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 40-0]'),
('evt_1787723641497_7e5uf', 'match_1787723625046', 0, 0, '00:54:01', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 0-0]'),
('evt_1787723641722_j1huc', 'match_1787723625046', 0, 0, '00:54:01', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 15-0]'),
('evt_1787723641937_fer06', 'match_1787723625046', 0, 0, '00:54:01', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 30-0]'),
('evt_1787723642153_58rgp', 'match_1787723625046', 0, 0, '00:54:02', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 40-0]'),
('evt_1787723642385_v3liu', 'match_1787723625046', 0, 0, '00:54:02', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-0 [Pts: 0-0]'),
('evt_1787723642609_29086', 'match_1787723625046', 0, 0, '00:54:02', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-0 [Pts: 15-0]'),
('evt_1787723642827_myhar', 'match_1787723625046', 0, 0, '00:54:02', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-0 [Pts: 30-0]'),
('evt_1787723643051_h8ed7', 'match_1787723625046', 0, 0, '00:54:03', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-0 [Pts: 40-0]'),
('evt_1787723643293_go4ed', 'match_1787723625046', 0, 0, '00:54:03', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 0-0]'),
('evt_1787723643518_2qwxm', 'match_1787723625046', 0, 0, '00:54:03', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 15-0]'),
('evt_1787723643753_vlzn9', 'match_1787723625046', 0, 0, '00:54:03', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 30-0]'),
('evt_1787723643993_ugzpb', 'match_1787723625046', 0, 0, '00:54:03', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 40-0]'),
('evt_1787723644224_4we3w', 'match_1787723625046', 0, 0, '00:54:04', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 1-0 [Pts: 0-0]'),
('evt_1787723644465_9ofl6', 'match_1787723625046', 0, 0, '00:54:04', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 1-0 [Pts: 15-0]'),
('evt_1787723644689_d6km0', 'match_1787723625046', 0, 0, '00:54:04', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 1-0 [Pts: 30-0]'),
('evt_1787723644937_2dh78', 'match_1787723625046', 0, 0, '00:54:04', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 1-0 [Pts: 40-0]'),
('evt_1787723645159_64cwt', 'match_1787723625046', 0, 0, '00:54:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 2-0 [Pts: 0-0]'),
('evt_1787723645391_jx482', 'match_1787723625046', 0, 0, '00:54:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 2-0 [Pts: 15-0]'),
('evt_1787723645630_xb2s9', 'match_1787723625046', 0, 0, '00:54:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 2-0 [Pts: 30-0]'),
('evt_1787723645871_jwo3e', 'match_1787723625046', 0, 0, '00:54:05', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 2-0 [Pts: 40-0]'),
('evt_1787723646100_w6nox', 'match_1787723625046', 0, 0, '00:54:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 3-0 [Pts: 0-0]'),
('evt_1787723646338_gon2u', 'match_1787723625046', 0, 0, '00:54:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 3-0 [Pts: 15-0]'),
('evt_1787723646643_8iflj', 'match_1787723625046', 0, 0, '00:54:06', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 3-0 [Pts: 30-0]'),
('evt_1787723647077_br63e', 'match_1787723625046', 0, 0, '00:54:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 3-0 [Pts: 40-0]'),
('evt_1787723647307_b5b7f', 'match_1787723625046', 0, 0, '00:54:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 4-0 [Pts: 0-0]'),
('evt_1787723647521_9bwqh', 'match_1787723625046', 0, 0, '00:54:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 4-0 [Pts: 15-0]'),
('evt_1787723647751_uvm6p', 'match_1787723625046', 0, 0, '00:54:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 4-0 [Pts: 30-0]'),
('evt_1787723647981_gvgnu', 'match_1787723625046', 0, 0, '00:54:07', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 4-0 [Pts: 40-0]'),
('evt_1787723648461_hxf16', 'match_1787723625046', 0, 0, '00:54:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 5-0 [Pts: 0-0]'),
('evt_1787723648772_gv2fe', 'match_1787723625046', 0, 0, '00:54:08', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 5-0 [Pts: 15-0]'),
('evt_1787723649000_6mrig', 'match_1787723625046', 0, 0, '00:54:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 5-0 [Pts: 30-0]'),
('evt_1787723649236_03o99', 'match_1787723625046', 0, 0, '00:54:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 5-0 [Pts: 40-0]'),
('evt_1787723649474_kek18', 'match_1787723625046', 0, 0, '00:54:09', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 6-0 [Pts: 0-0]'),
('evt_1787750071431_g1gbo', 'match_1787750047902', 0, 0, '08:14:31 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 15-0]'),
('evt_1787750071702_6pg9u', 'match_1787750047902', 0, 0, '08:14:31 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 15-15]'),
('evt_1787750071891_r94vo', 'match_1787750047902', 0, 0, '08:14:31 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 30-15]'),
('evt_1787750072178_358qx', 'match_1787750047902', 0, 0, '08:14:32 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: 40-15]'),
('evt_1787750072432_o3dql', 'match_1787750047902', 0, 0, '08:14:32 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 40-30]'),
('evt_1787750073395_nkl8i', 'match_1787750047902', 0, 0, '08:14:33 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 0-0 [Pts: 40-40]'),
('evt_1787750073642_ojuzg', 'match_1787750047902', 0, 0, '08:14:33 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 0-0 [Pts: AD-40]'),
('evt_1787750074277_ix9st', 'match_1787750047902', 0, 0, '08:14:34 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 0-0]'),
('evt_1787750074446_bvrw6', 'match_1787750047902', 0, 0, '08:14:34 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 15-0]'),
('evt_1787750074602_vgk8d', 'match_1787750047902', 0, 0, '08:14:34 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 30-0]'),
('evt_1787750074759_3hpvu', 'match_1787750047902', 0, 0, '08:14:34 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 1-0 [Pts: 40-0]'),
('evt_1787750074916_si9u3', 'match_1787750047902', 0, 0, '08:14:34 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 0-0]'),
('evt_1787750075080_a7dmt', 'match_1787750047902', 0, 0, '08:14:35 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 15-0]'),
('evt_1787750075227_9drlu', 'match_1787750047902', 0, 0, '08:14:35 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 30-0]'),
('evt_1787750075392_10mcl', 'match_1787750047902', 0, 0, '08:14:35 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 2-0 [Pts: 40-0]'),
('evt_1787750075550_75n69', 'match_1787750047902', 0, 0, '08:14:35 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 0-0]'),
('evt_1787750075719_k17gk', 'match_1787750047902', 0, 0, '08:14:35 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 15-0]'),
('evt_1787750075869_76sm0', 'match_1787750047902', 0, 0, '08:14:35 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 30-0]'),
('evt_1787750076048_h5pif', 'match_1787750047902', 0, 0, '08:14:36 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 3-0 [Pts: 40-0]'),
('evt_1787750076392_o0l6m', 'match_1787750047902', 0, 0, '08:14:36 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 0-0]'),
('evt_1787750076568_rjkmr', 'match_1787750047902', 0, 0, '08:14:36 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 15-0]'),
('evt_1787750076794_fkik3', 'match_1787750047902', 0, 0, '08:14:36 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 30-0]'),
('evt_1787750076980_hn6tp', 'match_1787750047902', 0, 0, '08:14:36 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 4-0 [Pts: 40-0]'),
('evt_1787750077182_3jwos', 'match_1787750047902', 0, 0, '08:14:37 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-0 [Pts: 0-0]'),
('evt_1787750077366_pucm6', 'match_1787750047902', 0, 0, '08:14:37 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-0 [Pts: 15-0]'),
('evt_1787750077567_ha3wh', 'match_1787750047902', 0, 0, '08:14:37 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-0 [Pts: 30-0]'),
('evt_1787750077793_ewokd', 'match_1787750047902', 0, 0, '08:14:37 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 5-0 [Pts: 40-0]'),
('evt_1787750077984_5he8m', 'match_1787750047902', 0, 0, '08:14:37 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 0-0]'),
('evt_1787750078190_7js9f', 'match_1787750047902', 0, 0, '08:14:38 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 15-0]'),
('evt_1787750078609_kr7ua', 'match_1787750047902', 0, 0, '08:14:38 a.m.', 'A', NULL, NULL, 'POINT', 'ochoa / jimenez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 30-0]'),
('evt_1787750079128_kdvbi', 'match_1787750047902', 0, 0, '08:14:39 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 30-15]'),
('evt_1787750079348_pmk40', 'match_1787750047902', 0, 0, '08:14:39 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 30-30]'),
('evt_1787750079530_69s77', 'match_1787750047902', 0, 0, '08:14:39 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-0 [Pts: 30-40]'),
('evt_1787750079712_qp2ch', 'match_1787750047902', 0, 0, '08:14:39 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-1 [Pts: 0-0]'),
('evt_1787750080213_9nhu2', 'match_1787750047902', 0, 0, '08:14:40 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-1 [Pts: 0-15]'),
('evt_1787750080509_n51f1', 'match_1787750047902', 0, 0, '08:14:40 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-1 [Pts: 0-30]'),
('evt_1787750080712_040v9', 'match_1787750047902', 0, 0, '08:14:40 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-1 [Pts: 0-40]'),
('evt_1787750080923_mvkm3', 'match_1787750047902', 0, 0, '08:14:40 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-2 [Pts: 0-0]'),
('evt_1787750081112_skd98', 'match_1787750047902', 0, 0, '08:14:41 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-2 [Pts: 0-15]'),
('evt_1787750081296_gtiau', 'match_1787750047902', 0, 0, '08:14:41 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-2 [Pts: 0-30]'),
('evt_1787750081860_hejom', 'match_1787750047902', 0, 0, '08:14:41 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-2 [Pts: 0-40]'),
('evt_1787750082057_68hgd', 'match_1787750047902', 0, 0, '08:14:42 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-3 [Pts: 0-0]'),
('evt_1787750082259_oo6fs', 'match_1787750047902', 0, 0, '08:14:42 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-3 [Pts: 0-15]'),
('evt_1787750082442_36wik', 'match_1787750047902', 0, 0, '08:14:42 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-3 [Pts: 0-30]'),
('evt_1787750082621_gemn6', 'match_1787750047902', 0, 0, '08:14:42 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-3 [Pts: 0-40]'),
('evt_1787750082842_671hh', 'match_1787750047902', 0, 0, '08:14:42 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-4 [Pts: 0-0]'),
('evt_1787750083061_ar9jd', 'match_1787750047902', 0, 0, '08:14:43 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-4 [Pts: 0-15]'),
('evt_1787750083256_hs1u3', 'match_1787750047902', 0, 0, '08:14:43 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-4 [Pts: 0-30]'),
('evt_1787750083437_mu0pd', 'match_1787750047902', 0, 0, '08:14:43 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-4 [Pts: 0-40]'),
('evt_1787750083626_sg3yu', 'match_1787750047902', 0, 0, '08:14:43 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-5 [Pts: 0-0]'),
('evt_1787750083813_335nz', 'match_1787750047902', 0, 0, '08:14:43 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-5 [Pts: 0-15]'),
('evt_1787750084001_x7uxf', 'match_1787750047902', 0, 0, '08:14:44 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-5 [Pts: 0-30]'),
('evt_1787750084177_d2dlc', 'match_1787750047902', 0, 0, '08:14:44 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-5 [Pts: 0-40]'),
('evt_1787750084365_3bzyp', 'match_1787750047902', 0, 0, '08:14:44 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-0 [Pts: 0-0]'),
('evt_1787750084566_khgsb', 'match_1787750047902', 0, 0, '08:14:44 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-0 [Pts: 0-15]'),
('evt_1787750084757_0ga66', 'match_1787750047902', 0, 0, '08:14:44 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-0 [Pts: 0-30]'),
('evt_1787750085075_plxta', 'match_1787750047902', 0, 0, '08:14:45 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-0 [Pts: 0-40]'),
('evt_1787750085281_hm0w0', 'match_1787750047902', 0, 0, '08:14:45 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-1 [Pts: 0-0]'),
('evt_1787750085470_l188u', 'match_1787750047902', 0, 0, '08:14:45 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-1 [Pts: 0-15]'),
('evt_1787750085672_91vad', 'match_1787750047902', 0, 0, '08:14:45 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-1 [Pts: 0-30]'),
('evt_1787750085859_9m481', 'match_1787750047902', 0, 0, '08:14:45 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-1 [Pts: 0-40]'),
('evt_1787750086079_ao5vh', 'match_1787750047902', 0, 0, '08:14:46 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-2 [Pts: 0-0]'),
('evt_1787750086280_hu8tp', 'match_1787750047902', 0, 0, '08:14:46 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-2 [Pts: 0-15]'),
('evt_1787750086475_jqs2d', 'match_1787750047902', 0, 0, '08:14:46 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-2 [Pts: 0-30]'),
('evt_1787750086660_nq8uq', 'match_1787750047902', 0, 0, '08:14:46 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-2 [Pts: 0-40]'),
('evt_1787750086850_3xsir', 'match_1787750047902', 0, 0, '08:14:46 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-3 [Pts: 0-0]'),
('evt_1787750087028_7aa26', 'match_1787750047902', 0, 0, '08:14:47 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-3 [Pts: 0-15]'),
('evt_1787750087235_m3s7c', 'match_1787750047902', 0, 0, '08:14:47 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-3 [Pts: 0-30]'),
('evt_1787750087425_kwh7s', 'match_1787750047902', 0, 0, '08:14:47 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-3 [Pts: 0-40]'),
('evt_1787750087634_mp453', 'match_1787750047902', 0, 0, '08:14:47 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-4 [Pts: 0-0]'),
('evt_1787750087835_w25h1', 'match_1787750047902', 0, 0, '08:14:47 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-4 [Pts: 0-15]'),
('evt_1787750088032_xdq1l', 'match_1787750047902', 0, 0, '08:14:48 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-4 [Pts: 0-30]'),
('evt_1787750088220_1z2yc', 'match_1787750047902', 0, 0, '08:14:48 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-4 [Pts: 0-40]'),
('evt_1787750088419_a1kld', 'match_1787750047902', 0, 0, '08:14:48 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-5 [Pts: 0-0]'),
('evt_1787750088706_gvocf', 'match_1787750047902', 0, 0, '08:14:48 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-5 [Pts: 0-15]'),
('evt_1787750088913_w8w4c', 'match_1787750047902', 0, 0, '08:14:48 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-5 [Pts: 0-30]'),
('evt_1787750089116_u0q46', 'match_1787750047902', 0, 0, '08:14:49 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-5 [Pts: 0-40]'),
('evt_1787750089349_5b17t', 'match_1787750047902', 0, 0, '08:14:49 a.m.', 'B', NULL, NULL, 'POINT', 'torres / lopez gana punto (POINT)', 'S1: 6-0 | S2: 0-6 | S3: 0-6 [Pts: 0-0]');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `match_players`
--

CREATE TABLE `match_players` (
  `match_id` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `pair_id` varchar(255) DEFAULT NULL,
  `team` enum('A','B') NOT NULL,
  `player_number` tinyint(3) UNSIGNED NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notifications`
--

CREATE TABLE `notifications` (
  `id` varchar(255) NOT NULL,
  `title` text NOT NULL,
  `body` text DEFAULT NULL,
  `timestamp` text NOT NULL,
  `read` int(11) NOT NULL,
  `type` text NOT NULL,
  `link_id` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `notifications`
--

INSERT INTO `notifications` (`id`, `title`, `body`, `timestamp`, `read`, `type`, `link_id`) VALUES
('notif_1', '🔴 ¡Partido en Vivo Activo!', 'Gran Final: Galán / Lebrón vs Coello / Tapia se está disputando en Pista Central.', 'Hace 5 min', 0, 'MATCH', 'match_live_01'),
('notif_2', '🎾 Horario de tu próximo partido', 'Atención: Tu partido de Cuartos de Final se jugará hoy a las 18:30 h en Pista 2.', 'Hace 1 hora', 0, 'MATCH', 'match_upcoming_02'),
('notif_3', '🏆 Inscripciones Abiertas', 'Se ha abierto la inscripción para la Copa Abierta Barcelona 2026.', 'Ayer', 1, 'TOURNAMENT', 'tour_open_barcelona');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pairs`
--

CREATE TABLE `pairs` (
  `id` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `player1_id` text NOT NULL,
  `player2_id` text NOT NULL,
  `player1_name` text NOT NULL,
  `player2_name` text NOT NULL,
  `player1_avatar` text DEFAULT NULL,
  `player2_avatar` text DEFAULT NULL,
  `created_at` text DEFAULT NULL,
  `status` text NOT NULL,
  `tournaments_disputed` int(11) DEFAULT NULL,
  `titles_won` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `pairs`
--

INSERT INTO `pairs` (`id`, `name`, `player1_id`, `player2_id`, `player1_name`, `player2_name`, `player1_avatar`, `player2_avatar`, `created_at`, `status`, `tournaments_disputed`, `titles_won`) VALUES
('pair_1787699331943', 'ochoa / jimenez', 'usr_1787699245097', 'usr_1787699287537', 'german ochoa', 'jhoan jimenez', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', '2026-08-25', 'ACTIVE', NULL, NULL),
('pair_1787699340031', 'torres / lopez', 'usr_1787699179707', 'usr_1787699316417', 'Leo torres', 'daniel lopez', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', '2026-08-25', 'ACTIVE', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `privacy_settings`
--

CREATE TABLE `privacy_settings` (
  `user_id` varchar(255) NOT NULL,
  `profile_visibility` enum('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PUBLIC',
  `points_visibility` enum('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PUBLIC',
  `games_visibility` enum('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PUBLIC',
  `tournaments_visibility` enum('PUBLIC','PRIVATE') NOT NULL DEFAULT 'PUBLIC',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profiles`
--

CREATE TABLE `profiles` (
  `user_id` varchar(255) NOT NULL,
  `bio` text DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `preferred_position` enum('RIGHT','LEFT','BOTH') DEFAULT NULL,
  `skill_level` enum('BEGINNER','INTERMEDIATE','ADVANCED','PRO') DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tournaments`
--

CREATE TABLE `tournaments` (
  `id` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `logo` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `category` text DEFAULT NULL,
  `level` text DEFAULT NULL,
  `location` text DEFAULT NULL,
  `start_date` text DEFAULT NULL,
  `end_date` text DEFAULT NULL,
  `status` text DEFAULT NULL,
  `format` text DEFAULT NULL,
  `max_pairs` int(11) DEFAULT NULL,
  `registered_pair_ids` text DEFAULT NULL,
  `rules` text DEFAULT NULL,
  `court_ids` text DEFAULT NULL,
  `registered_user_ids` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tournament_categories`
--

CREATE TABLE `tournament_categories` (
  `id` varchar(255) NOT NULL,
  `tournament_id` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `level` varchar(100) DEFAULT NULL,
  `max_pairs` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tournament_pairs`
--

CREATE TABLE `tournament_pairs` (
  `tournament_id` varchar(255) NOT NULL,
  `pair_id` varchar(255) NOT NULL,
  `category_id` varchar(255) DEFAULT NULL,
  `seed` int(11) DEFAULT NULL,
  `status` enum('REGISTERED','ACTIVE','ELIMINATED','CHAMPION','WITHDRAWN') NOT NULL DEFAULT 'REGISTERED',
  `joined_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tournament_players`
--

CREATE TABLE `tournament_players` (
  `tournament_id` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `category_id` varchar(255) DEFAULT NULL,
  `status` enum('REGISTERED','ACTIVE','ELIMINATED','WITHDRAWN','CHAMPION') NOT NULL DEFAULT 'REGISTERED',
  `joined_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tournament_rounds`
--

CREATE TABLE `tournament_rounds` (
  `id` varchar(255) NOT NULL,
  `tournament_id` varchar(255) NOT NULL,
  `category_id` varchar(255) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `round_number` int(11) NOT NULL,
  `round_type` enum('GROUP','ROUND_OF_32','ROUND_OF_16','QUARTERFINAL','SEMIFINAL','FINAL') NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` varchar(255) NOT NULL,
  `name` text NOT NULL,
  `surname` text NOT NULL,
  `username` text NOT NULL,
  `email` text NOT NULL,
  `role` text NOT NULL,
  `avatar` text DEFAULT NULL,
  `level` text DEFAULT NULL,
  `position` text DEFAULT NULL,
  `dominant_hand` text DEFAULT NULL,
  `current_pair_id` text DEFAULT NULL,
  `points` int(11) DEFAULT 0,
  `partner_name` text DEFAULT NULL,
  `phone` text DEFAULT NULL,
  `stats` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `surname`, `username`, `email`, `role`, `avatar`, `level`, `position`, `dominant_hand`, `current_pair_id`, `points`, `partner_name`, `phone`, `stats`) VALUES
('usr_1787699179707', 'Leo', 'torres', 'leo', 'leo@gmail.com', 'PLAYER', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', 'Intermedio', 'Ambas', NULL, NULL, 240, NULL, '30000000', '{\"pointsWon\": 0, \"winners\": 0, \"smashes\": 0, \"smashesWon\": 0, \"voleasWon\": 0, \"bandejas\": 0, \"viboras\": 0, \"remates\": 0, \"netPointsWon\": 0, \"touches\": 0, \"shots\": 0, \"serves\": 0, \"firstServes\": 0, \"secondServes\": 0, \"aces\": 0, \"doubleFaults\": 0, \"breakPoints\": 0, \"breakPointsWon\": 0, \"recoveries\": 0, \"globos\": 0, \"devoluciones\": 0, \"movesCount\": 0, \"matchesPlayed\": 4, \"matchesWon\": 1, \"matchesLost\": 3, \"setsWon\": 1, \"setsLost\": 8, \"gamesWon\": 0, \"gamesLost\": 0, \"timePlayedMin\": 0, \"avgSpeedKmh\": 0, \"distanceKm\": 0, \"points\": 240}'),
('usr_1787699245097', 'german', 'ochoa', 'german', 'german@gmail.com', 'PLAYER', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', 'Intermedio', 'Drive (Derecha)', NULL, NULL, 480, NULL, '3000000', '{\"pointsWon\": 0, \"winners\": 0, \"smashes\": 0, \"smashesWon\": 0, \"voleasWon\": 0, \"bandejas\": 0, \"viboras\": 0, \"remates\": 0, \"netPointsWon\": 0, \"touches\": 0, \"shots\": 0, \"serves\": 0, \"firstServes\": 0, \"secondServes\": 0, \"aces\": 0, \"doubleFaults\": 0, \"breakPoints\": 0, \"breakPointsWon\": 0, \"recoveries\": 0, \"globos\": 0, \"devoluciones\": 0, \"movesCount\": 0, \"matchesPlayed\": 4, \"matchesWon\": 3, \"matchesLost\": 1, \"setsWon\": 4, \"setsLost\": 5, \"gamesWon\": 0, \"gamesLost\": 0, \"timePlayedMin\": 0, \"avgSpeedKmh\": 0, \"distanceKm\": 0, \"points\": 480}'),
('usr_1787699287537', 'jhoan', 'jimenez', 'jhoan', 'jhoan@gmail.com', 'PLAYER', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', 'Intermedio', 'Drive (Derecha)', NULL, NULL, 480, NULL, '300000', '{\"pointsWon\": 0, \"winners\": 0, \"smashes\": 0, \"smashesWon\": 0, \"voleasWon\": 0, \"bandejas\": 0, \"viboras\": 0, \"remates\": 0, \"netPointsWon\": 0, \"touches\": 0, \"shots\": 0, \"serves\": 0, \"firstServes\": 0, \"secondServes\": 0, \"aces\": 0, \"doubleFaults\": 0, \"breakPoints\": 0, \"breakPointsWon\": 0, \"recoveries\": 0, \"globos\": 0, \"devoluciones\": 0, \"movesCount\": 0, \"matchesPlayed\": 4, \"matchesWon\": 3, \"matchesLost\": 1, \"setsWon\": 4, \"setsLost\": 5, \"gamesWon\": 0, \"gamesLost\": 0, \"timePlayedMin\": 0, \"avgSpeedKmh\": 0, \"distanceKm\": 0, \"points\": 480}'),
('usr_1787699316417', 'daniel', 'lopez', 'daniel', 'daniel@gmail.com', 'PLAYER', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80', 'Intermedio', 'Drive (Derecha)', NULL, NULL, 240, NULL, '30000', '{\"pointsWon\": 0, \"winners\": 0, \"smashes\": 0, \"smashesWon\": 0, \"voleasWon\": 0, \"bandejas\": 0, \"viboras\": 0, \"remates\": 0, \"netPointsWon\": 0, \"touches\": 0, \"shots\": 0, \"serves\": 0, \"firstServes\": 0, \"secondServes\": 0, \"aces\": 0, \"doubleFaults\": 0, \"breakPoints\": 0, \"breakPointsWon\": 0, \"recoveries\": 0, \"globos\": 0, \"devoluciones\": 0, \"movesCount\": 0, \"matchesPlayed\": 4, \"matchesWon\": 1, \"matchesLost\": 3, \"setsWon\": 1, \"setsLost\": 8, \"gamesWon\": 0, \"gamesLost\": 0, \"timePlayedMin\": 0, \"avgSpeedKmh\": 0, \"distanceKm\": 0, \"points\": 240}'),
('usr_carlos_admin', 'Carlos', 'Gómez', 'carlospadel', 'carlos@padelpro.app', 'ADMIN', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80', 'Avanzado', 'Revés (Izquierda)', 'Derecha', 'pair_galan_lebron', 1520, 'Juan Lebrón', '+34 612 345 678', '{\"points_won\": 1842, \"winners\": 312, \"smashes\": 180, \"smashes_won\": 142, \"voleas_won\": 128, \"bandejas\": 95, \"viboras\": 64, \"remates\": 110, \"net_points_won\": 412, \"touches\": 4210, \"shots\": 3890, \"serves\": 820, \"first_serves\": 610, \"second_serves\": 210, \"aces\": 42, \"double_faults\": 18, \"break_points\": 94, \"break_points_won\": 58, \"recoveries\": 182, \"globos\": 340, \"devoluciones\": 680, \"points_saved\": 88, \"unforced_errors\": 187, \"distance_km\": 94.3, \"time_played_min\": 1420, \"avg_speed_kmh\": 12.4, \"moves_count\": 2840, \"matches_played\": 24, \"matches_won\": 17, \"matches_lost\": 7, \"sets_won\": 38, \"sets_lost\": 21, \"games_won\": 241, \"games_lost\": 198}');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_auth`
--

CREATE TABLE `users_auth` (
  `user_id` varchar(255) NOT NULL,
  `email` text NOT NULL,
  `hashed_password` text NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `email_verified_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `users_auth`
--

INSERT INTO `users_auth` (`user_id`, `email`, `hashed_password`, `last_login`, `email_verified_at`, `created_at`, `updated_at`) VALUES
('usr_1787371091916', 'lucho@gmail.com', '$2b$12$.SSyVqDZPfV2FBBhOW5PNedwhqmJ.xPQWAqMyGK7OxlE2MN6t.3CK', NULL, NULL, '2026-08-30 18:09:42', '2026-08-30 18:09:42'),
('usr_carlos_admin', 'admin@padelpro.app', '$2b$12$9HUHq/VNk03bpCjXvIjri.lAfLdDgPU4kWaEfY3BL5PvPZhKR9Tbq', NULL, NULL, '2026-08-30 18:09:42', '2026-08-30 18:09:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_points`
--

CREATE TABLE `user_points` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `match_id` varchar(255) DEFAULT NULL,
  `tournament_id` varchar(255) DEFAULT NULL,
  `points` int(11) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_roles`
--

CREATE TABLE `user_roles` (
  `user_id` varchar(255) NOT NULL,
  `role_id` int(10) UNSIGNED NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `businesses`
--
ALTER TABLE `businesses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_business_created_by` (`created_by`);

--
-- Indices de la tabla `business_users`
--
ALTER TABLE `business_users`
  ADD PRIMARY KEY (`business_id`,`user_id`),
  ADD KEY `idx_business_users_user` (`user_id`);

--
-- Indices de la tabla `courts`
--
ALTER TABLE `courts`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `gesture_config`
--
ALTER TABLE `gesture_config`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `matches`
--
ALTER TABLE `matches`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `match_events`
--
ALTER TABLE `match_events`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `match_players`
--
ALTER TABLE `match_players`
  ADD PRIMARY KEY (`match_id`,`user_id`),
  ADD KEY `idx_match_players_user` (`user_id`),
  ADD KEY `idx_match_players_pair` (`pair_id`);

--
-- Indices de la tabla `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pairs`
--
ALTER TABLE `pairs`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `privacy_settings`
--
ALTER TABLE `privacy_settings`
  ADD PRIMARY KEY (`user_id`);

--
-- Indices de la tabla `profiles`
--
ALTER TABLE `profiles`
  ADD PRIMARY KEY (`user_id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_roles_name` (`name`);

--
-- Indices de la tabla `tournaments`
--
ALTER TABLE `tournaments`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tournament_categories`
--
ALTER TABLE `tournament_categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_tc_tournament` (`tournament_id`);

--
-- Indices de la tabla `tournament_pairs`
--
ALTER TABLE `tournament_pairs`
  ADD PRIMARY KEY (`tournament_id`,`pair_id`),
  ADD KEY `idx_tp_pair` (`pair_id`),
  ADD KEY `idx_tp_category` (`category_id`);

--
-- Indices de la tabla `tournament_players`
--
ALTER TABLE `tournament_players`
  ADD PRIMARY KEY (`tournament_id`,`user_id`),
  ADD KEY `idx_tournament_players_user` (`user_id`),
  ADD KEY `idx_tournament_players_category` (`category_id`);

--
-- Indices de la tabla `tournament_rounds`
--
ALTER TABLE `tournament_rounds`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_round_tournament` (`tournament_id`),
  ADD KEY `idx_round_category` (`category_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`) USING HASH,
  ADD UNIQUE KEY `email` (`email`) USING HASH;

--
-- Indices de la tabla `users_auth`
--
ALTER TABLE `users_auth`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`) USING HASH;

--
-- Indices de la tabla `user_points`
--
ALTER TABLE `user_points`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_points_user` (`user_id`),
  ADD KEY `idx_user_points_match` (`match_id`),
  ADD KEY `idx_user_points_tournament` (`tournament_id`);

--
-- Indices de la tabla `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`user_id`,`role_id`),
  ADD KEY `idx_user_roles_role` (`role_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `user_points`
--
ALTER TABLE `user_points`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
