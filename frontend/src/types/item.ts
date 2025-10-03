export interface ItemResponse {
  id: string;
  name: string;
  category: string;
  serial_number_1: string;
  serial_number_2: string | null;
  serial_number_3: string | null;
  owner: string;
  location: string;
  status: string;
  created_at: string;
}

export interface InventoryItem {
  id: string;
  item: string;
  category: string;
  serialNumber1: string;
  serialNumber2: string | null;
  serialNumber3: string | null;
  ownerEmail: string;
  ownerInitials: string;
  location: string;
}

export function mapItemResponseToInventory(item: ItemResponse): InventoryItem {
  const initials = item.owner
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
    ownerInitials: initials,
    location: item.location,
  };
}

export interface ImportResult {
  created: ItemResponse[];
  errors: { row: number; message: string }[];
}

export interface ImportItemError {
  row: number;
  error: string;
}

export interface ImportItemsResponse {
  created: ItemResponse[];
  errors: ImportItemError[];
}
