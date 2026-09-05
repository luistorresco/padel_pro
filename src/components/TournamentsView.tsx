import React, { useState } from 'react';
import { Tournament, Pair, UserRole, Match, Court } from '../types';

interface TournamentsViewProps {
  tournaments: Tournament[];
  pairs: Pair[];
  courts: Court[];
  matches?: Match[];
  role: UserRole;
  onCreateTournament: (newTour: Tournament) => void;
  onRegisterPair: (tournamentId: string, pairId: string, courtId: string, dateTime: string) => void;
  onDeleteTournament?: (tourId: string) => void;
  onOpenMatch?: (matchId: string) => void;
  onGenerateBracket?: (tournamentId: string) => void;
  onUpdateMatchDateTime?: (matchId: string, dateTime: string) => void;
  onUpdateMatchCourt?: (matchId: string, courtId: string, courtName: string) => void;
}

export const TournamentsView: React.FC<TournamentsViewProps> = ({
  tournaments,
  pairs,
  courts,
  matches = [],
  role,
  onCreateTournament,
  onRegisterPair,
  onDeleteTournament,
  onOpenMatch,
  onGenerateBracket,
  onUpdateMatchDateTime,
  onUpdateMatchCourt,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('TODAS');
  const [selectedStatus, setSelectedStatus] = useState<string>('TODOS');
  const [selectedTournament, setSelectedTournament] = useState<Tournament | null>(null);
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);
  const [registeringTournamentId, setRegisteringTournamentId] = useState<string | null>(null);
  const [registerPairId, setRegisterPairId] = useState<string>('');
  const [registerCourtId, setRegisterCourtId] = useState<string>('');
  const [registerDateTime, setRegisterDateTime] = useState<string>('');
  const [editingMatchDateTimeId, setEditingMatchDateTimeId] = useState<string | null>(null);
  const [editMatchDateTimeValue, setEditMatchDateTimeValue] = useState<string>('');
  const [editingMatchCourtId, setEditingMatchCourtId] = useState<string | null>(null);
  const [editMatchCourtValue, setEditMatchCourtValue] = useState<string>('');

  // New Tournament Form
  const [newTourName, setNewTourName] = useState<string>('');
  const [newTourCat, setNewTourCat] = useState<'Masculino' | 'Femenino' | 'Mixto'>('Masculino');
  const [newTourLvl, setNewTourLvl] = useState<'Principiante' | 'Intermedio' | 'Avanzado' | 'Profesional'>('Intermedio');
  const [newTourLocation, setNewTourLocation] = useState<string>('Club Central Pádel');
  const [newTourFormat, setNewTourFormat] = useState<any>('Grupos + eliminación directa');
  const [newTourStartDate, setNewTourStartDate] = useState<string>('');
  const [newTourEndDate, setNewTourEndDate] = useState<string>('');
  const [newTourSetsToWin, setNewTourSetsToWin] = useState<number>(2);
  const [newTourGoldenPoint, setNewTourGoldenPoint] = useState<boolean>(true);
  const [newTourTieBreakAt, setNewTourTieBreakAt] = useState<number>(6);
  const [newTourFinalSetTieBreak, setNewTourFinalSetTieBreak] = useState<boolean>(true);
  const [newTourPointsChampion, setNewTourPointsChampion] = useState<number>(1000);
  const [newTourPointsRunnerUp, setNewTourPointsRunnerUp] = useState<number>(600);
  const [newTourPointsSemiFinals, setNewTourPointsSemiFinals] = useState<number>(360);
  const [newTourPointsQuarterFinals, setNewTourPointsQuarterFinals] = useState<number>(180);
  const [newTourPointsGroupStage, setNewTourPointsGroupStage] = useState<number>(90);

  const filteredTournaments = tournaments.filter((t) => {
    if (selectedCategory !== 'TODAS' && t.category !== selectedCategory) return false;
    if (selectedStatus !== 'TODOS' && t.status !== selectedStatus) return false;
    return true;
  });

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTourName.trim()) return;

    const today = new Date().toISOString().split('T')[0];
    const newTour: Tournament = {
      id: 'tour_' + Date.now(),
      name: newTourName,
      logo: '🏆',
      description: 'Torneo organizado mediante el panel administrativo de Padel Pro.',
      category: newTourCat,
      level: newTourLvl,
      location: newTourLocation,
      startDate: newTourStartDate || today,
      endDate: newTourEndDate || new Date(Date.now() + 86400000 * 5).toISOString().split('T')[0],
      status: 'REGISTRATION',
      format: newTourFormat,
      maxPairs: 16,
      registeredPairIds: [],
      registeredUserIds: [],
      rules: {
        setsToWin: newTourSetsToWin,
        goldenPoint: newTourGoldenPoint,
        tieBreakAt: newTourTieBreakAt,
        finalSetTieBreak: newTourFinalSetTieBreak,
        pointsDistribution: {
          champion: newTourPointsChampion,
          runnerUp: newTourPointsRunnerUp,
          semiFinals: newTourPointsSemiFinals,
          quarterFinals: newTourPointsQuarterFinals,
          groupStage: newTourPointsGroupStage,
        },
      },
      courtIds: ['crt_central', 'crt_2'],
    };

    onCreateTournament(newTour);
    setShowCreateModal(false);
    setNewTourName('');
    setNewTourStartDate('');
    setNewTourEndDate('');
    setNewTourPointsChampion(1000);
    setNewTourPointsRunnerUp(600);
    setNewTourPointsSemiFinals(360);
    setNewTourPointsQuarterFinals(180);
    setNewTourPointsGroupStage(90);
  };

  return (
    <div className="flex flex-col gap-5 pb-24 px-4 pt-3 w-full">
      {/* View Header */}
      <div className="flex items-center justify-between border-b border-[#333539] pb-3">
        <div>
          <h2 className="font-headline font-black text-[22px] text-white tracking-tight flex items-center gap-2">
            <span className="material-symbols-outlined text-[#c3f400] text-[28px]">emoji_events</span>
            Torneos de Pádel
          </h2>
          <p className="text-[12px] text-[#c4c9ac] font-mono-stats">
            Gestiona inscripciones, fases de grupos y eliminatorias
          </p>
        </div>

        {role === 'ADMIN' && (
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-[#c3f400] text-[#161e00] font-headline font-bold text-[12px] py-2 px-3.5 rounded-lg flex items-center gap-1 hover:bg-[#abd600] transition-all active:scale-95 shadow-md"
          >
            <span className="material-symbols-outlined text-[18px]">add_circle</span>
            <span>Crear Torneo</span>
          </button>
        )}
      </div>

      {/* Category Filters */}
      <div className="flex gap-2 overflow-x-auto pb-1 no-scrollbar text-[12px] font-mono-stats">
        {['TODAS', 'Masculino', 'Femenino', 'Mixto'].map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 rounded-full font-bold transition-all whitespace-nowrap ${
              selectedCategory === cat
                ? 'bg-[#c3f400] text-[#161e00] shadow-[0_0_10px_rgba(195,244,0,0.3)]'
                : 'bg-[#282a2e] text-[#c4c9ac] hover:text-white border border-[#333539]'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Tournaments Grid */}
      <div className="flex flex-col gap-4">
        {filteredTournaments.map((tour) => {
          const registeredCount = (tour.registeredPairIds || []).length;
          return (
            <div
              key={tour.id}
              className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] hover:border-[#c3f400]/50 transition-all flex flex-col gap-3 shadow-lg"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-[#282a2e] flex items-center justify-center text-[24px] border border-[#333539]">
                    {tour.logo}
                  </div>
                  <div>
                    <h3 className="font-headline font-bold text-[17px] text-white leading-tight">
                      {tour.name}
                    </h3>
                    <div className="flex items-center gap-2 mt-1 text-[11px] font-mono-stats text-[#c4c9ac]">
                      <span className="bg-[#282a2e] px-2 py-0.5 rounded text-[#c3f400] font-bold">
                        {tour.category}
                      </span>
                      <span>•</span>
                      <span>{tour.level}</span>
                    </div>
                  </div>
                </div>

                <span
                  className={`text-[10px] font-mono-stats font-bold px-2.5 py-1 rounded-full uppercase border ${
                    tour.status === 'ACTIVE' || tour.status === 'IN_PROGRESS'
                      ? 'bg-[#c3f400]/10 text-[#c3f400] border-[#c3f400]/30'
                      : tour.status === 'REGISTRATION' || tour.status === 'OPEN'
                      ? 'bg-[#deed2e]/10 text-[#deed2e] border-[#deed2e]/30'
                      : 'bg-[#282a2e] text-[#c4c9ac] border-[#333539]'
                  }`}
                >
                  {tour.status === 'ACTIVE' || tour.status === 'IN_PROGRESS'
                    ? 'EN CURSO'
                    : tour.status === 'REGISTRATION' || tour.status === 'OPEN'
                    ? 'INSCRIPCION'
                    : 'PROXIMO'}
                </span>
              </div>

              <p className="text-[12px] text-[#c4c9ac] line-clamp-2 leading-relaxed">
                {tour.description}
              </p>

              {/* Tournament Details Info Bar */}
              <div className="grid grid-cols-3 gap-2 bg-[#0c0e12] p-2.5 rounded-lg text-[11px] font-mono-stats border border-[#333539]">
                <div>
                  <span className="text-[#8e9379] block">Lugar:</span>
                  <span className="font-bold text-white truncate block">{tour.location}</span>
                </div>
                <div>
                  <span className="text-[#8e9379] block">Formato:</span>
                  <span className="font-bold text-white truncate block">{tour.format}</span>
                </div>
                <div>
                  <span className="text-[#8e9379] block">Parejas:</span>
                  <span className="font-bold text-[#c3f400]">
                    {registeredCount} / {tour.maxPairs}
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2 mt-1">
                <button
                  onClick={() => setSelectedTournament(tour)}
                  className="flex-1 bg-[#282a2e] hover:bg-[#333539] text-white font-mono-stats text-[12px] font-bold py-2 px-3 rounded-lg border border-[#333539] flex items-center justify-center gap-1.5"
                >
                  <span className="material-symbols-outlined text-[16px]">visibility</span>
                  <span>Ver Clasificación & Cuadro</span>
                </button>

                {(tour.status === 'REGISTRATION' || tour.status === 'OPEN') && pairs.length > 0 && (
                  <button
                    onClick={() => setRegisteringTournamentId(tour.id)}
                    className="bg-[#c3f400] hover:bg-[#abd600] text-[#161e00] font-mono-stats text-[12px] font-bold py-2 px-3 rounded-lg flex items-center justify-center gap-1"
                  >
                    <span>Inscribir Mi Pareja</span>
                  </button>
                )}

                {registeringTournamentId === tour.id && (
                  <div className="flex flex-col gap-1.5 mt-2">
                    <select
                      value={registerPairId}
                      onChange={(e) => setRegisterPairId(e.target.value)}
                      className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px]"
                    >
                      <option value="">Seleccionar pareja...</option>
                      {pairs
                        .filter((p) => !tour.registeredPairIds.includes(p.id))
                        .map((p) => (
                          <option key={p.id} value={p.id}>
                            {p.name}
                          </option>
                        ))}
                    </select>
                    <select
                      value={registerCourtId}
                      onChange={(e) => setRegisterCourtId(e.target.value)}
                      className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px]"
                    >
                      <option value="">Sin pista</option>
                      {courts.map((c) => (
                        <option key={c.id} value={c.id}>
                          {c.name} ({c.status})
                        </option>
                      ))}
                    </select>
                    <input
                      type="datetime-local"
                      value={registerDateTime}
                      onChange={(e) => setRegisterDateTime(e.target.value)}
                      className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px]"
                    />
                    <button
                      onClick={() => {
                        if (!registerPairId) return;
                        onRegisterPair(tour.id, registerPairId, registerCourtId, registerDateTime);
                        setRegisteringTournamentId(null);
                        setRegisterPairId('');
                        setRegisterCourtId('');
                        setRegisterDateTime('');
                      }}
                      className="bg-[#c3f400] text-[#161e00] px-2 py-1 rounded text-[11px] font-bold"
                    >
                      Confirmar inscripción
                    </button>
                    <button
                      onClick={() => {
                        setRegisteringTournamentId(null);
                        setRegisterPairId('');
                        setRegisterCourtId('');
                        setRegisterDateTime('');
                      }}
                      className="bg-[#333539] text-white px-2 py-1 rounded text-[11px]"
                    >
                      Cancelar
                    </button>
                  </div>
                )}

                {role === 'ADMIN' && onDeleteTournament && (
                  <button
                    onClick={() => setDeleteConfirmId(tour.id)}
                    className="bg-[#282a2e] hover:bg-[#FF3B30]/20 text-[#FF3B30] font-mono-stats text-[12px] font-bold py-2 px-3 rounded-lg border border-[#FF3B30]/30 flex items-center justify-center gap-1 active:scale-95"
                    title="Eliminar torneo"
                  >
                    <span className="material-symbols-outlined text-[16px]">delete</span>
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Tournament Details & Bracket Modal */}
      {selectedTournament && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#1e2023] rounded-2xl p-5 border border-[#333539] max-w-3xl w-full max-h-[85vh] overflow-y-auto flex flex-col gap-4 shadow-2xl">
            <div className="flex items-start justify-between border-b border-[#333539] pb-3">
              <div>
                <h3 className="font-headline font-bold text-[18px] text-white">
                  {selectedTournament.name}
                </h3>
                <span className="text-[11px] font-mono-stats text-[#c3f400]">
                  {selectedTournament.format} • {selectedTournament.category} • {selectedTournament.level}
                </span>
                <div className="flex items-center gap-3 mt-1 text-[11px] font-mono-stats text-[#c4c9ac]">
                  <span>📍 {selectedTournament.location}</span>
                  <span>📅 {selectedTournament.startDate} → {selectedTournament.endDate}</span>
                </div>
              </div>
              <button
                onClick={() => setSelectedTournament(null)}
                className="text-[#c4c9ac] hover:text-white p-1"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            {/* Quick Actions */}
            <div className="flex flex-wrap gap-2">
              {onGenerateBracket && (
                <button
                  onClick={() => onGenerateBracket(selectedTournament.id)}
                  className="bg-[#c3f400] text-[#161e00] text-[11px] font-bold px-3 py-2 rounded-lg"
                >
                  <span className="material-symbols-outlined text-[14px] mr-1">account_tree</span>
                  Generar Grupos
                </button>
              )}
              {(selectedTournament.status === 'REGISTRATION' || selectedTournament.status === 'OPEN') && pairs.length > 0 && (
                <button
                  onClick={() => setRegisteringTournamentId(selectedTournament.id)}
                  className="bg-[#282a2e] hover:bg-[#333539] text-white text-[11px] font-bold px-3 py-2 rounded-lg border border-[#333539]"
                >
                  <span className="material-symbols-outlined text-[14px] mr-1">person_add</span>
                  Inscribir Pareja
                </button>
              )}
              {role === 'ADMIN' && onDeleteTournament && (
                <button
                  onClick={() => {
                    setSelectedTournament(null);
                    onDeleteTournament(selectedTournament.id);
                  }}
                  className="bg-[#282a2e] hover:bg-[#FF3B30]/20 text-[#FF3B30] text-[11px] font-bold px-3 py-2 rounded-lg border border-[#FF3B30]/30"
                >
                  <span className="material-symbols-outlined text-[14px] mr-1">delete</span>
                  Eliminar Torneo
                </button>
              )}
            </div>

            {/* Inscribir Pareja inline */}
            {registeringTournamentId === selectedTournament.id && (
              <div className="bg-[#0c0e12] p-3 rounded-xl border border-[#c3f400]/40 flex flex-col gap-2">
                <span className="text-[#c3f400] font-bold text-[11px] uppercase">Inscribir pareja en {selectedTournament.name}</span>
                <select
                  value={registerPairId}
                  onChange={(e) => setRegisterPairId(e.target.value)}
                  className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px]"
                >
                  <option value="">Seleccionar pareja...</option>
                  {pairs
                    .filter((p) => !selectedTournament.registeredPairIds.includes(p.id))
                    .map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name}
                      </option>
                    ))}
                </select>
                <select
                  value={registerCourtId}
                  onChange={(e) => setRegisterCourtId(e.target.value)}
                  className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px]"
                >
                  <option value="">Sin pista</option>
                  {courts.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.status})
                    </option>
                  ))}
                </select>
                <input
                  type="datetime-local"
                  value={registerDateTime}
                  onChange={(e) => setRegisterDateTime(e.target.value)}
                  className="bg-[#111317] border border-[#333539] text-white p-2 rounded text-[11px]"
                />
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      if (!registerPairId) return;
                      onRegisterPair(selectedTournament.id, registerPairId, registerCourtId, registerDateTime);
                      setRegisteringTournamentId(null);
                      setRegisterPairId('');
                      setRegisterCourtId('');
                      setRegisterDateTime('');
                    }}
                    className="bg-[#c3f400] text-[#161e00] px-2 py-1.5 rounded text-[11px] font-bold"
                  >
                    Confirmar inscripción
                  </button>
                  <button
                    onClick={() => {
                      setRegisteringTournamentId(null);
                      setRegisterPairId('');
                      setRegisterCourtId('');
                      setRegisterDateTime('');
                    }}
                    className="bg-[#333539] text-white px-2 py-1.5 rounded text-[11px]"
                  >
                    Cancelar
                  </button>
                </div>
              </div>
            )}

            {/* Programación de Partidos */}
            <div>
              <h4 className="font-headline font-bold text-[14px] text-white mb-2 flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[#c3f400] text-[18px]">schedule</span>
                Programación de Partidos
              </h4>
              <div className="flex flex-col gap-2">
                {matches.filter((m) => m.tournamentId === selectedTournament.id).length === 0 ? (
                  <div className="bg-[#0c0e12] p-4 rounded-xl border border-[#333539] text-[12px] font-mono-stats text-[#8e9379] text-center">
                    No hay partidos programados. Inscribe parejas y genera los grupos.
                  </div>
                ) : (
                  matches
                    .filter((m) => m.tournamentId === selectedTournament.id)
                    .sort((a, b) => (a.dateTime || '').localeCompare(b.dateTime || ''))
                    .map((m) => {
                      const isEditingDateTime = editingMatchDateTimeId === m.id;
                      const isEditingCourt = editingMatchCourtId === m.id;
                      return (
                        <div
                          key={m.id}
                          className="bg-[#0c0e12] p-3 rounded-xl border border-[#333539] flex flex-col gap-2 font-mono-stats text-[12px]"
                        >
                          <div className="flex items-center justify-between text-[11px]">
                            <span className="text-[#c3f400] font-bold uppercase">{m.roundName || 'Fase de Grupos'}</span>
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                                m.status === 'LIVE' || m.status === 'IN_PROGRESS'
                                  ? 'bg-[#FF3B30] text-white'
                                  : m.status === 'FINISHED'
                                  ? 'bg-[#c3f400]/20 text-[#c3f400]'
                                  : 'bg-[#282a2e] text-[#8e9379]'
                              }`}
                            >
                              {m.status === 'LIVE' || m.status === 'IN_PROGRESS' ? '🔴 En Vivo' : m.status === 'FINISHED' ? '✅ Finalizado' : '⏳ Próximo'}
                            </span>
                          </div>

                          <div className="flex flex-col gap-1 bg-[#1e2023] p-2 rounded-lg border border-[#333539]">
                            <div className="flex items-center justify-between">
                              <span className={`font-bold ${m.winnerTeam === 'A' ? 'text-[#c3f400]' : 'text-white'}`}>
                                {m.pairAName}
                              </span>
                              <span className="text-[11px] text-[#c4c9ac]">Pareja A</span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span className={`font-bold ${m.winnerTeam === 'B' ? 'text-[#c3f400]' : 'text-white'}`}>
                                {m.pairBName}
                              </span>
                              <span className="text-[11px] text-[#c4c9ac]">Pareja B</span>
                            </div>
                          </div>

                          <div className="flex flex-col gap-1.5 text-[11px]">
                            <div className="flex items-center justify-between text-[#c4c9ac]">
                              <span>Pista: <b className="text-white">{m.courtName || 'Sin asignar'}</b></span>
                              {!isEditingCourt ? (
                                <button
                                  onClick={() => {
                                    setEditingMatchCourtId(m.id);
                                    setEditMatchCourtValue(m.courtId || '');
                                  }}
                                  className="text-[#c3f400] hover:underline"
                                >
                                  Editar pista
                                </button>
                              ) : (
                                <div className="flex gap-1">
                                  <select
                                    value={editMatchCourtValue}
                                    onChange={(e) => setEditMatchCourtValue(e.target.value)}
                                    className="bg-[#111317] border border-[#333539] text-white p-1 rounded text-[10px]"
                                  >
                                    <option value="">Sin pista</option>
                                    {courts.map((c) => (
                                      <option key={c.id} value={c.id}>
                                        {c.name}
                                      </option>
                                    ))}
                                  </select>
                                  <button
                                    onClick={() => {
                                      if (onUpdateMatchCourt) {
                                        const court = courts.find((c) => c.id === editMatchCourtValue);
                                        if (court) {
                                          onUpdateMatchCourt(m.id, court.id, court.name);
                                        }
                                        setEditingMatchCourtId(null);
                                      }
                                    }}
                                    className="bg-[#c3f400] text-[#161e00] px-2 py-1 rounded text-[10px] font-bold"
                                  >
                                    Ok
                                  </button>
                                  <button
                                    onClick={() => setEditingMatchCourtId(null)}
                                    className="bg-[#333539] text-white px-2 py-1 rounded text-[10px]"
                                  >
                                    X
                                  </button>
                                </div>
                              )}
                            </div>
                            <div className="flex items-center justify-between text-[#c4c9ac]">
                              <span>Fecha/Hora: <b className="text-white">{m.dateTime || 'Sin programar'}</b></span>
                              {!isEditingDateTime ? (
                                <button
                                  onClick={() => {
                                    const d = new Date(m.dateTime || '');
                                    const localIso = isNaN(d.getTime()) ? '' : new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
                                    setEditMatchDateTimeValue(localIso);
                                    setEditingMatchDateTimeId(m.id);
                                  }}
                                  className="text-[#c3f400] hover:underline"
                                >
                                  Editar fecha/hora
                                </button>
                              ) : (
                                <div className="flex gap-1">
                                  <input
                                    type="datetime-local"
                                    value={editMatchDateTimeValue}
                                    onChange={(e) => setEditMatchDateTimeValue(e.target.value)}
                                    className="bg-[#111317] border border-[#333539] text-white p-1 rounded text-[10px]"
                                  />
                                  <button
                                    onClick={() => {
                                      if (onUpdateMatchDateTime) {
                                        onUpdateMatchDateTime(m.id, editMatchDateTimeValue);
                                        setEditingMatchDateTimeId(null);
                                      }
                                    }}
                                    className="bg-[#c3f400] text-[#161e00] px-2 py-1 rounded text-[10px] font-bold"
                                  >
                                    Ok
                                  </button>
                                  <button
                                    onClick={() => setEditingMatchDateTimeId(null)}
                                    className="bg-[#333539] text-white px-2 py-1 rounded text-[10px]"
                                  >
                                    X
                                  </button>
                                </div>
                              )}
                            </div>
                          </div>

                          {m.status !== 'FINISHED' && onOpenMatch && (
                            <button
                              onClick={() => {
                                setSelectedTournament(null);
                                onOpenMatch(m.id);
                              }}
                              className="bg-[#282a2e] hover:bg-[#333539] text-[#c3f400] text-[11px] font-bold py-1.5 rounded flex items-center justify-center gap-1 mt-0.5 border border-[#333539]"
                            >
                              <span className="material-symbols-outlined text-[14px]">sports_tennis</span>
                              Abrir Mesa de Control
                            </button>
                          )}
                        </div>
                      );
                    })
                )}
              </div>
            </div>

            {/* Clasificación */}
            <div>
              <h4 className="font-headline font-bold text-[14px] text-white mb-2 flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[#c3f400] text-[18px]">
                  table_chart
                </span>
                Clasificación
              </h4>
              <div className="overflow-x-auto bg-[#0c0e12] rounded-xl border border-[#333539]">
                <table className="w-full text-left font-mono-stats text-[11px]">
                  <thead className="bg-[#282a2e] text-[#c4c9ac] uppercase text-[10px]">
                    <tr>
                      <th className="p-2.5">Pareja</th>
                      <th className="p-2.5">PJ</th>
                      <th className="p-2.5">PG</th>
                      <th className="p-2.5">PP</th>
                      <th className="p-2.5 text-[#c3f400]">PTS</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#333539]">
                    {(selectedTournament.registeredPairIds || []).map((pId, idx) => {
                      const p = pairs.find((pair) => pair.id === pId);
                      const pairMatches = matches.filter((m) => m.tournamentId === selectedTournament.id && (m.pairAId === pId || m.pairBId === pId) && m.status === 'FINISHED');
                      const wins = pairMatches.filter((m) => m.winnerPairId === pId).length;
                      const losses = pairMatches.length - wins;
                      const points = wins * 3;
                      return (
                        <tr key={pId} className="hover:bg-[#282a2e]/50">
                          <td className="p-2.5 font-bold text-white truncate max-w-[160px]">
                            {p ? p.name : `Pareja #${idx + 1}`}
                          </td>
                          <td className="p-2.5">{pairMatches.length}</td>
                          <td className="p-2.5 font-bold text-[#c3f400]">{wins}</td>
                          <td className="p-2.5 text-[#ffdad6]">{losses}</td>
                          <td className="p-2.5 font-black text-[#c3f400] text-[12px]">{points}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Points Rules Info */}
            <div className="bg-[#282a2e] p-3 rounded-xl text-[11px] font-mono-stats border border-[#333539]">
              <span className="text-[#c3f400] font-bold block mb-1">
                REGLAS OFICIALES Y PUNTOS DE RANKING:
              </span>
              <ul className="list-disc list-inside text-[#c4c9ac] space-y-0.5">
                <li>Sets a ganar: {selectedTournament.rules.setsToWin}</li>
                <li>Punto de Oro: {selectedTournament.rules.goldenPoint ? 'ACTIVADO' : 'DESACTIVADO'}</li>
                <li>Tie-break en: {selectedTournament.rules.tieBreakAt}</li>
                <li>Campeón: {selectedTournament.rules.pointsDistribution?.champion ?? 0} pts</li>
                <li>Finalista: {selectedTournament.rules.pointsDistribution?.runnerUp ?? 0} pts</li>
                <li>Semifinalista: {selectedTournament.rules.pointsDistribution?.semiFinals ?? 0} pts</li>
                <li>Cuartos: {selectedTournament.rules.pointsDistribution?.quarterFinals ?? 0} pts</li>
                <li>Fase de grupos: {selectedTournament.rules.pointsDistribution?.groupStage ?? 0} pts</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Create Tournament Admin Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <form
            onSubmit={handleCreateSubmit}
            className="bg-[#1e2023] rounded-2xl p-5 border border-[#333539] max-w-md w-full flex flex-col gap-4 shadow-2xl"
          >
            <div className="flex items-center justify-between border-b border-[#333539] pb-2">
              <h3 className="font-headline font-bold text-[18px] text-white">Crear Nuevo Torneo</h3>
              <button
                type="button"
                onClick={() => setShowCreateModal(false)}
                className="text-[#c4c9ac] hover:text-white"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <div className="flex flex-col gap-3 font-mono-stats text-[12px]">
              <div>
                <label className="text-[#c4c9ac] block mb-1">Nombre del Torneo</label>
                <input
                  type="text"
                  required
                  placeholder="Ej. Open Primavera 2026"
                  value={newTourName}
                  onChange={(e) => setNewTourName(e.target.value)}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Fecha inicio</label>
                  <input
                    type="date"
                    required
                    value={newTourStartDate}
                    onChange={(e) => setNewTourStartDate(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  />
                </div>
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Fecha fin</label>
                  <input
                    type="date"
                    required
                    value={newTourEndDate}
                    onChange={(e) => setNewTourEndDate(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[#c4c9ac] block mb-1">Categoría</label>
                  <select
                    value={newTourCat}
                    onChange={(e: any) => setNewTourCat(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  >
                    <option value="Masculino">Masculino</option>
                    <option value="Femenino">Femenino</option>
                    <option value="Mixto">Mixto</option>
                  </select>
                </div>

                <div>
                  <label className="text-[#c4c9ac] block mb-1">Nivel</label>
                  <select
                    value={newTourLvl}
                    onChange={(e: any) => setNewTourLvl(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                  >
                    <option value="Principiante">Principiante</option>
                    <option value="Intermedio">Intermedio</option>
                    <option value="Avanzado">Avanzado</option>
                    <option value="Profesional">Profesional</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-[#c4c9ac] block mb-1">Ubicación / Club</label>
                <input
                  type="text"
                  value={newTourLocation}
                  onChange={(e) => setNewTourLocation(e.target.value)}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                />
              </div>

              <div>
                <label className="text-[#c4c9ac] block mb-1">Formato</label>
                <select
                  value={newTourFormat}
                  onChange={(e: any) => setNewTourFormat(e.target.value)}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                >
                  <option value="Eliminación directa">Eliminación directa</option>
                  <option value="Fase de grupos">Fase de grupos</option>
                  <option value="Todos contra todos">Todos contra todos</option>
                  <option value="Grupos + eliminación directa">Grupos + eliminación directa</option>
                </select>
              </div>

              <div className="bg-[#0c0e12] p-3 rounded-xl border border-[#333539]">
                <span className="text-[#c3f400] font-bold block mb-2 text-[11px] uppercase">Reglas del torneo</span>
                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div>
                    <label className="text-[#c4c9ac] block mb-0.5">Sets a ganar</label>
                    <select
                      value={newTourSetsToWin}
                      onChange={(e) => setNewTourSetsToWin(Number(e.target.value))}
                      className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded"
                    >
                      <option value={2}>2</option>
                      <option value={3}>3</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-[#c4c9ac] block mb-0.5">Punto de oro</label>
                    <select
                      value={newTourGoldenPoint ? '1' : '0'}
                      onChange={(e) => setNewTourGoldenPoint(e.target.value === '1')}
                      className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded"
                    >
                      <option value="1">Activado</option>
                      <option value="0">Desactivado</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-[#c4c9ac] block mb-0.5">Tie-break en</label>
                    <input
                      type="number"
                      min={1}
                      max={13}
                      value={newTourTieBreakAt}
                      onChange={(e) => setNewTourTieBreakAt(Number(e.target.value))}
                      className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded"
                    />
                  </div>
                  <div>
                    <label className="text-[#c4c9ac] block mb-0.5">Tie-break set final</label>
                    <select
                      value={newTourFinalSetTieBreak ? '1' : '0'}
                      onChange={(e) => setNewTourFinalSetTieBreak(e.target.value === '1')}
                      className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded"
                    >
                      <option value="1">Activado</option>
                      <option value="0">Desactivado</option>
                    </select>
                  </div>
                </div>
                <div className="mt-2">
                  <span className="text-[#c4c9ac] block mb-1 text-[11px]">Distribución de puntos</span>
                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    <div>
                      <label className="text-[#8e9379] block mb-0.5">Campeón</label>
                      <input type="number" value={newTourPointsChampion} onChange={(e) => setNewTourPointsChampion(Number(e.target.value))} className="w-full bg-[#111317] border border-[#333539] text-white p-1.5 rounded" />
                    </div>
                    <div>
                      <label className="text-[#8e9379] block mb-0.5">Finalista</label>
                      <input type="number" value={newTourPointsRunnerUp} onChange={(e) => setNewTourPointsRunnerUp(Number(e.target.value))} className="w-full bg-[#111317] border border-[#333539] text-white p-1.5 rounded" />
                    </div>
                    <div>
                      <label className="text-[#8e9379] block mb-0.5">Semifinal</label>
                      <input type="number" value={newTourPointsSemiFinals} onChange={(e) => setNewTourPointsSemiFinals(Number(e.target.value))} className="w-full bg-[#111317] border border-[#333539] text-white p-1.5 rounded" />
                    </div>
                    <div>
                      <label className="text-[#8e9379] block mb-0.5">Cuartos</label>
                      <input type="number" value={newTourPointsQuarterFinals} onChange={(e) => setNewTourPointsQuarterFinals(Number(e.target.value))} className="w-full bg-[#111317] border border-[#333539] text-white p-1.5 rounded" />
                    </div>
                    <div className="col-span-2">
                      <label className="text-[#8e9379] block mb-0.5">Fase de grupos</label>
                      <input type="number" value={newTourPointsGroupStage} onChange={(e) => setNewTourPointsGroupStage(Number(e.target.value))} className="w-full bg-[#111317] border border-[#333539] text-white p-1.5 rounded" />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <button
              type="submit"
              className="bg-[#c3f400] text-[#161e00] font-headline font-bold text-[14px] py-3 rounded-xl hover:bg-[#abd600] transition-all shadow-md mt-2"
            >
              Publicar Torneo
            </button>
          </form>
        </div>
      )}

      {/* Delete Tournament Confirmation */}
      {deleteConfirmId && onDeleteTournament && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#1e2023] rounded-2xl p-5 border border-[#333539] max-w-sm w-full flex flex-col gap-4 shadow-2xl">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-[#FF3B30] text-[32px]">warning</span>
              <h3 className="font-headline font-bold text-[18px] text-white">Eliminar Torneo</h3>
            </div>
            <p className="text-[12px] text-[#c4c9ac] font-mono-stats">
              Esta acción eliminará permanentemente el torneo y todos sus partidos asociados. Esta operación no se puede deshacer.
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
                  onDeleteTournament(deleteConfirmId);
                  setDeleteConfirmId(null);
                  setSelectedTournament(null);
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
