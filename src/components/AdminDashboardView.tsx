import React, { useState } from 'react';
import { User, Tournament, Match, Court, AuditLog, PlayerStats } from '../types';

interface AdminDashboardViewProps {
  players: User[];
  tournaments: Tournament[];
  matches: Match[];
  courts: Court[];
  auditLogs: AuditLog[];
  onUpdateMatchCourt: (matchId: string, courtId: string, courtName: string) => void;
  onUpdateMatchDateTime: (matchId: string, dateTime: string) => void;
  onUpdateTournament: (tournamentId: string, updates: Record<string, unknown>) => void;
  onRegisterUserForTournament: (tournamentId: string, userId: string) => void;
  onRunUnitTests: () => void;
  onCreateUser: (user: User) => void;
  onDeleteUser: (userId: string) => void;
}

const emptyStats: PlayerStats = {
  pointsWon: 0,
  winners: 0,
  smashes: 0,
  smashesWon: 0,
  voleasWon: 0,
  bandejas: 0,
  viboras: 0,
  remates: 0,
  netPointsWon: 0,
  touches: 0,
  shots: 0,
  serves: 0,
  firstServes: 0,
  secondServes: 0,
  aces: 0,
  doubleFaults: 0,
  breakPoints: 0,
  breakPointsWon: 0,
  recoveries: 0,
  globos: 0,
  devoluciones: 0,
  pointsSaved: 0,
  unforcedErrors: 0,
  distanceKm: 0,
  timePlayedMin: 0,
  avgSpeedKmh: 0,
  movesCount: 0,
  matchesPlayed: 0,
  matchesWon: 0,
  matchesLost: 0,
  setsWon: 0,
  setsLost: 0,
  gamesWon: 0,
  gamesLost: 0,
};

