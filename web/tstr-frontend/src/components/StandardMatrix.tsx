import React from 'react';

interface Standard {
  id: string;
  code: string;
  name: string;
}

interface Lab {
  id: string;
  business_name: string;
  capabilities: string[]; // List of standard IDs
}

interface StandardMatrixProps {
  standards: Standard[];
  labs: Lab[];
}

const StandardMatrix: React.FC<StandardMatrixProps> = ({ standards, labs }) => {
  return (
    <div className="w-full overflow-x-auto rounded-3xl border border-white/10 bg-[#0a0a0b] backdrop-blur-md shadow-2xl">
      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b border-white/5">
            <th className="p-6 text-left text-sm font-black uppercase tracking-[0.2em] text-slate-500 bg-white/5 sticky left-0 z-20">
              Testing Standard
            </th>
            {labs.map((lab) => (
              <th key={lab.id} className="p-6 text-center min-w-[100px] max-w-[120px]">
                <div className="text-sm font-black uppercase tracking-[0.1em] text-white leading-tight break-words">
                  {lab.business_name}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {standards.map((std) => (
            <tr key={std.id} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
              <td className="p-6 sticky left-0 z-10 bg-[#0a0a0b] group-hover:bg-[#111112]">
                <div className="flex flex-col">
                  <span className="text-lg font-bold text-blue-400 font-mono tracking-tight">{std.code}</span>
                  <span className="text-sm text-slate-400 font-medium leading-tight max-w-[280px] mt-2">{std.name}</span>
                </div>
              </td>
              {labs.map((lab) => {
                const isCapable = lab.capabilities.includes(std.id);
                return (
                  <td key={`${lab.id}-${std.id}`} className="p-6 text-center">
                    {isCapable ? (
                      <div className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="3">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    ) : (
                      <div className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-white/10 text-slate-500">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="3">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M18 12H6" />
                        </svg>
                      </div>
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StandardMatrix;
