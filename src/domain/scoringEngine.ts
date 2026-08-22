import { Match, MatchEvent, SetScore, GameScore, PadelPointScore, MatchEventType } from '../types';

const POINT_SEQUENCE: PadelPointScore[] = ['0', '15', '30', '40'];

export function createInitialGameScore(serverTeam: 'A' | 'B' = 'A'): GameScore {
  return {
    teamAPoints: '0',
    teamBPoints: '0',
    serverTeam,
    isDeuce: false,
  };
}

export function createInitialSetScore(): SetScore {
  return {
    teamAGames: 0,
    teamBGames: 0,
    isTieBreak: false,
    tieBreakPoints: { teamA: 0, teamB: 0 },
  };
}

/**
 * Award a point to Team A or Team B, applying official padel scoring state machine.
 */
export function awardPoint(
  currentMatch: Match,
  team: 'A' | 'B',
  eventType: MatchEventType = 'POINT',
  playerId?: string,
  playerName?: string
): { updatedMatch: Match; event: MatchEvent } {
  if (currentMatch.status === 'FINISHED') {
    throw new Error('El partido ya ha finalizado.');
  }

  // Deep clone match state
  const match: Match = JSON.parse(JSON.stringify(currentMatch));
  const otherTeam: 'A' | 'B' = team === 'A' ? 'B' : 'A';

  if (!match.currentGame) {
    match.currentGame = createInitialGameScore('A');
  }

  let currentSet = match.sets[match.currentSetIndex];
  if (!currentSet) {
    currentSet = createInitialSetScore();
    match.sets[match.currentSetIndex] = currentSet;
  }

  let gameWonBy: 'A' | 'B' | null = null;

  // Handle Tie-break mode if 6-6
  if (currentSet.isTieBreak) {
    if (!currentSet.tieBreakPoints) {
      currentSet.tieBreakPoints = { teamA: 0, teamB: 0 };
    }
    
    if (team === 'A') {
      currentSet.tieBreakPoints.teamA++;
    } else {
      currentSet.tieBreakPoints.teamB++;
    }

    const ptsA = currentSet.tieBreakPoints.teamA;
    const ptsB = currentSet.tieBreakPoints.teamB;

    // Tie-break win condition: >= 7 points and lead by >= 2
    if (ptsA >= 7 && ptsA - ptsB >= 2) {
      gameWonBy = 'A';
    } else if (ptsB >= 7 && ptsB - ptsA >= 2) {
      gameWonBy = 'B';
    }
  } else {
    // Normal game scoring
    const ptsTeamKey = team === 'A' ? 'teamAPoints' : 'teamBPoints';
    const ptsOtherKey = team === 'A' ? 'teamBPoints' : 'teamAPoints';

    const currentTeamScore = match.currentGame[ptsTeamKey];
    const currentOtherScore = match.currentGame[ptsOtherKey];

    if (match.goldenPoint && currentTeamScore === '40' && currentOtherScore === '40') {
      // Golden point rules: Whoever wins this point wins the game immediately!
      gameWonBy = team;
    } else if (currentTeamScore === '40' && currentOtherScore === '40') {
      // Advantage rule
      match.currentGame[ptsTeamKey] = 'AD';
      match.currentGame.isDeuce = false;
    } else if (currentTeamScore === 'AD') {
      // Winning point from Advantage
      gameWonBy = team;
    } else if (currentOtherScore === 'AD') {
      // Opponent had advantage, back to Deuce (40-40)
      match.currentGame[ptsOtherKey] = '40';
      match.currentGame.isDeuce = true;
    } else if (currentTeamScore === '40') {
      // Win game from 40 if opponent is not 40 or AD
      if (currentOtherScore !== '40') {
        gameWonBy = team;
      }
    } else {
      // Simple progression: 0 -> 15 -> 30 -> 40
      const currentIndex = POINT_SEQUENCE.indexOf(currentTeamScore);
      if (currentIndex >= 0 && currentIndex < POINT_SEQUENCE.length - 1) {
        match.currentGame[ptsTeamKey] = POINT_SEQUENCE[currentIndex + 1];
      }
      
      if (match.currentGame.teamAPoints === '40' && match.currentGame.teamBPoints === '40') {
        match.currentGame.isDeuce = true;
      }
    }
  }

  // Process game win if gameWonBy is set
  if (gameWonBy) {
    if (gameWonBy === 'A') {
      currentSet.teamAGames++;
    } else {
      currentSet.teamBGames++;
    }

    // Reset game score
    const nextServer = match.currentGame.serverTeam === 'A' ? 'B' : 'A';
    match.currentGame = createInitialGameScore(nextServer);

    // Check if set is won
    const gamesA = currentSet.teamAGames;
    const gamesB = currentSet.teamBGames;

    let setWonBy: 'A' | 'B' | null = null;

    if (currentSet.isTieBreak) {
      setWonBy = gamesA > gamesB ? 'A' : 'B';
    } else {
      if (gamesA >= 6 && gamesA - gamesB >= 2) {
        setWonBy = 'A';
      } else if (gamesB >= 6 && gamesB - gamesA >= 2) {
        setWonBy = 'B';
      } else if (gamesA === 6 && gamesB === 6) {
        currentSet.isTieBreak = true;
        currentSet.tieBreakPoints = { teamA: 0, teamB: 0 };
      }
    }

    if (setWonBy) {
      currentSet.winner = setWonBy;
      
      // Count total sets won
      const setsWonA = match.sets.filter((s) => s.winner === 'A').length;
      const setsWonB = match.sets.filter((s) => s.winner === 'B').length;

      if (setsWonA >= match.setsToWin) {
        match.status = 'FINISHED';
        match.winnerPairId = match.pairAId;
      } else if (setsWonB >= match.setsToWin) {
        match.status = 'FINISHED';
        match.winnerPairId = match.pairBId;
      } else {
        // Move to next set
        match.currentSetIndex++;
        match.sets[match.currentSetIndex] = createInitialSetScore();
      }
    }
  }

  // Format current score description for the snapshot
  const scoreDesc = formatMatchSnapshot(match);

  const event: MatchEvent = {
    id: 'evt_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5),
    matchId: match.id,
    setNumber: match.currentSetIndex + 1,
    gameNumber: currentSet.teamAGames + currentSet.teamBGames + 1,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
    winningPairId: team,
    playerId,
    playerName,
    eventType,
    description: `${team === 'A' ? match.pairAName : match.pairBName} gana punto (${eventType})`,
    scoreSnapshot: scoreDesc,
  };

  return { updatedMatch: match, event };
}

