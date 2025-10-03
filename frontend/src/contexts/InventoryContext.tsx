import { createContext, useContext, useEffect, useState } from 'react';
import { InventoryItem, mapItemResponseToInventory } from '../models/item';
import { fetchItems } from '../services/items.service';

interface InventoryContextValue {
  items: InventoryItem[];
  loading: boolean;
  error: string | null;
  refresh: () => void;
}

const InventoryContext = createContext<InventoryContextValue | undefined>(undefined);

export function InventoryProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const data = await fetchItems();
      setItems(data.map(mapItemResponseToInventory));
      setError(null);
    } catch (err: any) {
      setError(err.message ?? 'Failed to load inventory');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load(); // load once when the app starts
  }, []);

  return (
    <InventoryContext.Provider value={{ items, loading, error, refresh: load }}>
      {children}
    </InventoryContext.Provider>
  );
}

export function useInventoryContext() {
  const ctx = useContext(InventoryContext);
  if (!ctx) {
    throw new Error('useInventoryContext must be used inside <InventoryProvider>');
  }
  return ctx;
}
