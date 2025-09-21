import { UserResponse } from '../types/user';
import { apiFetch } from './api';

export async function fetchUser(userId: string): Promise<UserResponse> {
  return apiFetch<UserResponse>(`/users/${userId}`);
}
