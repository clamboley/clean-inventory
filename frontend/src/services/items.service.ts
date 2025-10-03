import { ImportItemsResponse, ItemResponse } from '../models/item';
import { apiFetch } from '../api/client';

export async function fetchItems(): Promise<ItemResponse[]> {
  const data = await apiFetch<{ items: ItemResponse[] }>('/items');
  return data.items;
}

export async function uploadItems(file: File): Promise<ImportItemsResponse> {
  const fd = new FormData();
  fd.append('file', file);

  return apiFetch<ImportItemsResponse>('/items/import', {
    method: 'POST',
    body: fd,
  });
}

export interface CreateItemRequest {
  name: string;
  category: string;
  serial_number_1: string;
  serial_number_2?: string | null;
  serial_number_3?: string | null;
  owner: string; // email
  location: string;
}

export async function createItem(payload: CreateItemRequest): Promise<ItemResponse> {
  return apiFetch<ItemResponse>('/items', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
