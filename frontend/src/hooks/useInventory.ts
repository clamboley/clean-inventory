import { useEffect, useState } from 'react';
import { fetchItems } from '../services/items.service';
import { fetchUser } from '../services/users.service';
import { InventoryItem, ItemResponse } from '../types/item';

export function useInventory() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const backendItems: ItemResponse[] = await fetchItems();

        const mapped: InventoryItem[] = await Promise.all(
          backendItems.map(async (item) => {
            let ownerName: string | null = null;
            let ownerInitials: string | null = null;

            if (item.owner_id) {
              try {
                const user = await fetchUser(item.owner_id);
                ownerName = user.name;
                ownerInitials = user.email.split('@')[0].split('.').map((part) => part[0]).join('').toUpperCase();
              } catch (err) {
                console.warn(`Failed to fetch user ${item.owner_id}`, err);
              }
            }

            return {
              id: item.id,
              item: item.name,
              category: item.category,
              serialNumber: item.serial_number,
              owner: ownerName ?? 'Unkown',
              ownerInitials,
              location: item.location,
            };
          })
        );

        setItems(mapped);
      } catch (err: any) {
        setError(err.message || 'Failed to load inventory');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return { items, loading, error };
}
