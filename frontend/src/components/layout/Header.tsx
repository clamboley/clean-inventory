import { Group, Text } from '@mantine/core';
import { ColorSchemeToggle } from './ColorSchemeToggle';

export function Header() {
  return (
    <Group h="100%" px="md" justify="space-between">
      <Text fw={500}>My App</Text>
      <ColorSchemeToggle />
    </Group>
  );
}