export const AdminDashboardView: React.FC<AdminDashboardViewProps> = ({
  players,
  tournaments,
  matches,
  courts,
  auditLogs,
  onUpdateMatchCourt,
  onUpdateMatchDateTime,
  onUpdateTournament,
  onRegisterUserForTournament,
  onRunUnitTests,
  onCreateUser,
  onDeleteUser,
}) => {
  const [adminTab, setAdminTab] = useState<'PANEL' | 'USUARIOS' | 'PISTAS' | 'TORNEOS' | 'AUDITORIA'>('PANEL');
  const [showCreateUserModal, setShowCreateUserModal] = useState<boolean>(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);
  const [editingMatchId, setEditingMatchId] = useState<string | null>(null);
  const [editMatchDateTime, setEditMatchDateTime] = useState<string>('');
  const [editingTournamentId, setEditingTournamentId] = useState<string | null>(null);
  const [editTournamentStart, setEditTournamentStart] = useState<string>('');
  const [editTournamentEnd, setEditTournamentEnd] = useState<string>('');
  const [selectedTournamentForUsers, setSelectedTournamentForUsers] = useState<string | null>(null);

  const [newUserName, setNewUserName] = useState<string>('');
  const [newUserSurname, setNewUserSurname] = useState<string>('');
  const [newUserUsername, setNewUserUsername] = useState<string>('');
  const [newUserEmail, setNewUserEmail] = useState<string>('');
  const [newUserRole, setNewUserRole] = useState<'PLAYER' | 'ADMIN'>('PLAYER');
  const [newUserLevel, setNewUserLevel] = useState<'Principiante' | 'Intermedio' | 'Avanzado' | 'Profesional'>('Intermedio');
  const [newUserPosition, setNewUserPosition] = useState<'Drive (Derecha)' | 'Revés (Izquierda)' | 'Ambas'>('Drive (Derecha)');
  const [newUserHand, setNewUserHand] = useState<'Derecha' | 'Zurda'>('Derecha');
  const [newUserPhone, setNewUserPhone] = useState<string>('');

  const activeTournaments = tournaments.filter((t) => t.status === 'ACTIVE').length;
  const liveMatches = matches.filter((m) => m.status === 'LIVE').length;

  const handleCreateUserSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUserName.trim() || !newUserSurname.trim() || !newUserUsername.trim() || !newUserEmail.trim()) return;

    const newUser: User = {
      id: 'usr_' + Date.now(),
      name: newUserName.trim(),
      surname: newUserSurname.trim(),
      username: newUserUsername.trim(),
      email: newUserEmail.trim(),
      role: newUserRole,
      avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80',
      level: newUserLevel,
      position: newUserPosition,
      dominantHand: newUserHand,
      points: 0,
      stats: { ...emptyStats },
      phone: newUserPhone.trim() || undefined,
    };

    onCreateUser(newUser);
    setShowCreateUserModal(false);
    setNewUserName('');
    setNewUserSurname('');
    setNewUserUsername('');
    setNewUserEmail('');
    setNewUserRole('PLAYER');
    setNewUserLevel('Intermedio');
    setNewUserPosition('Drive (Derecha)');
    setNewUserHand('Derecha');
    setNewUserPhone('');
  };

  return (
    <div className="flex flex-col gap-5 pb-24 px-4 pt-3 w-full">
      {/* Title */}
      <div className="flex items-center justify-between border-b border-[#333539] pb-3">
        <div>
          <h2 className="font-headline font-black text-[22px] text-white tracking-tight flex items-center gap-2">
            <span className="material-symbols-outlined text-[#c3f400] text-[28px]">shield</span>
            Panel Administrativo Padel Pro
          </h2>
          <p className="text-[12px] text-[#c4c9ac] font-mono-stats">
            Control de usuarios, asignación de pistas, torneos y auditoría
          </p>
        </div>

        <button
          onClick={onRunUnitTests}
          className="bg-[#282a2e] hover:bg-[#333539] text-[#c3f400] text-[11px] font-mono-stats font-bold py-2 px-3 rounded-lg border border-[#c3f400]/40 flex items-center gap-1"
        >
          <span className="material-symbols-outlined text-[16px]">bug_report</span>
          <span>Pruebas Scoring</span>
        </button>
      </div>

      {/* Admin Subtabs */}
      <div className="flex gap-1 bg-[#1e2023] p-1.5 rounded-xl border border-[#333539] text-[11px] font-mono-stats font-bold">
        {(['PANEL', 'USUARIOS', 'PISTAS', 'TORNEOS', 'AUDITORIA'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setAdminTab(tab)}
            className={`flex-1 py-2 rounded-lg transition-all ${
              adminTab === tab
                ? 'bg-[#c3f400] text-[#161e00] shadow-md'
                : 'text-[#c4c9ac] hover:text-white'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Panel Stats Metrics Grid */}
      {adminTab === 'PANEL' && (
        <div className="flex flex-col gap-4">
          <div className="grid grid-cols-2 gap-3 font-mono-stats">
            <div className="bg-[#1e2023] p-4 rounded-xl border border-[#333539]">
              <span className="text-[#8e9379] text-[11px] block">Torneos Activos</span>
              <span className="font-headline font-black text-[28px] text-[#c3f400] mt-1 block">
                {activeTournaments}
              </span>
            </div>

            <div className="bg-[#1e2023] p-4 rounded-xl border border-[#333539]">
              <span className="text-[#8e9379] text-[11px] block">Partidos en Vivo</span>
              <span className="font-headline font-black text-[28px] text-[#FF3B30] mt-1 block flex items-center gap-2">
                {liveMatches}
                {liveMatches > 0 && <span className="w-2.5 h-2.5 rounded-full bg-[#FF3B30] pulse-animation" />}
              </span>
            </div>

            <div className="bg-[#1e2023] p-4 rounded-xl border border-[#333539]">
              <span className="text-[#8e9379] text-[11px] block">Jugadores Registrados</span>
              <span className="font-headline font-black text-[28px] text-white mt-1 block">
                {players.length}
              </span>
            </div>

            <div className="bg-[#1e2023] p-4 rounded-xl border border-[#333539]">
              <span className="text-[#8e9379] text-[11px] block">Pistas Disponibles</span>
              <span className="font-headline font-black text-[28px] text-white mt-1 block">
                {courts.filter((c) => c.status === 'AVAILABLE').length} / {courts.length}
              </span>
            </div>
          </div>

          {/* Quick Match Court Re-Assignment */}
          <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] flex flex-col gap-3">
            <h3 className="font-headline font-bold text-[15px] text-white border-b border-[#333539] pb-2">
              🎾 Programación y Asignación de Pistas
            </h3>

            <div className="flex flex-col gap-2">
              {matches.map((m) => (
                <div
                  key={m.id}
                  className="bg-[#282a2e] p-3 rounded-lg border border-[#333539] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-[12px] font-mono-stats"
                >
                  <div className="flex-1">
                    <span className="font-bold text-white block">
                      {m.pairAName} VS {m.pairBName}
                    </span>
                    <span className="text-[11px] text-[#c4c9ac] block mt-0.5">
                      Pista: <b className="text-[#c3f400]">{m.courtName || 'Sin asignar'}</b>
                    </span>
                    <span className="text-[11px] text-[#c4c9ac] block mt-0.5">
                      Fecha/Hora: <b className="text-white">{m.dateTime || 'Sin programar'}</b>
                    </span>
                  </div>

                  <div className="flex flex-col gap-1.5 w-full sm:w-auto">
                    <select
                      value={m.courtId || ''}
                      onChange={(e) => {
                        const selectedCourt = courts.find((c) => c.id === e.target.value);
                        if (selectedCourt) {
                          onUpdateMatchCourt(m.id, selectedCourt.id, selectedCourt.name);
                        }
                      }}
                      className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px]"
                    >
                      <option value="">Sin pista</option>
                      {courts.map((c) => (
                        <option key={c.id} value={c.id}>
                          {c.name} ({c.status})
                        </option>
                      ))}
                    </select>

                    {editingMatchId === m.id ? (
                      <div className="flex gap-1">
                        <input
                          type="datetime-local"
                          value={editMatchDateTime}
                          onChange={(e) => setEditMatchDateTime(e.target.value)}
                          className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px] flex-1"
                        />
                        <button
                          onClick={() => {
                            onUpdateMatchDateTime(m.id, editMatchDateTime);
                            setEditingMatchId(null);
                            setEditMatchDateTime('');
                          }}
                          className="bg-[#c3f400] text-[#161e00] px-2 py-1 rounded text-[11px] font-bold"
                        >
                          Guardar
                        </button>
                        <button
                          onClick={() => {
                            setEditingMatchId(null);
                            setEditMatchDateTime('');
                          }}
                          className="bg-[#333539] text-white px-2 py-1 rounded text-[11px]"
                        >
                          Cancelar
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => {
                          const d = new Date(m.dateTime || '');
                          const localIso = isNaN(d.getTime()) ? '' : new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
                          setEditMatchDateTime(localIso);
                          setEditingMatchId(m.id);
                        }}
                        className="bg-[#333539] hover:bg-[#37393d] text-white px-2 py-1.5 rounded text-[11px]"
                      >
                        📅 Programar fecha/hora
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Users Management */}
      {adminTab === 'USUARIOS' && (
        <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] flex flex-col gap-3">
          <div className="flex items-center justify-between border-b border-[#333539] pb-2">
            <h3 className="font-headline font-bold text-[16px] text-white">
              Gestión de Usuarios y Roles
            </h3>
            <button
              onClick={() => setShowCreateUserModal(true)}
              className="bg-[#c3f400] text-[#161e00] font-headline font-bold text-[12px] py-2 px-3.5 rounded-lg flex items-center gap-1 hover:bg-[#abd600] transition-all active:scale-95 shadow-md"
            >
              <span className="material-symbols-outlined text-[18px]">person_add</span>
              <span>Nuevo Usuario</span>
            </button>
          </div>

          <div className="flex flex-col gap-2">
            {players.map((p) => (
              <div
                key={p.id}
                className="bg-[#282a2e] p-3 rounded-lg border border-[#333539] flex items-center justify-between text-[12px] font-mono-stats"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full overflow-hidden border border-[#333539]">
                    <img src={p.avatar} alt="" className="w-full h-full object-cover" />
                  </div>
                  <div>
                    <span className="font-bold text-white block">
                      {p.name} {p.surname}
                    </span>
                    <span className="text-[10px] text-[#c4c9ac]">
                      @{p.username} • {p.email}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="bg-[#c3f400]/10 text-[#c3f400] font-bold px-2.5 py-1 rounded">
                    {p.role}
                  </span>
                  {p.id !== 'usr_carlos_admin' && (
                    <button
                      onClick={() => setDeleteConfirmId(p.id)}
                      className="text-[#FF3B30] hover:bg-[#FF3B30]/10 p-1.5 rounded-lg transition-colors active:scale-95"
                      title="Eliminar usuario"
                    >
                      <span className="material-symbols-outlined text-[18px]">delete</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Courts Management */}
      {adminTab === 'PISTAS' && (
        <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] flex flex-col gap-3">
          <h3 className="font-headline font-bold text-[16px] text-white border-b border-[#333539] pb-2">
            Estado de Pistas del Club
          </h3>

          <div className="grid grid-cols-2 gap-3 text-[12px] font-mono-stats">
            {courts.map((c) => (
              <div
                key={c.id}
                className="bg-[#282a2e] p-3.5 rounded-lg border border-[#333539] flex flex-col gap-1"
              >
                <span className="font-bold text-white text-[13px]">{c.name}</span>
                <span className="text-[11px] text-[#c4c9ac]">{c.location}</span>
                <span
                  className={`mt-2 font-bold px-2 py-0.5 rounded text-[10px] inline-block w-max ${
                    c.status === 'AVAILABLE'
                      ? 'bg-[#c3f400]/10 text-[#c3f400]'
                      : 'bg-[#FF3B30]/10 text-[#FF3B30]'
                  }`}
                >
                  {c.status === 'AVAILABLE' ? 'DISPONIBLE' : 'OCUPADA EN PARTIDO'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tournaments Management */}
      {adminTab === 'TORNEOS' && (
        <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] flex flex-col gap-3">
          <h3 className="font-headline font-bold text-[16px] text-white border-b border-[#333539] pb-2">
            🏆 Programación de Torneos e Inscripciones
          </h3>

          <div className="flex flex-col gap-3">
            {tournaments.map((t) => (
              <div
                key={t.id}
                className="bg-[#282a2e] p-3.5 rounded-lg border border-[#333539] flex flex-col gap-2 text-[12px] font-mono-stats"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white text-[13px]">{t.name}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    t.status === 'ACTIVE' ? 'bg-[#c3f400]/10 text-[#c3f400]' :
                    t.status === 'REGISTRATION' ? 'bg-blue-500/10 text-blue-400' :
                    t.status === 'UPCOMING' ? 'bg-yellow-500/10 text-yellow-400' :
                    'bg-[#FF3B30]/10 text-[#FF3B30]'
                  }`}>
                    {t.status}
                  </span>
                </div>

                <div className="text-[11px] text-[#c4c9ac]">
                  <div>📍 {t.location}</div>
                  <div>📅 {t.startDate} → {t.endDate}</div>
                  <div>👥 {t.registeredUserIds.length} jugadores / {t.registeredPairIds.length} parejas</div>
                </div>

                {editingTournamentId === t.id ? (
                  <div className="flex flex-col gap-1.5 mt-1">
                    <div className="flex gap-2">
                      <div className="flex-1">
                        <label className="text-[10px] text-[#8e9379] block mb-0.5">Inicio</label>
                        <input
                          type="date"
                          value={editTournamentStart}
                          onChange={(e) => setEditTournamentStart(e.target.value)}
                          className="w-full bg-[#111317] border border-[#333539] text-white p-1.5 rounded text-[11px]"
                        />
                      </div>
                      <div className="flex-1">
                        <label className="text-[10px] text-[#8e9379] block mb-0.5">Fin</label>
                        <input
                          type="date"
                          value={editTournamentEnd}
                          onChange={(e) => setEditTournamentEnd(e.target.value)}
                          className="w-full bg-[#111317] border border-[#333539] text-white p-1.5 rounded text-[11px]"
                        />
                      </div>
                    </div>
                    <div className="flex gap-1">
                      <button
                        onClick={() => {
                          onUpdateTournament(t.id, { startDate: editTournamentStart, endDate: editTournamentEnd });
                          setEditingTournamentId(null);
                        }}
                        className="bg-[#c3f400] text-[#161e00] px-2 py-1 rounded text-[11px] font-bold flex-1"
                      >
                        Guardar
                      </button>
                      <button
                        onClick={() => {
                          setEditingTournamentId(null);
                          setEditTournamentStart('');
                          setEditTournamentEnd('');
                        }}
                        className="bg-[#333539] text-white px-2 py-1 rounded text-[11px] flex-1"
                      >
                        Cancelar
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    <button
                      onClick={() => {
                        setEditingTournamentId(t.id);
                        setEditTournamentStart(t.startDate);
                        setEditTournamentEnd(t.endDate);
                      }}
                      className="bg-[#333539] hover:bg-[#37393d] text-white px-2 py-1.5 rounded text-[11px]"
                    >
                      📅 Programar fechas
                    </button>

                    {selectedTournamentForUsers === t.id ? (
                      <div className="flex flex-col gap-1.5 w-full mt-1">
                        <select
                          onChange={(e) => {
                            if (e.target.value) {
                              onRegisterUserForTournament(t.id, e.target.value);
                              e.target.value = '';
                            }
                          }}
                          className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px]"
                          defaultValue=""
                        >
                          <option value="" disabled>Inscribir jugador...</option>
                          {players
                            .filter((p) => !t.registeredUserIds.includes(p.id))
                            .map((p) => (
                              <option key={p.id} value={p.id}>
                                {p.name} {p.surname} (@{p.username})
                              </option>
                            ))}
                        </select>
                        <button
                          onClick={() => setSelectedTournamentForUsers(null)}
                          className="bg-[#333539] text-white px-2 py-1 rounded text-[11px]"
                        >
                          Cerrar inscripción
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => setSelectedTournamentForUsers(t.id)}
                        className="bg-[#c3f400] hover:bg-[#abd600] text-[#161e00] px-2 py-1.5 rounded text-[11px] font-bold"
                      >
                        👤 Inscribir jugadores
                      </button>
                    )}
                  </div>
                )}

                {t.registeredUserIds.length > 0 && (
                  <div className="mt-1.5 flex flex-wrap gap-1">
                    {t.registeredUserIds.map((uid) => {
                      const player = players.find((p) => p.id === uid);
                      if (!player) return null;
                      return (
                        <span key={uid} className="bg-[#333539] text-white px-2 py-0.5 rounded text-[10px]">
                          {player.name} {player.surname}
                        </span>
                      );
                    })}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Audit Log Table */}
      {adminTab === 'AUDITORIA' && (
        <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] flex flex-col gap-3">
          <h3 className="font-headline font-bold text-[16px] text-white border-b border-[#333539] pb-2">
            Registro de Auditoría (AuditLog)
          </h3>

          <div className="flex flex-col gap-2 max-h-96 overflow-y-auto">
            {auditLogs.map((log) => (
              <div
                key={log.id}
                className="bg-[#282a2e] p-3 rounded-lg border border-[#333539] flex flex-col gap-1 text-[11px] font-mono-stats"
              >
                <div className="flex items-center justify-between text-[#c3f400] font-bold">
                  <span>{log.action}</span>
                  <span className="text-[#8e9379]">{log.timestamp}</span>
                </div>
                <span className="text-white font-semibold">{log.target}</span>
                <p className="text-[#c4c9ac]">{log.details}</p>
                <span className="text-[10px] text-[#8e9379] mt-1">Por: {log.adminName}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Create User Modal */}
      {showCreateUserModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <form
            onSubmit={handleCreateUserSubmit}
            className="bg-[#1e2023] rounded-2xl p-5 border border-[#333539] max-w-md w-full flex flex-col gap-4 shadow-2xl"
          >
            <div className="flex items-center justify-between border-b border-[#333539] pb-2">
              <h3 className="font-headline font-bold text-[18px] text-white">Registrar Nuevo Usuario</h3>
              <button
                type="button"
                onClick={() => setShowCreateUserModal(false)}
                className="text-[#c4c9ac] hover:text-white"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <div className="flex flex-col gap-3 font-mono-stats text-[12px]">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Nombre</label>
                  <input
                    type="text"
                    required
                    placeholder="Nombre"
                    value={newUserName}
                    onChange={(e) => setNewUserName(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  />
                </div>
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Apellido</label>
                  <input
                    type="text"
                    required
                    placeholder="Apellido"
                    value={newUserSurname}
                    onChange={(e) => setNewUserSurname(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  />
                </div>
              </div>

              <div>
                <label className="text-[#c4c9ac] block mb-1">Usuario</label>
                <input
                  type="text"
                  required
                  placeholder="@username"
                  value={newUserUsername}
                  onChange={(e) => setNewUserUsername(e.target.value)}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                />
              </div>

              <div>
                <label className="text-[#c4c9ac] block mb-1">Email</label>
                <input
                  type="email"
                  required
                  placeholder="correo@ejemplo.com"
                  value={newUserEmail}
                  onChange={(e) => setNewUserEmail(e.target.value)}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                />
              </div>

              <div>
                <label className="text-[#c4c9ac] block mb-1">Teléfono (opcional)</label>
                <input
                  type="tel"
                  placeholder="+34 600 000 000"
                  value={newUserPhone}
                  onChange={(e) => setNewUserPhone(e.target.value)}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Rol</label>
                  <select
                    value={newUserRole}
                    onChange={(e: any) => setNewUserRole(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  >
                    <option value="PLAYER">Jugador</option>
                    <option value="ADMIN">Administrador</option>
                  </select>
                </div>
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Nivel</label>
                  <select
                    value={newUserLevel}
                    onChange={(e: any) => setNewUserLevel(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  >
                    <option value="Principiante">Principiante</option>
                    <option value="Intermedio">Intermedio</option>
                    <option value="Avanzado">Avanzado</option>
                    <option value="Profesional">Profesional</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Posición</label>
                  <select
                    value={newUserPosition}
                    onChange={(e: any) => setNewUserPosition(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  >
                    <option value="Drive (Derecha)">Drive (Derecha)</option>
                    <option value="Revés (Izquierda)">Revés (Izquierda)</option>
                    <option value="Ambas">Ambas</option>
                  </select>
                </div>
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Mano Dominante</label>
                  <select
                    value={newUserHand}
                    onChange={(e: any) => setNewUserHand(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  >
                    <option value="Derecha">Derecha</option>
                    <option value="Zurda">Zurda</option>
                  </select>
                </div>
              </div>
            </div>

            <button
              type="submit"
              className="bg-[#c3f400] text-[#161e00] font-headline font-bold text-[14px] py-3 rounded-xl hover:bg-[#abd600] transition-all shadow-md mt-2"
            >
              Registrar Usuario
            </button>
          </form>
        </div>
      )}

      {/* Delete User Confirmation */}
      {deleteConfirmId && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#1e2023] rounded-2xl p-5 border border-[#333539] max-w-sm w-full flex flex-col gap-4 shadow-2xl">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-[#FF3B30] text-[32px]">warning</span>
              <h3 className="font-headline font-bold text-[18px] text-white">Eliminar Usuario</h3>
            </div>
            <p className="text-[12px] text-[#c4c9ac] font-mono-stats">
              Esta acción eliminará permanentemente al usuario del sistema. Esta operación no se puede deshacer.
            </p>
            <div className="flex gap-2 mt-1">
              <button
                onClick={() => setDeleteConfirmId(null)}
                className="flex-1 bg-[#282a2e] hover:bg-[#333539] text-white font-mono-stats text-[12px] font-bold py-2.5 rounded-lg border border-[#333539]"
              >
                Cancelar
              </button>
              <button
                onClick={() => {
                  onDeleteUser(deleteConfirmId);
                  setDeleteConfirmId(null);
                }}
                className="flex-1 bg-[#FF3B30] hover:bg-[#e02d24] text-white font-mono-stats text-[12px] font-bold py-2.5 rounded-lg"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
