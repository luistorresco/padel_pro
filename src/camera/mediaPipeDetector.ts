import { HandLandmarker, FilesetResolver } from '@mediapipe/tasks-vision';

let handLandmarkerInstance: HandLandmarker | null = null;
let isInitializing = false;
let initFailed = false;

export async function getHandLandmarker(): Promise<HandLandmarker | null> {
  if (handLandmarkerInstance) return handLandmarkerInstance;
  if (initFailed) return null;
  if (isInitializing) return null;

  isInitializing = true;
  try {
    const vision = await FilesetResolver.forVisionTasks(
      'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1/wasm'
    );
    handLandmarkerInstance = await HandLandmarker.createFromOptions(vision, {
      baseOptions: {
        modelAssetPath:
          'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
        delegate: 'GPU',
      },
      runningMode: 'VIDEO',
      numHands: 1,
    });
    console.log('MediaPipe HandLandmarker initialized successfully!');
    isInitializing = false;
    return handLandmarkerInstance;
  } catch (err) {
    console.warn('MediaPipe CDN/WASM initialization failed, using Pixel Vision fallback:', err);
    initFailed = true;
    isInitializing = false;
    return null;
  }
}
