import React, { useState } from 'react';
import { User } from '../types';

interface PlayerProfileViewProps {
  player: User;
  onUpdateProfile?: (updatedPlayer: User) => void;
}

export const PlayerProfileView: React.FC<PlayerProfileViewProps> = ({
  player,
  onUpdateProfile,
}) => {
  const [activeTab, setActiveTab] = useState<'RESUMEN' | 'OFENSIVAS' | 'DEFENSIVAS' | 'FISICAS'>('RESUMEN');
  const [isEditing, setIsEditing] = useState<boolean>(false);

  // Edit form state
  const [name, setName] = useState(player.name);
  const [surname, setSurname] = useState(player.surname);
  const [level, setLevel] = useState(player.level);
  const [position, setPosition] = useState(player.position);
  const [dominantHand, setDominantHand] = useState(player.dominantHand);

  const stats = player.stats || {};
  const winRate =
    (stats.matchesPlayed || 0) > 0
      ? Math.round((stats.matchesWon || 0) / (stats.matchesPlayed || 0) * 100)
      : 0;

  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    if (onUpdateProfile) {
      onUpdateProfile({
        ...player,
        name,
        surname,
        level,
        position,
        dominantHand,
      });
    }
    setIsEditing(false);
  };

  return (
    <div className="flex flex-col gap-5 pb-24 px-4 pt-3 w-full">
      {/* Profile Header Card */}
      <div className="bg-[#1e2023] rounded-2xl p-5 border border-[#333539] flex flex-col gap-4 shadow-xl relative overflow-hidden">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-20 h-20 rounded-full overflow-hidden border-2 border-[#c3f400] shadow-lg flex-shrink-0">
              <img src={player.avatar} alt="" className="w-full h-full object-cover" />
            </div>

            <div>
              <h2 className="font-headline font-black text-[22px] text-white leading-tight">
                {player.name} {player.surname}
              </h2>
              <span className="text-[12px] font-mono-stats text-[#c3f400] font-bold">
                @{player.username}
              </span>
              <div className="flex flex-wrap gap-1.5 mt-2 font-mono-stats text-[10px]">
                <span className="bg-[#c3f400]/10 text-[#c3f400] border border-[#c3f400]/30 px-2 py-0.5 rounded font-bold">
                  {player.level}
                </span>
                <span className="bg-[#282a2e] text-white px-2 py-0.5 rounded border border-[#333539]">
                  {player.position}
                </span>
                <span className="bg-[#282a2e] text-[#c4c9ac] px-2 py-0.5 rounded border border-[#333539]">
                  Mano: {player.dominantHand}
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={() => setIsEditing(!isEditing)}
            className="p-2 bg-[#282a2e] hover:bg-[#333539] text-[#c3f400] rounded-xl border border-[#333539]"
            title="Editar Perfil"
          >
            <span className="material-symbols-outlined text-[20px]">edit</span>
          </button>
        </div>

        {/* Current Pair Banner */}
        <div className="bg-[#0c0e12] p-3 rounded-xl border border-[#333539] flex items-center justify-between">
          <div>
            <span className="text-[10px] font-mono-stats text-[#8e9379] block uppercase">
              Pareja Actual de Pádel:
            </span>
            <span className="font-headline font-bold text-[14px] text-white">
              {player.partnerName || 'Sin pareja registrada'}
            </span>
          </div>

          <span className="font-mono-stats font-black text-[16px] text-[#c3f400] bg-[#c3f400]/10 px-3 py-1 rounded-lg border border-[#c3f400]/20">
            {player.points} pts
          </span>
        </div>
      </div>

      {/* Edit Modal */}
      {isEditing && (
        <form
          onSubmit={handleSaveProfile}
          className="bg-[#282a2e] p-4 rounded-xl border border-[#c3f400] flex flex-col gap-3 font-mono-stats text-[12px]"
        >
          <h3 className="font-bold text-white border-b border-[#333539] pb-1">
            Editar Datos del Jugador
          </h3>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[#c4c9ac] block mb-1">Nombre</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded"
              />
            </div>
            <div>
              <label className="text-[#c4c9ac] block mb-1">Apellido</label>
              <input
                type="text"
                value={surname}
                onChange={(e) => setSurname(e.target.value)}
                className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[#c4c9ac] block mb-1">Nivel</label>
              <select
                value={level}
                onChange={(e: any) => setLevel(e.target.value)}
                className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded"
              >
                <option value="Principiante">Principiante</option>
                <option value="Intermedio">Intermedio</option>
                <option value="Avanzado">Avanzado</option>
                <option value="Profesional">Profesional</option>
              </select>
            </div>
            <div>
              <label className="text-[#c4c9ac] block mb-1">Mano Dominante</label>
              <select
                value={dominantHand}
                onChange={(e: any) => setDominantHand(e.target.value)}
                className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded"
              >
                <option value="Derecha">Derecha</option>
                <option value="Zurda">Zurda</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            className="bg-[#c3f400] text-[#161e00] font-bold py-2 rounded mt-1"
          >
            Guardar Cambios
          </button>
        </form>
      )}

      {/* Stats Category Tabs */}
      <div className="flex gap-1.5 bg-[#1e2023] p-1.5 rounded-xl border border-[#333539] text-[11px] font-mono-stats font-bold">
        {(['RESUMEN', 'OFENSIVAS', 'DEFENSIVAS', 'FISICAS'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 py-2 rounded-lg transition-all ${
              activeTab === tab
                ? 'bg-[#c3f400] text-[#161e00] shadow-md'
                : 'text-[#c4c9ac] hover:text-white'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Content Panels */}
      {activeTab === 'RESUMEN' && (
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-[#1e2023] p-4 rounded-xl border border-[#333539] flex flex-col justify-center text-center">
            <span className="text-[11px] font-mono-stats text-[#8e9379]">Partidos Jugados</span>
            <span className="font-headline font-black text-[32px] text-white mt-1">
              {stats.matchesPlayed}
            </span>
            <span className="text-[11px] font-mono-stats text-[#c3f400]">
              {stats.matchesWon} PG / {stats.matchesLost} PP
            </span>
          </div>

          <div className="bg-[#1e2023] p-4 rounded-xl border border-[#333539] flex flex-col justify-center text-center">
            <span className="text-[11px] font-mono-stats text-[#8e9379]">% Victorias</span>
            <span className="font-headline font-black text-[32px] text-[#c3f400] mt-1">
              {winRate}%
            </span>
            <span className="text-[11px] font-mono-stats text-[#c4c9ac]">
              {stats.setsWon} Sets Ganados
            </span>
          </div>

          <div className="col-span-2 bg-[#1e2023] p-4 rounded-xl border border-[#333539] flex flex-col gap-2">
            <h4 className="font-headline font-bold text-[14px] text-white border-b border-[#333539] pb-2">
              Balance de Juegos & Puntos
            </h4>

            <div className="grid grid-cols-2 gap-2 text-[12px] font-mono-stats">
              <div className="bg-[#0c0e12] p-2.5 rounded border border-[#333539]">
                <span className="text-[#8e9379] block">Juegos Ganados:</span>
                <span className="font-bold text-[#c3f400] text-[16px]">{stats.gamesWon}</span>
              </div>
              <div className="bg-[#0c0e12] p-2.5 rounded border border-[#333539]">
                <span className="text-[#8e9379] block">Juegos Perdidos:</span>
                <span className="font-bold text-[#ffdad6] text-[16px]">{stats.gamesLost}</span>
              </div>
              <div className="bg-[#0c0e12] p-2.5 rounded border border-[#333539]">
                <span className="text-[#8e9379] block">Puntos Totales:</span>
                <span className="font-bold text-white text-[16px]">{stats.pointsWon}</span>
              </div>
              <div className="bg-[#0c0e12] p-2.5 rounded border border-[#333539]">
                <span className="text-[#8e9379] block">Puntos de Red:</span>
                <span className="font-bold text-[#c3f400] text-[16px]">{stats.netPointsWon}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'OFENSIVAS' && (
        <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] grid grid-cols-2 gap-3 text-[12px] font-mono-stats">
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Winners (Ganadores):</span>
            <span className="font-bold text-[#c3f400] text-[20px]">{stats.winners}</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Smashes Efectivos:</span>
            <span className="font-bold text-white text-[20px]">{stats.smashesWon} / {stats.smashes}</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Voleas Ganadoras:</span>
            <span className="font-bold text-[#c3f400] text-[20px]">{stats.voleasWon}</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Bandejas:</span>
            <span className="font-bold text-white text-[20px]">{stats.bandejas}</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Víboras:</span>
            <span className="font-bold text-white text-[20px]">{stats.viboras}</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Break Points Ganados:</span>
            <span className="font-bold text-[#c3f400] text-[20px]">{stats.breakPointsWon} / {stats.breakPoints}</span>
          </div>
        </div>
      )}

      {activeTab === 'DEFENSIVAS' && (
        <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] grid grid-cols-2 gap-3 text-[12px] font-mono-stats">
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Recuperaciones:</span>
            <span className="font-bold text-[#c3f400] text-[20px]">{stats.recoveries}</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Globos Profundos:</span>
            <span className="font-bold text-white text-[20px]">{stats.globos}</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Puntos Salvados:</span>
            <span className="font-bold text-white text-[20px]">{stats.pointsSaved}</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Errores No Forzados:</span>
            <span className="font-bold text-[#ffdad6] text-[20px]">{stats.unforcedErrors}</span>
          </div>
        </div>
      )}

      {activeTab === 'FISICAS' && (
        <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] grid grid-cols-2 gap-3 text-[12px] font-mono-stats">
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Distancia Recorrida:</span>
            <span className="font-bold text-[#c3f400] text-[20px]">{stats.distanceKm} km</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Tiempo de Juego:</span>
            <span className="font-bold text-white text-[20px]">{Math.floor(stats.timePlayedMin / 60)}h {stats.timePlayedMin % 60}m</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Velocidad Promedio:</span>
            <span className="font-bold text-white text-[20px]">{stats.avgSpeedKmh} km/h</span>
          </div>
          <div className="bg-[#0c0e12] p-3 rounded-lg border border-[#333539]">
            <span className="text-[#8e9379] block">Desplazamientos:</span>
            <span className="font-bold text-white text-[20px]">{stats.movesCount}</span>
          </div>
        </div>
      )}
    </div>
  );
};
