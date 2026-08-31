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
import { LoginScreen } from './components/LoginScreen';
import { api, API_BASE_NORMALIZED, setAuthToken } from './api';
import { createInitialGameScore } from './domain/scoringEngine';

const EMPTY_STATS = {
  pointsWon: 0, winners: 0, smashes: 0, smashesWon: 0, voleasWon: 0,
  bandejas: 0, viboras: 0, remates: 0, netPointsWon: 0, touches: 0,
  shots: 0, serves: 0, firstServes: 0, secondServes: 0, aces: 0,
  doubleFaults: 0, breakPoints: 0, breakPointsWon: 0, recoveries: 0,
  globos: 0, devoluciones: 0, pointsSaved: 0, unforcedErrors: 0,
  distanceKm: 0, timePlayedMin: 0, avgSpeedKmh: 0, movesCount: 0,
  matchesPlayed: 0, matchesWon: 0, matchesLost: 0, setsWon: 0, setsLost: 0,
  gamesWon: 0, gamesLost: 0,
};

export default function App() {
  // Global Application State
  const [role, setRole] = useState<UserRole>('ADMIN');
  const [activeTab, setActiveTab] = useState<ActiveTab>('home');
  const [loading, setLoading] = useState<boolean>(true);
  const [session, setSession] = useState<{ user: User; token: string } | null>(null);

  const [user, setUser] = useState<User | null>(null);
  const [players, setPlayers] = useState<User[]>([]);
  const [pairs, setPairs] = useState<Pair[]>([]);
  const [tournaments, setTournaments] = useState<Tournament[]>([]);
  const [matches, setMatches] = useState<Match[]>([]);
  const [courts, setCourts] = useState<Court[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);

  // Overlay Modals & Drawers
  const [selectedMatchId, setSelectedMatchId] = useState<string | null>(null);
  const [selectedPlayer, setSelectedPlayer] = useState<User | null>(null);
  const [showNotificationsDrawer, setShowNotificationsDrawer] = useState<boolean>(false);
  const [showMenuDrawer, setShowMenuDrawer] = useState<boolean>(false);
  const [showUnitTestModal, setShowUnitTestModal] = useState<boolean>(false);

  const normalizeTournamentStatus = (status: string) => {
    switch (status) {
      case 'IN_PROGRESS':
        return 'ACTIVE';
      case 'OPEN':
        return 'REGISTRATION';
      case 'DRAFT':
        return 'UPCOMING';
      default:
        return status;
    }
  };

  const normalizeMatchStatus = (status: string) => {
    switch (status) {
      case 'IN_PROGRESS':
        return 'LIVE';
      case 'SCHEDULED':
        return 'UPCOMING';
      default:
        return status;
    }
  };

  // Load initial data from backend
  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      setLoading(true);
      try {
        const token = sessionStorage.getItem('padel_pro_token');
        let currentUser: User | null = null;

        if (token) {
          try {
            setAuthToken(token);
            currentUser = await api.authMe(token);
            if (!cancelled && currentUser) {
              setSession({ user: currentUser, token });
              setUser(currentUser);
              setRole(currentUser.role);
            }
          } catch {
            setAuthToken(null);
            sessionStorage.removeItem('padel_pro_token');
          }
        }

        let backendAvailable = false;
        try {
          const health = await api.health();
          backendAvailable = !!health && health.status === 'ok';
        } catch {
          backendAvailable = false;
        }

        if (!backendAvailable) {
          return;
        }

        if (role === 'ADMIN') {
          try {
            await api.adminMigrate();
          } catch {
            // non-blocking
          }
        }

        const [usersResult, pairsData, tournamentsData, matchesData, courtsData, auditLogsData, notificationsData] = await Promise.allSettled([
          api.getUsers(),
          api.getPairs(),
          api.getTournaments(),
          api.getMatches(),
          api.getCourts(),
          api.getAuditLogs(),
          api.getNotifications(),
        ]);

        if (cancelled) return;

        const extract = (item: PromiseSettledResult<any>): any =>
          item.status === 'fulfilled' ? item.value : undefined;

        const users = extract(usersResult);
        const pairs = extract(pairsData);
        const tournaments = extract(tournamentsData);
        const matches = extract(matchesData);
        const courts = extract(courtsData);
        const auditLogs = extract(auditLogsData);
        const notifications = extract(notificationsData);

        if (users && users.length > 0) {
          const normalizedUsers = users.map((u: any) => ({
            ...u,
            stats: u.stats && typeof u.stats === 'object' ? u.stats : EMPTY_STATS,
            avatar: u.avatar || '',
            level: u.level || 'Intermedio',
            position: u.position || 'Drive (Derecha)',
            dominantHand: u.dominantHand || 'Derecha',
          }));
          setPlayers(normalizedUsers as User[]);
          if (!currentUser) {
            const fallbackUser = await api.getCurrentUser();
            if (fallbackUser) {
              const typedFallback = fallbackUser as User;
              setUser({
                ...typedFallback,
                stats: typedFallback.stats && typeof typedFallback.stats === 'object' ? typedFallback.stats : EMPTY_STATS,
                avatar: typedFallback.avatar || '',
                level: typedFallback.level || 'Intermedio',
                position: typedFallback.position || 'Drive (Derecha)',
                dominantHand: typedFallback.dominantHand || 'Derecha',
              });
            }
          }
        }
        if (pairs) {
          // Backend now returns enriched pairs with player1Name, player2Name etc.
          // Normalize to ensure consistent format for frontend
          const normalizedPairs = (pairs as any[]).map((p) => ({
            ...p,
            player1Id: p.player1Id || p.player1_id,
            player2Id: p.player2Id || p.player2_id,
            player1Name: p.player1Name || p.player1_name || 'Jugador 1',
            player2Name: p.player2Name || p.player2_name || 'Jugador 2',
            player1Avatar: p.player1Avatar || p.player1_avatar || '',
            player2Avatar: p.player2Avatar || p.player2_avatar || '',
            tournamentsDisputed: p.tournamentsDisputed ?? p.tournaments_disputed ?? 0,
            titlesWon: p.titlesWon ?? p.titles_won ?? 0,
            createdAt: p.createdAt || p.created_at || new Date().toISOString(),
          }));
          setPairs(normalizedPairs as Pair[]);
        }
        if (tournaments) {
          const normalizedTournaments = tournaments.map((t: any) => ({
            ...t,
            status: normalizeTournamentStatus(t.status),
            startDate: t.start_date || t.startDate || '',
            endDate: t.end_date || t.endDate || '',
          }));
          setTournaments(normalizedTournaments as Tournament[]);
        }
        if (matches) {
          const normalizedMatches = (matches as Match[]).map((m) => ({
            ...m,
            status: normalizeMatchStatus(m.status),
            currentGame: m.currentGame && typeof m.currentGame === 'object' && Object.keys(m.currentGame).length > 0
              ? m.currentGame
              : createInitialGameScore('A'),
            playerA1Name: m.playerA1Name || 'Jugador 1',
            playerA2Name: m.playerA2Name || 'Jugador 2',
            playerB1Name: m.playerB1Name || 'Jugador 3',
            playerB2Name: m.playerB2Name || 'Jugador 4',
            playerA1Avatar: m.playerA1Avatar || '',
            playerA2Avatar: m.playerA2Avatar || '',
            playerB1Avatar: m.playerB1Avatar || '',
            playerB2Avatar: m.playerB2Avatar || '',
            pairAName: m.pairAName || 'Pareja A',
            pairBName: m.pairBName || 'Pareja B',
            courtName: m.courtName || 'Pista por definir',
            roundName: m.roundName || 'Eliminatoria',
          }));
          setMatches(normalizedMatches);
        }
        if (courts) setCourts(courts as Court[]);
        if (auditLogs) setAuditLogs(auditLogs as AuditLog[]);
        if (notifications) setNotifications(notifications as NotificationItem[]);
      } catch (error) {
        console.warn('[App] Backend unavailable, using local fallback data.', error);
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
  const nextUpcomingMatch = matches.find((m) => m.status === 'UPCOMING');

  // Handlers
  const handleToggleRole = () => {
    setRole((prev) => (prev === 'ADMIN' ? 'PLAYER' : 'ADMIN'));
  };

  const handleLogin = async (userData: any, token: string) => {
    const typedUser = userData as User;
    sessionStorage.setItem('padel_pro_token', token);
    setAuthToken(token);
    setSession({ user: typedUser, token });
    setUser(typedUser);
    setRole(typedUser.role);

    try {
      const users = await api.getUsers();
      if (users && users.length > 0) {
        setPlayers(users as User[]);
      }
    } catch (e) {
      console.warn('[App] Failed to reload users after login', e);
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('padel_pro_token');
    setAuthToken(null);
    setSession(null);
    setUser(null);
    setRole('ADMIN');
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
        winner_team: isWinnerA ? 'A' : 'B',
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
      }

      const [usersAfter, pairsAfter, tournamentsAfter, matchesAfter] = await Promise.all([
        api.getUsers(),
        api.getPairs(),
        api.getTournaments(),
        api.getMatches(),
      ]);

      setPlayers(usersAfter as User[]);
      setPairs(pairsAfter as Pair[]);
      setTournaments(tournamentsAfter as Tournament[]);
      setMatches((matchesAfter as Match[]).map((m) => ({
        ...m,
        currentGame: m.currentGame || createInitialGameScore('A'),
      })));

      const updatedUser = (usersAfter as User[]).find((u) => u.id === user.id);
      if (updatedUser) {
        setUser(updatedUser);
        setSelectedPlayer((prev) => (prev && prev.id === updatedUser.id ? updatedUser : prev));
      }

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

  const handleRegisterPairForTournament = async (tournamentId: string, pairId: string, courtId: string, dateTime: string) => {
    setTournaments((prev) =>
      prev.map((t) => {
        if (t.id !== tournamentId) return t;
        const registeredPairIds = t.registeredPairIds.includes(pairId) ? t.registeredPairIds : [...t.registeredPairIds, pairId];
        const courtIds = courtId && !t.courtIds.includes(courtId) ? [...t.courtIds, courtId] : t.courtIds;
        return { ...t, registeredPairIds, courtIds };
      })
    );
    await api.registerPairForTournament(tournamentId, pairId, courtId, dateTime);
  };

  const handleCreatePair = async (newPair: Pair) => {
    setPairs((prev) => [newPair, ...prev]);
    try {
      await api.createPair(newPair as unknown as Record<string, unknown>);
      const updated = await api.getPairs();
      if (updated) setPairs(updated as Pair[]);
    } catch (error) {
      console.error('[App] Failed to create pair via API.', error);
      setPairs((prev) => prev.filter((p) => p.id !== newPair.id));
      alert('No se pudo guardar la pareja en el servidor.');
    }
  };

  const handleDeletePair = async (pairId: string) => {
    const previous = pairs;
    setPairs((prev) => prev.filter((p) => p.id !== pairId));
    try {
      await api.deletePair(pairId);
      const updated = await api.getPairs();
      if (updated) setPairs(updated as Pair[]);
    } catch (error) {
      console.error('[App] Failed to delete pair via API.', error);
      setPairs(previous);
      alert('No se pudo eliminar la pareja en el servidor.');
    }
  };

  const handleUpdateMatchCourt = async (matchId: string, courtId: string, courtName: string) => {
    setMatches((prev) =>
      prev.map((m) => (m.id === matchId ? { ...m, courtId, courtName } : m))
    );
    alert(`Pista reasignada a: ${courtName}`);
    await api.updateMatchCourt(matchId, courtId, courtName);
  };

  const handleUpdateMatchDateTime = async (matchId: string, dateTime: string) => {
    const fullMatch = matches.find((m) => m.id === matchId);
    if (!fullMatch) return;
    const updatedMatch = { ...fullMatch, dateTime };
    setMatches((prev) =>
      prev.map((m) => (m.id === matchId ? updatedMatch : m))
    );
    alert('Fecha y hora del partido actualizada');
    await api.updateMatch(matchId, updatedMatch as unknown as Record<string, unknown>);
  };

  const handleCreateMatch = async (newMatch: Match) => {
    setMatches((prev) => [newMatch, ...prev]);
    try {
      await api.createMatch(newMatch as unknown as Record<string, unknown>);
      alert('Partido creado correctamente');
    } catch (error) {
      console.error('[App] Failed to create match via API.', error);
      setMatches((prev) => prev.filter((m) => m.id !== newMatch.id));
      alert('No se pudo crear el partido en el servidor.');
    }
  };

  const handleDeleteMatch = async (matchId: string) => {
    setMatches((prev) => prev.filter((m) => m.id !== matchId));
    try {
      await api.deleteMatch(matchId);
      alert('Partido eliminado correctamente');
    } catch (error) {
      console.error('[App] Failed to delete match via API.', error);
      alert('No se pudo eliminar el partido en el servidor.');
    }
  };

  const handleUpdateTournament = async (tournamentId: string, updates: Record<string, unknown>) => {
    setTournaments((prev) =>
      prev.map((t) => (t.id === tournamentId ? { ...t, ...updates } : t))
    );
    await api.updateTournament(tournamentId, updates);
  };

  const handleRegisterUserForTournament = async (tournamentId: string, userId: string) => {
    setTournaments((prev) =>
      prev.map((t) => {
        if (t.id === tournamentId && !t.registeredUserIds.includes(userId)) {
          return { ...t, registeredUserIds: [...t.registeredUserIds, userId] };
        }
        return t;
      })
    );
    alert('¡Jugador inscrito correctamente en el torneo!');
    await api.registerUser(tournamentId, userId);
  };

  const handleCreateUser = async (newUser: User) => {
    setPlayers((prev) => [...prev, newUser]);
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
    try {
      await api.createUser(newUser as unknown as Record<string, unknown>);
      const users = await api.getUsers();
      if (users && users.length > 0) {
        setPlayers(users as User[]);
      }
    } catch (error) {
      console.error('[App] Failed to create user via API.', error);
    }
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
      {loading && (
        <div className="flex items-center justify-center min-h-screen">
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <div className="w-8 h-8 border-2 border-[#c3f400] border-t-transparent rounded-full animate-spin" />
            <p className="font-mono-stats text-[12px] text-[#c4c9ac]">Conectando con el servidor...</p>
          </div>
        </div>
      )}

      {!loading && !session && (
        <LoginScreen onLogin={handleLogin} apiBase={API_BASE_NORMALIZED} />
      )}

      {session && (
        <>
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
                  {nextUpcomingMatch && (
                    <section className="flex flex-col gap-3">
                      <h2 className="font-headline font-bold text-[16px] text-[#c4c9ac] uppercase tracking-wider pl-1">
                        Próximos Partidos
                      </h2>

                      <div className="flex flex-col gap-2">
                        {matches
                          .filter((m) => m.status === 'UPCOMING')
                          .sort((a, b) => new Date(a.dateTime).getTime() - new Date(b.dateTime).getTime())
                          .slice(0, 3)
                          .map((m) => (
                            <div
                              key={m.id}
                              onClick={() => setSelectedMatchId(m.id)}
                              className="bg-[#1e2023] rounded-xl p-4 flex items-center gap-4 border border-[#333539] relative overflow-hidden group hover:border-[#c3f400]/50 transition-all cursor-pointer shadow-lg"
                            >
                              {/* Calendar Date Block */}
                              <div className="w-14 h-14 rounded-xl bg-[#0c0e12] flex flex-col items-center justify-center border border-[#333539] flex-shrink-0">
                                {(() => {
                                  const d = new Date(m.dateTime || '');
                                  const month = isNaN(d.getTime()) ? '' : d.toLocaleString('es-ES', { month: 'short' }).toUpperCase();
                                  const day = isNaN(d.getTime()) ? '' : d.getDate();
                                  return (
                                    <>
                                      <span className="font-mono-stats text-[10px] text-[#FF3B30] uppercase font-bold tracking-widest">
                                        {month}
                                      </span>
                                      <span className="font-headline font-black text-[22px] leading-none text-white mt-0.5">
                                        {day}
                                      </span>
                                    </>
                                  );
                                })()}
                              </div>

                              {/* Match Info */}
                              <div className="flex flex-col flex-1 gap-1 min-w-0">
                                <div className="flex items-center gap-1.5 text-[#c3f400]">
                                  <span className="material-symbols-outlined text-[14px]">schedule</span>
                                  <span className="font-mono-stats text-[12px] font-bold">
                                    {m.dateTime ? m.dateTime.split(' ').pop() : ''}
                                  </span>
                                </div>
                                <div className="font-headline font-bold text-[15px] text-white truncate">
                                  {m.pairAName} VS {m.pairBName}
                                </div>
                                <div className="flex items-center gap-1.5 text-[#c4c9ac] text-[12px] font-mono-stats">
                                  <span className="material-symbols-outlined text-[14px]">location_on</span>
                                  <span className="truncate">{m.courtName || 'Pista por definir'}</span>
                                </div>
                              </div>
                            </div>
                          ))}
                      </div>
                    </section>
                  )}
                </div>
              )}

              {/* TOURNAMENTS VIEW */}
              {activeTab === 'tourneys' && (
                <TournamentsView
                  tournaments={tournaments}
                  pairs={pairs}
                  courts={courts}
                  matches={matches}
                  role={role}
                  onCreateTournament={handleCreateTournament}
                  onRegisterPair={handleRegisterPairForTournament}
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
                    if (updated.id) {
                      await api.updateUser(updated.id, updated as unknown as Record<string, unknown>);
                    }
                  }}
                />
              )}

              {/* ADMIN DASHBOARD VIEW */}
              {activeTab === 'admin' && (
                <AdminDashboardView
                  players={players}
                  pairs={pairs}
                  tournaments={tournaments}
                  matches={matches}
                  courts={courts}
                  auditLogs={auditLogs}
                  role={role}
                  onUpdateMatchCourt={handleUpdateMatchCourt}
                  onUpdateMatchDateTime={handleUpdateMatchDateTime}
                  onDeleteMatch={handleDeleteMatch}
                  onUpdateTournament={handleUpdateTournament}
                  onRegisterUserForTournament={handleRegisterUserForTournament}
                  onCreateMatch={handleCreateMatch}
                  onRunUnitTests={() => setShowUnitTestModal(true)}
                  onCreateUser={handleCreateUser}
                  onDeleteUser={handleDeleteUser}
                />
              )}
            </>
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
                  {session && (
                    <button
                      onClick={() => {
                        handleLogout();
                        setShowMenuDrawer(false);
                      }}
                      className="p-2.5 rounded-lg hover:bg-[#2e1d1d] text-left text-[#ffb4ab] flex items-center gap-3"
                    >
                      <span className="material-symbols-outlined text-[#FF3B30]">logout</span> Cerrar Sesión
                    </button>
                  )}
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
        </>
      )}
    </div>
  );
}
