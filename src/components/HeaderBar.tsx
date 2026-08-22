import React, { useState } from 'react';
import { UserRole, NotificationItem } from '../types';

interface HeaderBarProps {
  role: UserRole;
  onToggleRole: () => void;
  notifications: NotificationItem[];
  onOpenNotifications: () => void;
  onOpenProfile: () => void;
  onOpenMenu: () => void;
  activeLiveMatchCount: number;
}

export const HeaderBar: React.FC<HeaderBarProps> = ({
  role,
  onToggleRole,
  notifications,
  onOpenNotifications,
  onOpenProfile,
  onOpenMenu,
  activeLiveMatchCount,
}) => {
  const unreadCount = notifications.filter((n) => !n.read).length;

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#1a1c1f]/90 backdrop-blur-md border-b border-[#333539] px-4 py-2.5 flex items-center justify-between shadow-md">
      {/* Left Menu & App Brand */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenMenu}
          className="text-[#c4c9ac] hover:text-[#c3f400] transition-colors p-2 rounded-lg hover:bg-[#282a2e] active:scale-95"
          title="Menú Principal"
        >
          <span className="material-symbols-outlined text-[24px]">menu</span>
        </button>

        <div className="flex items-center gap-2">
          <h1 className="font-headline font-black text-[22px] tracking-tight text-[#c3f400] flex items-center gap-1.5">
            PADEL PRO
          </h1>
          {activeLiveMatchCount > 0 && (
            <span className="inline-flex items-center gap-1 text-[10px] font-mono-stats font-bold bg-[#93000a]/80 text-[#ffdad6] border border-[#ffb4ab]/30 px-2 py-0.5 rounded-full">
              <span className="w-2 h-2 rounded-full bg-[#FF3B30] pulse-animation"></span>
              EN VIVO
            </span>
          )}
        </div>
      </div>

      {/* Right Controls: Role Switcher, Notifications, Profile */}
      <div className="flex items-center gap-2">
        {/* Role Switcher Badge */}
        <button
          onClick={onToggleRole}
          className={`px-2.5 py-1 rounded-full text-[11px] font-mono-stats font-bold flex items-center gap-1.5 border transition-all active:scale-95 ${
            role === 'ADMIN'
              ? 'bg-[#c3f400] text-[#161e00] border-[#c3f400] shadow-[0_0_10px_rgba(195,244,0,0.3)]'
              : 'bg-[#282a2e] text-[#e2e2e7] border-[#444933] hover:border-[#c3f400]'
          }`}
          title="Cambiar entre modo Jugador y Administrador"
        >
          <span className="material-symbols-outlined text-[14px]">
            {role === 'ADMIN' ? 'admin_panel_settings' : 'sports_tennis'}
          </span>
          <span>{role}</span>
        </button>

        {/* Notifications */}
        <button
          onClick={onOpenNotifications}
          className="relative text-[#e2e2e7] p-2 rounded-lg hover:bg-[#282a2e] transition-colors active:scale-95"
          title="Notificaciones"
        >
          <span className="material-symbols-outlined text-[22px]">notifications</span>
          {unreadCount > 0 && (
            <span className="absolute top-1 right-1 w-4 h-4 bg-[#FF3B30] text-white font-mono-stats font-bold text-[9px] rounded-full flex items-center justify-center">
              {unreadCount}
            </span>
          )}
        </button>

        {/* User Avatar */}
        <div
          onClick={onOpenProfile}
          className="w-9 h-9 rounded-full overflow-hidden border border-[#c3f400]/60 cursor-pointer hover:ring-2 hover:ring-[#c3f400] transition-all scale-95 active:scale-90"
          title="Ver Mi Perfil"
        >
          <img
            src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"
            alt="Avatar Jugador"
            className="w-full h-full object-cover"
          />
        </div>
      </div>
    </header>
  );
};
