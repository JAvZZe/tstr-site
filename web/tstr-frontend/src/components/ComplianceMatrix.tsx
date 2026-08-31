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
      <div className="rounded-xl border-2 border-dashed border-gray-200 bg-gray-50 p-8 text-center">
        <p className="text-gray-500">No verified capabilities listed for this facility.</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-shadow hover:shadow-md">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left">
          <thead className="border-b border-gray-200 bg-gray-50">
            <tr>
              <th className="p-4 text-sm font-bold uppercase tracking-wider text-gray-700">
                Standard / Code
              </th>
              <th className="p-4 text-sm font-bold uppercase tracking-wider text-gray-700">
                Scope of Accreditation
              </th>
              <th className="p-4 text-center text-sm font-bold uppercase tracking-wider text-gray-700">
                Trust Status
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {capabilities.map((cap) => (
              <tr key={cap.id} className="transition-colors hover:bg-blue-50/30">
                <td className="p-4 align-top">
                  <div className="font-mono font-bold text-blue-700">{cap.standard.code}</div>
                </td>
                <td className="p-4 align-top">
                  <div className="mb-1 font-bold text-gray-900">{cap.standard.name}</div>
                  {cap.standard.description && (
                    <p className="text-xs leading-relaxed text-gray-500">
                      {cap.standard.description}
                    </p>
                  )}
                  {cap.notes && (
                    <div className="mt-2 rounded border border-yellow-100 bg-yellow-50 p-2 text-[10px] italic text-yellow-800">
                      Note: {cap.notes}
                    </div>
                  )}
                </td>
                <td className="p-4 text-center align-middle">
                  <TrustBadge level={cap.verified ? 'verified' : 'aggregated'} size="md" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="border-t border-gray-100 bg-gray-50 p-3 text-center text-[10px] text-gray-400">
        * TSTR Verified means documentation has been reviewed by our technical team.
      </div>
    </div>
  );
};

export default ComplianceMatrix;
