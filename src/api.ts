const API_BASE_NORMALIZED = (import.meta as unknown as { env?: Record<string, string | undefined> }).env?.VITE_API_BASE_NORMALIZED || 'http://localhost:8000';
const API_BASE_NORMALIZED_NORMALIZED = API_BASE_NORMALIZED.replace(/\/+$/, '');

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
  getUsers: () => fetch(`${API_BASE_NORMALIZED}/api/users`).then(handleResponse),
  getUser: (userId: string) => fetch(`${API_BASE_NORMALIZED}/api/users/${userId}`).then(handleResponse),
  getCurrentUser: () => fetch(`${API_BASE_NORMALIZED}/api/users/me`).then(handleResponse),
  createUser: (user: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  }).then(handleResponse),
  updateUser: (userId: string, user: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/users/${userId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  }).then(handleResponse),
  deleteUser: (userId: string) => fetch(`${API_BASE_NORMALIZED}/api/users/${userId}`, { method: 'DELETE' }).then(handleResponse),

  getPairs: () => fetch(`${API_BASE_NORMALIZED}/api/pairs`).then(handleResponse),
  getPair: (pairId: string) => fetch(`${API_BASE_NORMALIZED}/api/pairs/${pairId}`).then(handleResponse),
  createPair: (pair: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/pairs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(pair),
  }).then(handleResponse),
  deletePair: (pairId: string) => fetch(`${API_BASE_NORMALIZED}/api/pairs/${pairId}`, { method: 'DELETE' }).then(handleResponse),

  getTournaments: () => fetch(`${API_BASE_NORMALIZED}/api/tournaments`).then(handleResponse),
  getTournament: (tournamentId: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}`).then(handleResponse),
  createTournament: (tournament: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/tournaments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(tournament),
  }).then(handleResponse),
  deleteTournament: (tournamentId: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}`, { method: 'DELETE' }).then(handleResponse),
  registerPair: (tournamentId: string, pairId: string) => fetch(`${API_BASE_NORMALIZED}/api/tournaments/${tournamentId}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pair_id: pairId }),
  }).then(handleResponse),

  getCourts: () => fetch(`${API_BASE_NORMALIZED}/api/courts`).then(handleResponse),
  getCourt: (courtId: string) => fetch(`${API_BASE_NORMALIZED}/api/courts/${courtId}`).then(handleResponse),
  updateCourt: (courtId: string, court: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/courts/${courtId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(court),
  }).then(handleResponse),

  getMatches: () => fetch(`${API_BASE_NORMALIZED}/api/matches`).then(handleResponse),
  getMatch: (matchId: string) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}`).then(handleResponse),
  updateMatch: (matchId: string, match: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(match),
  }).then(handleResponse),
  updateMatchCourt: (matchId: string, courtId: string, courtName: string) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}/court`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ court_id: courtId, court_name: courtName }),
  }).then(handleResponse),
  finishMatch: (matchId: string, body: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}/finish`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }).then(handleResponse),
  createMatchEvent: (matchId: string, event: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/matches/${matchId}/events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(event),
  }).then(handleResponse),

  getAuditLogs: () => fetch(`${API_BASE_NORMALIZED}/api/audit-logs`).then(handleResponse),
  createAuditLog: (log: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/audit-logs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(log),
  }).then(handleResponse),

  getNotifications: () => fetch(`${API_BASE_NORMALIZED}/api/notifications`).then(handleResponse),
  createNotification: (notification: Record<string, unknown>) => fetch(`${API_BASE_NORMALIZED}/api/notifications`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(notification),
  }).then(handleResponse),

  getStats: () => fetch(`${API_BASE_NORMALIZED}/api/stats`).then(handleResponse),
};
