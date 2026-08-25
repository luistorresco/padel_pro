import React, { useState } from 'react';
import { Tournament, Pair, UserRole, Match } from '../types';

interface TournamentsViewProps {
  tournaments: Tournament[];
  pairs: Pair[];
  matches?: Match[];
  role: UserRole;
  onCreateTournament: (newTour: Tournament) => void;
  onRegisterPair: (tournamentId: string, pairId: string) => void;
  onDeleteTournament?: (tourId: string) => void;
  onOpenMatch?: (matchId: string) => void;
}

export const TournamentsView: React.FC<TournamentsViewProps> = ({
  tournaments,
  pairs,
  matches = [],
  role,
  onCreateTournament,
  onRegisterPair,
  onDeleteTournament,
  onOpenMatch,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('TODAS');
  const [selectedStatus, setSelectedStatus] = useState<string>('TODOS');
  const [selectedTournament, setSelectedTournament] = useState<Tournament | null>(null);
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);

  // New Tournament Form
  const [newTourName, setNewTourName] = useState<string>('');
  const [newTourCat, setNewTourCat] = useState<'Masculino' | 'Femenino' | 'Mixto'>('Masculino');
  const [newTourLvl, setNewTourLvl] = useState<'Principiante' | 'Intermedio' | 'Avanzado' | 'Profesional'>('Intermedio');
  const [newTourLocation, setNewTourLocation] = useState<string>('Club Central Pádel');
  const [newTourFormat, setNewTourFormat] = useState<any>('Grupos + eliminación directa');

  const filteredTournaments = tournaments.filter((t) => {
    if (selectedCategory !== 'TODAS' && t.category !== selectedCategory) return false;
    if (selectedStatus !== 'TODOS' && t.status !== selectedStatus) return false;
    return true;
  });

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTourName.trim()) return;

    const newTour: Tournament = {
      id: 'tour_' + Date.now(),
      name: newTourName,
      logo: '🏆',
      description: 'Torneo organizado mediante el panel administrativo de Padel Pro.',
      category: newTourCat,
      level: newTourLvl,
      location: newTourLocation,
      startDate: new Date().toISOString().split('T')[0],
      endDate: new Date(Date.now() + 86400000 * 5).toISOString().split('T')[0],
      status: 'REGISTRATION',
      format: newTourFormat,
      maxPairs: 16,
      registeredPairIds: [],
      registeredUserIds: [],
      rules: {
        setsToWin: 2,
        goldenPoint: true,
        tieBreakAt: 6,
        finalSetTieBreak: true,
        pointsDistribution: { champion: 1000, runnerUp: 600, semiFinals: 360, quarterFinals: 180, groupStage: 90 },
      },
      courtIds: ['crt_central', 'crt_2'],
    };

    onCreateTournament(newTour);
    setShowCreateModal(false);
    setNewTourName('');
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
                    tour.status === 'ACTIVE'
                      ? 'bg-[#c3f400]/10 text-[#c3f400] border-[#c3f400]/30'
                      : tour.status === 'REGISTRATION'
                      ? 'bg-[#deed2e]/10 text-[#deed2e] border-[#deed2e]/30'
                      : 'bg-[#282a2e] text-[#c4c9ac] border-[#333539]'
                  }`}
                >
                  {tour.status === 'ACTIVE'
                    ? 'EN CURSO'
                    : tour.status === 'REGISTRATION'
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

                {tour.status === 'REGISTRATION' && pairs.length > 0 && (
                  <button
                    onClick={() => {
                      if (pairs[0]) onRegisterPair(tour.id, pairs[0].id);
                    }}
                    className="bg-[#c3f400] hover:bg-[#abd600] text-[#161e00] font-mono-stats text-[12px] font-bold py-2 px-3 rounded-lg flex items-center justify-center gap-1"
                  >
                    <span>Inscribir Mi Pareja</span>
                  </button>
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
          <div className="bg-[#1e2023] rounded-2xl p-5 border border-[#333539] max-w-lg w-full max-h-[85vh] overflow-y-auto flex flex-col gap-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-[#333539] pb-3">
              <div>
                <h3 className="font-headline font-bold text-[18px] text-white">
                  {selectedTournament.name}
                </h3>
                <span className="text-[11px] font-mono-stats text-[#c3f400]">
                  {selectedTournament.format} • {selectedTournament.category}
                </span>
              </div>
              <button
                onClick={() => setSelectedTournament(null)}
                className="text-[#c4c9ac] hover:text-white p-1"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            {/* Bracket & Tournament Matches Section */}
            <div>
              <h4 className="font-headline font-bold text-[14px] text-white mb-2 flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[#c3f400] text-[18px]">
                  account_tree
                </span>
                Cuadro del Torneo y Reajuste de Llaves
              </h4>

              <div className="flex flex-col gap-2.5">
                {matches.filter((m) => m.tournamentId === selectedTournament.id).length === 0 ? (
                  <div className="bg-[#0c0e12] p-4 rounded-xl border border-[#333539] text-[12px] font-mono-stats text-[#8e9379] text-center">
                    No hay partidos programados todavía para este torneo.
                  </div>
                ) : (
                  matches
                    .filter((m) => m.tournamentId === selectedTournament.id)
                    .map((m) => {
                      const setsWonA = m.sets.filter((s) => s.winner === 'A').length;
                      const setsWonB = m.sets.filter((s) => s.winner === 'B').length;
                      const winnerName = m.winnerTeam === 'A' ? m.pairAName : m.winnerTeam === 'B' ? m.pairBName : (setsWonA > setsWonB ? m.pairAName : setsWonB > setsWonA ? m.pairBName : null);

                      return (
                        <div
                          key={m.id}
                          className="bg-[#0c0e12] p-3 rounded-xl border border-[#333539] flex flex-col gap-2 font-mono-stats text-[12px]"
                        >
                          <div className="flex items-center justify-between text-[11px]">
                            <span className="text-[#c3f400] font-bold uppercase">{m.roundName || 'Fase de Grupos'}</span>
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                                m.status === 'LIVE'
                                  ? 'bg-[#FF3B30] text-white'
                                  : m.status === 'FINISHED'
                                  ? 'bg-[#c3f400]/20 text-[#c3f400]'
                                  : 'bg-[#282a2e] text-[#8e9379]'
                              }`}
                            >
                              {m.status === 'LIVE' ? '🔴 En Vivo' : m.status === 'FINISHED' ? '✅ Finalizado' : '⏳ Próximo'}
                            </span>
                          </div>

                          <div className="flex flex-col gap-1 bg-[#1e2023] p-2 rounded-lg border border-[#333539]">
                            {/* Team A */}
                            <div className="flex items-center justify-between">
                              <span className={`font-bold ${m.status === 'FINISHED' && (m.winnerTeam === 'A' || winnerName === m.pairAName) ? 'text-[#c3f400]' : 'text-white'}`}>
                                {m.pairAName} {m.status === 'FINISHED' && (m.winnerTeam === 'A' || winnerName === m.pairAName) ? '🏆' : ''}
                              </span>
                              <span className="font-bold text-white">{setsWonA}</span>
                            </div>
                            {/* Team B */}
                            <div className="flex items-center justify-between">
                              <span className={`font-bold ${m.status === 'FINISHED' && (m.winnerTeam === 'B' || winnerName === m.pairBName) ? 'text-[#c3f400]' : 'text-white'}`}>
                                {m.pairBName} {m.status === 'FINISHED' && (m.winnerTeam === 'B' || winnerName === m.pairBName) ? '🏆' : ''}
                              </span>
                              <span className="font-bold text-white">{setsWonB}</span>
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

            {/* Standings Group Table */}
            <div>
              <h4 className="font-headline font-bold text-[14px] text-white mb-2 flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[#c3f400] text-[18px]">
                  table_chart
                </span>
                Tabla de Posiciones - Grupo A
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
                    {selectedTournament.registeredPairIds.map((pId, idx) => {
                      const p = pairs.find((pair) => pair.id === pId);
                      return (
                        <tr key={pId} className="hover:bg-[#282a2e]/50">
                          <td className="p-2.5 font-bold text-white truncate max-w-[120px]">
                            {p ? p.name : `Pareja #${idx + 1}`}
                          </td>
                          <td className="p-2.5">3</td>
                          <td className="p-2.5 font-bold text-[#c3f400]">{3 - idx}</td>
                          <td className="p-2.5 text-[#ffdad6]">{idx}</td>
                          <td className="p-2.5 font-black text-[#c3f400] text-[12px]">
                            {(3 - idx) * 3}
                          </td>
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
                <li>Campeón: {selectedTournament.rules.pointsDistribution.champion} pts</li>
                <li>Finalista: {selectedTournament.rules.pointsDistribution.runnerUp} pts</li>
                <li>Semifinalista: {selectedTournament.rules.pointsDistribution.semiFinals} pts</li>
                <li>Punto de Oro: {selectedTournament.rules.goldenPoint ? 'ACTIVADO' : 'DESACTIVADO'}</li>
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