/**
 * Format score overview string
 */
export function formatMatchSnapshot(match: Match): string {
  const setsStr = match.sets
    .map((s, idx) => {
      if (s.isTieBreak && s.tieBreakPoints) {
        return `S${idx + 1}: ${s.teamAGames}-${s.teamBGames} (${s.tieBreakPoints.teamA}-${s.tieBreakPoints.teamB})`;
      }
      return `S${idx + 1}: ${s.teamAGames}-${s.teamBGames}`;
    })
    .join(' | ');

  const currentPoints = match.sets[match.currentSetIndex]?.isTieBreak
    ? `TB: ${match.sets[match.currentSetIndex].tieBreakPoints?.teamA}-${match.sets[match.currentSetIndex].tieBreakPoints?.teamB}`
    : `Pts: ${match.currentGame?.teamAPoints ?? '-'}-${match.currentGame?.teamBPoints ?? '-'}`;

  return `${setsStr} [${currentPoints}]`;
}

/**
 * Recalculate match state from scratch by replaying events (for perfect Undo and integrity)
 */
export function replayEventsOnMatch(initialMatch: Match, events: MatchEvent[]): Match {
  // Start with fresh match clone reset to 0-0
  const cleanMatch: Match = JSON.parse(JSON.stringify(initialMatch));
  cleanMatch.status = 'LIVE';
  cleanMatch.currentSetIndex = 0;
  cleanMatch.sets = [createInitialSetScore()];
  cleanMatch.currentGame = createInitialGameScore('A');
  cleanMatch.winnerPairId = undefined;

  let current = cleanMatch;
  for (const ev of events) {
    if (ev.eventType === 'CORRECTION_UNDO') continue;
    const result = awardPoint(current, ev.winningPairId, ev.eventType, ev.playerId, ev.playerName);
    current = result.updatedMatch;
  }
  return current;
}

/**
 * Run Domain Scoring Unit Tests
 */
