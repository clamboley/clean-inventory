import { useEffect, useState } from 'react';
import { Button, Drawer, Group, Select, Stack, TextInput } from '@mantine/core';
import { CreateItemRequest } from '../../services/items.service';
import { fetchUsers } from '../../services/users.service';
import { UserResponse } from '../../types/user';

interface AddItemDrawerProps {
  opened: boolean;
  onClose: () => void;
  onSubmit: (data: CreateItemRequest) => void;
}

export function AddItemDrawer({ opened, onClose, onSubmit }: AddItemDrawerProps) {
  const [form, setForm] = useState({
    name: '',
    category: '',
    serial_number_1: '',
    serial_number_2: '',
    serial_number_3: '',
    owner: null as string | null,
    location: '',
  });

  const [users, setUsers] = useState<UserResponse[]>([]);

  useEffect(() => {
    fetchUsers().then(setUsers).catch(console.error);
  }, []);

  const updateField = <K extends keyof typeof form>(field: K, value: (typeof form)[K]) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = () => {
    if (!isValid) return;

    const payload: CreateItemRequest = {
      name: form.name,
      category: form.category,
      serial_number_1: form.serial_number_1,
      serial_number_2: form.serial_number_2 || null,
      serial_number_3: form.serial_number_3 || null,
      owner: form.owner!,
      location: form.location,
    };

    onSubmit(payload);

    // Reset form
    setForm({
      name: '',
      category: '',
      serial_number_1: '',
      serial_number_2: '',
      serial_number_3: '',
      owner: null,
      location: '',
    });
    onClose();
  };

  const isValid =
    form.name.trim() &&
    form.category.trim() &&
    form.serial_number_1.trim() &&
    form.owner &&
    form.location.trim();

  return (
    <Drawer opened={opened} onClose={onClose} title="Add Inventory Item" size="md" padding="xl">
      <Stack>
        <TextInput
          label="Item Name"
          placeholder="e.g. Dell XPS 13"
          value={form.name}
          onChange={(e) => updateField('name', e.currentTarget.value)}
          required
        />

        <TextInput
          label="Category"
          placeholder="e.g. Laptop, Monitor, etc."
          value={form.category}
          onChange={(e) => updateField('category', e.currentTarget.value)}
          required
        />

        <TextInput
          label="Serial Number 1"
          placeholder="e.g. SN123456"
          value={form.serial_number_1}
          onChange={(e) => updateField('serial_number_1', e.currentTarget.value)}
          required
        />

        <TextInput
          label="Serial Number 2"
          placeholder="Optional"
          value={form.serial_number_2}
          onChange={(e) => updateField('serial_number_2', e.currentTarget.value)}
        />

        <TextInput
          label="Serial Number 3"
          placeholder="Optional"
          value={form.serial_number_3}
          onChange={(e) => updateField('serial_number_3', e.currentTarget.value)}
        />

        <Select
          label="Owner Email"
          placeholder="Select owner"
          data={users.map((u) => ({ value: u.email, label: `${u.first_name} ${u.last_name} (${u.email})` }))}
          value={form.owner}
          onChange={(val) => updateField('owner', val)}
          clearable
          required
        />

        <TextInput
          label="Location"
          placeholder="e.g. London Office"
          value={form.location}
          onChange={(e) => updateField('location', e.currentTarget.value)}
          required
        />

        <Group justify="flex-end" mt="md">
          <Button variant="default" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={!isValid}>
            Add Item
          </Button>
        </Group>
      </Stack>
    </Drawer>
  );
}
