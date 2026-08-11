import { useOrderFulfillmentStore } from '@/store/orderFulfillmentStore';
import { GlassPanel } from '@/components/ui/GlassPanel';
import { formatTime } from '@/lib/utils';
import { cn } from '@/lib/utils';
import { useState } from 'react';

function MenuIcon() {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  );
}

function FullscreenIcon() {
  return (
    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V6a2 2 0 012-2h2m4 0h8a2 2 0 012 2v8m-4 4h2a2 2 0 002-2v-2m0-8h2m-18 2v8a2 2 0 002 2h2" />
    </svg>
  );
}

function ExitFullscreenIcon() {
  return (
    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 9V4M9 9H4M15 9h5M15 9V4m0 5v5m0 0h5m-5 0v5m0 0v5m0-5H9m6 0H9" />
    </svg>
  );
}

const iconButton = cn(
  'flex h-9 w-9 items-center justify-center rounded-lg border border-glass-border',
  'bg-glass-bg-soft text-ink-muted transition-all duration-150 ease-expo-out',
  'hover:bg-glass-bg hover:text-ink-strong active:scale-[0.95]'
);

export function Header() {
  const { loading, lastUpdated, fetchOrders, autoRefresh, setAutoRefresh, setSidebarOpen } =
    useOrderFulfillmentStore();
  const [isFullscreen, setIsFullscreen] = useState(false);

  const toggleFullscreen = async () => {
    try {
      if (document.fullscreenElement) {
        await document.exitFullscreen();
        setIsFullscreen(false);
      } else {
        await document.documentElement.requestFullscreen();
        setIsFullscreen(true);
      }
    } catch {
      setIsFullscreen(!!document.fullscreenElement);
    }
  };

  return (
    <header className="flex flex-col gap-3 px-4 pb-3 pt-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 sm:pt-5">
      <div className="flex min-w-0 items-center gap-3">
        <button
          onClick={() => setSidebarOpen(true)}
          aria-label="Open navigation"
          className={cn(iconButton, 'lg:hidden')}
        >
          <MenuIcon />
        </button>
        <div className="min-w-0">
          <h1 className="truncate text-xl font-semibold text-ink-strong sm:text-2xl">
            Order Fulfillment Dashboard
          </h1>
          <p className="text-sm text-ink-muted">Real-time warehouse monitoring</p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <GlassPanel variant="secondary" className="flex items-center gap-2 px-3 py-1.5">
          <span className="text-xs text-ink-muted">Last updated</span>
          <span className="text-xs font-mono tabular-nums text-ink-strong">
            {lastUpdated ? formatTime(lastUpdated) : '—'}
          </span>
        </GlassPanel>

        <button
          role="switch"
          aria-checked={autoRefresh}
          aria-label="Toggle auto refresh"
          onClick={() => setAutoRefresh(!autoRefresh)}
          className="group flex items-center gap-2"
        >
          <span
            className={cn(
              'relative h-5 w-9 rounded-full border transition-colors duration-200 ease-expo-out',
              autoRefresh
                ? 'border-brand bg-brand'
                : 'border-glass-border-strong bg-glass-bg-strong'
            )}
          >
            <span
              className={cn(
                'absolute top-1/2 h-3.5 w-3.5 -translate-y-1/2 rounded-full bg-white shadow transition-transform duration-200 ease-expo-out',
                autoRefresh ? 'left-[18px]' : 'left-1'
              )}
            />
          </span>
          <span className="text-sm text-ink-muted group-hover:text-ink">Auto Refresh</span>
        </button>

        <button
          onClick={toggleFullscreen}
          aria-label={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'}
          className={iconButton}
        >
          {isFullscreen ? <ExitFullscreenIcon /> : <FullscreenIcon />}
        </button>

        <button
          onClick={fetchOrders}
          disabled={loading}
          className={cn(
            'flex items-center gap-2 rounded-lg bg-brand px-4 py-2 text-sm font-medium text-white',
            'shadow-lg shadow-brand/30 transition-all duration-150 ease-expo-out',
            'hover:bg-brand-hover active:scale-[0.97]',
            'disabled:cursor-not-allowed disabled:opacity-50'
          )}
        >
          {loading ? (
            <>
              <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Refreshing...
            </>
          ) : (
            <>
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Refresh
            </>
          )}
        </button>
      </div>
    </header>
  );
}