export function runPadelScoringUnitTests(): { passed: number; total: number; logs: string[] } {
  const logs: string[] = [];
  let passed = 0;
  let total = 0;

  function assert(condition: boolean, desc: string) {
    total++;
    if (condition) {
      passed++;
      logs.push(`✅ PASS: ${desc}`);
    } else {
      logs.push(`❌ FAIL: ${desc}`);
    }
  }

  try {
    const baseMatch: Match = {
      id: 'test_m1',
      courtName: 'Pista 1',
      dateTime: '2026-08-08 12:00',
      pairAId: 'pair_a',
      pairBId: 'pair_b',
      pairAName: 'Galán / Lebrón',
      pairBName: 'Coello / Tapia',
      playerA1Id: 'p1', playerA2Id: 'p2', playerB1Id: 'p3', playerB2Id: 'p4',
      playerA1Name: 'A1', playerA2Name: 'A2', playerB1Name: 'B1', playerB2Name: 'B2',
      playerA1Avatar: '', playerA2Avatar: '', playerB1Avatar: '', playerB2Avatar: '',
      status: 'LIVE',
      sets: [createInitialSetScore()],
      currentGame: createInitialGameScore('A'),
      currentSetIndex: 0,
      elapsedTimeSec: 100,
      goldenPoint: false,
      setsToWin: 2,
    };

    // Test 1: 0 -> 15 -> 30 -> 40 -> Game
    let m = JSON.parse(JSON.stringify(baseMatch));
    m = awardPoint(m, 'A').updatedMatch;
    assert(m.currentGame.teamAPoints === '15', '1. Point Team A -> 15-0');

    m = awardPoint(m, 'A').updatedMatch;
    assert(m.currentGame.teamAPoints === '30', '2. Point Team A -> 30-0');

    m = awardPoint(m, 'A').updatedMatch;
    assert(m.currentGame.teamAPoints === '40', '3. Point Team A -> 40-0');

    m = awardPoint(m, 'A').updatedMatch;
    assert(m.sets[0].teamAGames === 1 && m.currentGame.teamAPoints === '0', '4. Win Game 1 for Team A');

    // Test 2: Deuce and Advantage
    m = JSON.parse(JSON.stringify(baseMatch));
    // 40-40 setup
    for (let i = 0; i < 3; i++) m = awardPoint(m, 'A').updatedMatch;
    for (let i = 0; i < 3; i++) m = awardPoint(m, 'B').updatedMatch;
    assert(m.currentGame.teamAPoints === '40' && m.currentGame.teamBPoints === '40', '5. 40-40 Deuce reach');

    m = awardPoint(m, 'A').updatedMatch;
    assert(m.currentGame.teamAPoints === 'AD', '6. Point Team A at Deuce -> Advantage Team A');

    m = awardPoint(m, 'B').updatedMatch;
    assert(m.currentGame.teamAPoints === '40' && m.currentGame.teamBPoints === '40', '7. Opponent Point at AD -> Back to Deuce (40-40)');

    // Test 3: Golden Point rule
    let mGolden = JSON.parse(JSON.stringify(baseMatch));
    mGolden.goldenPoint = true;
    for (let i = 0; i < 3; i++) mGolden = awardPoint(mGolden, 'A').updatedMatch;
    for (let i = 0; i < 3; i++) mGolden = awardPoint(mGolden, 'B').updatedMatch;
    assert(mGolden.currentGame.teamAPoints === '40' && mGolden.currentGame.teamBPoints === '40', '8. Golden point at 40-40');
    
    mGolden = awardPoint(mGolden, 'A').updatedMatch;
    assert(mGolden.sets[0].teamAGames === 1, '9. Golden Point winner directly wins game');

    // Test 4: Tie-Break at 6-6
    let mTB = JSON.parse(JSON.stringify(baseMatch));
    mTB.sets[0].teamAGames = 6;
    mTB.sets[0].teamBGames = 6;
    mTB.sets[0].isTieBreak = true;
    mTB.sets[0].tieBreakPoints = { teamA: 6, teamB: 6 };

    mTB = awardPoint(mTB, 'A').updatedMatch;
    assert(mTB.sets[0].tieBreakPoints?.teamA === 7, '10. Tie-break point A -> 7-6');
    assert(mTB.sets[0].winner === undefined, '11. Need 2-point lead in Tie-break');

    mTB = awardPoint(mTB, 'A').updatedMatch;
    assert(mTB.sets[0].winner === 'A', '12. Win Tie-break 8-6 -> Set won by Team A');

  } catch (err: any) {
    logs.push(`⚠️ ERROR DURING TESTS: ${err.message}`);
  }

  return { passed, total, logs };
}
