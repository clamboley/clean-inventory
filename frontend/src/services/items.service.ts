import { apiFetch } from '../api/client';
import { ImportItemsResponse, ItemResponse } from '../models/item';

export async function fetchItems(): Promise<ItemResponse[]> {
  const data = await apiFetch<{ items: ItemResponse[] }>('/items');
  return data.items;
}

export async function fetchItem(itemId: string): Promise<ItemResponse> {
  return apiFetch<ItemResponse>(`/items/${itemId}`);
}

export async function deleteItem(itemId: string): Promise<void> {
  await apiFetch(`/items/${itemId}`, {
    method: 'DELETE',
  });
}

export interface CreateItemRequest {
  name: string;
  category: string;
  serial_number_1: string;
  serial_number_2?: string | null;
  serial_number_3?: string | null;
  owner: string;
  location: string;
}

export async function createItem(payload: CreateItemRequest): Promise<ItemResponse> {
  return apiFetch<ItemResponse>('/items', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export interface UpdateItemRequest {
  name?: string;
  category?: string;
  serial_number_1?: string;
  serial_number_2?: string | null;
  serial_number_3?: string | null;
  owner?: string;
  location?: string;
  status?: string;
}

export async function updateItem(
  itemId: string,
  payload: UpdateItemRequest
): Promise<ItemResponse> {
  return apiFetch<ItemResponse>(`/items/${itemId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}

export async function uploadItems(file: File): Promise<ImportItemsResponse> {
  const fd = new FormData();
  fd.append('file', file);

  return apiFetch<ImportItemsResponse>('/items/import', {
    method: 'POST',
    body: fd,
  });
}
