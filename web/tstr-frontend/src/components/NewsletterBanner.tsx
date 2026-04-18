import React, { useState } from 'react';

export default function NewsletterBanner() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (status === 'loading') return;

    setStatus('loading');
    setMessage('');

    try {
      const response = await fetch('/api/newsletter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ firstName, lastName, email }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      setStatus('success');
      setMessage('Thanks for subscribing!');
      setFirstName('');
      setLastName('');
      setEmail('');
    } catch (err: any) {
      setStatus('error');
      setMessage(err.message);
    }
  };

  if (status === 'success') {
    return (
      <div className="bg-orange-500 text-white py-2 px-4 text-center animate-fade-in">
        <p className="font-semibold text-sm md:text-base">
          ✨ {message}
        </p>
      </div>
    );
  }

  return (
    <div className="bg-orange-500 text-white py-0 px-1 shadow-md transition-all duration-300 overflow-hidden border-b border-orange-400/20">
      <div className="max-w-4xl mx-auto flex flex-col lg:flex-row items-center justify-center gap-x-6 gap-y-0.5 min-h-[36px]">
        <div className="flex-shrink-0 text-center lg:text-left">
          <div className="flex flex-col lg:flex-row lg:items-center gap-0 lg:gap-2">
            <span className="font-black text-[12px] md:text-[13px] tracking-tighter uppercase leading-none">
              Join Our Newsletter
            </span>
            <span className="hidden lg:inline text-white/30">|</span>
            <span className="font-medium text-[10px] md:text-[11px] text-white/80 tracking-tight leading-none">
              Industry testing updates
            </span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-center justify-center gap-1 w-full lg:w-auto">
          <input
            required
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            disabled={status === 'loading'}
            className="w-full sm:w-24 bg-orange-600/30 border border-orange-400/20 rounded px-1.5 py-0.5 text-[11px] placeholder:text-orange-100/50 focus:outline-none focus:ring-1 focus:ring-white/50 transition-all text-white h-7"
          />
          <input
            required
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            disabled={status === 'loading'}
            className="w-full sm:w-24 bg-orange-600/30 border border-orange-400/20 rounded px-1.5 py-0.5 text-[11px] placeholder:text-orange-100/50 focus:outline-none focus:ring-1 focus:ring-white/50 transition-all text-white h-7"
          />
          <input
            required
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={status === 'loading'}
            className="w-full sm:w-40 bg-orange-600/30 border border-orange-400/20 rounded px-1.5 py-0.5 text-[11px] placeholder:text-orange-100/50 focus:outline-none focus:ring-1 focus:ring-white/50 transition-all text-white h-7"
          />
          <button
            type="submit"
            disabled={status === 'loading'}
            className="w-full sm:w-auto bg-white text-orange-600 hover:bg-orange-50 px-2.5 h-7 rounded text-[11px] font-bold shadow-sm transition-all flex items-center justify-center whitespace-nowrap"
          >
            {status === 'loading' ? (
              <svg className="animate-spin h-3 w-3 mr-1" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            ) : null}
            Subscribe
          </button>
        </form>
      </div>
      {status === 'error' && (
        <p className="text-center text-[9px] pb-0.5 text-orange-100 italic">
          ⚠️ {message}
        </p>
      )}
    </div>
  );
}
