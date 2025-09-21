import { useState } from 'react';
import {
  IconChevronRight,
  IconCircleOff,
  IconGauge,
  IconHome2,
  IconLayoutSidebarLeftCollapse,
  IconLayoutSidebarLeftExpand,
  IconPackage,
  IconMoon,
  IconSun,
  IconDeviceDesktop,
} from '@tabler/icons-react';
import {
  AppShell,
  Badge,
  Button,
  Group,
  NavLink,
  Stack,
  Text,
  Tooltip,
  ActionIcon,
  useMantineColorScheme,
} from '@mantine/core';

function ColorSchemeToggle() {
  const { setColorScheme } = useMantineColorScheme();

  return (
    <Group gap="xs">
      <Tooltip label="Light" position="bottom">
        <ActionIcon
          variant="subtle"
          onClick={() => setColorScheme('light')}
          aria-label="Set light theme"
        >
          <IconSun size={20} />
        </ActionIcon>
      </Tooltip>

      <Tooltip label="Dark" position="bottom">
        <ActionIcon
          variant="subtle"
          onClick={() => setColorScheme('dark')}
          aria-label="Set dark theme"
        >
          <IconMoon size={20} />
        </ActionIcon>
      </Tooltip>

      <Tooltip label="Auto" position="bottom">
        <ActionIcon
          variant="subtle"
          onClick={() => setColorScheme('auto')}
          aria-label="Set auto theme"
        >
          <IconDeviceDesktop size={20} />
        </ActionIcon>
      </Tooltip>
    </Group>
  );
}

export function HomePage() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: collapsed ? 80 : 240,
        breakpoint: 'sm',
      }}
      padding="md"
    >
      {/* Header */}
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Text>Header that is not used for now</Text>
          <ColorSchemeToggle />
        </Group>
      </AppShell.Header>

      {/* Navbar */}
      <AppShell.Navbar p="md">
        <Stack gap="xs" style={{ flexGrow: 1 }}>
          <Tooltip label="Dashboard" disabled={!collapsed} position="right">
            <NavLink
              href="#required-for-focus"
              label={!collapsed && 'Dashboard'}
              leftSection={<IconHome2 size={20} stroke={1.5} />}
            />
          </Tooltip>

          <Tooltip label="Inventory" disabled={!collapsed} position="right">
            <NavLink
              href="#required-for-focus"
              label={!collapsed && 'Inventory'}
              leftSection={<IconPackage size={20} stroke={1.5} />}
            />
          </Tooltip>

          <Tooltip label="With right section" disabled={!collapsed} position="right">
            <NavLink
              href="#required-for-focus"
              label={!collapsed && 'With right section'}
              leftSection={<IconGauge size={20} stroke={1.5} />}
              rightSection={
                !collapsed && (
                  <IconChevronRight size={14} stroke={1.5} className="mantine-rotate-rtl" />
                )
              }
            />
          </Tooltip>

          <Tooltip label="Disabled" disabled={!collapsed} position="right">
            <NavLink
              href="#required-for-focus"
              label={!collapsed && 'Disabled'}
              leftSection={<IconCircleOff size={20} stroke={1.5} />}
              disabled
            />
          </Tooltip>

          <Tooltip label="With description" disabled={!collapsed} position="right">
            <NavLink
              href="#required-for-focus"
              label={!collapsed && 'With description'}
              description={!collapsed ? 'Additional information' : undefined}
              leftSection={
                <Badge size="sm" color="red" circle>
                  3
                </Badge>
              }
            />
          </Tooltip>
        </Stack>

        {/* Toggle Sidebar Collapse */}
        <Button
          variant="subtle"
          onClick={() => setCollapsed((c) => !c)}
          leftSection={
            collapsed ? (
              <IconLayoutSidebarLeftExpand size={20} />
            ) : (
              <IconLayoutSidebarLeftCollapse size={20} />
            )
          }
        >
          {!collapsed && 'Collapse'}
        </Button>
      </AppShell.Navbar>

      {/* Main Content */}
      <AppShell.Main>
        <Text>This is the main section, your app content here.</Text>
        <Text>Layout used in most cases – Navbar and Header with fixed position</Text>
      </AppShell.Main>
    </AppShell>
  );
}
