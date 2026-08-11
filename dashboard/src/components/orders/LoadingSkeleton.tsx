import { GlassCard } from '@/components/ui/GlassCard';

interface LoadingSkeletonProps {
  count?: number;
}

export function LoadingSkeleton({ count = 6 }: LoadingSkeletonProps) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6">
      {Array.from({ length: count }).map((_, i) => (
        <GlassCard
          key={i}
          style={{ animationDelay: `${Math.min(i, 12) * 40}ms` }}
          className="relative flex flex-col gap-3 overflow-hidden p-4 animate-pulse-subtle"
        >
          <div className="absolute inset-y-0 left-0 w-[3px] rounded-l-xl bg-glass-bg-strong" />
          <div className="flex items-start justify-between gap-2 pl-1.5">
            <div className="flex-1">
              <div className="mb-1 h-3 w-10 rounded bg-glass-bg-strong animate-shimmer" />
              <div className="h-5 w-20 rounded bg-glass-bg-strong animate-shimmer" />
            </div>
            <div className="h-5 w-16 rounded-full bg-glass-bg-strong animate-shimmer" />
          </div>
          <div className="border-t border-glass-border pt-3 pl-1.5">
            <div className="mb-1.5 h-3 w-14 rounded bg-glass-bg-strong animate-shimmer" />
            <div className="h-4 w-28 rounded bg-glass-bg-strong animate-shimmer" />
          </div>
          <div className="border-t border-glass-border pt-3 pl-1.5">
            <div className="mb-1.5 h-3 w-12 rounded bg-glass-bg-strong animate-shimmer" />
            <div className="h-4 w-24 rounded bg-glass-bg-strong animate-shimmer" />
          </div>
        </GlassCard>
      ))}
    </div>
  );
}