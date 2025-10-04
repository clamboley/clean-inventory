import { useEffect, useState } from 'react';
import {
  Button,
  Divider,
  Grid,
  Group,
  Modal,
  Select,
  Stack,
  TextInput,
} from '@mantine/core';
import { useUsersContext } from '../../contexts/UsersContext';
import { UpdateItemRequest } from '../../services/items.service';

interface UpdateItemModalProps {
  opened: boolean;
  onClose: () => void;
  item: {
    id: string;
    name: string;
    category: string;
    serial_number_1: string;
    serial_number_2?: string | null;
    serial_number_3?: string | null;
    owner: string;
    location: string;
  };
  onSubmit: (id: string, data: UpdateItemRequest) => void;
}

export function UpdateItemModal({ opened, onClose, item, onSubmit }: UpdateItemModalProps) {
  const [form, setForm] = useState({
    name: '',
    category: '',
    serial_number_1: '',
    serial_number_2: '',
    serial_number_3: '',
    owner: '' as string | null,
    location: '',
  });

  const { users } = useUsersContext();

  useEffect(() => {
    if (item) {
      setForm({
        name: item.name || '',
        category: item.category || '',
        serial_number_1: item.serial_number_1 || '',
        serial_number_2: item.serial_number_2 || '',
        serial_number_3: item.serial_number_3 || '',
        owner: item.owner || null,
        location: item.location || '',
      });
    }
  }, [item]);

  const updateField = <K extends keyof typeof form>(field: K, value: (typeof form)[K]) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = () => {
    if (!isValid) {
      return;
    }

    const payload: UpdateItemRequest = {
      name: form.name,
      category: form.category,
      serial_number_1: form.serial_number_1,
      serial_number_2: form.serial_number_2 || null,
      serial_number_3: form.serial_number_3 || null,
      owner: form.owner!,
      location: form.location,
    };

    onSubmit(item.id, payload);
    onClose();
  };

  const isValid =
    form.name.trim() &&
    form.category.trim() &&
    form.serial_number_1.trim() &&
    form.owner &&
    form.location.trim();

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="Update Item"
      size="lg"
      overlayProps={{ backgroundOpacity: 0.55, blur: 2 }}
      centered
    >
      <Stack gap="lg">
        <Divider label="Item Information" labelPosition="center" />

        <TextInput
          label="Item Name"
          placeholder={item.name || 'Item name'}
          value={form.name}
          onChange={(e) => updateField('name', e.currentTarget.value)}
          required
          withAsterisk
        />

        <TextInput
          label="Category"
          placeholder={item.category || 'Category'}
          value={form.category}
          onChange={(e) => updateField('category', e.currentTarget.value)}
          required
          withAsterisk
        />

        <Divider label="Serial Numbers" labelPosition="center" />

        <Grid>
          <Grid.Col span={12}>
            <TextInput
              label="Serial Number 1"
              placeholder={item.serial_number_1 || 'Primary serial number'}
              value={form.serial_number_1}
              onChange={(e) => updateField('serial_number_1', e.currentTarget.value)}
              required
              withAsterisk
            />
          </Grid.Col>
          <Grid.Col span={6}>
            <TextInput
              label="Serial Number 2"
              placeholder={item.serial_number_2 || 'Optional'}
              value={form.serial_number_2}
              onChange={(e) => updateField('serial_number_2', e.currentTarget.value)}
            />
          </Grid.Col>
          <Grid.Col span={6}>
            <TextInput
              label="Serial Number 3"
              placeholder={item.serial_number_3 || 'Optional'}
              value={form.serial_number_3}
              onChange={(e) => updateField('serial_number_3', e.currentTarget.value)}
            />
          </Grid.Col>
        </Grid>

        <Divider label="Ownership" labelPosition="center" />

        <Select
          label="Owner Email"
          placeholder={item.owner || 'Select owner'}
          data={users.map((u) => ({
            value: u.email,
            label: `${u.first_name} ${u.last_name} (${u.email})`,
          }))}
          value={form.owner}
          onChange={(val) => updateField('owner', val)}
          clearable
          searchable
          required
          withAsterisk
        />

        <TextInput
          label="Location"
          placeholder={item.location || 'Location'}
          value={form.location}
          onChange={(e) => updateField('location', e.currentTarget.value)}
          required
          withAsterisk
        />

        <Divider />

        <Group justify="flex-end" mt="md">
          <Button variant="default" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={!isValid} color="blue">
            Update Item
          </Button>
        </Group>
      </Stack>
    </Modal>
  );
}
