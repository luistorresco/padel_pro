import React, { useState } from 'react';
import { runPadelScoringUnitTests } from '../domain/scoringEngine';

interface RuleEngineTesterModalProps {
  onClose: () => void;
}

export const RuleEngineTesterModal: React.FC<RuleEngineTesterModalProps> = ({ onClose }) => {
  const [testResults, setTestResults] = useState<{ passed: number; total: number; logs: string[] } | null>(null);

  const handleRun = () => {
    const res = runPadelScoringUnitTests();
    setTestResults(res);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-[#1e2023] rounded-2xl p-5 border border-[#c3f400] max-w-lg w-full max-h-[85vh] overflow-y-auto flex flex-col gap-4 shadow-2xl">
        <div className="flex items-center justify-between border-b border-[#333539] pb-3">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-[#c3f400] text-[24px]">bug_report</span>
            <h3 className="font-headline font-bold text-[18px] text-white">
              Inspector de Pruebas del Motor de Puntuación
            </h3>
          </div>
          <button onClick={onClose} className="text-[#c4c9ac] hover:text-white">
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        <p className="text-[12px] font-mono-stats text-[#c4c9ac]">
          Ejecuta la suite de pruebas unitarias para validar la máquina de estados de pádel (0 → 15 → 30 → 40 → Deuce → Ventaja → Golden Point → Tie-Break → Set → Partido).
        </p>

        <button
          onClick={handleRun}
          className="bg-[#c3f400] text-[#161e00] font-headline font-black text-[14px] py-3 rounded-xl hover:bg-[#abd600] transition-all shadow-md flex items-center justify-center gap-2"
        >
          <span className="material-symbols-outlined text-[20px]">play_arrow</span>
          <span>EJECUTAR PRUEBAS UNITARIAS</span>
        </button>

        {testResults && (
          <div className="flex flex-col gap-3 mt-2">
            <div className="bg-[#0c0e12] p-3 rounded-xl border border-[#333539] flex items-center justify-between font-mono-stats text-[13px]">
              <span className="text-white">Resultado:</span>
              <span className="font-black text-[#c3f400]">
                {testResults.passed} / {testResults.total} PASARON CON ÉXITO ✅
              </span>
            </div>

            <div className="bg-[#111317] p-3 rounded-xl border border-[#333539] max-h-60 overflow-y-auto font-mono-stats text-[11px] flex flex-col gap-1.5">
              {testResults.logs.map((log, idx) => (
                <div key={idx} className="text-[#c4c9ac]">
                  {log}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
