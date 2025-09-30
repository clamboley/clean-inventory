import { ImportItemsResponse, ItemResponse } from '../types/item';
import { apiFetch } from './api';

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