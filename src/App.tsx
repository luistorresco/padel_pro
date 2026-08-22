/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import {
  User,
  UserRole,
  Pair,
  Tournament,
  Match,
  Court,
  AuditLog,
  NotificationItem,
  MatchEvent,
} from './types';
import {
  INITIAL_USER,
  INITIAL_PLAYERS,
  INITIAL_PAIRS,
  INITIAL_TOURNAMENTS,
  INITIAL_MATCHES,
  INITIAL_COURTS,
  INITIAL_AUDIT_LOGS,
  INITIAL_NOTIFICATIONS,
} from './data/mockData';
import { HeaderBar } from './components/HeaderBar';
import { BottomNav, ActiveTab } from './components/BottomNav';
import { LiveMatchCard } from './components/LiveMatchCard';
import { MatchController } from './components/MatchController';
import { TournamentsView } from './components/TournamentsView';
import { RankingsView } from './components/RankingsView';
import { PlayerProfileView } from './components/PlayerProfileView';
import { PairsView } from './components/PairsView';
import { AdminDashboardView } from './components/AdminDashboardView';
import { RuleEngineTesterModal } from './components/RuleEngineTesterModal';
import { api } from './api';
import { createInitialGameScore } from './domain/scoringEngine';

export default function App() {
  // Global Application State
  const [role, setRole] = useState<UserRole>('ADMIN');
  const [activeTab, setActiveTab] = useState<ActiveTab>('home');
  const [loading, setLoading] = useState<boolean>(true);
  const [usingFallback, setUsingFallback] = useState<boolean>(false);

  const [user, setUser] = useState<User>(INITIAL_USER);
  const [players, setPlayers] = useState<User[]>(INITIAL_PLAYERS);
  const [pairs, setPairs] = useState<Pair[]>(INITIAL_PAIRS);
  const [tournaments, setTournaments] = useState<Tournament[]>(INITIAL_TOURNAMENTS);
  const [matches, setMatches] = useState<Match[]>(INITIAL_MATCHES);
  const [courts, setCourts] = useState<Court[]>(INITIAL_COURTS);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>(INITIAL_AUDIT_LOGS);
  const [notifications, setNotifications] = useState<NotificationItem[]>(INITIAL_NOTIFICATIONS);

  // Overlay Modals & Drawers
  const [selectedMatchId, setSelectedMatchId] = useState<string | null>(null);
  const [selectedPlayer, setSelectedPlayer] = useState<User | null>(null);
  const [showNotificationsDrawer, setShowNotificationsDrawer] = useState<boolean>(false);
  const [showMenuDrawer, setShowMenuDrawer] = useState<boolean>(false);
  const [showUnitTestModal, setShowUnitTestModal] = useState<boolean>(false);

  // Load initial data from backend
  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      setLoading(true);
      try {
        const [users, pairsData, tournamentsData, matchesData, courtsData, auditLogsData, notificationsData] = await Promise.all([
          api.getUsers(),
          api.getPairs(),
          api.getTournaments(),
          api.getMatches(),
          api.getCourts(),
          api.getAuditLogs(),
          api.getNotifications(),
        ]);

        if (cancelled) return;

        if (users && users.length > 0) {
          setPlayers(users);
          const current = await api.getCurrentUser();
          if (current) {
            const typedCurrent = current as User;
            setUser(typedCurrent);
          }
        }
        if (pairsData) setPairs(pairsData as Pair[]);
        if (tournamentsData) setTournaments(tournamentsData as Tournament[]);
        if (matchesData) {
          const normalizedMatches = (matchesData as Match[]).map((m) => ({
            ...m,
            currentGame: m.currentGame || createInitialGameScore('A'),
          }));
          setMatches(normalizedMatches);
        }
        if (courtsData) setCourts(courtsData as Court[]);
        if (auditLogsData) setAuditLogs(auditLogsData as AuditLog[]);
        if (notificationsData) setNotifications(notificationsData as NotificationItem[]);
      } catch (error) {
        console.warn('[App] Backend unavailable, using local fallback data.', error);
        if (!cancelled) {
          setUsingFallback(true);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadData();

    return () => {
      cancelled = true;
    };
  }, []);

  // Active Live Match
  const activeLiveMatch = matches.find((m) => m.status === 'LIVE') || matches[0];
  const liveCount = matches.filter((m) => m.status === 'LIVE').length;

  // Handlers
  const handleToggleRole = () => {
    setRole((prev) => (prev === 'ADMIN' ? 'PLAYER' : 'ADMIN'));
  };

  const handleUpdateMatch = async (updatedMatch: Match, newEvent?: MatchEvent) => {
    const currentMatch = matches.find((m) => m.id === updatedMatch.id);
    const isJustFinished = updatedMatch.status === 'FINISHED' && currentMatch?.status !== 'FINISHED';

    let nextMatchesList = matches.map((m) => (m.id === updatedMatch.id ? updatedMatch : m));

    if (isJustFinished) {
      const isWinnerA = updatedMatch.winnerTeam === 'A' ||
        updatedMatch.sets.filter((s) => s.winner === 'A').length >= (updatedMatch.setsToWin || 2);

      const winnerPairId = isWinnerA ? updatedMatch.pairAId : updatedMatch.pairBId;
      const winnerPairName = isWinnerA ? updatedMatch.pairAName : updatedMatch.pairBName;
      const loserPairId = isWinnerA ? updatedMatch.pairBId : updatedMatch.pairAId;
      const loserPairName = isWinnerA ? updatedMatch.pairBName : updatedMatch.pairAName;

      const winnerPlayerIds = isWinnerA
        ? [updatedMatch.playerA1Id, updatedMatch.playerA2Id]
        : [updatedMatch.playerB1Id, updatedMatch.playerB2Id];
      const loserPlayerIds = isWinnerA
        ? [updatedMatch.playerB1Id, updatedMatch.playerB2Id]
        : [updatedMatch.playerA1Id, updatedMatch.playerA2Id];

      const winnerPlayer1 = isWinnerA
        ? { id: updatedMatch.playerA1Id, name: updatedMatch.playerA1Name, avatar: updatedMatch.playerA1Avatar }
        : { id: updatedMatch.playerB1Id, name: updatedMatch.playerB1Name, avatar: updatedMatch.playerB1Avatar };
      const winnerPlayer2 = isWinnerA
        ? { id: updatedMatch.playerA2Id, name: updatedMatch.playerA2Name, avatar: updatedMatch.playerA2Avatar }
        : { id: updatedMatch.playerB2Id, name: updatedMatch.playerB2Name, avatar: updatedMatch.playerB2Avatar };

      const setsWonA = updatedMatch.sets.filter((s) => s.winner === 'A').length;
      const setsWonB = updatedMatch.sets.filter((s) => s.winner === 'B').length;
      const gamesWonA = updatedMatch.sets.reduce((sum, s) => sum + (s.teamAGames || 0), 0);
      const gamesWonB = updatedMatch.sets.reduce((sum, s) => sum + (s.teamBGames || 0), 0);

      const notificationBody = `¡Victoria para ${winnerPairName}! Se han otorgado +150 pts de ranking y la pareja avanza en el torneo.`;

      const finishBody = {
        winner_team: updatedMatch.winnerTeam,
        create_notification: true,
        notification: {
          id: 'notif_' + Date.now(),
          title: '🏆 ¡Partido Finalizado y Torneo Reajustado!',
          body: notificationBody,
          timestamp: 'Ahora',
          read: false,
          type: 'MATCH',
          linkId: updatedMatch.id,
        },
        create_audit: true,
        audit: {
          id: 'audit_' + Date.now(),
          adminName: user.name + ' ' + user.surname,
          adminEmail: user.email,
          action: 'PARTIDO_FINALIZADO',
          target: `Partido ${updatedMatch.id} (${updatedMatch.roundName || 'Eliminatoria'})`,
          details: `Ganador: ${winnerPairName} vs ${loserPairName}. Puntos asignados en ranking y cuadro reajustado.`,
          timestamp: new Date().toLocaleString(),
        },
      };

      try {
        await api.finishMatch(updatedMatch.id, finishBody as unknown as Record<string, unknown>);
      } catch (error) {
        console.error('[App] Failed to finish match via API, applying local fallback.', error);
        setPlayers((prevPlayers) =>
          prevPlayers.map((p) => {
            const isWinner = winnerPlayerIds.includes(p.id);
            const isLoser = loserPlayerIds.includes(p.id);
            if (!isWinner && !isLoser) return p;

            const myTeamWon = isWinner;
            const mySetsWon = myTeamWon ? (isWinnerA ? setsWonA : setsWonB) : (isWinnerA ? setsWonB : setsWonA);
            const mySetsLost = myTeamWon ? (isWinnerA ? setsWonB : setsWonA) : (isWinnerA ? setsWonA : setsWonB);
            const myGamesWon = myTeamWon ? (isWinnerA ? gamesWonA : gamesWonB) : (isWinnerA ? gamesWonB : gamesWonA);
            const myGamesLost = myTeamWon ? (isWinnerA ? gamesWonB : gamesWonA) : (isWinnerA ? gamesWonA : gamesWonB);

            return {
              ...p,
              points: p.points + (myTeamWon ? 150 : 30),
              stats: {
                ...p.stats,
                matchesPlayed: p.stats.matchesPlayed + 1,
                matchesWon: myTeamWon ? p.stats.matchesWon + 1 : p.stats.matchesWon,
                matchesLost: !myTeamWon ? p.stats.matchesLost + 1 : p.stats.matchesLost,
                setsWon: p.stats.setsWon + mySetsWon,
                setsLost: p.stats.setsLost + mySetsLost,
                gamesWon: p.stats.gamesWon + myGamesWon,
                gamesLost: p.stats.gamesLost + myGamesLost,
              },
            };
          })
        );

        setUser((prevUser) => {
          const isWinner = winnerPlayerIds.includes(prevUser.id);
          const isLoser = loserPlayerIds.includes(prevUser.id);
          if (!isWinner && !isLoser) return prevUser;

          const myTeamWon = isWinner;
          const mySetsWon = myTeamWon ? (isWinnerA ? setsWonA : setsWonB) : (isWinnerA ? setsWonB : setsWonA);
          const mySetsLost = myTeamWon ? (isWinnerA ? setsWonB : setsWonA) : (isWinnerA ? setsWonA : setsWonB);
          const myGamesWon = myTeamWon ? (isWinnerA ? gamesWonA : gamesWonB) : (isWinnerA ? gamesWonB : gamesWonA);
          const myGamesLost = myTeamWon ? (isWinnerA ? gamesWonB : gamesWonA) : (isWinnerA ? gamesWonA : gamesWonB);

          return {
            ...prevUser,
            points: prevUser.points + (myTeamWon ? 150 : 30),
            stats: {
              ...prevUser.stats,
              matchesPlayed: prevUser.stats.matchesPlayed + 1,
              matchesWon: myTeamWon ? prevUser.stats.matchesWon + 1 : prevUser.stats.matchesWon,
              matchesLost: !myTeamWon ? prevUser.stats.matchesLost + 1 : prevUser.stats.matchesLost,
              setsWon: prevUser.stats.setsWon + mySetsWon,
              setsLost: prevUser.stats.setsLost + mySetsLost,
              gamesWon: prevUser.stats.gamesWon + myGamesWon,
              gamesLost: prevUser.stats.gamesLost + myGamesLost,
            },
          };
        });

        setPairs((prevPairs) =>
          prevPairs.map((pair) => {
            if (pair.id === winnerPairId) {
              return {
                ...pair,
                tournamentsDisputed: (pair.tournamentsDisputed || 0) + 1,
                titlesWon: updatedMatch.roundName === 'Gran Final' ? (pair.titlesWon || 0) + 1 : (pair.titlesWon || 0),
              };
            }
            return pair;
          })
        );

        if (updatedMatch.tournamentId) {
          const tourId = updatedMatch.tournamentId;
          const tourMatches = nextMatchesList.filter((m) => m.tournamentId === tourId);

          let targetRoundName = 'Semifinal';
          if (updatedMatch.roundName === 'Cuartos de Final') {
            targetRoundName = 'Semifinal';
          } else if (updatedMatch.roundName === 'Semifinal') {
            targetRoundName = 'Gran Final';
          }

          if (updatedMatch.roundName === 'Gran Final') {
            setTournaments((prevTours) =>
              prevTours.map((t) => (t.id === tourId ? { ...t, status: 'FINISHED' } : t))
            );
          } else {
            let nextRoundMatch = tourMatches.find(
              (m) => m.roundName === targetRoundName && m.status === 'UPCOMING'
            );

            if (nextRoundMatch) {
              nextMatchesList = nextMatchesList.map((m) => {
                if (m.id === nextRoundMatch!.id) {
                  if (!m.pairAId || m.pairAId === 'pair_tbd' || m.pairAName.includes('Por Definir')) {
                    return {
                      ...m,
                      pairAId: winnerPairId,
                      pairAName: winnerPairName,
                      playerA1Id: winnerPlayer1.id,
                      playerA1Name: winnerPlayer1.name,
                      playerA1Avatar: winnerPlayer1.avatar,
                      playerA2Id: winnerPlayer2.id,
                      playerA2Name: winnerPlayer2.name,
                      playerA2Avatar: winnerPlayer2.avatar,
                    };
                  } else if (!m.pairBId || m.pairBId === 'pair_tbd' || m.pairBName.includes('Por Definir')) {
                    return {
                      ...m,
                      pairBId: winnerPairId,
                      pairBName: winnerPairName,
                      playerB1Id: winnerPlayer1.id,
                      playerB1Name: winnerPlayer1.name,
                      playerB1Avatar: winnerPlayer1.avatar,
                      playerB2Id: winnerPlayer2.id,
                      playerB2Name: winnerPlayer2.name,
                      playerB2Avatar: winnerPlayer2.avatar,
                    };
                  }
                }
                return m;
              });
            } else {
              const newNextMatch: Match = {
                id: 'match_auto_' + Date.now(),
                tournamentId: tourId,
                tournamentName: updatedMatch.tournamentName,
                courtId: 'crt_central',
                courtName: 'Pista Central',
                dateTime: new Date(Date.now() + 86400000).toISOString().replace('T', ' ').slice(0, 16),
                pairAId: winnerPairId,
                pairBId: 'pair_tbd',
                pairAName: winnerPairName,
                pairBName: 'Rival Por Definir',
                playerA1Id: winnerPlayer1.id,
                playerA1Name: winnerPlayer1.name,
                playerA1Avatar: winnerPlayer1.avatar,
                playerA2Id: winnerPlayer2.id,
                playerA2Name: winnerPlayer2.name,
                playerA2Avatar: winnerPlayer2.avatar,
                playerB1Id: 'usr_tbd1',
                playerB2Id: 'usr_tbd2',
                playerB1Name: 'Jugador 1',
                playerB2Name: 'Jugador 2',
                playerB1Avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150',
                playerB2Avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150',
                status: 'UPCOMING',
                sets: [{ teamAGames: 0, teamBGames: 0, isTieBreak: false }],
                currentGame: { teamAPoints: '0', teamBPoints: '0', serverTeam: 'A' },
                currentSetIndex: 0,
                elapsedTimeSec: 0,
                goldenPoint: true,
                setsToWin: 2,
                roundName: targetRoundName,
              };
              nextMatchesList = [newNextMatch, ...nextMatchesList];
            }
          }
        }

        const newNotif: NotificationItem = {
          id: 'notif_' + Date.now(),
          title: '🏆 ¡Partido Finalizado y Torneo Reajustado!',
          body: notificationBody,
          timestamp: 'Ahora',
          read: false,
          type: 'MATCH',
          linkId: updatedMatch.id,
        };
        setNotifications((prev) => [newNotif, ...prev]);

        const finishAudit: AuditLog = {
          id: 'audit_' + Date.now(),
          adminName: user.name + ' ' + user.surname,
          adminEmail: user.email,
          action: 'PARTIDO_FINALIZADO',
          target: `Partido ${updatedMatch.id} (${updatedMatch.roundName || 'Eliminatoria'})`,
          details: `Ganador: ${winnerPairName} vs ${loserPairName}. Puntos asignados en ranking y cuadro reajustado.`,
          timestamp: new Date().toLocaleString(),
        };
        setAuditLogs((prev) => [finishAudit, ...prev]);
      }
    }

    setMatches(nextMatchesList);

    if (newEvent) {
      const newAudit: AuditLog = {
        id: 'audit_' + Date.now(),
        adminName: user.name + ' ' + user.surname,
        adminEmail: user.email,
        action: 'PUNTO_REGISTRADO',
        target: `Partido ${updatedMatch.id}`,
        details: newEvent.description,
        timestamp: new Date().toLocaleString(),
      };
      setAuditLogs((prev) => [newAudit, ...prev]);

      api.createMatchEvent(updatedMatch.id, {
        id: newEvent.id,
        match_id: updatedMatch.id,
        set_number: 0,
        game_number: 0,
        timestamp: newEvent.timestamp,
        winning_pair_id: newEvent.winningPairId,
        player_id: newEvent.playerId,
        player_name: newEvent.playerName,
        event_type: newEvent.eventType,
        description: newEvent.description,
        score_snapshot: newEvent.scoreSnapshot,
      }).catch((error) => {
        console.error('[App] Failed to create match event via API.', error);
      });
    }

    api.updateMatch(updatedMatch.id, updatedMatch as unknown as Record<string, unknown>).catch((error) => {
      console.error('[App] Failed to update match via API.', error);
    });
  };

  const handleCreateTournament = async (newTour: Tournament) => {
    setTournaments((prev) => [newTour, ...prev]);
    const newAudit: AuditLog = {
      id: 'audit_' + Date.now(),
      adminName: user.name + ' ' + user.surname,
      adminEmail: user.email,
      action: 'CREACION_TORNEO',
      target: newTour.name,
      details: `Torneo ${newTour.category} (${newTour.level}) publicado`,
      timestamp: new Date().toLocaleString(),
    };
    setAuditLogs((prev) => [newAudit, ...prev]);

    api.createTournament(newTour as unknown as Record<string, unknown>).catch((error) => {
      console.error('[App] Failed to create tournament via API.', error);
    });
  };

  const handleRegisterPair = async (tournamentId: string, pairId: string) => {
    setTournaments((prev) =>
      prev.map((t) => {
        if (t.id === tournamentId && !t.registeredPairIds.includes(pairId)) {
          return { ...t, registeredPairIds: [...t.registeredPairIds, pairId] };
        }
        return t;
      })
    );
    alert('¡Pareja inscrita correctamente en el torneo!');

    api.registerPair(tournamentId, pairId).catch((error) => {
      console.error('[App] Failed to register pair via API.', error);
    });
  };

  const handleCreatePair = async (newPair: Pair) => {
    setPairs((prev) => [newPair, ...prev]);
    api.createPair(newPair as unknown as Record<string, unknown>).catch((error) => {
      console.error('[App] Failed to create pair via API.', error);
    });
  };

  const handleDeletePair = async (pairId: string) => {
    setPairs((prev) => prev.filter((p) => p.id !== pairId));
    api.deletePair(pairId).catch((error) => {
      console.error('[App] Failed to delete pair via API.', error);
    });
  };

  const handleUpdateMatchCourt = async (matchId: string, courtId: string, courtName: string) => {
    setMatches((prev) =>
      prev.map((m) => (m.id === matchId ? { ...m, courtId, courtName } : m))
    );
    alert(`Pista reasignada a: ${courtName}`);
    await api.updateMatchCourt(matchId, courtId, courtName);
  };

  const handleCreateUser = async (newUser: User) => {
    setPlayers((prev) => [...prev, newUser]);
    setUser((prev) => ({ ...newUser, currentPairId: prev.currentPairId, partnerName: prev.partnerName }));
    const newAudit: AuditLog = {
      id: 'audit_' + Date.now(),
      adminName: user.name + ' ' + user.surname,
      adminEmail: user.email,
      action: 'CREACION_USUARIO',
      target: newUser.name + ' ' + newUser.surname,
      details: `Usuario ${newUser.username} (${newUser.email}) registrado como ${newUser.role}`,
      timestamp: new Date().toLocaleString(),
    };
    setAuditLogs((prev) => [newAudit, ...prev]);
    api.createUser(newUser as unknown as Record<string, unknown>).catch((error) => {
      console.error('[App] Failed to create user via API.', error);
    });
  };

  const handleDeleteUser = async (userId: string) => {
    setPlayers((prev) => prev.filter((p) => p.id !== userId));
    if (user.id === userId) {
      const fallback = players.find((p) => p.id !== userId) || players[0];
      if (fallback) setUser(fallback);
    }
    const newAudit: AuditLog = {
      id: 'audit_' + Date.now(),
      adminName: user.name + ' ' + user.surname,
      adminEmail: user.email,
      action: 'ELIMINACION_USUARIO',
      target: userId,
      details: `Usuario eliminado del sistema`,
      timestamp: new Date().toLocaleString(),
    };
    setAuditLogs((prev) => [newAudit, ...prev]);
    api.deleteUser(userId).catch((error) => {
      console.error('[App] Failed to delete user via API.', error);
    });
  };

  const handleDeleteTournament = async (tourId: string) => {
    setTournaments((prev) => prev.filter((t) => t.id !== tourId));
    setMatches((prev) => prev.filter((m) => m.tournamentId !== tourId));
    const newAudit: AuditLog = {
      id: 'audit_' + Date.now(),
      adminName: user.name + ' ' + user.surname,
      adminEmail: user.email,
      action: 'ELIMINACION_TORNEO',
      target: tourId,
      details: `Torneo eliminado del sistema junto con sus partidos asociados`,
      timestamp: new Date().toLocaleString(),
    };
    setAuditLogs((prev) => [newAudit, ...prev]);
    api.deleteTournament(tourId).catch((error) => {
      console.error('[App] Failed to delete tournament via API.', error);
    });
  };

  return (
    <div className="min-h-screen bg-[#111317] text-[#e2e2e7] font-sans antialiased relative selection:bg-[#c3f400] selection:text-[#161e00]">
      {/* Fixed Top Bar */}
      <HeaderBar
        role={role}
        onToggleRole={handleToggleRole}
        notifications={notifications}
        onOpenNotifications={() => setShowNotificationsDrawer(true)}
        onOpenProfile={() => {
          setSelectedPlayer(user);
          setActiveTab('profile');
        }}
        onOpenMenu={() => setShowMenuDrawer(true)}
        activeLiveMatchCount={liveCount}
      />

      {/* Main View Router Content Area */}
      <main className="pt-[68px] pb-[88px] min-h-[calc(100vh-150px)]">
        {loading && (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <div className="w-8 h-8 border-2 border-[#c3f400] border-t-transparent rounded-full animate-spin" />
            <p className="font-mono-stats text-[12px] text-[#c4c9ac]">Conectando con el servidor...</p>
          </div>
        )}

        {!loading && usingFallback && (
          <div className="px-4 pt-3">
            <div className="bg-[#282a2e] border border-[#c3f400]/40 text-[#c3f400] text-[11px] font-mono-stats p-2.5 rounded-lg">
              Backend no disponible. Mostrando datos locales.
            </div>
          </div>
        )}

        {!loading && (
          <>
            {/* HOME DASHBOARD VIEW */}
            {activeTab === 'home' && (
              <div className="flex flex-col gap-6 px-4 pt-3 w-full">
                {/* Live Now Section */}
                <section className="flex flex-col gap-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-[#FF3B30] pulse-animation" />
                      <h2 className="font-headline font-bold text-[18px] text-white tracking-wide uppercase">
                        Live Now
                      </h2>
                    </div>
                    <span className="font-mono-stats text-[11px] text-[#c4c9ac]">
                      Padel Pro Arena
                    </span>
                  </div>

                  {/* Active Match Scorecard */}
                  {activeLiveMatch && (
                    <LiveMatchCard
                      match={activeLiveMatch}
                      onOpenMatch={(id) => setSelectedMatchId(id)}
                    />
                  )}
                </section>

                {/* Quick Actions Bento Grid */}
                <section className="grid grid-cols-2 gap-3">
                  {/* Primary Bento Action */}
                  <button
                    onClick={() => setSelectedMatchId(activeLiveMatch.id)}
                    className="col-span-2 bg-[#c3f400] text-[#161e00] rounded-xl p-4 flex items-center justify-between transition-transform active:scale-[0.98] shadow-lg border border-[#c3f400]/40 group"
                  >
                    <div className="flex flex-col items-start text-left">
                      <span className="font-headline font-extrabold text-[18px] leading-tight">
                        Iniciar Partido & Control por Gestos
                      </span>
                      <span className="font-mono-stats text-[11px] opacity-80 mt-1">
                        Marcador inteligente con cámara
                      </span>
                    </div>
                    <div className="w-10 h-10 rounded-full bg-[#161e00]/10 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                      <span className="material-symbols-outlined text-[24px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                        play_arrow
                      </span>
                    </div>
                  </button>

                  {/* Secondary Bento Actions */}
                  <button
                    onClick={() => setActiveTab('tourneys')}
                    className="bg-[#1e2023] rounded-xl p-4 flex flex-col items-start gap-3 border border-[#333539] hover:border-[#c3f400]/40 hover:bg-[#282a2e] transition-all active:scale-95 text-left shadow-md"
                  >
                    <span className="material-symbols-outlined text-[#c3f400] text-[28px]">search</span>
                    <span className="font-headline font-bold text-[15px] leading-tight text-white">
                      Buscar<br />Torneo
                    </span>
                  </button>

                  <button
                    onClick={() => {
                      setSelectedPlayer(user);
                      setActiveTab('profile');
                    }}
                    className="bg-[#1e2023] rounded-xl p-4 flex flex-col items-start gap-3 border border-[#333539] hover:border-[#c3f400]/40 hover:bg-[#282a2e] transition-all active:scale-95 text-left shadow-md"
                  >
                    <span className="material-symbols-outlined text-[#c3f400] text-[28px]">bar_chart</span>
                    <span className="font-headline font-bold text-[15px] leading-tight text-white">
                      Mis<br />Estadísticas
                    </span>
                  </button>
                </section>

                {/* My Next Match Card */}
                <section className="flex flex-col gap-3">
                  <h2 className="font-headline font-bold text-[16px] text-[#c4c9ac] uppercase tracking-wider pl-1">
                    Mi Próximo Partido
                  </h2>

                  <div
                    onClick={() => setSelectedMatchId('match_upcoming_02')}
                    className="bg-[#1e2023] rounded-xl p-4 flex items-center gap-4 border border-[#333539] relative overflow-hidden group hover:border-[#c3f400]/50 transition-all cursor-pointer shadow-lg"
                  >
                    {/* Calendar Date Block */}
                    <div className="w-14 h-14 rounded-xl bg-[#0c0e12] flex flex-col items-center justify-center border border-[#333539] flex-shrink-0">
                      <span className="font-mono-stats text-[10px] text-[#FF3B30] uppercase font-bold tracking-widest">
                        OCT
                      </span>
                      <span className="font-headline font-black text-[22px] leading-none text-white mt-0.5">
                        24
                      </span>
                    </div>

                    {/* Match Info */}
                    <div className="flex flex-col flex-1 gap-1 min-w-0">
                      <div className="flex items-center gap-1.5 text-[#c3f400]">
                        <span className="material-symbols-outlined text-[14px]">schedule</span>
                        <span className="font-mono-stats text-[12px] font-bold">18:30 - 20:00</span>
                      </div>
                      <div className="font-headline font-bold text-[15px] text-white truncate">
                        Cuartos de Final - Pro League
                      </div>
                      <div className="flex items-center gap-1.5 text-[#c4c9ac] text-[12px] font-mono-stats">
                        <span className="material-symbols-outlined text-[14px]">location_on</span>
                        <span className="truncate">Pista 2 • Club Central</span>
                      </div>
                    </div>

                    {/* Partner Avatar */}
                    <div className="flex flex-col items-center justify-center flex-shrink-0 gap-1 pl-2 border-l border-[#333539]">
                      <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-[#c3f400]/60">
                        <img
                          src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80"
                          alt="Partner"
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <span className="font-mono-stats text-[9px] text-[#c4c9ac]">Pareja</span>
                    </div>
                  </div>
                </section>
              </div>
            )}

            {/* TOURNAMENTS VIEW */}
            {activeTab === 'tourneys' && (
              <TournamentsView
                tournaments={tournaments}
                pairs={pairs}
                matches={matches}
                role={role}
                onCreateTournament={handleCreateTournament}
                onRegisterPair={handleRegisterPair}
                onDeleteTournament={handleDeleteTournament}
                onOpenMatch={(id) => {
                  setSelectedMatchId(id);
                  setActiveTab('matches');
                }}
              />
            )}

            {/* MATCHES VIEW */}
            {activeTab === 'matches' && (
              <div className="flex flex-col gap-4 pb-24 px-4 pt-3 w-full">
                <div className="border-b border-[#333539] pb-3">
                  <h2 className="font-headline font-black text-[22px] text-white tracking-tight flex items-center gap-2">
                    <span className="material-symbols-outlined text-[#c3f400] text-[28px]">sports_tennis</span>
                    Partidos & Marcador en Vivo
                  </h2>
                  <p className="text-[12px] text-[#c4c9ac] font-mono-stats">
                    Selecciona un partido para abrir la mesa de control o activar gestos de cámara
                  </p>
                </div>

                <div className="flex flex-col gap-4">
                  {matches.map((m) => (
                    <LiveMatchCard
                      key={m.id}
                      match={m}
                      onOpenMatch={(id) => setSelectedMatchId(id)}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* RANKING VIEW */}
            {activeTab === 'ranking' && (
              <RankingsView
                players={players}
                onSelectPlayer={(p) => {
                  setSelectedPlayer(p);
                  setActiveTab('profile');
                }}
              />
            )}

            {/* PAIRS VIEW */}
            {activeTab === 'pairs' && (
              <PairsView
                pairs={pairs}
                players={players}
                role={role}
                onCreatePair={handleCreatePair}
                onDissolvePair={handleDeletePair}
              />
            )}

            {/* PROFILE VIEW */}
            {activeTab === 'profile' && (
              <PlayerProfileView
                player={selectedPlayer || user}
                onUpdateProfile={async (updated) => {
                  setUser(updated);
                  setPlayers((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
                  await api.updateUser(updated.id, updated as unknown as Record<string, unknown>);
                }}
              />
            )}

            {/* ADMIN DASHBOARD VIEW */}
            {activeTab === 'admin' && (
              <AdminDashboardView
                players={players}
                tournaments={tournaments}
                matches={matches}
                courts={courts}
                auditLogs={auditLogs}
                onUpdateMatchCourt={handleUpdateMatchCourt}
                onRunUnitTests={() => setShowUnitTestModal(true)}
                onCreateUser={handleCreateUser}
                onDeleteUser={handleDeleteUser}
              />
            )}
          </>
        )}
      </main>

      {/* FULLSCREEN MATCH CONTROLLER & CAMERA GESTURES OVERLAY */}
      {selectedMatchId && (
        <MatchController
          match={matches.find((m) => m.id === selectedMatchId) || matches[0]}
          onUpdateMatch={handleUpdateMatch}
          onClose={() => setSelectedMatchId(null)}
        />
      )}

      {/* UNIT TEST INSPECTOR MODAL */}
      {showUnitTestModal && (
        <RuleEngineTesterModal onClose={() => setShowUnitTestModal(false)} />
      )}

      {/* NOTIFICATIONS DRAWER */}
      {showNotificationsDrawer && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex justify-end">
          <div className="bg-[#1e2023] w-full max-w-sm h-full p-4 border-l border-[#333539] flex flex-col gap-4 shadow-2xl overflow-y-auto">
            <div className="flex items-center justify-between border-b border-[#333539] pb-3">
              <h3 className="font-headline font-bold text-[18px] text-white flex items-center gap-2">
                <span className="material-symbols-outlined text-[#c3f400]">notifications</span>
                Notificaciones (FCM)
              </h3>
              <button
                onClick={() => setShowNotificationsDrawer(false)}
                className="text-[#c4c9ac] hover:text-white"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <div className="flex flex-col gap-2.5">
              {notifications.map((n) => (
                <div
                  key={n.id}
                  className="bg-[#282a2e] p-3 rounded-xl border border-[#333539] flex flex-col gap-1 text-[12px] font-mono-stats"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">{n.title}</span>
                    <span className="text-[10px] text-[#8e9379]">{n.timestamp}</span>
                  </div>
                  <p className="text-[#c4c9ac] text-[11px] leading-relaxed">{n.body}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* MAIN MENU DRAWER */}
      {showMenuDrawer && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex justify-start">
          <div className="bg-[#1e2023] w-full max-w-xs h-full p-5 border-r border-[#333539] flex flex-col gap-5 shadow-2xl overflow-y-auto">
            <div className="flex items-center justify-between border-b border-[#333539] pb-3">
              <h3 className="font-headline font-black text-[20px] text-[#c3f400]">
                PADEL PRO MENU
              </h3>
              <button onClick={() => setShowMenuDrawer(false)} className="text-[#c4c9ac]">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <div className="flex flex-col gap-2 font-mono-stats text-[13px]">
              <button
                onClick={() => {
                  setActiveTab('home');
                  setShowMenuDrawer(false);
                }}
                className="p-2.5 rounded-lg hover:bg-[#282a2e] text-left text-white flex items-center gap-3"
              >
                <span className="material-symbols-outlined text-[#c3f400]">home</span> Inicio
              </button>
              <button
                onClick={() => {
                  setActiveTab('tourneys');
                  setShowMenuDrawer(false);
                }}
                className="p-2.5 rounded-lg hover:bg-[#282a2e] text-left text-white flex items-center gap-3"
              >
                <span className="material-symbols-outlined text-[#c3f400]">emoji_events</span> Torneos
              </button>
              <button
                onClick={() => {
                  setActiveTab('matches');
                  setShowMenuDrawer(false);
                }}
                className="p-2.5 rounded-lg hover:bg-[#282a2e] text-left text-white flex items-center gap-3"
              >
                <span className="material-symbols-outlined text-[#c3f400]">sports_tennis</span> Partidos
              </button>
              <button
                onClick={() => {
                  setActiveTab('ranking');
                  setShowMenuDrawer(false);
                }}
                className="p-2.5 rounded-lg hover:bg-[#282a2e] text-left text-white flex items-center gap-3"
              >
                <span className="material-symbols-outlined text-[#c3f400]">leaderboard</span> Ranking
              </button>
              <button
                onClick={() => {
                  setActiveTab('pairs');
                  setShowMenuDrawer(false);
                }}
                className="p-2.5 rounded-lg hover:bg-[#282a2e] text-left text-white flex items-center gap-3"
              >
                <span className="material-symbols-outlined text-[#c3f400]">groups</span> Parejas
              </button>
              <button
                onClick={() => {
                  setShowUnitTestModal(true);
                  setShowMenuDrawer(false);
                }}
                className="p-2.5 rounded-lg hover:bg-[#282a2e] text-left text-white flex items-center gap-3"
              >
                <span className="material-symbols-outlined text-[#c3f400]">bug_report</span> Pruebas Scoring
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Fixed Bottom Nav Bar */}
      <BottomNav
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        role={role}
        isMatchLiveNow={liveCount > 0}
      />
    </div>
  );
}
