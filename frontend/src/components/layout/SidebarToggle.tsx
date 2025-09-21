import { IconLayoutSidebarLeftCollapse, IconLayoutSidebarLeftExpand } from '@tabler/icons-react';
import { Button } from '@mantine/core';

interface SidebarToggleProps {
  collapsed: boolean;
  setCollapsed: (collapsed: boolean) => void;
}

export function SidebarToggle({ collapsed, setCollapsed }: SidebarToggleProps) {
  return (
    <Button
      variant="subtle"
      onClick={() => setCollapsed(!collapsed)}
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
  );
}
