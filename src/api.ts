const API_BASE_NORMALIZED = ((import.meta as unknown as { env?: Record<string, string | undefined> }).env?.VITE_API_BASE_NORMALIZED || '/api').replace(/\/+$/, '');

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
  getUser: (userId: string) => fetch(`${API_BASE_NORMALIZED}/api/users/${userId}`, { headers: mergeHeaders() }).then(handleResponse),
  getCurrentUser: () => fetch(`${API_BASE_NORMALIZED}/api/users/me`).then(handleResponse),
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
  getTournament: (tournamentId: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}`, { headers: mergeHeaders() }).then(handleResponse),
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
  registerPair: (tournamentId: string, pairId: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}/register`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ pair_id: pairId }),
  }).then(handleResponse),
  registerUser: (tournamentId: string, userId: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}/register_user`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ user_id: userId }),
  }).then(handleResponse),

  getCourts: () => fetch(`${API_BASE_NORMALIZED}/api/courts`, { headers: mergeHeaders() }).then(handleResponse),
  getCourt: (courtId: string) => fetch(`${API_BASE_NORMALIZED}/api/courts/${courtId}`, { headers: mergeHeaders() }).then(handleResponse),
  updateCourt: (courtId: string, court: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/courts/${courtId}`, {
    method: 'PUT',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(court),
  }).then(handleResponse),

  getMatches: () => fetch(`${API_BASE_NORMALIZED}/api/matches`, { headers: mergeHeaders() }).then(handleResponse),
  getMatch: (matchId: string) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}`, { headers: mergeHeaders() }).then(handleResponse),
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
  createMatchEvent: (matchId: string, event: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}/events`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(event),
  }).then(handleResponse),

  getAuditLogs: () => fetch(`${API_BASE_NORMALIZED}/api/audit-logs`, { headers: mergeHeaders() }).then(handleResponse),
  createAuditLog: (log: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/audit-logs`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(log),
  }).then(handleResponse),

  getNotifications: () => fetch(`${API_BASE_NORMALIZED}/api/notifications`, { headers: mergeHeaders() }).then(handleResponse),
  createNotification: (notification: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/notifications`, {
    method: 'POST',
    headers: mergeHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(notification),
  }).then(handleResponse),

  getStats: () => fetch(`${API_BASE_NORMALIZED}/api/stats`, { headers: mergeHeaders() }).then(handleResponse),

  login: (email: string, password: string) => fetch(`${API_BASE_NORMALIZED}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  }).then(handleResponse),

  register: (data: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  }).then(handleResponse),

  authMe: (token: string) => fetch(`${API_BASE_NORMALIZED}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  }).then(handleResponse),
};
