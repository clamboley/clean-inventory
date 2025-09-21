import { Tooltip, NavLink } from '@mantine/core';
import { IconChevronRight } from '@tabler/icons-react';
import { Link, useLocation } from 'react-router-dom';

interface NavItemProps {
  collapsed: boolean;
  label: string;
  icon: React.ReactNode;
  to: string;
  disabled?: boolean;
}

export function NavItem({
  collapsed,
  label,
  icon,
  to,
  disabled,
}: NavItemProps) {
  const location = useLocation();
  const active = location.pathname === to;

  return (
    <Tooltip label={label} disabled={!collapsed} position="right">
      <NavLink
        component={Link}
        to={to}
        label={!collapsed && label}
        leftSection={icon}
        disabled={disabled}
        active={active}
      />
    </Tooltip>
  );
}
