import React, { useState } from 'react';

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
        ? { email, password, name, surname, username, role: 'PLAYER' }
        : { email, password };

      const response = await fetch(`${apiBase}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.message || 'Error en la autenticación');
      }

      onLogin(data, data.access_token);
    } catch (err: any) {
      setError(err.message || 'Error desconocido');
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

          {!isRegister && (
            <div className="mt-4 p-3 bg-[#282a2e] rounded-lg border border-[#333539]">
              <p className="text-[11px] font-mono-stats text-[#c4c9ac] text-center">
                <span className="text-[#c3f400] font-bold">Admin:</span> admin@padelpro.app / PadelPro2026!
              </p>
            </div>
          )}
        </div>

        <p className="text-center text-[10px] text-[#8e9379] font-mono-stats mt-6">
          Padel Pro © 2026 - Acceso restringido a usuarios registrados
        </p>
      </div>
    </div>
  );
};
