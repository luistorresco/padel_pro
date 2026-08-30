import React, { useState } from 'react';
import { Pair, User, UserRole } from '../types';

interface PairsViewProps {
  pairs: Pair[];
  players: User[];
  role: UserRole;
  onCreatePair: (newPair: Pair) => void;
  onDissolvePair: (pairId: string) => void;
}

export const PairsView: React.FC<PairsViewProps> = ({
  pairs,
  players,
  role,
  onCreatePair,
  onDissolvePair,
}) => {
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [player1Id, setPlayer1Id] = useState<string>(players[0]?.id || '');
  const [player2Id, setPlayer2Id] = useState<string>(players[1]?.id || '');

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (player1Id === player2Id) {
      alert('Debes seleccionar dos jugadores diferentes para formar una pareja.');
      return;
    }

    const p1 = players.find((p) => p.id === player1Id);
    const p2 = players.find((p) => p.id === player2Id);

    if (!p1 || !p2) return;

    const newPair: Pair = {
      id: 'pair_' + Date.now(),
      name: `${p1.surname} / ${p2.surname}`,
      player1Id: p1.id,
      player2Id: p2.id,
      player1Name: `${p1.name} ${p1.surname}`,
      player2Name: `${p2.name} ${p2.surname}`,
      player1Avatar: p1.avatar,
      player2Avatar: p2.avatar,
      createdAt: new Date().toISOString().split('T')[0],
      status: 'ACTIVE',
      tournamentsDisputed: 0,
      titlesWon: 0,
    };

    onCreatePair({
      ...newPair,
      name: newPair.name,
      player1Id: newPair.player1Id,
      player2Id: newPair.player2Id,
    });
    setShowCreateModal(false);
  };

  return (
    <div className="flex flex-col gap-5 pb-24 px-4 pt-3 w-full">
      {/* Title */}
      <div className="flex items-center justify-between border-b border-[#333539] pb-3">
        <div>
          <h2 className="font-headline font-black text-[22px] text-white tracking-tight flex items-center gap-2">
            <span className="material-symbols-outlined text-[#c3f400] text-[28px]">groups</span>
            Parejas Competitivas
          </h2>
          <p className="text-[12px] text-[#c4c9ac] font-mono-stats">
            Formación y gestión de parejas de pádel
          </p>
        </div>

        {role === 'ADMIN' && (
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-[#c3f400] text-[#161e00] font-headline font-bold text-[12px] py-2 px-3.5 rounded-lg flex items-center gap-1 hover:bg-[#abd600] transition-all shadow-md"
          >
            <span className="material-symbols-outlined text-[18px]">add_circle</span>
            <span>Formar Pareja</span>
          </button>
        )}
      </div>

      {/* Pairs List */}
      <div className="flex flex-col gap-3.5">
        {pairs.map((pair) => (
          <div
            key={pair.id}
            className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] flex flex-col gap-3 shadow-lg"
          >
            <div className="flex items-center justify-between border-b border-[#333539] pb-2">
              <h3 className="font-headline font-bold text-[17px] text-white">
                {pair.name}
              </h3>
              <span className="bg-[#c3f400]/10 text-[#c3f400] font-mono-stats text-[10px] font-bold px-2.5 py-0.5 rounded border border-[#c3f400]/20">
                {pair.status}
              </span>
            </div>

            {/* Players Duo */}
            <div className="grid grid-cols-2 gap-3 items-center my-1">
              {/* Player 1 */}
              <div className="flex items-center gap-2.5 bg-[#0c0e12] p-2.5 rounded-lg border border-[#333539]">
                <div className="w-10 h-10 rounded-full overflow-hidden border border-[#c3f400] flex-shrink-0">
                  <img src={pair.player1Avatar} alt="" className="w-full h-full object-cover" />
                </div>
                <div className="truncate">
                  <span className="text-[10px] font-mono-stats text-[#8e9379] block">Jugador 1</span>
                  <span className="font-headline font-bold text-[13px] text-white truncate block">
                    {pair.player1Name}
                  </span>
                </div>
              </div>

              {/* Player 2 */}
              <div className="flex items-center gap-2.5 bg-[#0c0e12] p-2.5 rounded-lg border border-[#333539]">
                <div className="w-10 h-10 rounded-full overflow-hidden border border-[#c3f400] flex-shrink-0">
                  <img src={pair.player2Avatar} alt="" className="w-full h-full object-cover" />
                </div>
                <div className="truncate">
                  <span className="text-[10px] font-mono-stats text-[#8e9379] block">Jugador 2</span>
                  <span className="font-headline font-bold text-[13px] text-white truncate block">
                    {pair.player2Name}
                  </span>
                </div>
              </div>
            </div>

            {/* Stats Footer */}
            <div className="flex items-center justify-between text-[11px] font-mono-stats text-[#c4c9ac] pt-1">
              <span>
                Torneos Disputados: <b className="text-white">{pair.tournamentsDisputed || 0}</b>
              </span>
              <span>
                Títulos Ganados: <b className="text-[#c3f400]">{pair.titlesWon || 0} 🏆</b>
              </span>

              {role === 'ADMIN' && (
                <button
                  onClick={() => onDissolvePair(pair.id)}
                  className="text-[#ffdad6] hover:text-[#FF3B30] text-[10px] underline"
                >
                  Separar Pareja
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Create Pair Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <form
            onSubmit={handleCreateSubmit}
            className="bg-[#1e2023] rounded-2xl p-5 border border-[#333539] max-w-md w-full flex flex-col gap-4 shadow-2xl"
          >
            <div className="flex items-center justify-between border-b border-[#333539] pb-2">
              <h3 className="font-headline font-bold text-[18px] text-white">Formar Nueva Pareja</h3>
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
                <label className="text-[#c4c9ac] block mb-1">Primer Jugador</label>
                <select
                  value={player1Id}
                  onChange={(e) => setPlayer1Id(e.target.value)}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                >
                  {players.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name} {p.surname} ({p.level})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-[#c4c9ac] block mb-1">Segundo Jugador</label>
                <select
                  value={player2Id}
                  onChange={(e) => setPlayer2Id(e.target.value)}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2.5 rounded-lg"
                >
                  {players.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name} {p.surname} ({p.level})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              type="submit"
              className="bg-[#c3f400] text-[#161e00] font-headline font-bold text-[14px] py-3 rounded-xl hover:bg-[#abd600] transition-all shadow-md mt-2"
            >
              Confirmar Pareja
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
