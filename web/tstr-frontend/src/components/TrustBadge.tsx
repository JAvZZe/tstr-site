import React from 'react';

interface TrustBadgeProps {
  level: 'aggregated' | 'claimed' | 'verified';
  size?: 'sm' | 'md' | 'lg';
}

const TrustBadge: React.FC<TrustBadgeProps> = ({ level, size = 'md' }) => {
  const config = {
    aggregated: {
      label: 'Public Data',
      icon: '🤖',
      classes: 'bg-gray-100 text-gray-600 border-gray-200',
      description: 'Sourced from public records. Unverified.'
    },
    claimed: {
      label: 'Claimed',
      icon: '👤',
      classes: 'bg-blue-50 text-blue-700 border-blue-200',
      description: 'Profile managed by a company representative.'
    },
    verified: {
      label: 'TSTR Verified',
      icon: '🛡️',
      classes: 'bg-green-100 text-green-800 border-green-300 font-bold shadow-sm',
      description: 'Accreditations manually verified by TSTR engineers.'
    }
  };

  const { label, icon, classes, description } = config[level];
  
  const sizeClasses = {
    sm: 'text-[10px] px-1.5 py-0.5',
    md: 'text-xs px-2.5 py-1',
    lg: 'text-sm px-4 py-2'
  };

  return (
    <div 
      className={`inline-flex items-center gap-1.5 rounded-full border ${classes} ${sizeClasses[size]} transition-all cursor-default`}
      title={description}
    >
      <span>{icon}</span>
      <span>{label}</span>
    </div>
  );
};

export default TrustBadge;
