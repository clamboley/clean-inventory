import { AppShell } from '@mantine/core';
import { Navbar } from './Navbar';
import { Header } from './Header';
import { useState } from 'react';

export function AppLayout({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{ width: collapsed ? 80 : 240, breakpoint: 'sm' }}
      padding="md"
    >
      <AppShell.Header>
        <Header />
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <Navbar collapsed={collapsed} setCollapsed={setCollapsed} />
      </AppShell.Navbar>

      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
}
