import { FrappeProvider } from 'frappe-react-sdk';

import { Dashboard } from './components/layout/Dashboard';
import { useOrderFulfillmentStore } from './store/orderFulfillmentStore';
import { useEffect } from 'react';

function App() {
  const fetchOrders = useOrderFulfillmentStore(state => state.fetchOrders);
  
  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  return (
    <FrappeProvider>
      <Dashboard />
    </FrappeProvider>
  );
}

export default App