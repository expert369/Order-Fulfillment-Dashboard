import { cn } from '@/lib/utils';
import { CSSProperties, ReactNode } from 'react';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
}

export function GlassCard({ children, className, style }: GlassCardProps) {
  return (
    <div
      style={style}
      className={cn(
        'backdrop-blur-[var(--blur-glass)] bg-glass-bg-soft border-glass-border',
        'border rounded-xl shadow-md shadow-black/5',
        'transition duration-200 ease-expo-out',
        className
      )}
    >
      {children}
    </div>
  );
}