import { ItemResponse } from '../types/item';
import { apiFetch } from './api';

export async function fetchItems(): Promise<ItemResponse[]> {
  const data = await apiFetch<{ items: ItemResponse[] }>('/items');
  return data.items;
}
