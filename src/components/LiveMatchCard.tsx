import React from 'react';
import { Match } from '../types';

interface LiveMatchCardProps {
  match: Match;
  onOpenMatch: (matchId: string) => void;
}

export const LiveMatchCard: React.FC<LiveMatchCardProps> = ({ match, onOpenMatch }) => {
  const isLive = match.status === 'LIVE';

  return (
    <div className="bg-[#1e2023] rounded-xl p-4 flex flex-col gap-3.5 border border-[#333539] shadow-xl relative overflow-hidden group hover:border-[#c3f400]/50 transition-all">
      {/* Decorative ambient glow */}
      <div className="absolute -top-12 -right-12 w-36 h-36 bg-[#c3f400]/10 rounded-full blur-3xl pointer-events-none" />

      {/* Top Header */}
      <div className="flex justify-between items-center border-b border-[#333539]/80 pb-2">
        <div className="flex items-center gap-2">
          {isLive ? (
            <>
              <div className="w-2.5 h-2.5 rounded-full bg-[#FF3B30] pulse-animation" />
              <span className="font-mono-stats font-bold text-[12px] text-[#ffdad6] uppercase tracking-wider">
                EN VIVO • {match.courtName}
              </span>
            </>
          ) : (
            <span className="font-mono-stats font-medium text-[12px] text-[#c4c9ac]">
              {match.roundName || 'Partido'} • {match.courtName}
            </span>
          )}
        </div>
        <span className="font-mono-stats text-[11px] text-[#c3f400] bg-[#c3f400]/10 px-2 py-0.5 rounded-md font-semibold border border-[#c3f400]/20">
          {match.goldenPoint ? '⚡ Punto de Oro' : 'Ventaja Tradicional'}
        </span>
      </div>

      {/* Teams Grid */}
      <div className="flex justify-between items-stretch">
        {/* Team A */}
        <div className="flex flex-col gap-0.5 w-[42%]">
          <div className="font-headline font-bold text-[16px] text-white leading-tight truncate">
            {match.playerA1Name}
          </div>
          <div className="font-headline font-bold text-[16px] text-white leading-tight truncate">
            {match.playerA2Name}
          </div>
          <div className="font-mono-stats text-[11px] text-[#c4c9ac] mt-1">Pareja A</div>
        </div>

        {/* VS Divider */}
        <div className="flex flex-col items-center justify-center px-1">
          <span className="font-mono-stats text-[12px] font-bold text-[#444933] bg-[#282a2e] px-2 py-1 rounded">
            VS
          </span>
        </div>

        {/* Team B */}
        <div className="flex flex-col gap-0.5 w-[42%] text-right">
          <div className="font-headline font-bold text-[16px] text-white leading-tight truncate">
            {match.playerB1Name}
          </div>
          <div className="font-headline font-bold text-[16px] text-white leading-tight truncate">
            {match.playerB2Name}
          </div>
          <div className="font-mono-stats text-[11px] text-[#c4c9ac] mt-1">Pareja B</div>
        </div>
      </div>

      {/* Score Board */}
      <div className="mt-1 flex bg-[#282a2e] rounded-lg p-1 border border-[#333539]">
        {/* Labels */}
        <div className="flex flex-col justify-center gap-1 px-2 py-1.5 w-14 border-r border-[#333539]">
          <div className="font-mono-stats text-[11px] text-[#c4c9ac] font-bold">PA</div>
          <div className="font-mono-stats text-[11px] text-[#c4c9ac] font-bold">PB</div>
        </div>

        {/* Sets */}
        {match.sets.map((set, idx) => {
          const isActiveSet = idx === match.currentSetIndex && isLive;
          return (
            <div
              key={idx}
              className={`flex flex-col items-center justify-center gap-0.5 flex-1 py-1 rounded transition-all ${
                isActiveSet
                  ? 'bg-[#333539]/80 border border-[#c3f400]/80 shadow-[0_0_10px_rgba(195,244,0,0.2)]'
                  : ''
              }`}
            >
              <span
                className={`font-mono-stats text-[10px] font-bold mb-0.5 ${
                  isActiveSet ? 'text-[#c3f400]' : 'text-[#8e9379]'
                }`}
              >
                S{idx + 1}
              </span>
              <div
                className={`font-headline font-extrabold text-[18px] leading-none ${
                  set.winner === 'A' ? 'text-[#c3f400]' : 'text-white'
                }`}
              >
                {set.teamAGames}
              </div>
              <div
                className={`font-headline font-extrabold text-[18px] leading-none ${
                  set.winner === 'B' ? 'text-[#c3f400]' : 'text-[#c4c9ac]'
                }`}
              >
                {set.teamBGames}
              </div>
            </div>
          );
        })}

        {/* Current Points */}
        {isLive && (
          <div className="flex flex-col items-center justify-center gap-0.5 flex-1 py-1 pl-2 border-l border-[#333539]">
            <span className="font-mono-stats text-[10px] text-[#c3f400] font-bold mb-0.5">PTS</span>
            <div className="font-mono-stats font-extrabold text-[16px] text-[#c3f400] leading-none">
              {match.currentGame?.teamAPoints ?? '-'}
            </div>
            <div className="font-mono-stats font-extrabold text-[16px] text-white leading-none">
              {match.currentGame?.teamBPoints ?? '-'}
            </div>
          </div>
        )}
      </div>

      {/* Action CTA */}
      <button
        onClick={() => onOpenMatch(match.id)}
        className="w-full mt-1 bg-[#c3f400] text-[#161e00] font-headline font-bold py-2.5 px-4 rounded-lg flex items-center justify-center gap-2 hover:bg-[#abd600] active:scale-[0.98] transition-all shadow-md"
      >
        <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
          videocam
        </span>
        <span>Mesa de Control & Gestos de Cámara</span>
      </button>
    </div>
  );
};
