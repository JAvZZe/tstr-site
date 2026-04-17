import React, { useState, useEffect } from 'react';

interface ContactLabModalProps {
  listingId?: string;
  labName?: string;
  preferredStandard?: string;
  preferredIndustry?: string;
}

export default function ContactLabModal({ 
  listingId, 
  labName = "Global Technical Registry", 
  preferredStandard,
  preferredIndustry 
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
      : `Hi TSTR Team,\n\nI am looking for a qualified laboratory for ${preferredStandard ? preferredStandard + ' ' : 'technical'} testing within the ${preferredIndustry ? preferredIndustry : ''} industry.\n\nPlease help me identify verified facilities that meet these requirements.\n\nThank you.`
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
      setFormData(prev => ({ ...prev, industry: preferredIndustry }));
    }
  }, [preferredIndustry]);

  const industries = [
    'Oil & Gas', 'Biopharma', 'Pharmaceutical', 'Environmental', 
    'Materials Testing', 'Hydrogen Infrastructure', 'Aerospace', 
    'Automotive', 'Renewable Energy', 'Other'
  ];

  const roles = [
    'Procurement Manager', 'Senior Engineer', 'Project Manager', 
    'Lab Director', 'QA/QC Manager', 'Consultant', 'Owner/CEO', 'Other'
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch('/api/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ listingId, ...formData })
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
        message: ''
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
          boxShadow: '0 4px 15px rgba(0,0,80,0.2)'
        }}
      >
        Request Quote / Contact Lab
      </button>
    );
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="p-6 bg-gradient-to-r from-[#000080] to-[#32CD32] text-white flex justify-between items-center">
          <h2 className="text-2xl font-bold">Contact {labName}</h2>
          <button 
            onClick={() => setIsOpen(false)}
            className="text-white hover:text-gray-200 text-3xl font-light leading-none"
          >
            &times;
          </button>
        </div>

        {/* Content */}
        <div className="p-8 overflow-y-auto">
          {isSuccess ? (
            <div className="text-center py-8">
              <div className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6 text-4xl">
                ✓
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Request Sent Successfully!</h3>
              <p className="text-gray-600 mb-8">
                The lab has been notified of your request. They will contact you directly at <strong>{formData.email}</strong>.
              </p>
              
              <div className="bg-blue-50 p-6 rounded-xl border border-blue-100 text-left">
                <h4 className="font-bold text-blue-900 mb-2">Want to track your requests?</h4>
                <p className="text-blue-800 text-sm mb-4">
                  Register for a free Buyer Account to manage all your RFQs, save favorite labs, and access exclusive industry whitepapers.
                </p>
                <a 
                  href={`/login?redirect_to=${encodeURIComponent(window.location.pathname)}`}
                  className="inline-block bg-[#000080] text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-900 transition-colors"
                >
                  Create Buyer Account
                </a>
              </div>
              
              <button 
                onClick={() => setIsOpen(false)}
                className="mt-8 text-gray-500 hover:text-gray-700 font-medium"
              >
                Close Window
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <p className="text-gray-600 text-sm">
                Fill out the form below to send a direct enquiry to the lab. Your data is protected and will only be shared with the selected service provider.
              </p>

              {error && (
                <div className="bg-red-50 text-red-700 p-4 rounded-lg border border-red-200">
                  {error}
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name *</label>
                  <input 
                    required
                    type="text"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#32CD32] focus:border-transparent"
                    placeholder="John Doe"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Business Email *</label>
                  <input 
                    required
                    type="email"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#32CD32] focus:border-transparent"
                    placeholder="john@company.com"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-1">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Company Name</label>
                  <input 
                    type="text"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#32CD32] focus:border-transparent"
                    placeholder="Acme Corp"
                    value={formData.company}
                    onChange={(e) => setFormData({...formData, company: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Industry *</label>
                  <select 
                    required
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#32CD32] focus:border-transparent bg-white"
                    value={formData.industry}
                    onChange={(e) => setFormData({...formData, industry: e.target.value})}
                  >
                    <option value="">Select Industry</option>
                    {industries.map(i => <option key={i} value={i}>{i}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Your Role *</label>
                  <select 
                    required
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#32CD32] focus:border-transparent bg-white"
                    value={formData.role}
                    onChange={(e) => setFormData({...formData, role: e.target.value})}
                  >
                    <option value="">Select Role</option>
                    {roles.map(r => <option key={r} value={r}>{r}</option>)}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Requirements / Message *</label>
                <textarea 
                  required
                  rows={4}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#32CD32] focus:border-transparent"
                  value={formData.message}
                  onChange={(e) => setFormData({...formData, message: e.target.value})}
                />
              </div>

              <div className="pt-4 flex flex-col md:flex-row gap-4">
                <button 
                  disabled={isSubmitting}
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-[#000080] to-[#32CD32] text-white py-4 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50"
                >
                  {isSubmitting ? 'Sending Request...' : 'Send Request for Quote'}
                </button>
                <button 
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="px-8 py-4 border border-gray-300 rounded-xl font-semibold text-gray-600 hover:bg-gray-50 transition-colors"
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
