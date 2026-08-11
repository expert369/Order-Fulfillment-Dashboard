import { useOrderFulfillmentStore } from '@/store/orderFulfillmentStore';
import { OrderGrid } from '@/components/orders/OrderGrid';
import { EmptyState } from '@/components/orders/EmptyState';
import { ErrorState } from '@/components/orders/ErrorState';
import { LoadingSkeleton } from '@/components/orders/LoadingSkeleton';
import { GlassPanel } from '@/components/ui/GlassPanel';
import { cn } from '@/lib/utils';

export function MainContent() {
  const { orders, selectedPhase, loading, error } = useOrderFulfillmentStore();

  const visibleOrders = selectedPhase === 'all'
    ? orders
    : orders.filter(o => o.current_phase === selectedPhase);

  return (
    <main className="min-w-0 flex-1 px-4 pb-6 sm:px-6 ">
      <GlassPanel variant="primary" className="h-[86%] overflow-y-auto p-3 sm:p-4">
        {error && <ErrorState message={error} />}
        {loading && orders.length === 0 && <LoadingSkeleton count={6} />}
        {!loading && !error && visibleOrders.length === 0 && <EmptyState phase={selectedPhase} />}
        {!error && visibleOrders.length > 0 && (
          <div className={cn('transition-opacity duration-200 h-screen', loading && 'opacity-40')}>
            <OrderGrid orders={visibleOrders} />
          </div>
        )}
      </GlassPanel>
    </main>
  );
}