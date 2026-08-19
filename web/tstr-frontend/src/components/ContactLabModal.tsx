import React, { useState, useEffect } from 'react';

interface ContactLabModalProps {
  listingId?: string;
  labName?: string;
  preferredStandard?: string;
  preferredIndustry?: string;
}

export default function ContactLabModal({
  listingId,
  labName = 'Global Technical Registry',
  preferredStandard,
  preferredIndustry,
}: ContactLabModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    industry: preferredIndustry || '',
    role: '',
    message: listingId
      ? `Hi ${labName},\n\nI found your facility on TSTR.directory and am interested in your ${preferredStandard ? preferredStandard + ' ' : ''}testing services.\n\nPlease provide a quote or technical contact for further discussion.\n\nThank you.`
      : `Hi TSTR Team,\n\nI am looking for a qualified laboratory for ${preferredStandard ? preferredStandard + ' ' : 'technical'} testing within the ${preferredIndustry ? preferredIndustry : ''} industry.\n\nPlease help me identify verified facilities that meet these requirements.\n\nThank you.`,
  });

  // Handle URL Hash triggering (#rfq)
  useEffect(() => {
    const handleHashChange = () => {
      if (window.location.hash === '#rfq') {
        setIsOpen(true);
      }
    };

    // Initial check
    if (window.location.hash === '#rfq') {
      setIsOpen(true);
    }

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  // Update form if props change
  useEffect(() => {
    if (preferredIndustry) {
      setFormData((prev) => ({ ...prev, industry: preferredIndustry }));
    }
  }, [preferredIndustry]);

  const industries = [
    'Oil & Gas',
    'Biopharma',
    'Pharmaceutical',
    'Environmental',
    'Materials Testing',
    'Hydrogen Infrastructure',
    'Aerospace',
    'Automotive',
    'Renewable Energy',
    'Other',
  ];

  const roles = [
    'Procurement Manager',
    'Senior Engineer',
    'Project Manager',
    'Lab Director',
    'QA/QC Manager',
    'Consultant',
    'Owner/CEO',
    'Other',
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      // Posts to the gated RFQ endpoint: the enquiry reaches us first and we
      // forward it to the lab. /api/leads emailed the lab directly, which broke
      // the model we operate on.
      const response = await fetch('/api/rfq', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          listing_id: listingId,
          buyer_name: formData.name,
          buyer_email: formData.email,
          buyer_company: formData.company,
          buyer_role: formData.role,
          sector: formData.industry,
          standard: preferredStandard,
          service_needed: preferredStandard
            ? `${preferredStandard} testing`
            : `${formData.industry || 'Testing'} enquiry`,
          message: formData.message,
        }),
      });

      const result = await response.json();

      if (!response.ok) throw new Error(result.error || 'Failed to submit request');

      setIsSuccess(true);
      // Reset form
      setFormData({
        name: '',
        email: '',
        company: '',
        industry: '',
        role: '',
        message: '',
      });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="btn btn-primary w-full md:w-auto"
        style={{
          background: 'linear-gradient(135deg, #000080 0%, #32CD32 100%)',
          color: 'white',
          padding: '1rem 2rem',
          borderRadius: '8px',
          fontWeight: 'bold',
          fontSize: '1.1rem',
          marginTop: '1.5rem',
          boxShadow: '0 4px 15px rgba(0,0,80,0.2)',
        }}
      >
        Request Quote / Contact Lab
      </button>
    );
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4 backdrop-blur-sm">
      <div className="flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl bg-white shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between bg-gradient-to-r from-[#000080] to-[#32CD32] p-6 text-white">
          <h2 className="text-2xl font-bold">Contact {labName}</h2>
          <button
            onClick={() => setIsOpen(false)}
            className="text-3xl font-light leading-none text-white hover:text-gray-200"
          >
            &times;
          </button>
        </div>

        {/* Content */}
        <div className="overflow-y-auto p-8">
          {isSuccess ? (
            <div className="py-8 text-center">
              <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-green-100 text-4xl text-green-600">
                ✓
              </div>
              <h3 className="mb-2 text-2xl font-bold text-gray-900">Request Sent Successfully!</h3>
              <p className="mb-8 text-gray-600">
                The lab has been notified of your request. They will contact you directly at{' '}
                <strong>{formData.email}</strong>.
              </p>

              <div className="rounded-xl border border-blue-100 bg-blue-50 p-6 text-left">
                <h4 className="mb-2 font-bold text-blue-900">Want to track your requests?</h4>
                <p className="mb-4 text-sm text-blue-800">
                  Register for a free Buyer Account to manage all your RFQs, save favorite labs, and
                  access exclusive industry whitepapers.
                </p>
                <a
                  href={`/login?redirect_to=${encodeURIComponent(window.location.pathname)}`}
                  className="inline-block rounded-lg bg-[#000080] px-6 py-2 font-semibold text-white transition-colors hover:bg-blue-900"
                >
                  Create Buyer Account
                </a>
              </div>

              <button
                onClick={() => setIsOpen(false)}
                className="mt-8 font-medium text-gray-500 hover:text-gray-700"
              >
                Close Window
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <p className="text-sm text-gray-600">
                Fill out the form below to send a direct enquiry to the lab. Your data is protected
                and will only be shared with the selected service provider.
              </p>

              {error && (
                <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
                  {error}
                </div>
              )}

              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm font-semibold text-gray-700">
                    Full Name *
                  </label>
                  <input
                    required
                    type="text"
                    className="w-full rounded-lg border border-gray-300 p-3 focus:border-transparent focus:ring-2 focus:ring-[#32CD32]"
                    placeholder="John Doe"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </div>
                <div>
                  <label className="mb-2 block text-sm font-semibold text-gray-700">
                    Business Email *
                  </label>
                  <input
                    required
                    type="email"
                    className="w-full rounded-lg border border-gray-300 p-3 focus:border-transparent focus:ring-2 focus:ring-[#32CD32]"
                    placeholder="john@company.com"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
                <div className="md:col-span-1">
                  <label className="mb-2 block text-sm font-semibold text-gray-700">
                    Company Name
                  </label>
                  <input
                    type="text"
                    className="w-full rounded-lg border border-gray-300 p-3 focus:border-transparent focus:ring-2 focus:ring-[#32CD32]"
                    placeholder="Acme Corp"
                    value={formData.company}
                    onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                  />
                </div>
                <div>
                  <label className="mb-2 block text-sm font-semibold text-gray-700">
                    Industry *
                  </label>
                  <select
                    required
                    className="w-full rounded-lg border border-gray-300 bg-white p-3 focus:border-transparent focus:ring-2 focus:ring-[#32CD32]"
                    value={formData.industry}
                    onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                  >
                    <option value="">Select Industry</option>
                    {industries.map((i) => (
                      <option key={i} value={i}>
                        {i}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="mb-2 block text-sm font-semibold text-gray-700">
                    Your Role *
                  </label>
                  <select
                    required
                    className="w-full rounded-lg border border-gray-300 bg-white p-3 focus:border-transparent focus:ring-2 focus:ring-[#32CD32]"
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  >
                    <option value="">Select Role</option>
                    {roles.map((r) => (
                      <option key={r} value={r}>
                        {r}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-gray-700">
                  Requirements / Message *
                </label>
                <textarea
                  required
                  rows={4}
                  className="w-full rounded-lg border border-gray-300 p-3 focus:border-transparent focus:ring-2 focus:ring-[#32CD32]"
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                />
              </div>

              <div className="flex flex-col gap-4 pt-4 md:flex-row">
                <button
                  disabled={isSubmitting}
                  type="submit"
                  className="flex-1 rounded-xl bg-gradient-to-r from-[#000080] to-[#32CD32] py-4 text-lg font-bold text-white shadow-lg transition-all hover:shadow-xl disabled:opacity-50"
                >
                  {isSubmitting ? 'Sending Request...' : 'Send Request for Quote'}
                </button>
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="rounded-xl border border-gray-300 px-8 py-4 font-semibold text-gray-600 transition-colors hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
