// AddItemDrawer.tsx
import { useState } from 'react';
import { Button, Drawer, Group, Select, Stack, TextInput } from '@mantine/core';
import { CreateItemRequest } from '../../services/items.service';

interface AddItemDrawerProps {
  opened: boolean;
  onClose: () => void;
  onSubmit: (data: CreateItemRequest) => void;
}

const categories = [
  'Laptop',
  'Desktop',
  'Monitor',
  'Keyboard',
  'Mouse',
  'Tablet',
  'Phone',
  'Printer',
  'Server',
  'Router',
];

export function AddItemDrawer({ opened, onClose, onSubmit }: AddItemDrawerProps) {
  const [name, setName] = useState('');
  const [category, setCategory] = useState<string | null>(null);
  const [serialNumber, setSerialNumber] = useState('');
  const [owner, setOwner] = useState('');
  const [location, setLocation] = useState('');

  const handleSubmit = () => {
    if (!name || !category || !serialNumber || !owner || !location) return;

    const payload: CreateItemRequest = {
      name,
      category,
      serial_number_1: serialNumber,
      owner,
      location,
    };

    onSubmit(payload);

    // Reset
    setName('');
    setCategory(null);
    setSerialNumber('');
    setOwner('');
    setLocation('');
    onClose();
  };

  return (
    <Drawer opened={opened} onClose={onClose} title="Add Inventory Item" size="md" padding="xl">
      <Stack>
        <TextInput
          label="Item Name"
          placeholder="e.g. Dell XPS 13"
          value={name}
          onChange={(e) => setName(e.currentTarget.value)}
          required
        />
        <Select
          label="Category"
          placeholder="Select category"
          data={categories}
          value={category}
          onChange={setCategory}
          required
        />
        <TextInput
          label="Serial Number"
          placeholder="e.g. SN123456"
          value={serialNumber}
          onChange={(e) => setSerialNumber(e.currentTarget.value)}
          required
        />
        <TextInput
          label="Owner Email"
          placeholder="e.g. john.doe@example.com"
          value={owner}
          onChange={(e) => setOwner(e.currentTarget.value)}
          required
        />
        <TextInput
          label="Location"
          placeholder="e.g. London Office"
          value={location}
          onChange={(e) => setLocation(e.currentTarget.value)}
          required
        />

        <Group justify="flex-end" mt="md">
          <Button variant="default" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleSubmit}>Add Item</Button>
        </Group>
      </Stack>
    </Drawer>
  );
}
