import React from 'react';
import TrustBadge from './TrustBadge';

interface Capability {
  id: string;
  verified: boolean;
  notes?: string;
  standard: {
    code: string;
    name: string;
    description?: string;
  };
}

interface ComplianceMatrixProps {
  capabilities: Capability[];
}

const ComplianceMatrix: React.FC<ComplianceMatrixProps> = ({ capabilities }) => {
  if (!capabilities || capabilities.length === 0) {
    return (
      <div className="p-8 text-center bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
        <p className="text-gray-500">No verified capabilities listed for this facility.</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="p-4 font-bold text-gray-700 text-sm uppercase tracking-wider">Standard / Code</th>
              <th className="p-4 font-bold text-gray-700 text-sm uppercase tracking-wider">Scope of Accreditation</th>
              <th className="p-4 font-bold text-gray-700 text-sm uppercase tracking-wider text-center">Trust Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {capabilities.map((cap) => (
              <tr key={cap.id} className="hover:bg-blue-50/30 transition-colors">
                <td className="p-4 align-top">
                  <div className="font-mono font-bold text-blue-700">{cap.standard.code}</div>
                </td>
                <td className="p-4 align-top">
                  <div className="font-bold text-gray-900 mb-1">{cap.standard.name}</div>
                  {cap.standard.description && (
                    <p className="text-xs text-gray-500 leading-relaxed">{cap.standard.description}</p>
                  )}
                  {cap.notes && (
                    <div className="mt-2 p-2 bg-yellow-50 text-yellow-800 text-[10px] rounded border border-yellow-100 italic">
                      Note: {cap.notes}
                    </div>
                  )}
                </td>
                <td className="p-4 align-middle text-center">
                  <TrustBadge level={cap.verified ? 'verified' : 'aggregated'} size="md" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="bg-gray-50 p-3 text-[10px] text-gray-400 border-t border-gray-100 text-center">
        * TSTR Verified means documentation has been reviewed by our technical team.
      </div>
    </div>
  );
};

export default ComplianceMatrix;
