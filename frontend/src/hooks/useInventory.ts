// src/hooks/useInventory.ts
import { useEffect, useState } from "react";
import { fetchItems } from "../services/items.service";
import { fetchUsers } from "../services/users.service";
import { InventoryItem, ItemResponse } from "../types/item";
import { UserResponse } from "../types/user";

export function useInventory() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [backendItems, backendUsers]: [ItemResponse[], UserResponse[]] = await Promise.all([
          fetchItems(),
          fetchUsers(),
        ]);

        // Build user map for quick lookups
        const userMap = new Map<string, UserResponse>();
        backendUsers.forEach((u) => userMap.set(u.id, u));

        const mapped: InventoryItem[] = backendItems.map((item) => {
          let ownerName: string | null = null;
          let ownerInitials: string | null = null;

          if (item.owner_id && userMap.has(item.owner_id)) {
            const user = userMap.get(item.owner_id)!;
            ownerName = user.name;
            ownerInitials = user.email.split('@')[0].split('.').map((part) => part[0]).join('').toUpperCase();
          }

          return {
            id: item.id,
            item: item.name,
            category: item.category,
            serialNumber: item.serial_number,
            owner: ownerName ?? "Unknown",
            ownerInitials,
            location: item.location,
          };
        });

        setItems(mapped);
      } catch (err: any) {
        console.error(err);
        setError(err.message || "Failed to load inventory");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return { items, loading, error };
}

