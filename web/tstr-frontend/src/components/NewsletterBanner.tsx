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
    <div className="bg-orange-500 text-white py-1 px-4 shadow-md transition-all duration-300 overflow-hidden">
      <div className="max-w-6xl mx-auto flex flex-col xl:flex-row items-center justify-between gap-1 xl:gap-4">
        <div className="flex-shrink-0 text-center xl:text-left max-w-[240px] xl:max-w-none">
          <div className="flex flex-col xl:flex-row xl:items-center gap-0 xl:gap-2">
            <span className="font-black text-[13px] md:text-sm tracking-tighter uppercase leading-none">
              Join Our Newsletter
            </span>
            <span className="hidden xl:inline text-white/40">|</span>
            <span className="font-medium text-[11px] md:text-xs text-white/90 tracking-tight leading-none mt-0.5 xl:mt-0">
              Get the latest industry testing updates
            </span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row flex-wrap items-center justify-center gap-1.5 w-full xl:w-auto mt-1 xl:mt-0">
          <input
            required
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            disabled={status === 'loading'}
            className="w-full sm:w-32 bg-orange-600/50 border border-orange-400/50 rounded px-3 py-1 text-sm placeholder:text-orange-100 focus:outline-none focus:ring-1 focus:ring-white transition-all text-white"
          />
          <input
            required
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            disabled={status === 'loading'}
            className="w-full sm:w-32 bg-orange-600/50 border border-orange-400/50 rounded px-3 py-1 text-sm placeholder:text-orange-100 focus:outline-none focus:ring-1 focus:ring-white transition-all text-white"
          />
          <input
            required
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={status === 'loading'}
            className="w-full sm:w-48 bg-orange-600/50 border border-orange-400/50 rounded px-3 py-1 text-sm placeholder:text-orange-100 focus:outline-none focus:ring-1 focus:ring-white transition-all text-white"
          />
          <button
            type="submit"
            disabled={status === 'loading'}
            className="w-full sm:w-auto bg-white text-orange-600 hover:bg-orange-50 px-4 py-1 rounded text-sm font-bold shadow-sm transition-all flex items-center justify-center whitespace-nowrap"
          >
            {status === 'loading' ? (
              <svg className="animate-spin h-4 w-4 mr-2" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            ) : null}
            Subscribe
          </button>
        </form>
      </div>
      {status === 'error' && (
        <p className="text-center text-[10px] mt-1 text-orange-100 italic">
          ⚠️ {message}
        </p>
      )}
    </div>
  );
}
