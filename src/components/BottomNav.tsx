import React from 'react';
import { UserRole } from '../types';

export type ActiveTab = 'home' | 'tourneys' | 'matches' | 'ranking' | 'profile' | 'pairs' | 'admin';

interface BottomNavProps {
  activeTab: ActiveTab;
  onSelectTab: (tab: ActiveTab) => void;
  role: UserRole;
  isMatchLiveNow?: boolean;
}

export const BottomNav: React.FC<BottomNavProps> = ({
  activeTab,
  onSelectTab,
  role,
  isMatchLiveNow = false,
}) => {
  const navItems = [
    { id: 'home' as ActiveTab, label: 'Inicio', icon: 'home' },
    { id: 'tourneys' as ActiveTab, label: 'Torneos', icon: 'emoji_events' },
    { id: 'matches' as ActiveTab, label: 'Partido Live', icon: 'sports_tennis', highlight: isMatchLiveNow },
    { id: 'ranking' as ActiveTab, label: 'Ranking', icon: 'leaderboard' },
    { id: 'pairs' as ActiveTab, label: 'Parejas', icon: 'groups' },
    { id: 'profile' as ActiveTab, label: 'Perfil', icon: 'person' },
  ];

  if (role === 'ADMIN') {
    navItems.push({ id: 'admin' as ActiveTab, label: 'Admin Panel', icon: 'shield' });
  }

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-[#0c0e12]/95 backdrop-blur-xl border-t border-[#333539] px-2 py-2 flex justify-around items-center shadow-[0_-4px_24px_rgba(0,0,0,0.6)]">
      {navItems.map((item) => {
        const isActive = activeTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => onSelectTab(item.id)}
            className={`flex flex-col items-center justify-center transition-all duration-200 py-1 px-2.5 rounded-xl relative ${
              isActive
                ? 'bg-[#c3f400] text-[#161e00] font-bold shadow-[0_0_12px_rgba(195,244,0,0.4)] scale-105'
                : 'text-[#c4c9ac] hover:text-white hover:bg-[#282a2e]/60 scale-95'
            }`}
          >
            {item.highlight && !isActive && (
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-[#FF3B30] rounded-full pulse-animation" />
            )}
            <span
              className="material-symbols-outlined text-[22px]"
              style={{ fontVariationSettings: isActive ? "'FILL' 1" : "'FILL' 0" }}
            >
              {item.icon}
            </span>
            <span className="font-mono-stats text-[10px] mt-0.5 tracking-tight font-medium whitespace-nowrap">
              {item.label}
            </span>
          </button>
        );
      })}
    </nav>
  );
};
