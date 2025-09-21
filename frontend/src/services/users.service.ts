import { UserResponse } from '../types/user';
import { apiFetch } from './api';

export async function fetchUsers(): Promise<UserResponse[]> {
  const data = await apiFetch<{ users: UserResponse[] }>('/users');
  return data.users;
}
