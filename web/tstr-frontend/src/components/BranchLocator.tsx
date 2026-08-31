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
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {branches.map((branch) => (
        <a
          key={branch.id}
          href={`/company/${branch.slug}`}
          className="group relative rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-300 hover:border-blue-400 hover:shadow-xl"
        >
          <div className="flex h-full flex-col">
            <div className="mb-4 flex items-start justify-between">
              <span className="text-[10px] font-black uppercase tracking-widest text-blue-500">
                {branch.region}
              </span>
              {branch.verified && <TrustBadge level="verified" size="sm" />}
            </div>

            <h3 className="mb-2 text-xl font-extrabold leading-tight text-gray-900 group-hover:text-blue-600">
              {branch.business_name}
            </h3>

            {branch.address && (
              <p className="mb-4 line-clamp-2 text-sm text-gray-500">📍 {branch.address}</p>
            )}

            <div className="mt-auto flex items-center justify-between border-t border-gray-50 pt-4">
              <span className="text-xs font-bold text-blue-600 transition-transform group-hover:translate-x-1">
                View Full Capabilities →
              </span>
              <div className="flex -space-x-2">
                <div className="flex h-6 w-6 items-center justify-center rounded-full border-2 border-white bg-blue-100 text-[8px] font-bold text-blue-600">
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
