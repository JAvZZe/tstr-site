import React from 'react';

const LabManagerTeaser: React.FC = () => {
  return (
    <div className="relative overflow-hidden bg-[#0a0a0a] border border-white/10 rounded-[2.5rem] p-8 md:p-12 shadow-2xl group transition-all duration-700 hover:border-blue-500/30">
      {/* Ambient backgrounds */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/10 blur-[80px] rounded-full -mr-20 -mt-20 group-hover:bg-blue-600/20 transition-all duration-700"></div>
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-indigo-600/5 blur-[100px] rounded-full -ml-20 -mb-20 transition-all duration-700"></div>

      <div className="relative z-10 flex flex-col lg:flex-row items-center gap-12">
        {/* Left Side: Content */}
        <div className="flex-1 space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full text-blue-400 text-[10px] font-black uppercase tracking-[0.25em]">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span>
            Lab Manager Portal
          </div>
          
          <h2 className="text-4xl md:text-5xl font-black text-white tracking-tighter leading-none uppercase">
            Control Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Digital Presence</span>
          </h2>
          
          <p className="text-slate-400 text-lg md:text-xl font-light leading-relaxed max-w-xl">
            Unclaimed profiles lose 85% of high-intent technical leads. Take control of your facility's reputation, verify your standards, and access direct RFQ management.
          </p>

          <ul className="space-y-4">
            {[
              "Verified Accuracy Badge",
              "Direct RFQ Management Dashboard",
              "Advanced Search Appearance Metrics",
              "Standard Compliance Verification"
            ].map((item, i) => (
              <li key={i} className="flex items-center gap-4 text-slate-300 font-bold uppercase text-[10px] tracking-widest">
                <div className="w-5 h-5 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="3">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                {item}
              </li>
            ))}
          </ul>

          <div className="pt-4">
            <a 
              href="/claim" 
              className="inline-block px-10 py-5 bg-white text-black text-xs font-black uppercase tracking-[0.2em] rounded-2xl hover:bg-blue-500 hover:text-white transition-all transform hover:scale-105 shadow-xl"
            >
              Claim Your Free Profile
            </a>
          </div>
        </div>

        {/* Right Side: Visual Teaser (Locked Portal) */}
        <div className="w-full lg:w-[450px] shrink-0">
          <div className="relative p-1 bg-gradient-to-br from-white/10 via-white/5 to-transparent rounded-[2rem]">
            <div className="bg-[#050505] rounded-[1.9rem] p-6 border border-white/5 relative overflow-hidden aspect-[4/3] flex flex-col gap-4">
              {/* Simulated Dashboard Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/30"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/30"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/30"></div>
                </div>
                <div className="h-4 w-32 bg-white/5 rounded-full"></div>
              </div>

              {/* Blurred Stats */}
              <div className="grid grid-cols-2 gap-4 blur-[4px] opacity-20 pointer-events-none transition-all duration-1000 group-hover:blur-[2px] group-hover:opacity-30">
                <div className="h-24 bg-blue-500/10 rounded-2xl border border-white/5"></div>
                <div className="h-24 bg-emerald-500/10 rounded-2xl border border-white/5"></div>
                <div className="h-32 col-span-2 bg-white/5 rounded-2xl border border-white/5 px-6 py-4 flex flex-col gap-3">
                    <div className="h-2 w-3/4 bg-white/10 rounded-full"></div>
                    <div className="h-2 w-1/2 bg-white/5 rounded-full"></div>
                    <div className="mt-auto h-4 w-full bg-white/5 rounded-full overflow-hidden">
                        <div className="h-full w-[60%] bg-blue-500/20"></div>
                    </div>
                </div>
              </div>

              {/* Overlay Lock */}
              <div className="absolute inset-0 flex flex-col items-center justify-center z-20">
                <div className="w-20 h-20 rounded-3xl bg-blue-600/20 border-2 border-blue-500/40 backdrop-blur-md flex items-center justify-center text-blue-400 shadow-[0_0_30px_rgba(37,99,235,0.3)] animate-bounce-subtle">
                  <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <p className="mt-6 text-blue-400 font-black uppercase text-[10px] tracking-[0.3em] bg-blue-500/10 px-4 py-2 rounded-full border border-blue-500/20">
                  Access Restricted
                </p>
              </div>

              {/* Dynamic noise texture */}
              <div className="absolute inset-0 opacity-[0.03] pointer-events-none mix-blend-overlay bg-[url('https://grainy-gradients.vercel.app/noise.svg')]"></div>
            </div>
          </div>
        </div>
      </div>
      
      <style>{`
        @keyframes bounce-subtle {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-5px); }
        }
        .animate-bounce-subtle {
          animation: bounce-subtle 3s infinite ease-in-out;
        }
      `}</style>
    </div>
  );
};

export default LabManagerTeaser;
