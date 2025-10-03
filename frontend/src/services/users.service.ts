import { UserResponse } from '../models/user';
import { apiFetch } from '../api/client';

export async function fetchUsers(): Promise<UserResponse[]> {
  const data = await apiFetch<{ users: UserResponse[] }>('/users');
  return data.users;
}
