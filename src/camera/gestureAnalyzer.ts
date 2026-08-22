import { GestureConfiguration, GestureType, RecognizedGestureState } from '../types';

export const DEFAULT_GESTURE_CONFIG: GestureConfiguration = {
  pointTeamAGesture: 'OPEN_PALM',
  pointTeamBGesture: 'CLOSED_FIST',
  undoGesture: 'THUMB_DOWN',
  pauseTimerGesture: 'PEACE_SIGN',
  resumeTimerGesture: 'THUMB_UP',
  cooldownMs: 1500,
  minConfidence: 0.70,
  requiredHoldFrames: 10,
  detectionZone: {
    enabled: false,
    xMin: 0.1,
    yMin: 0.1,
    xMax: 0.9,
    yMax: 0.9,
  },
  mode: 'ONE_HAND',
};

export type GestureStatePhase = 'IDLE' | 'GESTURE_DETECTED' | 'VALIDATING' | 'CONFIRMED' | 'ACTION_EXECUTED' | 'COOLDOWN';

export class GestureRecognizerEngine {
  private config: GestureConfiguration;
  private currentPhase: GestureStatePhase = 'IDLE';
  private detectedGesture: GestureType = 'NONE';
  private consecutiveFrames = 0;
  private cooldownTimer: any = null;
  private lastActionTimestamp = 0;

  constructor(config: GestureConfiguration = DEFAULT_GESTURE_CONFIG) {
    this.config = config;
  }

  public updateConfig(newConfig: GestureConfiguration) {
    this.config = newConfig;
  }

  public getConfig(): GestureConfiguration {
    return this.config;
  }

  /**
   * Analyze raw hand landmark coordinates from MediaPipe or video analyzer
   * Landmarks array format: 21 points with x, y, z normalized [0..1]
   */
  public analyzeHandLandmarks(
    landmarks: Array<{ x: number; y: number; z: number }>[],
    confidence = 0.85
  ): RecognizedGestureState {
    const now = Date.now();

    // Check Cooldown phase
    if (this.currentPhase === 'COOLDOWN') {
      const remaining = this.config.cooldownMs - (now - this.lastActionTimestamp);
      if (remaining > 0) {
        return {
          gesture: 'NONE',
          confidence: 0,
          progressPercent: 0,
          statusText: `⏱️ COOLDOWN (${(remaining / 1000).toFixed(1)}s)`,
          handCount: landmarks.length,
        };
      } else {
        this.currentPhase = 'IDLE';
        this.detectedGesture = 'NONE';
        this.consecutiveFrames = 0;
      }
    }

    if (!landmarks || landmarks.length === 0) {
      this.resetToIdle();
      return {
        gesture: 'NONE',
        confidence: 0,
        progressPercent: 0,
        statusText: 'Buscando manos en cámara...',
        handCount: 0,
      };
    }

    const mainHand = landmarks[0];

    // Filter Detection Zone if enabled
    if (this.config.detectionZone.enabled) {
      const wrist = mainHand[0];
      const zone = this.config.detectionZone;
      if (wrist.x < zone.xMin || wrist.x > zone.xMax || wrist.y < zone.yMin || wrist.y > zone.yMax) {
        this.resetToIdle();
        return {
          gesture: 'NONE',
          confidence: 0,
          progressPercent: 0,
          statusText: '⚠️ Mano fuera de la Zona de Gestos',
          handCount: landmarks.length,
        };
      }
    }

    if (confidence < this.config.minConfidence) {
      this.resetToIdle();
      return {
        gesture: 'NONE',
        confidence,
        progressPercent: 0,
        statusText: 'Confianza insuficiente en el gesto',
        handCount: landmarks.length,
      };
    }

    // Classify hand shape gesture from landmark positions
    const classifiedGesture = classifyGestureFromLandmarks(mainHand);

    if (classifiedGesture === 'NONE') {
      this.resetToIdle();
      return {
        gesture: 'NONE',
        confidence,
        progressPercent: 0,
        statusText: 'Mano detectada (sin gesto activo)',
        handCount: landmarks.length,
      };
    }

    // Map classified gesture shape to domain action
    const mappedAction = this.mapGestureToAction(classifiedGesture);

    if (mappedAction === 'NONE') {
      this.resetToIdle();
      return {
        gesture: 'NONE',
        confidence,
        progressPercent: 0,
        statusText: `Gesto ${classifiedGesture} (sin acción asignada)`,
        handCount: landmarks.length,
      };
    }

    // State machine: Hold validation for N frames
    if (this.detectedGesture !== mappedAction) {
      this.detectedGesture = mappedAction;
      this.consecutiveFrames = 1;
      this.currentPhase = 'VALIDATING';
    } else {
      this.consecutiveFrames++;
    }

    const progress = Math.min(100, Math.round((this.consecutiveFrames / this.config.requiredHoldFrames) * 100));

    if (this.consecutiveFrames >= this.config.requiredHoldFrames) {
      this.currentPhase = 'CONFIRMED';
      this.lastActionTimestamp = Date.now();
      this.currentPhase = 'COOLDOWN';

      return {
        gesture: mappedAction,
        confidence,
        progressPercent: 100,
        statusText: `✅ GESTO CONFIRMADO: ${getGestureLabel(mappedAction)}`,
        handCount: landmarks.length,
      };
    }

    return {
      gesture: mappedAction,
      confidence,
      progressPercent: progress,
      statusText: `✊ MANTÉN GESTO: ${getGestureLabel(mappedAction)} (${progress}%)`,
      handCount: landmarks.length,
    };
  }

