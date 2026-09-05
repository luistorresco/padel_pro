const API_BASE_NORMALIZED = ((import.meta as unknown as { env?: Record<string, string | undefined> }).env?.VITE_API_BASE_NORMALIZED || '').replace(/\/+$/, '');

export { API_BASE_NORMALIZED };

let authToken: string | null = null;

export function setAuthToken(token: string | null) {
  authToken = token;
}

function mergeHeaders(base: Record<string, string> = {}): Record<string, string> {
  if (authToken) {
    return { ...base, Authorization: `Bearer ${authToken}` };
  }
  return base;
}

async function handleResponse(response: Response) {
  if (!response.ok) {
    const text = await response.text();
    let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
    try {
      const errorJson = JSON.parse(text);
      errorMessage = errorJson.detail || errorJson.message || errorMessage;
    } catch {
      if (text) errorMessage = text;
    }
    throw new Error(errorMessage);
  }
  return response.json();
}

export const api = {
  getUsers: () => fetch(`${API_BASE_NORMALIZED}/api/users`, { headers: mergeHeaders() }).then(handleResponse),
  getCurrentUser: () => fetch(`${API_BASE_NORMALIZED}/api/users/me`, { headers: mergeHeaders() }).then(handleResponse),
  createUser: (user: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/users`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(user),
  }).then(handleResponse),
  updateUser: (userId: string, user: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/users/${userId}`, {
    method: 'PUT',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(user),
  }).then(handleResponse),
  deleteUser: (userId: string) => fetch(`${API_BASE_NORMALIZED}/api/users/${userId}`, {
    method: 'DELETE',
    headers: mergeHeaders(),
  }).then(handleResponse),

  getPairs: () => fetch(`${API_BASE_NORMALIZED}/api/pairs`, { headers: mergeHeaders() }).then(handleResponse),
  getPair: (pairId: string) => fetch(`${API_BASE_NORMALIZED}/api/pairs/${pairId}`, { headers: mergeHeaders() }).then(handleResponse),
  createPair: (pair: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/pairs`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(pair),
  }).then(handleResponse),
  deletePair: (pairId: string) => fetch(`${API_BASE_NORMALIZED}/api/pairs/${pairId}`, {
    method: 'DELETE',
    headers: mergeHeaders(),
  }).then(handleResponse),

  getTournaments: () => fetch(`${API_BASE_NORMALIZED}/api/tournaments`, { headers: mergeHeaders() }).then(handleResponse),
  createTournament: (tournament: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/tournaments`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(tournament),
  }).then(handleResponse),
  deleteTournament: (tournamentId: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}`, {
    method: 'DELETE',
    headers: mergeHeaders(),
  }).then(handleResponse),
  updateTournament: (tournamentId: string, tournament: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}`, {
    method: 'PUT',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(tournament),
  }).then(handleResponse),
  registerPairForTournament: (tournamentId: string, pairId: string, courtId: string, dateTime: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}/register`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ pair_id: pairId, court_id: courtId, date_time: dateTime }),
  }).then(handleResponse),
  registerUser: (tournamentId: string, userId: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}/register_user`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ user_id: userId }),
  }).then(handleResponse),

  getCourts: () => fetch(`${API_BASE_NORMALIZED}/api/courts`, { headers: mergeHeaders() }).then(handleResponse),

  getMatches: () => fetch(`${API_BASE_NORMALIZED}/api/matches`, { headers: mergeHeaders() }).then(handleResponse),
  getMatch: (matchId: string) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}`, { headers: mergeHeaders() }).then(handleResponse),
  createMatch: (match: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/matches`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(match),
  }).then(handleResponse),
  updateMatch: (matchId: string, match: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}`, {
    method: 'PUT',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(match),
  }).then(handleResponse),
  updateMatchCourt: (matchId: string, courtId: string, courtName: string) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}/court`, {
    method: 'PUT',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ court_id: courtId, court_name: courtName }),
  }).then(handleResponse),
  finishMatch: (matchId: string, body: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}/finish`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(body),
  }).then(handleResponse),
  deleteMatch: (matchId: string) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}`, {
    method: 'DELETE',
    headers: mergeHeaders(),
  }).then(handleResponse),
  createMatchEvent: (matchId: string, event: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}/events`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(event),
  }).then(handleResponse),

  getAuditLogs: () => fetch(`${API_BASE_NORMALIZED}/api/audit-logs`, { headers: mergeHeaders() }).then(handleResponse),

  getNotifications: () => fetch(`${API_BASE_NORMALIZED}/api/notifications`, { headers: mergeHeaders() }).then(handleResponse),

  health: () => fetch(`${API_BASE_NORMALIZED}/api/health`).then(handleResponse),

  adminMigrate: () => fetch(`${API_BASE_NORMALIZED}/api/admin/migrate`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
  }).then(handleResponse),

  authMe: (token: string) => fetch(`${API_BASE_NORMALIZED}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  }).then(handleResponse),

  convertGuest: (body: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/users/convert-guest`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(body),
  }).then(handleResponse),
};
