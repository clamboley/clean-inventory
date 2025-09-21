import { useState } from 'react';
import { AppShell, Grid } from '@mantine/core';
import { Header } from './Header';
import { Navbar } from './Navbar';

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

      <AppShell.Main>
        <Grid>
          <Grid.Col span={0.5}></Grid.Col>
          <Grid.Col span={11}>{children}</Grid.Col>
          <Grid.Col span={0.5}></Grid.Col>
        </Grid>
      </AppShell.Main>
    </AppShell>
  );
}
