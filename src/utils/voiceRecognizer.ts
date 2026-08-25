export type VoiceCommand = 'POINT_A' | 'POINT_B' | 'UNDO' | 'NONE';

export interface VoiceCommandEngine {
  start(): void;
  stop(): void;
  isListening(): boolean;
}

export function createVoiceCommandEngine(onCommand: (cmd: VoiceCommand) => void): VoiceCommandEngine {
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

  if (!SpeechRecognition) {
    console.warn('Speech Recognition API not supported in this browser');
    return {
      start() {},
      stop() {},
      isListening() { return false; },
    };
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = false;
  recognition.lang = 'es-ES';

  let listening = false;

  recognition.onresult = (event: any) => {
    const last = event.results[event.results.length - 1];
    if (last.isFinal) {
      const transcript = normalizeTranscript(last[0].transcript);
      const cmd = classifyCommand(transcript);
      if (cmd !== 'NONE') {
        onCommand(cmd);
      }
    }
  };

  recognition.onerror = (event: any) => {
    console.warn('Speech recognition error:', event.error);
    if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
      listening = false;
    }
  };

  recognition.onend = () => {
    listening = false;
  };

  return {
    start() {
      if (listening) return;
      try {
        recognition.start();
        listening = true;
      } catch (e) {
        console.warn('Recognition start error:', e);
      }
    },
    stop() {
      if (!listening) return;
      try {
        recognition.stop();
      } catch (e) {
        // ignore stop errors
      }
      listening = false;
    },
    isListening() {
      return listening;
    },
  };
}

function normalizeTranscript(text: string): string {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\w\s]/g, '')
    .trim()
    .replace(/\s+/g, ' ');
}

function classifyCommand(text: string): VoiceCommand {
  if (text === 'grilla' || text === 'grillas') return 'POINT_A';
  if (text === 'perra' || text === 'perras') return 'POINT_B';
  if (text === 'deshacer' || text === 'desaser' || text === 'desazer') return 'UNDO';
  return 'NONE';
}
