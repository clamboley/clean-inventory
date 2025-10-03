import { createContext, useContext, useEffect, useState } from 'react';
import { UserResponse } from '../models/user';
import { fetchUsers } from '../services/users.service';

interface UsersContextValue {
  users: UserResponse[];
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

const UsersContext = createContext<UsersContextValue | undefined>(undefined);

export function UsersProvider({ children }: { children: React.ReactNode }) {
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const data = await fetchUsers();
      setUsers(data);
      setError(null);
    } catch (err: any) {
      setError(err.message ?? 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load(); // preload once when provider mounts
  }, []);

  return (
    <UsersContext.Provider value={{ users, loading, error, refresh: load }}>
      {children}
    </UsersContext.Provider>
  );
}

export function useUsersContext() {
  const ctx = useContext(UsersContext);
  if (!ctx) {
    throw new Error('useUsersContext must be used inside <UsersProvider>');
  }
  return ctx;
}
