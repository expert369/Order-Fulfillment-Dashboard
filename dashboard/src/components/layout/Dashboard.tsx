import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { MainContent } from './MainContent';
import { useOrderFulfillmentStore } from '@/store/orderFulfillmentStore';
import { cn } from '@/lib/utils';
import { useEffect } from 'react';

export function Dashboard() {
  const { sidebarOpen, setSidebarOpen } = useOrderFulfillmentStore();

  useEffect(() => {
    if (!sidebarOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setSidebarOpen(false);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [sidebarOpen, setSidebarOpen]);

  return (
    <div className="relative flex h-full overflow-hidden bg-surface">
      <div aria-hidden="true" className="pointer-events-none absolute inset-0">
        <div className="absolute -top-40 -left-40 h-[28rem] w-[28rem] rounded-full bg-glow-purple blur-3xl" />
        <div className="absolute -bottom-48 -right-32 h-[30rem] w-[30rem] rounded-full bg-glow-blue blur-3xl" />
      </div>

      <Sidebar className="hidden lg:flex" />

      <div
        className={cn(
          'fixed inset-0 z-50 lg:hidden',
          sidebarOpen ? 'pointer-events-auto' : 'pointer-events-none'
        )}
        aria-hidden={!sidebarOpen}
        {...((!sidebarOpen ? { inert: true } : {}) as Record<string, unknown>)}
      >
        <div
          aria-hidden="true"
          onClick={() => setSidebarOpen(false)}
          className={cn(
            'absolute inset-0 bg-black/50 backdrop-blur-sm transition-opacity duration-200 ease-expo-out',
            sidebarOpen ? 'opacity-100' : 'opacity-0'
          )}
        />
        <div
          role="dialog"
          aria-modal="true"
          aria-label="Order filters"
          className={cn(
            'absolute inset-y-0 left-0 w-4/5 max-w-[320px] transition-transform duration-200 ease-expo-out',
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          )}
        >
          <Sidebar />
        </div>
      </div>

      <div className="relative flex min-w-0 flex-1 flex-col">
        <Header />
        <MainContent />
      </div>
    </div>
  );
}