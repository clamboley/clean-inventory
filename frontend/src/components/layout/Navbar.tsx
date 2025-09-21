import {
  IconCircleOff,
  IconError404,
  IconGauge,
  IconHistory,
  IconHome2,
  IconPackage,
} from '@tabler/icons-react';
import { Indicator, Stack } from '@mantine/core';
import { NavItem } from '../common/NavItem';
import { SidebarToggle } from './SidebarToggle';

interface NavbarProps {
  collapsed: boolean;
  setCollapsed: (c: boolean) => void;
}

export function Navbar({ collapsed, setCollapsed }: NavbarProps) {
  return (
    <>
      <Stack gap="xs" style={{ flexGrow: 1 }}>
        <NavItem
          collapsed={collapsed}
          label="Home"
          icon={<IconHome2 size={20} stroke={1.5} />}
          to="/"
        />

        <NavItem
          collapsed={collapsed}
          label="Dashboard"
          icon={<Indicator size={14} inline label="2"><IconGauge size={20} stroke={1.5} /></Indicator>}
          to="/dashboard"
        />

        <NavItem
          collapsed={collapsed}
          label="Inventory"
          icon={<IconPackage size={20} stroke={1.5} />}
          to="/inventory"
        />

        <NavItem
          collapsed={collapsed}
          label="History"
          icon={<IconHistory size={20} stroke={1.5} />}
          to="*"
        />

        <NavItem
          collapsed={collapsed}
          label="Disabled"
          icon={<IconCircleOff size={20} stroke={1.5} />}
          to="#"
          disabled
        />

        <NavItem
          collapsed={collapsed}
          label="Error page"
          icon={<IconError404 size={20} stroke={1.5} />}
          to="*"
        />
      </Stack>

      <SidebarToggle collapsed={collapsed} setCollapsed={setCollapsed} />
    </>
  );
}
