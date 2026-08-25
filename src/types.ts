export type UserRole = 'PLAYER' | 'ADMIN';

export type PlayerLevel = 'Principiante' | 'Intermedio' | 'Avanzado' | 'Profesional';
export type DominantHand = 'Derecha' | 'Zurda';
export type CourtPosition = 'Drive (Derecha)' | 'Revés (Izquierda)' | 'Ambas';

export interface PlayerStats {
  // Offensive
  pointsWon: number;
  winners: number;
  smashes: number;
  smashesWon: number;
  voleasWon: number;
  bandejas: number;
  viboras: number;
  remates: number;
  netPointsWon: number;
  
  // Game & Serve
  touches: number;
  shots: number;
  serves: number;
  firstServes: number;
  secondServes: number;
  aces: number;
  doubleFaults: number;
  breakPoints: number;
  breakPointsWon: number;

  // Defensive
  recoveries: number;
  globos: number;
  devoluciones: number;
  pointsSaved: number;
  unforcedErrors: number;

  // Physical
  distanceKm: number;
  timePlayedMin: number;
  avgSpeedKmh: number;
  movesCount: number;

  // Totals
  matchesPlayed: number;
  matchesWon: number;
  matchesLost: number;
  setsWon: number;
  setsLost: number;
  gamesWon: number;
  gamesLost: number;
}

export interface User {
  id: string;
  name: string;
  surname: string;
  username: string;
  email: string;
  role: UserRole;
  avatar: string;
  level: PlayerLevel;
  position: CourtPosition;
  dominantHand: DominantHand;
  currentPairId?: string;
  points: number;
  stats: PlayerStats;
  partnerName?: string;
  phone?: string;
}

export interface Pair {
  id: string;
  name: string;
  player1Id: string;
  player2Id: string;
  player1Name: string;
  player2Name: string;
  player1Avatar: string;
  player2Avatar: string;
  createdAt: string;
  status: 'ACTIVE' | 'INACTIVE' | 'DISSOLVED';
  tournamentsDisputed?: number;
  titlesWon?: number;
}

export type TournamentCategory = 'Masculino' | 'Femenino' | 'Mixto';
export type TournamentLevel = 'Principiante' | 'Intermedio' | 'Avanzado' | 'Profesional' | 'Open';
export type TournamentStatus = 'UPCOMING' | 'REGISTRATION' | 'ACTIVE' | 'FINISHED' | 'CANCELLED';
export type TournamentFormat = 'Eliminación directa' | 'Fase de grupos' | 'Todos contra todos' | 'Grupos + eliminación directa';

export interface PointsDistribution {
  champion: number;
  runnerUp: number;
  semiFinals: number;
  quarterFinals: number;
  groupStage: number;
}

export interface TournamentRules {
  setsToWin: number; // 2 or 3
  goldenPoint: boolean; // Punto de oro (sin ventaja)
  tieBreakAt: number; // usually 6
  finalSetTieBreak: boolean;
  pointsDistribution: PointsDistribution;
}

export interface Tournament {
  id: string;
  name: string;
  logo: string;
  description: string;
  category: TournamentCategory;
  level: TournamentLevel;
  location: string;
  startDate: string;
  endDate: string;
  status: TournamentStatus;
  format: TournamentFormat;
  maxPairs: number;
  registeredPairIds: string[];
  registeredUserIds: string[];
  rules: TournamentRules;
  courtIds: string[];
}

export interface Court {
  id: string;
  name: string;
  location: string;
  number: number;
  status: 'AVAILABLE' | 'OCCUPIED' | 'MAINTENANCE';
  currentMatchId?: string;
}

export type PadelPointScore = '0' | '15' | '30' | '40' | 'AD' | 'GAME';

export interface GameScore {
  teamAPoints: PadelPointScore;
  teamBPoints: PadelPointScore;
  serverTeam: 'A' | 'B';
  isDeuce?: boolean;
}

export interface SetScore {
  teamAGames: number;
  teamBGames: number;
  isTieBreak: boolean;
  tieBreakPoints?: { teamA: number; teamB: number };
  winner?: 'A' | 'B';
}

export type MatchStatus = 'UPCOMING' | 'LIVE' | 'PAUSED' | 'FINISHED' | 'CANCELLED';

export interface Match {
  id: string;
  tournamentId?: string;
  tournamentName?: string;
  courtId?: string;
  courtName: string;
  dateTime: string;
  pairAId: string;
  pairBId: string;
  pairAName: string;
  pairBName: string;
  playerA1Id: string;
  playerA2Id: string;
  playerB1Id: string;
  playerB2Id: string;
  playerA1Name: string;
  playerA2Name: string;
  playerB1Name: string;
  playerB2Name: string;
  playerA1Avatar: string;
  playerA2Avatar: string;
  playerB1Avatar: string;
  playerB2Avatar: string;
  status: MatchStatus;
  sets: SetScore[];
  currentGame: GameScore;
  currentSetIndex: number;
  winnerPairId?: string;
  winnerTeam?: 'A' | 'B';
  startTimeMs?: number;
  elapsedTimeSec: number;
  goldenPoint: boolean;
  setsToWin: number;
  roundName?: string;
  pointHistory?: Array<{ team: 'A' | 'B'; timestamp: string }>;
}

export type MatchEventType = 
  | 'POINT' 
  | 'ACE' 
  | 'WINNER' 
  | 'SMASH' 
  | 'UNFORCED_ERROR' 
  | 'DOUBLE_FAULT' 
  | 'BREAK_POINT' 
  | 'CORRECTION_UNDO' 
  | 'PAUSE' 
  | 'RESUME';

export interface MatchEvent {
  id: string;
  matchId: string;
  setNumber: number;
  gameNumber: number;
  timestamp: string;
  winningPairId: 'A' | 'B';
  playerId?: string;
  playerName?: string;
  eventType: MatchEventType;
  description: string;
  scoreSnapshot: string;
}

export interface GestureConfiguration {
  pointTeamAGesture: string; // e.g., 'ROCK'
  pointTeamBGesture: string; // e.g., 'CALL'
  undoGesture: string; // e.g., 'THUMB_DOWN'
  cooldownMs: number;
  minConfidence: number;
  requiredHoldFrames: number;
  detectionZone: {
    enabled: boolean;
    xMin: number;
    yMin: number;
    xMax: number;
    yMax: number;
  };
  mode: 'ONE_HAND' | 'TWO_HANDS';
}

export type GestureType = 'POINT_TEAM_A' | 'POINT_TEAM_B' | 'UNDO' | 'NONE';

export interface RecognizedGestureState {
  gesture: GestureType;
  confidence: number;
  progressPercent: number;
  statusText: string;
  handCount: number;
}

export interface AuditLog {
  id: string;
  adminName: string;
  adminEmail: string;
  action: string;
  target: string;
  details: string;
  timestamp: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  body: string;
  timestamp: string;
  read: boolean;
  type: 'MATCH' | 'TOURNAMENT' | 'SYSTEM';
  linkId?: string;
}

export interface GroupTableEntry {
  pairId: string;
  pairName: string;
  played: number;
  won: number;
  lost: number;
  setsWon: number;
  setsLost: number;
  gamesWon: number;
  gamesLost: number;
  points: number;
}
