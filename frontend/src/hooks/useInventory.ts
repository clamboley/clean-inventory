import { useEffect, useState } from 'react';
import { fetchItems } from '../services/items.service';
import { InventoryItem, ItemResponse } from '../models/item';

export function useInventory() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const backendItems: ItemResponse[] = await fetchItems();

        const mapped: InventoryItem[] = backendItems.map((item) => {
          let ownerInitials: string = item.owner
            .split('@')[0]
            .split('.')
            .map((part) => part[0])
            .join('')
            .toUpperCase();

          return {
            id: item.id,
            item: item.name,
            category: item.category,
            serialNumber1: item.serial_number_1,
            serialNumber2: item.serial_number_2,
            serialNumber3: item.serial_number_3,
            ownerEmail: item.owner,
            ownerInitials: ownerInitials,
            location: item.location,
          };
        });

        setItems(mapped);
      } catch (err: any) {
        console.error(err);
        setError(err.message || 'Failed to load inventory');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return { items, loading, error };
}
