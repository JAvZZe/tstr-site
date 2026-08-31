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
      <div className="animate-fade-in bg-orange-500 px-4 py-2 text-center text-white">
        <p className="text-sm font-semibold md:text-base">✨ {message}</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden border-b border-orange-400/20 bg-orange-500 px-1 py-0 text-white shadow-md transition-all duration-300">
      <div className="mx-auto flex min-h-[36px] max-w-4xl flex-col items-center justify-center gap-x-6 gap-y-0.5 lg:flex-row">
        <div className="flex-shrink-0 text-center lg:text-left">
          <div className="flex flex-col gap-0 lg:flex-row lg:items-center lg:gap-2">
            <span className="text-[12px] font-black uppercase leading-none tracking-tighter md:text-[13px]">
              Join Our Newsletter
            </span>
            <span className="hidden text-white/30 lg:inline">|</span>
            <span className="text-[10px] font-medium leading-none tracking-tight text-white/80 md:text-[11px]">
              Industry testing updates
            </span>
          </div>
        </div>

        <form
          onSubmit={handleSubmit}
          className="flex w-full flex-col items-center justify-center gap-1 sm:flex-row lg:w-auto"
        >
          <input
            required
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            disabled={status === 'loading'}
            className="h-7 w-full rounded border border-orange-400/20 bg-orange-600/30 px-1.5 py-0.5 text-[11px] text-white transition-all placeholder:text-orange-100/50 focus:outline-none focus:ring-1 focus:ring-white/50 sm:w-24"
          />
          <input
            required
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            disabled={status === 'loading'}
            className="h-7 w-full rounded border border-orange-400/20 bg-orange-600/30 px-1.5 py-0.5 text-[11px] text-white transition-all placeholder:text-orange-100/50 focus:outline-none focus:ring-1 focus:ring-white/50 sm:w-24"
          />
          <input
            required
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={status === 'loading'}
            className="h-7 w-full rounded border border-orange-400/20 bg-orange-600/30 px-1.5 py-0.5 text-[11px] text-white transition-all placeholder:text-orange-100/50 focus:outline-none focus:ring-1 focus:ring-white/50 sm:w-40"
          />
          <button
            type="submit"
            disabled={status === 'loading'}
            className="flex h-7 w-full items-center justify-center whitespace-nowrap rounded bg-white px-2.5 text-[11px] font-bold text-orange-600 shadow-sm transition-all hover:bg-orange-50 sm:w-auto"
          >
            {status === 'loading' ? (
              <svg className="mr-1 h-3 w-3 animate-spin" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
            ) : null}
            Subscribe
          </button>
        </form>
      </div>
      {status === 'error' && (
        <p className="pb-0.5 text-center text-[9px] italic text-orange-100">⚠️ {message}</p>
      )}
    </div>
  );
}
