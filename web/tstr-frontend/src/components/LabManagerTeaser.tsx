import React from 'react';

const LabManagerTeaser: React.FC = () => {
  return (
    <div className="group relative overflow-hidden rounded-[2.5rem] border border-white/10 bg-[#0a0a0a] p-8 shadow-2xl transition-all duration-700 hover:border-blue-500/30 md:p-12">
      {/* Ambient backgrounds */}
      <div className="absolute right-0 top-0 -mr-20 -mt-20 h-64 w-64 rounded-full bg-blue-600/10 blur-[80px] transition-all duration-700 group-hover:bg-blue-600/20"></div>
      <div className="absolute bottom-0 left-0 -mb-20 -ml-20 h-64 w-64 rounded-full bg-indigo-600/5 blur-[100px] transition-all duration-700"></div>

      <div className="relative z-10 flex flex-col items-center gap-12 lg:flex-row">
        {/* Left Side: Content */}
        <div className="flex-1 space-y-8">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-2 text-[10px] font-black uppercase tracking-[0.25em] text-blue-400">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-blue-500"></span>
            Lab Manager Portal
          </div>

          <h2 className="text-4xl font-black uppercase leading-none tracking-tighter text-white md:text-5xl">
            Control Your{' '}
            <span className="bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              Digital Presence
            </span>
          </h2>

          <p className="max-w-xl text-lg font-light leading-relaxed text-slate-400 md:text-xl">
            Unclaimed profiles lose 85% of high-intent technical leads. Take control of your
            facility&#39;s reputation, verify your standards, and access direct RFQ management.
          </p>

          <ul className="space-y-4">
            {[
              'Verified Accuracy Badge',
              'Direct RFQ Management Dashboard',
              'Advanced Search Appearance Metrics',
              'Standard Compliance Verification',
            ].map((item, i) => (
              <li
                key={i}
                className="flex items-center gap-4 text-[10px] font-bold uppercase tracking-widest text-slate-300"
              >
                <div className="flex h-5 w-5 items-center justify-center rounded-lg border border-emerald-500/30 bg-emerald-500/20 text-emerald-400">
                  <svg
                    className="h-3 w-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    strokeWidth="3"
                  >
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
              className="inline-block transform rounded-2xl bg-white px-10 py-5 text-xs font-black uppercase tracking-[0.2em] text-black shadow-xl transition-all hover:scale-105 hover:bg-blue-500 hover:text-white"
            >
              Claim Your Free Profile
            </a>
          </div>
        </div>

        {/* Right Side: Visual Teaser (Locked Portal) */}
        <div className="w-full shrink-0 lg:w-[450px]">
          <div className="relative rounded-[2rem] bg-gradient-to-br from-white/10 via-white/5 to-transparent p-1">
            <div className="relative flex aspect-[4/3] flex-col gap-4 overflow-hidden rounded-[1.9rem] border border-white/5 bg-[#050505] p-6">
              {/* Simulated Dashboard Header */}
              <div className="mb-4 flex items-center justify-between">
                <div className="flex gap-2">
                  <div className="h-3 w-3 rounded-full border border-red-500/30 bg-red-500/20"></div>
                  <div className="h-3 w-3 rounded-full border border-yellow-500/30 bg-yellow-500/20"></div>
                  <div className="h-3 w-3 rounded-full border border-green-500/30 bg-green-500/20"></div>
                </div>
                <div className="h-4 w-32 rounded-full bg-white/5"></div>
              </div>

              {/* Blurred Stats */}
              <div className="pointer-events-none grid grid-cols-2 gap-4 opacity-20 blur-[4px] transition-all duration-1000 group-hover:opacity-30 group-hover:blur-[2px]">
                <div className="h-24 rounded-2xl border border-white/5 bg-blue-500/10"></div>
                <div className="h-24 rounded-2xl border border-white/5 bg-emerald-500/10"></div>
                <div className="col-span-2 flex h-32 flex-col gap-3 rounded-2xl border border-white/5 bg-white/5 px-6 py-4">
                  <div className="h-2 w-3/4 rounded-full bg-white/10"></div>
                  <div className="h-2 w-1/2 rounded-full bg-white/5"></div>
                  <div className="mt-auto h-4 w-full overflow-hidden rounded-full bg-white/5">
                    <div className="h-full w-[60%] bg-blue-500/20"></div>
                  </div>
                </div>
              </div>

              {/* Overlay Lock */}
              <div className="absolute inset-0 z-20 flex flex-col items-center justify-center">
                <div className="animate-bounce-subtle flex h-20 w-20 items-center justify-center rounded-3xl border-2 border-blue-500/40 bg-blue-600/20 text-blue-400 shadow-[0_0_30px_rgba(37,99,235,0.3)] backdrop-blur-md">
                  <svg
                    className="h-10 w-10"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    strokeWidth="2"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                    />
                  </svg>
                </div>
                <p className="mt-6 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-2 text-[10px] font-black uppercase tracking-[0.3em] text-blue-400">
                  Access Restricted
                </p>
              </div>

              {/* Dynamic noise texture */}
              <div className="pointer-events-none absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] mix-blend-overlay"></div>
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