  public triggerDirectAction(gesture: GestureType): RecognizedGestureState {
    this.lastActionTimestamp = Date.now();
    this.currentPhase = 'COOLDOWN';
    return {
      gesture,
      confidence: 1.0,
      progressPercent: 100,
      statusText: `⚡ EJECUTADO MANUALMENTE: ${getGestureLabel(gesture)}`,
      handCount: 1,
    };
  }

  private resetToIdle() {
    this.currentPhase = 'IDLE';
    this.detectedGesture = 'NONE';
    this.consecutiveFrames = 0;
  }

  private mapGestureToAction(classified: string): GestureType {
    if (classified === this.config.pointTeamAGesture) return 'POINT_TEAM_A';
    if (classified === this.config.pointTeamBGesture) return 'POINT_TEAM_B';
    if (classified === this.config.undoGesture) return 'UNDO';
    if (classified === this.config.pauseTimerGesture) return 'PAUSE_TIMER';
    if (classified === this.config.resumeTimerGesture) return 'RESUME_TIMER';
    return 'NONE';
  }
}

/**
 * Geometric vector classification of 21 hand landmarks
 * 0: Wrist
 * 4: Thumb Tip, 8: Index Tip, 12: Middle Tip, 16: Ring Tip, 20: Pinky Tip
 */
export function classifyGestureFromLandmarks(landmarks: Array<{ x: number; y: number; z: number }>): string {
  if (!landmarks || landmarks.length < 21) return 'NONE';

  const dist = (a: { x: number; y: number; z?: number }, b: { x: number; y: number; z?: number }) =>
    Math.hypot(a.x - b.x, a.y - b.y, (a.z || 0) - (b.z || 0));

  const wrist = landmarks[0];
  const thumbTip = landmarks[4];
  const indexTip = landmarks[8];
  const middleTip = landmarks[12];
  const ringTip = landmarks[16];
  const pinkyTip = landmarks[20];

  const indexMcp = landmarks[5];
  const indexPip = landmarks[6];
  const middlePip = landmarks[10];
  const ringPip = landmarks[14];
  const pinkyPip = landmarks[18];

  // Compare Tip distance from wrist vs PIP distance from wrist to determine extension
  const isIndexExtended = dist(wrist, indexTip) > dist(wrist, indexPip) * 1.15;
  const isMiddleExtended = dist(wrist, middleTip) > dist(wrist, middlePip) * 1.15;
  const isRingExtended = dist(wrist, ringTip) > dist(wrist, ringPip) * 1.15;
  const isPinkyExtended = dist(wrist, pinkyTip) > dist(wrist, pinkyPip) * 1.15;

  const openFingersCount =
    (isIndexExtended ? 1 : 0) +
    (isMiddleExtended ? 1 : 0) +
    (isRingExtended ? 1 : 0) +
    (isPinkyExtended ? 1 : 0);

  // Check Thumb direction when fingers are folded (closed fist or thumb gesture)
  if (openFingersCount === 0) {
    const isThumbUp = thumbTip.y < indexMcp.y - 0.04 && thumbTip.y < wrist.y - 0.04;
    const isThumbDown = thumbTip.y > wrist.y + 0.05;
    if (isThumbUp) return 'THUMB_UP';
    if (isThumbDown) return 'THUMB_DOWN';
    return 'CLOSED_FIST';
  }

  // Peace / Victory Sign (Index & Middle extended, Ring & Pinky folded)
  if (isIndexExtended && isMiddleExtended && !isRingExtended && !isPinkyExtended) {
    return 'PEACE_SIGN';
  }

  // Open Palm (All 4 fingers extended)
  if (isIndexExtended && isMiddleExtended && isRingExtended && isPinkyExtended) {
    return 'OPEN_PALM';
  }

  return 'NONE';
}

export function getGestureLabel(gesture: GestureType): string {
  switch (gesture) {
    case 'POINT_TEAM_A': return 'PUNTO PAREJA A (✋ Palma)';
    case 'POINT_TEAM_B': return 'PUNTO PAREJA B (✊ Puño)';
    case 'UNDO': return 'DESHACER PUNTO (👎 Pulgar Abajo)';
    case 'PAUSE_TIMER': return 'PAUSAR CRONÓMETRO (✌️ 2 Dedos)';
    case 'RESUME_TIMER': return 'REANUDAR CRONÓMETRO (👍 Pulgar Arriba)';
    default: return 'NINGUNO';
  }
}
