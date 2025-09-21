export interface ItemResponse {
  id: string;
  name: string;
  category: string;
  serial_number: string | null;
  owner_id: string | null;
  location: string | null;
  extra: Record<string, unknown>;
  status: string;
  created_at: string;
  updated_at: string;
  version: number;
}

export interface InventoryItem {
  id: string;
  item: string;
  category: string;
  serialNumber: string | null;
  owner: string | null;
  ownerInitials: string | null;
  location: string | null;
}
