import { IconMoodAngryFilled } from '@tabler/icons-react';
import { Group, Text } from '@mantine/core';
import { ColorSchemeToggle } from './ColorSchemeToggle';

export function Header() {
  return (
    <Group h="100%" px="md" justify="space-between">
      <Group>
        <IconMoodAngryFilled />
        <Text fw={500}>Inventory App</Text>
      </Group>
      <ColorSchemeToggle />
    </Group>
  );
}
