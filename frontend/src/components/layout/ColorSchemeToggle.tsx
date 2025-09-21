import { Group, Tooltip, ActionIcon, useMantineColorScheme } from '@mantine/core';
import { IconMoon, IconSun, IconDeviceDesktop } from '@tabler/icons-react';

export function ColorSchemeToggle() {
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
