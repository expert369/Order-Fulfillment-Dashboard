import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface GlassPanelProps {
  children: ReactNode;
  className?: string;
  variant?: 'primary' | 'secondary';
}

export function GlassPanel({ children, className, variant = 'primary' }: GlassPanelProps) {
  const baseStyles = `
    backdrop-blur-[var(--blur-glass)]
    border
    rounded-xl
    transition-colors duration-200 ease-expo-out
  `;

  const variantStyles = {
    primary: 'bg-glass-bg border-glass-border-strong shadow-lg shadow-black/10',
    secondary: 'bg-glass-bg-soft border-glass-border shadow-md shadow-black/5',
  };

  return (
    <div className={cn(baseStyles, variantStyles[variant], className)}>
      {children}
    </div>
  );
}