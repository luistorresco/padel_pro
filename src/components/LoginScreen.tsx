import React, { useState } from 'react';
import { PlayerStats } from '../types';

const EMPTY_STATS: PlayerStats = {
  pointsWon: 0, winners: 0, smashes: 0, smashesWon: 0, voleasWon: 0,
  bandejas: 0, viboras: 0, remates: 0, netPointsWon: 0, touches: 0,
  shots: 0, serves: 0, firstServes: 0, secondServes: 0, aces: 0,
  doubleFaults: 0, breakPoints: 0, breakPointsWon: 0, recoveries: 0,
  globos: 0, devoluciones: 0, pointsSaved: 0, unforcedErrors: 0,
  distanceKm: 0, timePlayedMin: 0, avgSpeedKmh: 0, movesCount: 0,
  matchesPlayed: 0, matchesWon: 0, matchesLost: 0, setsWon: 0, setsLost: 0,
  gamesWon: 0, gamesLost: 0,
};

interface LoginScreenProps {
  onLogin: (user: any, token: string) => void;
  apiBase: string;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onLogin, apiBase }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [surname, setSurname] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isRegister ? '/api/auth/register' : '/api/auth/login';
      const body = isRegister
        ? { email, password, name, surname, username, role: 'PLAYER', stats: EMPTY_STATS }
        : { email, password };

      const response = await fetch(`${apiBase}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.detail || data.message || `Error ${response.status}: ${response.statusText}`);
      }

      onLogin(data, data.access_token);
    } catch (err: any) {
      const message = err.message || '';
      if (message.includes('Failed to fetch') || message.includes('NetworkError') || message.includes('Network request failed')) {
        setError('No se pudo conectar con el servidor. Verifica tu conexión o intenta más tarde.');
      } else if (message.includes('401') || message.includes('Invalid credentials')) {
        setError('Email o contraseña incorrectos');
      } else if (message.includes('400')) {
        setError('Datos incompletos. Revisa los campos e intenta de nuevo.');
      } else if (message.includes('404')) {
        setError('Servicio no disponible. Contacta al administrador.');
      } else if (message) {
        setError(message);
      } else {
        setError('Error desconocido. Intenta nuevamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#111317] text-[#e2e2e7] font-sans antialiased flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="font-headline font-black text-[32px] text-white tracking-tight mb-2">
            PADEL PRO
          </h1>
          <p className="font-mono-stats text-[12px] text-[#c4c9ac]">
            {isRegister ? 'Crea tu cuenta para acceder' : 'Inicia sesión para continuar'}
          </p>
        </div>

        <div className="bg-[#1e2023] rounded-2xl p-6 border border-[#333539] shadow-2xl">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            {isRegister && (
              <>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-[11px] font-mono-stats text-[#c4c9ac] block mb-1">
                      Nombre
                    </label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full bg-[#111317] border border-[#333539] text-white p-3 rounded-lg text-[14px] font-mono-stats focus:border-[#c3f400] focus:outline-none transition-colors"
                      placeholder="Juan"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] font-mono-stats text-[#c4c9ac] block mb-1">
                      Apellido
                    </label>
                    <input
                      type="text"
                      value={surname}
                      onChange={(e) => setSurname(e.target.value)}
                      className="w-full bg-[#111317] border border-[#333539] text-white p-3 rounded-lg text-[14px] font-mono-stats focus:border-[#c3f400] focus:outline-none transition-colors"
                      placeholder="Pérez"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-[11px] font-mono-stats text-[#c4c9ac] block mb-1">
                    Nombre de usuario
                  </label>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full bg-[#111317] border border-[#333539] text-white p-3 rounded-lg text-[14px] font-mono-stats focus:border-[#c3f400] focus:outline-none transition-colors"
                    placeholder="juanpadel"
                  />
                </div>
              </>
            )}

            <div>
              <label className="text-[11px] font-mono-stats text-[#c4c9ac] block mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-[#111317] border border-[#333539] text-white p-3 rounded-lg text-[14px] font-mono-stats focus:border-[#c3f400] focus:outline-none transition-colors"
                placeholder="tu@email.com"
                required
              />
            </div>

            <div>
              <label className="text-[11px] font-mono-stats text-[#c4c9ac] block mb-1">
                Contraseña
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-[#111317] border border-[#333539] text-white p-3 rounded-lg text-[14px] font-mono-stats focus:border-[#c3f400] focus:outline-none transition-colors"
                placeholder="••••••••"
                required
              />
            </div>

            {error && (
              <div className="bg-[#2e1d1d] border border-[#ff3b30]/40 text-[#ffb4ab] text-[12px] font-mono-stats p-3 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#c3f400] hover:bg-[#abd600] text-[#161e00] font-headline font-bold text-[14px] py-3.5 rounded-xl transition-all active:scale-[0.98] shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Procesando...' : isRegister ? 'Registrarse' : 'Iniciar Sesión'}
            </button>
          </form>

          <div className="mt-4 text-center">
            <button
              onClick={() => {
                setIsRegister(!isRegister);
                setError('');
              }}
              className="text-[12px] font-mono-stats text-[#c3f400] hover:text-[#abd600] transition-colors"
            >
              {isRegister ? '¿Ya tienes cuenta? Inicia sesión' : '¿No tienes cuenta? Regístrate'}
            </button>
          </div>
        </div>

        <p className="text-center text-[10px] text-[#8e9379] font-mono-stats mt-6">
          Padel Pro © 2026 - Acceso restringido a usuarios registrados
        </p>
      </div>
    </div>
  );
};
