import React, { useState, useEffect, useRef } from 'react';
import { Match, MatchEvent, GestureConfiguration, GestureType, RecognizedGestureState } from '../types';
import { awardPoint, replayEventsOnMatch, formatMatchSnapshot, getLastScoringTeam } from '../domain/scoringEngine';
import { GestureRecognizerEngine, DEFAULT_GESTURE_CONFIG, getGestureLabel } from '../camera/gestureAnalyzer';
import { audioFx } from '../utils/audioSynthesizer';
import { createVoiceCommandEngine, VoiceCommandEngine } from '../utils/voiceRecognizer';
import { getHandLandmarker } from '../camera/mediaPipeDetector';
import { detectHandFromPixels } from '../camera/pixelVisionAnalyzer';

interface MatchControllerProps {
  match: Match;
  onUpdateMatch: (updatedMatch: Match, newEvent?: MatchEvent) => void;
  onClose: () => void;
}

export const MatchController: React.FC<MatchControllerProps> = ({
  match,
  onUpdateMatch,
  onClose,
}) => {
  // Timer State (Timestamp based)
  const [timerRunning, setTimerRunning] = useState<boolean>(match.status === 'LIVE');
  const [elapsedSec, setElapsedSec] = useState<number>(match.elapsedTimeSec || 0);

  // Gesture Engine State
  const [gestureModeActive, setGestureModeActive] = useState<boolean>(false);
  const [gestureConfig, setGestureConfig] = useState<GestureConfiguration>(DEFAULT_GESTURE_CONFIG);
  const [recognizedState, setRecognizedState] = useState<RecognizedGestureState>({
    gesture: 'NONE',
    confidence: 0,
    progressPercent: 0,
    statusText: 'Cámara inactiva',
    handCount: 0,
  });
  const [showGestureSettings, setShowGestureSettings] = useState<boolean>(false);
  const [cameraPermissionGranted, setCameraPermissionGranted] = useState<boolean | null>(null);

  // Voice Control State
  const [voiceModeActive, setVoiceModeActive] = useState<boolean>(false);
  const [voiceError, setVoiceError] = useState<string | null>(null);
  const [voiceStatus, setVoiceStatus] = useState<string>('Inactivo');
  const voiceRecognizerRef = useRef<VoiceCommandEngine | null>(null);

  // Edit Mode State ("Modo de edición para corregir errores rápidamente")
  const [isEditMode, setIsEditMode] = useState<boolean>(false);

  // Match Event History
  const [events, setEvents] = useState<MatchEvent[]>([]);

  // Confirmation Modal State for Resetting Match
  const [showResetConfirmModal, setShowResetConfirmModal] = useState<boolean>(false);

  // WebCam and Engine Refs
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const gestureEngineRef = useRef<GestureRecognizerEngine>(new GestureRecognizerEngine(gestureConfig));
  const animFrameIdRef = useRef<number | null>(null);
  const cameraInitRef = useRef(false);

  // Synchronized Mutable Refs to prevent stale closures in RAF loop
  const matchRef = useRef<Match>(match);
  const eventsRef = useRef<MatchEvent[]>(events);
  const onUpdateMatchRef = useRef(onUpdateMatch);

  useEffect(() => {
    matchRef.current = match;
  }, [match]);

  useEffect(() => {
    eventsRef.current = events;
  }, [events]);

  useEffect(() => {
    onUpdateMatchRef.current = onUpdateMatch;
  }, [onUpdateMatch]);

  // Timestamp Timer Effect
  useEffect(() => {
    let interval: any = null;
    if (timerRunning && match.status !== 'FINISHED') {
      const startTime = Date.now() - elapsedSec * 1000;
      interval = setInterval(() => {
        const nowSec = Math.floor((Date.now() - startTime) / 1000);
        setElapsedSec(nowSec);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [timerRunning, match.status]);

  // Sync elapsed seconds back to match object periodically
  useEffect(() => {
    if (elapsedSec !== match.elapsedTimeSec) {
      const updated = { ...matchRef.current, elapsedTimeSec: elapsedSec };
      matchRef.current = updated;
      onUpdateMatchRef.current(updated);
    }
  }, [elapsedSec]);

  // Start / Stop Camera Stream
  useEffect(() => {
    let stream: MediaStream | null = null;

    async function initCamera() {
      if (!gestureModeActive) {
        if (animFrameIdRef.current) {
          cancelAnimationFrame(animFrameIdRef.current);
          animFrameIdRef.current = null;
        }
        return;
      }

      if (cameraInitRef.current) return;
      cameraInitRef.current = true;

      if (!window.isSecureContext) {
        console.error('Camera requires HTTPS or localhost. Current origin:', window.location.origin);
        setCameraPermissionGranted(false);
        cameraInitRef.current = false;
        return;
      }

      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error('getUserMedia is not supported in this browser/context');
        setCameraPermissionGranted(false);
        cameraInitRef.current = false;
        return;
      }

      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { width: { ideal: 640 }, height: { ideal: 480 } },
          audio: false,
        });
      } catch (err) {
        console.warn('Primary camera request failed, trying fallback:', err);
        try {
          stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false,
          });
        } catch (fallbackErr) {
          console.warn('Camera access denied or unavailable:', fallbackErr);
          setCameraPermissionGranted(false);
          cameraInitRef.current = false;
          return;
        }
      }

      setCameraPermissionGranted(true);
      if (videoRef.current && stream) {
        videoRef.current.srcObject = stream;
        try {
          await videoRef.current.play();
        } catch (playErr) {
          console.warn('Video play failed:', playErr);
        }
        startLandmarkDetectionLoop();
      }
      cameraInitRef.current = false;
    }

    initCamera();

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
      if (animFrameIdRef.current) {
        cancelAnimationFrame(animFrameIdRef.current);
        animFrameIdRef.current = null;
      }
      cameraInitRef.current = false;
    };
  }, [gestureModeActive]);

  // Voice Recognition Effect
  useEffect(() => {
    if (!voiceModeActive) {
      if (voiceRecognizerRef.current) {
        voiceRecognizerRef.current.stop();
        voiceRecognizerRef.current = null;
      }
      setVoiceStatus('Inactivo');
      setVoiceError(null);
      return;
    }

    const engine = createVoiceCommandEngine((cmd: any) => {
      switch (cmd) {
        case 'POINT_A':
          handleAwardPoint('A', 'POINT');
          setVoiceStatus('Punto Pareja A');
          break;
        case 'POINT_B':
          handleAwardPoint('B', 'POINT');
          setVoiceStatus('Punto Pareja B');
          break;
        case 'UNDO':
          handleUndoLastPoint();
          setVoiceStatus('Deshacer');
          break;
      }
    });

    voiceRecognizerRef.current = engine;
    setVoiceError(null);
    setVoiceStatus('Escuchando...');

    try {
      engine.start();
    } catch (err: any) {
      setVoiceError(err.message || 'No se pudo iniciar el reconocimiento de voz');
      setVoiceStatus('Error');
    }

    return () => {
      engine.stop();
      voiceRecognizerRef.current = null;
    };
  }, [voiceModeActive]);

  // Landmark analysis loop on video canvas
  const startLandmarkDetectionLoop = () => {
    let handLandmarker: any = null;
    getHandLandmarker().then((hl) => {
      handLandmarker = hl;
    });

    const processFrame = () => {
      if (videoRef.current && canvasRef.current && gestureModeActive) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        if (video.readyState === 4 && ctx) {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;

          // Draw webcam frame
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

          let detectedLandmarks: any = null;
          let confidence = 0.85;

          // Try MediaPipe detector if initialized
          if (handLandmarker) {
            try {
              const mpResult = handLandmarker.detectForVideo(video, performance.now());
              if (mpResult && mpResult.landmarks && mpResult.landmarks.length > 0) {
                detectedLandmarks = mpResult.landmarks[0];
                confidence = 0.92;
              }
            } catch (err) {
              // Ignore and fallback
            }
          } else {
            // Fallback to real-time pixel vision tracker ONLY if MediaPipe is not available
            const pixelRes = detectHandFromPixels(ctx, canvas.width, canvas.height);
            if (pixelRes && pixelRes.confidence >= 0.75) {
              detectedLandmarks = pixelRes.landmarks;
              confidence = pixelRes.confidence;
            }
          }

          if (detectedLandmarks) {
            const state = gestureEngineRef.current.analyzeHandLandmarks([detectedLandmarks], confidence);
            setRecognizedState(state);

            // Draw rich skeleton overlay + HUD on canvas
            drawHandSkeletonOnCanvas(ctx, detectedLandmarks, state.progressPercent, state.gesture);

            // Execute gesture action if 100% confirmed
            if (state.progressPercent === 100 && state.gesture !== 'NONE') {
              executeGestureAction(state.gesture);
            }
          } else {
            setRecognizedState({
              gesture: 'NONE',
              confidence: 0,
              progressPercent: 0,
              statusText: '✋ Muestra tu mano a la cámara (Palma, Puño, Pulgar)',
              handCount: 0,
            });
          }
        }
      }
      animFrameIdRef.current = requestAnimationFrame(processFrame);
    };

    const onVideoReady = () => {
      if (canvasRef.current && videoRef.current) {
        canvasRef.current.width = videoRef.current.videoWidth;
        canvasRef.current.height = videoRef.current.videoHeight;
      }
      animFrameIdRef.current = requestAnimationFrame(processFrame);
    };

    if (videoRef.current && videoRef.current.readyState >= 2) {
      onVideoReady();
    } else if (videoRef.current) {
      videoRef.current.addEventListener('loadedmetadata', onVideoReady, { once: true });
    }
  };

  // Execute recognized gesture action on padel scoring engine
  const executeGestureAction = (gesture: GestureType) => {
    audioFx.playGestureDetectedChime();

    switch (gesture) {
      case 'POINT_TEAM_A':
        handleAwardPoint('A', 'POINT');
        break;
      case 'POINT_TEAM_B':
        handleAwardPoint('B', 'POINT');
        break;
      case 'UNDO':
        handleUndoLastPoint();
        break;
      default:
        break;
    }
  };

  // Award Point Handler
  const handleAwardPoint = (team: 'A' | 'B', eventType = 'POINT', playerId?: string, playerName?: string) => {
    let activeMatch = matchRef.current;
    if (activeMatch.status === 'FINISHED') {
      activeMatch = { ...activeMatch, status: 'LIVE', winnerTeam: undefined };
    }

    try {
      const result = awardPoint(activeMatch, team, eventType as any, playerId, playerName);
      audioFx.playPointSound();

      if (result.updatedMatch.status === 'FINISHED') {
        setTimerRunning(false);
        audioFx.playWinnerTrumpet();
      }

      const newEvents = [result.event, ...eventsRef.current];
      setEvents(newEvents);
      eventsRef.current = newEvents;
      matchRef.current = result.updatedMatch;
      onUpdateMatchRef.current(result.updatedMatch, result.event);
    } catch (err: any) {
      console.error('Error al otorgar punto:', err);
    }
  };

  // Undo Last Point
  const handleUndoLastPoint = () => {
    const currentEvents = eventsRef.current;
    if (currentEvents.length === 0) return;

    audioFx.playUndoSound();
    const remainingEvents = currentEvents.slice(1);
    setEvents(remainingEvents);
    eventsRef.current = remainingEvents;

    const replayedMatch = replayEventsOnMatch(matchRef.current, remainingEvents);
    matchRef.current = replayedMatch;
    onUpdateMatchRef.current(replayedMatch);
  };

  // Reset Complete Match Handler
  const handleResetMatch = () => {
    setShowResetConfirmModal(true);
  };

  const executeResetMatch = () => {
    const resetMatch: Match = {
      ...matchRef.current,
      status: 'PAUSED',
      currentSetIndex: 0,
      elapsedTimeSec: 0,
      sets: [
        { teamAGames: 0, teamBGames: 0, isTieBreak: false, tieBreakPoints: { teamA: 0, teamB: 0 } },
        { teamAGames: 0, teamBGames: 0, isTieBreak: false, tieBreakPoints: { teamA: 0, teamB: 0 } },
        { teamAGames: 0, teamBGames: 0, isTieBreak: false, tieBreakPoints: { teamA: 0, teamB: 0 } },
      ],
      currentGame: {
        teamAPoints: '0',
        teamBPoints: '0',
        serverTeam: 'A',
        isDeuce: false,
      },
      winnerTeam: undefined,
    };

    setTimerRunning(false);
    setElapsedSec(0);
    setEvents([]);
    eventsRef.current = [];
    matchRef.current = resetMatch;
    audioFx.playUndoSound();
    onUpdateMatchRef.current(resetMatch);
    setShowResetConfirmModal(false);
  };

  // Reset Timer Only
  const handleResetTimer = () => {
    setTimerRunning(false);
    setElapsedSec(0);
    const updated = { ...matchRef.current, elapsedTimeSec: 0, status: 'PAUSED' as const };
    matchRef.current = updated;
    onUpdateMatchRef.current(updated);
  };

  // Timer Controls
  const handlePauseTimer = () => {
    setTimerRunning(false);
    const updated = { ...matchRef.current, status: 'PAUSED' as const };
    matchRef.current = updated;
    onUpdateMatchRef.current(updated);
  };

  const handleResumeTimer = () => {
    setTimerRunning(true);
    const updated = { ...matchRef.current, status: 'LIVE' as const };
    matchRef.current = updated;
    onUpdateMatchRef.current(updated);
  };

  // Format Timer mm:ss or hh:mm:ss
  const formatTimer = (totalSec: number) => {
    const hrs = Math.floor(totalSec / 3600);
    const mins = Math.floor((totalSec % 3600) / 60);
    const secs = totalSec % 60;
    const pad = (n: number) => n.toString().padStart(2, '0');
    return hrs > 0 ? `${pad(hrs)}:${pad(mins)}:${pad(secs)}` : `${pad(mins)}:${pad(secs)}`;
  };

  return (
    <div className="fixed inset-0 z-50 bg-[#111317] text-[#e2e2e7] flex flex-col overflow-y-auto">
      {/* Top Header Controls */}
      <div className="bg-[#1a1c1f] border-b border-[#333539] px-4 py-3 flex items-center justify-between sticky top-0 z-30 shadow-md">
        <button
          onClick={onClose}
          className="flex items-center gap-1.5 text-[#c4c9ac] hover:text-white p-2 rounded-lg hover:bg-[#282a2e]"
        >
          <span className="material-symbols-outlined text-[20px]">arrow_back</span>
          <span className="font-mono-stats text-[12px] font-bold">Volver</span>
        </button>

        <div className="text-center">
          <h2 className="font-headline font-bold text-[16px] text-white tracking-tight">
            Mesa de Control de Partido
          </h2>
          <div className="text-[11px] font-mono-stats text-[#c3f400] flex items-center justify-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-[#FF3B30] pulse-animation" />
            <span>{match.tournamentName || 'Partido en Vivo'} • {match.courtName}</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Reset Match Button in Header */}
          <button
            onClick={handleResetMatch}
            className="px-2.5 py-1.5 rounded-lg text-[11px] font-mono-stats font-bold flex items-center gap-1 bg-[#2e1d1d] text-[#ffb4ab] border border-[#ff3b30]/40 hover:bg-[#3d2424] transition-all"
            title="Reiniciar el partido completo a 0-0"
          >
            <span className="material-symbols-outlined text-[16px]">restart_alt</span>
            <span className="hidden sm:inline">Reiniciar</span>
          </button>

          {/* Edit Mode Toggle */}
          <button
            onClick={() => setIsEditMode(!isEditMode)}
            className={`px-3 py-1.5 rounded-lg text-[11px] font-mono-stats font-bold flex items-center gap-1 border transition-all ${
              isEditMode
                ? 'bg-[#FF3B30] text-white border-[#FF3B30]'
                : 'bg-[#282a2e] text-[#c4c9ac] border-[#444933] hover:text-white'
            }`}
          >
            <span className="material-symbols-outlined text-[16px]">edit</span>
            <span>{isEditMode ? 'Guardar Cambios' : 'Edición Rápida'}</span>
          </button>
        </div>
      </div>

      {/* Main Scoreboard Area */}
        <div className="p-4 w-full flex flex-col gap-4">
        {/* Timer Bar & Golden Point Badge */}
        <div className="bg-[#1e2023] rounded-xl p-3 border border-[#333539] flex items-center justify-between shadow-lg">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-[#c3f400] text-[24px]">timer</span>
            <span className="font-mono-stats font-bold text-[24px] text-white tracking-wider">
              {formatTimer(elapsedSec)}
            </span>
          </div>

          {/* Timer Play / Pause / Undo / Reset */}
          <div className="flex items-center gap-1.5">
            {timerRunning ? (
              <button
                onClick={handlePauseTimer}
                className="bg-[#282a2e] hover:bg-[#333539] text-[#ffdad6] font-mono-stats text-[12px] font-bold px-2.5 py-1.5 rounded-lg border border-[#ffb4ab]/30 flex items-center gap-1"
              >
                <span className="material-symbols-outlined text-[16px]">pause</span> Pausar
              </button>
            ) : (
              <button
                onClick={handleResumeTimer}
                className="bg-[#c3f400] hover:bg-[#abd600] text-[#161e00] font-mono-stats text-[12px] font-bold px-2.5 py-1.5 rounded-lg flex items-center gap-1"
              >
                <span className="material-symbols-outlined text-[16px]">play_arrow</span> Reanudar
              </button>
            )}

            <button
              onClick={handleUndoLastPoint}
              className="bg-[#282a2e] hover:bg-[#333539] text-white font-mono-stats text-[12px] font-bold px-2.5 py-1.5 rounded-lg border border-[#333539] flex items-center gap-1"
              title="Deshacer último evento"
            >
              <span className="material-symbols-outlined text-[16px]">undo</span> Deshacer
            </button>

            <button
              onClick={handleResetMatch}
              className="bg-[#382020] hover:bg-[#4a2a2a] text-[#ffdad6] font-mono-stats text-[12px] font-bold px-2.5 py-1.5 rounded-lg border border-[#ff3b30]/40 flex items-center gap-1"
              title="Reiniciar todo el partido a 0-0"
            >
              <span className="material-symbols-outlined text-[16px]">restart_alt</span> Reiniciar
            </button>
          </div>
        </div>

        {/* GIANT HIGH-VISIBILITY SCOREBOARD */}
        <div className="bg-[#1e2023] rounded-2xl p-5 border-2 border-[#333539] shadow-2xl relative overflow-hidden">
          {/* Active Set Indicator */}
          <div className="text-center mb-3">
            <span className="font-mono-stats font-bold text-[12px] text-[#c3f400] uppercase tracking-widest bg-[#c3f400]/10 px-3 py-1 rounded-full border border-[#c3f400]/30">
              SET {match.currentSetIndex + 1} {match.sets[match.currentSetIndex]?.isTieBreak ? '(TIE-BREAK)' : ''}
            </span>
          </div>

          {/* Teams Comparison Row */}
          <div className="grid grid-cols-2 gap-4 text-center border-b border-[#333539] pb-4">
            {/* TEAM A */}
            <div className="flex flex-col items-center p-2 rounded-xl bg-[#282a2e]/50 border border-[#333539]">
              <div className="text-[#c3f400] font-mono-stats font-bold text-[11px] mb-1">PAREJA A</div>
              <h3 className="font-headline font-black text-[18px] text-white leading-tight">
                {match.pairAName}
              </h3>
              <p className="text-[12px] text-[#c4c9ac] mt-0.5">
                {match.playerA1Name} / {match.playerA2Name}
              </p>
            </div>

            {/* TEAM B */}
            <div className="flex flex-col items-center p-2 rounded-xl bg-[#282a2e]/50 border border-[#333539]">
              <div className="text-[#c3f400] font-mono-stats font-bold text-[11px] mb-1">PAREJA B</div>
              <h3 className="font-headline font-black text-[18px] text-white leading-tight">
                {match.pairBName}
              </h3>
              <p className="text-[12px] text-[#c4c9ac] mt-0.5">
                {match.playerB1Name} / {match.playerB2Name}
              </p>
            </div>
          </div>

           {/* Score Displays: Games in Sets & Current Point */}
           <div className="mt-4 grid grid-cols-2 gap-4">
             {/* Team A Points Display */}
             <div className="bg-[#0c0e12] rounded-xl p-4 text-center border border-[#333539] flex flex-col items-center justify-center">
               <span className="font-mono-stats text-[11px] text-[#c4c9ac] mb-1">PUNTOS PAREJA A</span>
               <div className="font-display-score text-[64px] leading-none text-[#c3f400]">
                 {match.currentGame?.teamAPoints ?? '-'}
               </div>

               <div className="mt-2 text-[10px] font-mono-stats font-bold uppercase tracking-wider">
                 {getLastScoringTeam(match) === 'A' ? (
                   <span className="text-[#c3f400]">⚡ Último punto: Pareja A</span>
                 ) : (
                   <span className="text-[#8e9379]">Último punto: —</span>
                 )}
               </div>

               {/* Set Games summary for Team A */}
               <div className="flex gap-2 mt-3 font-mono-stats text-[14px]">
                 {(match.sets || []).map((s, idx) => (
                   <span
                     key={idx}
                     className={`px-2 py-0.5 rounded font-bold ${
                       idx === match.currentSetIndex ? 'bg-[#c3f400] text-[#161e00]' : 'bg-[#282a2e] text-white'
                     }`}
                   >
                     S{idx + 1}: {s.teamAGames}
                   </span>
                 ))}
               </div>
             </div>

             {/* Team B Points Display */}
             <div className="bg-[#0c0e12] rounded-xl p-4 text-center border border-[#333539] flex flex-col items-center justify-center">
               <span className="font-mono-stats text-[11px] text-[#c4c9ac] mb-1">PUNTOS PAREJA B</span>
               <div className="font-display-score text-[64px] leading-none text-white">
                 {match.currentGame?.teamBPoints ?? '-'}
               </div>

               <div className="mt-2 text-[10px] font-mono-stats font-bold uppercase tracking-wider">
                 {getLastScoringTeam(match) === 'B' ? (
                   <span className="text-white">⚡ Último punto: Pareja B</span>
                 ) : (
                   <span className="text-[#8e9379]">Último punto: —</span>
                 )}
               </div>

               {/* Set Games summary for Team B */}
               <div className="flex gap-2 mt-3 font-mono-stats text-[14px]">
                 {(match.sets || []).map((s, idx) => (
                   <span
                     key={idx}
                     className={`px-2 py-0.5 rounded font-bold ${
                       idx === match.currentSetIndex ? 'bg-[#c3f400] text-[#161e00]' : 'bg-[#282a2e] text-white'
                     }`}
                   >
                     S{idx + 1}: {s.teamBGames}
                   </span>
                 ))}
               </div>
             </div>
           </div>

          {/* Quick Manual Score Buttons */}
          <div className="mt-5 grid grid-cols-2 gap-3">
            <button
              onClick={() => handleAwardPoint('A', 'POINT')}
              className="bg-[#c3f400] hover:bg-[#abd600] text-[#161e00] font-headline font-black text-[18px] py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition-all shadow-lg"
            >
              <span className="material-symbols-outlined text-[24px]">add_circle</span>
              <span>+ PUNTO PAREJA A</span>
            </button>

            <button
              onClick={() => handleAwardPoint('B', 'POINT')}
              className="bg-[#37393d] hover:bg-[#454749] text-white font-headline font-black text-[18px] py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition-all shadow-lg border border-[#444933]"
            >
              <span className="material-symbols-outlined text-[24px]">add_circle</span>
              <span>+ PUNTO PAREJA B</span>
            </button>
          </div>

          {/* Reset Match Main Action */}
          <div className="mt-3 text-center">
            <button
              onClick={handleResetMatch}
              className="w-full bg-[#2e1d1d] hover:bg-[#422222] text-[#ffdad6] font-mono-stats text-[12px] font-bold py-2.5 px-4 rounded-xl border border-[#ff3b30]/40 hover:border-[#ff3b30] transition-all flex items-center justify-center gap-2 shadow-sm"
            >
              <span className="material-symbols-outlined text-[18px]">restart_alt</span>
              <span>REINICIAR PARTIDO COMPLETO (0-0)</span>
            </button>
          </div>

          {/* Quick Action Event Chips */}
          <div className="mt-3 flex flex-wrap gap-2 justify-center border-t border-[#333539] pt-3">
            <button
              onClick={() => handleAwardPoint('A', 'ACE', match.playerA1Id, match.playerA1Name)}
              className="bg-[#282a2e] hover:bg-[#333539] text-[#c3f400] text-[11px] font-mono-stats px-2.5 py-1 rounded-lg border border-[#c3f400]/30"
            >
              🎾 Ace Pareja A
            </button>
            <button
              onClick={() => handleAwardPoint('A', 'WINNER', match.playerA2Id, match.playerA2Name)}
              className="bg-[#282a2e] hover:bg-[#333539] text-[#c3f400] text-[11px] font-mono-stats px-2.5 py-1 rounded-lg border border-[#c3f400]/30"
            >
              🔥 Winner Pareja A
            </button>
            <button
              onClick={() => handleAwardPoint('B', 'ACE', match.playerB1Id, match.playerB1Name)}
              className="bg-[#282a2e] hover:bg-[#333539] text-white text-[11px] font-mono-stats px-2.5 py-1 rounded-lg border border-[#333539]"
            >
              🎾 Ace Pareja B
            </button>
            <button
              onClick={() => handleAwardPoint('B', 'WINNER', match.playerB2Id, match.playerB2Name)}
              className="bg-[#282a2e] hover:bg-[#333539] text-white text-[11px] font-mono-stats px-2.5 py-1 rounded-lg border border-[#333539]"
            >
              💥 Winner Pareja B
            </button>
          </div>
        </div>

        {/* Quick Edit Mode Modal ("Modo de edición para corregir errores rápidamente") */}
        {isEditMode && (
          <div className="bg-[#282a2e] p-4 rounded-xl border border-[#FF3B30] flex flex-col gap-3">
            <div className="flex items-center justify-between border-b border-[#333539] pb-2">
              <span className="font-mono-stats text-[13px] font-bold text-[#FF3B30] flex items-center gap-1">
                <span className="material-symbols-outlined text-[18px]">build</span>
                MODO EDICIÓN DIRECTA
              </span>
              <span className="text-[11px] text-[#c4c9ac]">Ajusta juegos/sets manualmente</span>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[11px] font-mono-stats text-[#c4c9ac] block mb-1">
                  Juegos Set Actual Pareja A
                </label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  value={match.sets[match.currentSetIndex]?.teamAGames || 0}
                  onChange={(e) => {
                    const val = parseInt(e.target.value) || 0;
                    const updatedSets = [...match.sets];
                    updatedSets[match.currentSetIndex].teamAGames = val;
                    onUpdateMatch({ ...match, sets: updatedSets });
                  }}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded text-[14px] font-mono-stats font-bold"
                />
              </div>

              <div>
                <label className="text-[11px] font-mono-stats text-[#c4c9ac] block mb-1">
                  Juegos Set Actual Pareja B
                </label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  value={match.sets[match.currentSetIndex]?.teamBGames || 0}
                  onChange={(e) => {
                    const val = parseInt(e.target.value) || 0;
                    const updatedSets = [...match.sets];
                    updatedSets[match.currentSetIndex].teamBGames = val;
                    onUpdateMatch({ ...match, sets: updatedSets });
                  }}
                  className="w-full bg-[#111317] border border-[#333539] text-white p-2 rounded text-[14px] font-mono-stats font-bold"
                />
              </div>
            </div>
          </div>
        )}

        {/* FLAGSHIP CAMERA GESTURE CONTROL SECTION */}
        <div className="bg-[#1e2023] rounded-2xl p-4 border border-[#c3f400]/40 shadow-xl flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#c3f400] text-[24px]">videocam</span>
              <div>
                <h3 className="font-headline font-bold text-[16px] text-white">
                  Modo Control por Gestos de Cámara
                </h3>
                <p className="text-[11px] text-[#c4c9ac]">
                  Controla el marcador sin tocar la pantalla
                </p>
              </div>
            </div>

            <button
              onClick={() => setGestureModeActive(!gestureModeActive)}
              className={`px-4 py-2 rounded-xl font-mono-stats text-[12px] font-bold flex items-center gap-1.5 transition-all shadow-md ${
                gestureModeActive
                  ? 'bg-[#FF3B30] text-white animate-pulse'
                  : 'bg-[#c3f400] text-[#161e00] hover:bg-[#abd600]'
              }`}
            >
              <span className="material-symbols-outlined text-[18px]">
                {gestureModeActive ? 'videocam_off' : 'videocam'}
              </span>
              <span>{gestureModeActive ? 'DETENER GESTOS' : 'ACTIVAR CÁMARA'}</span>
            </button>
          </div>

          {/* Active Gesture Mode Panel */}
          {gestureModeActive && (
            <div className="flex flex-col gap-3 bg-[#0c0e12] rounded-xl p-3.5 border border-[#333539]">
              {/* Foreground Camera Active Banner */}
              <div className="bg-[#93000a]/40 border border-[#ffb4ab]/30 p-2 rounded-lg flex items-center justify-between">
                <div className="flex items-center gap-2 text-[12px] font-mono-stats font-bold text-[#ffdad6]">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#FF3B30] pulse-animation" />
                  <span>🔴 CÁMARA & RECONOCIMIENTO ACTIVO</span>
                </div>
                <button
                  onClick={() => setShowGestureSettings(!showGestureSettings)}
                  className="text-[11px] font-mono-stats text-[#c3f400] underline"
                >
                  Configurar
                </button>
              </div>

               {/* Camera Error Banner */}
               {cameraPermissionGranted === false && (
                 <div className="bg-red-900/40 border border-red-500/50 p-3 rounded-xl text-red-200 text-[12px] font-mono-stats flex flex-col gap-2">
                   <div className="flex items-center gap-2 font-bold">
                     <span className="material-symbols-outlined text-[18px]">warning</span>
                     <span>Cámara no disponible</span>
                   </div>
                   <p>
                     Asegúrate de acceder desde <strong>HTTPS</strong> o <strong>localhost</strong>, 
                     y de haber aceptado los permisos de cámara en el navegador.
                   </p>
                   <button
                     onClick={() => {
                       setCameraPermissionGranted(null);
                       setGestureModeActive(false);
                       setTimeout(() => setGestureModeActive(true), 100);
                     }}
                     className="self-start bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 px-3 py-1.5 rounded-lg text-[11px] font-bold transition-all"
                   >
                     Reintentar cámara
                   </button>
                 </div>
               )}

               {/* WebCam Video Canvas Preview */}
               <div className="relative aspect-video bg-[#111317] rounded-xl overflow-hidden border border-[#333539] flex items-center justify-center">
                 <div className="absolute inset-0 transform -scale-x-100">
                   <video ref={videoRef} className="absolute inset-0 w-full h-full object-cover" muted playsInline autoPlay />
                   <canvas ref={canvasRef} className="absolute inset-0 w-full h-full object-cover pointer-events-none" />
                 </div>

                {/* Gesture Overlay HUD */}
                <div className="absolute inset-x-3 bottom-3 bg-[#111317]/90 backdrop-blur-md p-3 rounded-xl border border-[#c3f400]/50 shadow-2xl">
                  <div className="flex items-center justify-between text-[12px] font-mono-stats mb-1.5">
                    <span className="font-bold text-[#c3f400]">{recognizedState.statusText}</span>
                    <span className="text-[#c4c9ac]">{recognizedState.progressPercent}%</span>
                  </div>

                  {/* Progress Hold Bar */}
                  <div className="w-full h-2.5 bg-[#282a2e] rounded-full overflow-hidden border border-[#333539]">
                    <div
                      className="h-full bg-[#c3f400] transition-all duration-150"
                      style={{ width: `${recognizedState.progressPercent}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Gesture Guide Cheat Sheet */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5 text-[11px] font-mono-stats text-center">
                <div className="bg-[#1b1e23] p-1.5 rounded border border-[#333539] flex flex-col items-center">
                  <span className="text-[16px]">🤘</span>
                  <span className="text-[#c3f400] font-bold">Rock</span>
                  <span className="text-[#8e9379] text-[9px]">Punto Pareja A</span>
                </div>
                <div className="bg-[#1b1e23] p-1.5 rounded border border-[#333539] flex flex-col items-center">
                  <span className="text-[16px]">📞</span>
                  <span className="text-white font-bold">Llamar</span>
                  <span className="text-[#8e9379] text-[9px]">Punto Pareja B</span>
                </div>
                <div className="bg-[#1b1e23] p-1.5 rounded border border-[#333539] flex flex-col items-center col-span-2 sm:col-span-1">
                  <span className="text-[16px]">👎</span>
                  <span className="text-[#ffdad6] font-bold">Pulgar Abajo</span>
                  <span className="text-[#8e9379] text-[9px]">Deshacer Punto</span>
                </div>
              </div>

              {/* Interactive Gesture Trigger Simulator Bar */}
              <div className="bg-[#282a2e] p-2.5 rounded-xl border border-[#333539]">
                <div className="text-[11px] font-mono-stats text-[#c4c9ac] mb-2 font-bold text-center">
                  ⚡ DISPARADOR RÁPIDO DE GESTOS (PRUEBA MANUAL):
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  <button
                    onClick={() => {
                      const res = gestureEngineRef.current.triggerDirectAction('POINT_TEAM_A');
                      setRecognizedState(res);
                      executeGestureAction('POINT_TEAM_A');
                    }}
                    className="bg-[#333539] hover:bg-[#37393d] text-[#c3f400] text-[11px] font-mono-stats py-2 px-1.5 rounded-lg border border-[#c3f400]/40 flex flex-col items-center gap-1"
                  >
                    <span className="text-[18px]">🤘</span>
                    <span>🤘 Punto A</span>
                  </button>

                  <button
                    onClick={() => {
                      const res = gestureEngineRef.current.triggerDirectAction('POINT_TEAM_B');
                      setRecognizedState(res);
                      executeGestureAction('POINT_TEAM_B');
                    }}
                    className="bg-[#333539] hover:bg-[#37393d] text-white text-[11px] font-mono-stats py-2 px-1.5 rounded-lg border border-white/20 flex flex-col items-center gap-1"
                  >
                    <span className="text-[18px]">📞</span>
                    <span>📞 Punto B</span>
                  </button>

                  <button
                    onClick={() => {
                      const res = gestureEngineRef.current.triggerDirectAction('UNDO');
                      setRecognizedState(res);
                      executeGestureAction('UNDO');
                    }}
                    className="bg-[#333539] hover:bg-[#37393d] text-[#ffdad6] text-[11px] font-mono-stats py-2 px-1.5 rounded-lg border border-[#ffb4ab]/30 flex flex-col items-center gap-1"
                  >
                    <span className="text-[18px]">👎</span>
                    <span>👎 Deshacer</span>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Gesture Settings Calibration Panel */}
          {showGestureSettings && (
            <div className="bg-[#282a2e] p-3.5 rounded-xl border border-[#333539] flex flex-col gap-2.5">
              <h4 className="font-headline font-bold text-[14px] text-white border-b border-[#333539] pb-1">
                ⚙️ Ajustes del Sistema de Gestos
              </h4>

              <div className="grid grid-cols-2 gap-3 text-[12px] font-mono-stats">
                <div>
                  <label className="text-[#c4c9ac] block mb-1">
                    Tiempo Cooldown (ms): {gestureConfig.cooldownMs}
                  </label>
                  <input
                    type="range"
                    min="500"
                    max="3000"
                    step="100"
                    value={gestureConfig.cooldownMs}
                    onChange={(e) => {
                      const updated = { ...gestureConfig, cooldownMs: parseInt(e.target.value) };
                      setGestureConfig(updated);
                      gestureEngineRef.current.updateConfig(updated);
                    }}
                    className="w-full accent-[#c3f400]"
                  />
                </div>

                <div>
                  <label className="text-[#c4c9ac] block mb-1">
                    Frames de Confirmación: {gestureConfig.requiredHoldFrames}
                  </label>
                  <input
                    type="range"
                    min="3"
                    max="15"
                    value={gestureConfig.requiredHoldFrames}
                    onChange={(e) => {
                      const updated = { ...gestureConfig, requiredHoldFrames: parseInt(e.target.value) };
                      setGestureConfig(updated);
                      gestureEngineRef.current.updateConfig(updated);
                    }}
                    className="w-full accent-[#c3f400]"
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        {/* VOICE CONTROL SECTION */}
        <div className="bg-[#1e2023] rounded-2xl p-4 border border-[#c3f400]/40 shadow-xl flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#c3f400] text-[24px]">mic</span>
              <div>
                <h3 className="font-headline font-bold text-[16px] text-white">
                  Control por Voz
                </h3>
                <p className="text-[11px] text-[#c4c9ac]">
                  Comandos: "local" (Pareja A), "visitante" (Pareja B), "deshacer"
                </p>
              </div>
            </div>

            <button
              onClick={() => setVoiceModeActive(!voiceModeActive)}
              className={`px-4 py-2 rounded-xl font-mono-stats text-[12px] font-bold flex items-center gap-1.5 transition-all shadow-md ${
                voiceModeActive
                  ? 'bg-[#FF3B30] text-white animate-pulse'
                  : 'bg-[#c3f400] text-[#161e00] hover:bg-[#abd600]'
              }`}
            >
              <span className="material-symbols-outlined text-[18px]">
                {voiceModeActive ? 'mic_off' : 'mic'}
              </span>
              <span>{voiceModeActive ? 'DETENER VOZ' : 'ACTIVAR VOZ'}</span>
            </button>
          </div>

          {voiceModeActive && (
            <div className="flex flex-col gap-3 bg-[#0c0e12] rounded-xl p-3.5 border border-[#333539]">
              <div className="bg-[#1e2023]/80 border border-[#c3f400]/30 p-2 rounded-lg flex items-center justify-between">
                <div className="flex items-center gap-2 text-[12px] font-mono-stats font-bold text-[#c3f400]">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#c3f400] pulse-animation" />
                  <span>🎤 ESCUCHANDO COMANDOS DE VOZ</span>
                </div>
                <span className="text-[11px] font-mono-stats text-[#c4c9ac]">
                  {voiceStatus}
                </span>
              </div>

              {voiceError && (
                <div className="bg-red-900/40 border border-red-500/50 p-3 rounded-xl text-red-200 text-[12px] font-mono-stats">
                  <div className="flex items-center gap-2 font-bold">
                    <span className="material-symbols-outlined text-[18px]">warning</span>
                    <span>Micrófono no disponible</span>
                  </div>
                  <p className="mt-1">{voiceError}</p>
                </div>
              )}

              <div className="grid grid-cols-3 gap-2 text-[11px] font-mono-stats text-center">
                <div className="bg-[#1b1e23] p-2 rounded border border-[#333539] flex flex-col items-center">
                  <span className="text-[16px]">🤘</span>
                  <span className="text-[#c3f400] font-bold">"Local"</span>
                  <span className="text-[#8e9379] text-[9px]">Punto Pareja A</span>
                </div>
                <div className="bg-[#1b1e23] p-2 rounded border border-[#333539] flex flex-col items-center">
                  <span className="text-[16px]">📞</span>
                  <span className="text-white font-bold">"Visitante"</span>
                  <span className="text-[#8e9379] text-[9px]">Punto Pareja B</span>
                </div>
                <div className="bg-[#1b1e23] p-2 rounded border border-[#333539] flex flex-col items-center">
                  <span className="text-[16px]">👎</span>
                  <span className="text-[#ffdad6] font-bold">"Deshacer"</span>
                  <span className="text-[#8e9379] text-[9px]">Undo último punto</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Match Events History Timeline */}
        <div className="bg-[#1e2023] rounded-xl p-4 border border-[#333539] flex flex-col gap-3">
          <h3 className="font-headline font-bold text-[15px] text-white flex items-center gap-2 border-b border-[#333539] pb-2">
            <span className="material-symbols-outlined text-[#c3f400] text-[20px]">history</span>
            Historial de Puntos del Partido ({events.length})
          </h3>

          <div className="max-h-48 overflow-y-auto flex flex-col gap-2">
            {events.length === 0 ? (
              <p className="text-[12px] text-[#c4c9ac] font-mono-stats text-center py-4">
                Sin eventos aún. Los puntos registrados aparecerán aquí.
              </p>
            ) : (
              events.map((ev) => (
                <div
                  key={ev.id}
                  className="bg-[#282a2e] p-2.5 rounded-lg border border-[#333539] flex items-center justify-between text-[12px] font-mono-stats"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-[#8e9379]">{ev.timestamp}</span>
                    <span className="font-bold text-white">{ev.description}</span>
                  </div>
                  <span className="text-[#c3f400] text-[11px] font-semibold bg-[#c3f400]/10 px-2 py-0.5 rounded">
                    {ev.scoreSnapshot}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Confirmation Modal for Resetting Complete Match */}
      {showResetConfirmModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#1b1e23] border border-[#ff3b30]/40 rounded-2xl p-6 max-w-sm w-full shadow-2xl flex flex-col items-center text-center animate-in fade-in zoom-in-95 duration-150">
            <div className="w-12 h-12 rounded-full bg-[#ff3b30]/15 flex items-center justify-center mb-3 text-[#ff3b30]">
              <span className="material-symbols-outlined text-[28px]">restart_alt</span>
            </div>
            <h3 className="font-headline font-bold text-[18px] text-white mb-2">
              ¿Reiniciar el partido?
            </h3>
            <p className="text-[#c4c9ac] text-[13px] mb-6 leading-relaxed">
              Esta acción restablecerá todos los puntos, juegos, sets y el cronómetro a <strong className="text-white">0 - 0</strong>.
            </p>
            <div className="flex gap-3 w-full">
              <button
                onClick={() => setShowResetConfirmModal(false)}
                className="flex-1 bg-[#282a2e] hover:bg-[#333539] text-[#c4c9ac] hover:text-white font-mono-stats text-[13px] font-bold py-2.5 px-4 rounded-xl border border-[#333539] transition-all"
              >
                Cancelar
              </button>
              <button
                onClick={executeResetMatch}
                className="flex-1 bg-[#ff3b30] hover:bg-[#e03126] text-white font-mono-stats text-[13px] font-bold py-2.5 px-4 rounded-xl shadow-lg transition-all flex items-center justify-center gap-1.5"
              >
                <span className="material-symbols-outlined text-[18px]">check</span>
                <span>Sí, Reiniciar</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Canvas drawing helper for skeleton overlay

function drawHandSkeletonOnCanvas(
  ctx: CanvasRenderingContext2D,
  landmarks: any[],
  progress: number,
  gesture: string
) {
  if (!landmarks || landmarks.length < 21) return;

  const w = ctx.canvas.width;
  const h = ctx.canvas.height;

  // Joint connections array for standard 21 hand landmarks
  const connections = [
    [0, 1], [1, 2], [2, 3], [3, 4], // Thumb
    [0, 5], [5, 6], [6, 7], [7, 8], // Index
    [0, 9], [9, 10], [10, 11], [11, 12], // Middle
    [0, 13], [13, 14], [14, 15], [15, 16], // Ring
    [0, 17], [17, 18], [18, 19], [19, 20], // Pinky
    [5, 9], [9, 13], [13, 17], // Palm bridge
  ];

  const strokeColor = progress === 100 ? '#c3f400' : progress > 50 ? '#00e5ff' : '#ffffff';

  // Draw bone lines
  ctx.strokeStyle = strokeColor;
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';

  connections.forEach(([i, j]) => {
    const pt1 = landmarks[i];
    const pt2 = landmarks[j];
    if (pt1 && pt2) {
      ctx.beginPath();
      ctx.moveTo(pt1.x * w, pt1.y * h);
      ctx.lineTo(pt2.x * w, pt2.y * h);
      ctx.stroke();
    }
  });

  // Draw joint landmarks
  landmarks.forEach((pt: any, idx: number) => {
    const x = pt.x * w;
    const y = pt.y * h;

    ctx.beginPath();
    ctx.arc(x, y, [4, 8, 12, 16, 20].includes(idx) ? 6 : 4, 0, Math.PI * 2);
    ctx.fillStyle = [4, 8, 12, 16, 20].includes(idx) ? '#c3f400' : '#111317';
    ctx.strokeStyle = '#c3f400';
    ctx.lineWidth = 2;
    ctx.fill();
    ctx.stroke();
  });

  // Draw gesture active label overlay on top of hand
  if (gesture && gesture !== 'NONE') {
    const wrist = landmarks[0];
    const wristX = wrist.x * w;
    const wristY = wrist.y * h - 30;

    const label = getGestureLabel(gesture as GestureType);
    ctx.font = 'bold 14px sans-serif';
    const textWidth = ctx.measureText(label).width;

    ctx.fillStyle = 'rgba(17, 19, 23, 0.85)';
    ctx.fillRect(wristX - textWidth / 2 - 8, wristY - 18, textWidth + 16, 26);

    ctx.strokeStyle = '#c3f400';
    ctx.lineWidth = 1;
    ctx.strokeRect(wristX - textWidth / 2 - 8, wristY - 18, textWidth + 16, 26);

    ctx.fillStyle = '#c3f400';
    ctx.fillText(label, wristX - textWidth / 2, wristY);
  }
}
