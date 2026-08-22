import React from 'react';
import { User } from '../types';

interface RankingsViewProps {
  players: User[];
  onSelectPlayer: (player: User) => void;
}

export const RankingsView: React.FC<RankingsViewProps> = ({ players, onSelectPlayer }) => {
  const sortedPlayers = [...players].sort((a, b) => b.points - a.points);

  return (
    <div className="flex flex-col gap-5 pb-24 px-4 pt-3 w-full">
      {/* View Title */}
      <div className="border-b border-[#333539] pb-3">
        <h2 className="font-headline font-black text-[22px] text-white tracking-tight flex items-center gap-2">
          <span className="material-symbols-outlined text-[#c3f400] text-[28px]">leaderboard</span>
          Ranking Oficial de Pádel 2026
        </h2>
        <p className="text-[12px] text-[#c4c9ac] font-mono-stats">
          Puntos acumulados por torneos disputados en la temporada
        </p>
      </div>

      {/* Podium Top 3 */}
      {sortedPlayers.length >= 3 && (
        <div className="grid grid-cols-3 gap-2.5 items-end my-2">
          {/* #2 Rank */}
          <div
            onClick={() => onSelectPlayer(sortedPlayers[1])}
            className="bg-[#1e2023] rounded-xl p-3 border border-[#333539] flex flex-col items-center text-center cursor-pointer hover:border-[#c3f400]/50 transition-all shadow-lg"
          >
            <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-slate-300 relative mb-1.5">
              <img src={sortedPlayers[1].avatar} alt="" className="w-full h-full object-cover" />
              <span className="absolute bottom-0 right-0 bg-slate-300 text-black font-mono-stats font-bold text-[9px] w-4 h-4 rounded-full flex items-center justify-center">
                2
              </span>
            </div>
            <span className="font-headline font-bold text-[13px] text-white truncate max-w-full">
              {sortedPlayers[1].name}
            </span>
            <span className="font-mono-stats font-extrabold text-[12px] text-[#c3f400] mt-0.5">
              {sortedPlayers[1].points} pts
            </span>
          </div>

          {/* #1 Rank (Center Podium) */}
          <div
            onClick={() => onSelectPlayer(sortedPlayers[0])}
            className="bg-[#1e2023] rounded-xl p-3.5 border-2 border-[#c3f400] flex flex-col items-center text-center cursor-pointer hover:scale-105 transition-all shadow-[0_0_20px_rgba(195,244,0,0.25)] relative"
          >
            <div className="absolute -top-3 bg-[#c3f400] text-[#161e00] text-[10px] font-mono-stats font-extrabold px-2 py-0.5 rounded-full">
              👑 LÍDER
            </div>
            <div className="w-14 h-14 rounded-full overflow-hidden border-2 border-[#c3f400] relative mb-1.5 mt-1">
              <img src={sortedPlayers[0].avatar} alt="" className="w-full h-full object-cover" />
              <span className="absolute bottom-0 right-0 bg-[#c3f400] text-[#161e00] font-mono-stats font-bold text-[10px] w-5 h-5 rounded-full flex items-center justify-center">
                1
              </span>
            </div>
            <span className="font-headline font-extrabold text-[15px] text-white truncate max-w-full">
              {sortedPlayers[0].name}
            </span>
            <span className="font-mono-stats font-black text-[14px] text-[#c3f400] mt-0.5">
              {sortedPlayers[0].points} pts
            </span>
          </div>

          {/* #3 Rank */}
          <div
            onClick={() => onSelectPlayer(sortedPlayers[2])}
            className="bg-[#1e2023] rounded-xl p-3 border border-[#333539] flex flex-col items-center text-center cursor-pointer hover:border-[#c3f400]/50 transition-all shadow-lg"
          >
            <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-amber-600 relative mb-1.5">
              <img src={sortedPlayers[2].avatar} alt="" className="w-full h-full object-cover" />
              <span className="absolute bottom-0 right-0 bg-amber-600 text-white font-mono-stats font-bold text-[9px] w-4 h-4 rounded-full flex items-center justify-center">
                3
              </span>
            </div>
            <span className="font-headline font-bold text-[13px] text-white truncate max-w-full">
              {sortedPlayers[2].name}
            </span>
            <span className="font-mono-stats font-extrabold text-[12px] text-[#c3f400] mt-0.5">
              {sortedPlayers[2].points} pts
            </span>
          </div>
        </div>
      )}

      {/* Leaderboard Table List */}
      <div className="bg-[#1e2023] rounded-xl border border-[#333539] overflow-hidden shadow-xl">
        <div className="bg-[#282a2e] px-4 py-2.5 font-mono-stats text-[11px] text-[#c4c9ac] flex items-center justify-between uppercase">
          <span>Posición / Jugador</span>
          <span>Puntos Totales</span>
        </div>

        <div className="divide-y divide-[#333539]">
          {sortedPlayers.map((player, idx) => (
            <div
              key={player.id}
              onClick={() => onSelectPlayer(player)}
              className="p-3 hover:bg-[#282a2e]/60 transition-colors flex items-center justify-between cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <span
                  className={`font-mono-stats font-black text-[14px] w-6 text-center ${
                    idx === 0
                      ? 'text-[#c3f400]'
                      : idx === 1
                      ? 'text-slate-300'
                      : idx === 2
                      ? 'text-amber-500'
                      : 'text-[#8e9379]'
                  }`}
                >
                  #{idx + 1}
                </span>

                <div className="w-9 h-9 rounded-full overflow-hidden border border-[#333539] flex-shrink-0">
                  <img src={player.avatar} alt="" className="w-full h-full object-cover" />
                </div>

                <div>
                  <h4 className="font-headline font-bold text-[14px] text-white leading-tight">
                    {player.name} {player.surname}
                  </h4>
                  <div className="text-[11px] font-mono-stats text-[#c4c9ac] flex items-center gap-2">
                    <span>{player.level}</span>
                    <span>•</span>
                    <span>{player.position}</span>
                  </div>
                </div>
              </div>

              <div className="font-mono-stats font-black text-[15px] text-[#c3f400]">
                {player.points} <span className="text-[10px] text-[#8e9379]">pts</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
