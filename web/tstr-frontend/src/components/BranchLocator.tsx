import React from 'react';
import TrustBadge from './TrustBadge';

interface Branch {
  id: string;
  business_name: string;
  slug: string;
  region: string;
  verified: boolean;
  address?: string;
}

interface BranchLocatorProps {
  branches: Branch[];
  groupName: string;
}

const BranchLocator: React.FC<BranchLocatorProps> = ({ branches, groupName }) => {
  if (!branches || branches.length === 0) return null;

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {branches.map((branch) => (
        <a 
          key={branch.id}
          href={`/company/${branch.slug}`} 
          className="group relative bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-xl hover:border-blue-400 transition-all duration-300"
        >
          <div className="flex flex-col h-full">
            <div className="mb-4 flex justify-between items-start">
              <span className="text-[10px] font-black text-blue-500 uppercase tracking-widest">{branch.region}</span>
              {branch.verified && <TrustBadge level="verified" size="sm" />}
            </div>
            
            <h3 className="text-xl font-extrabold text-gray-900 group-hover:text-blue-600 mb-2 leading-tight">
              {branch.business_name}
            </h3>
            
            {branch.address && (
              <p className="text-sm text-gray-500 mb-4 line-clamp-2">
                📍 {branch.address}
              </p>
            )}

            <div className="mt-auto pt-4 flex items-center justify-between border-t border-gray-50">
              <span className="text-xs font-bold text-blue-600 group-hover:translate-x-1 transition-transform">
                View Full Capabilities →
              </span>
              <div className="flex -space-x-2">
                <div className="w-6 h-6 rounded-full bg-blue-100 border-2 border-white flex items-center justify-center text-[8px] font-bold text-blue-600">
                  ISO
                </div>
              </div>
            </div>
          </div>
        </a>
      ))}
    </div>
  );
};

export default BranchLocator;
