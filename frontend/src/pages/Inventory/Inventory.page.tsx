import { useState } from 'react';
import {
  IconChevronDown,
  IconChevronUp,
  IconDots,
  IconMessages,
  IconNote,
  IconPencil,
  IconReportAnalytics,
  IconSearch,
  IconSelector,
  IconTrash,
} from '@tabler/icons-react';
import cx from 'clsx';
import {
  ActionIcon,
  Avatar,
  Badge,
  Center,
  Checkbox,
  Group,
  Loader,
  Menu,
  ScrollArea,
  Table,
  Text,
  TextInput,
  UnstyledButton,
} from '@mantine/core';
import { AppLayout } from '../../components/layout/AppLayout';
import { useInventory } from '../../hooks/useInventory';
import { InventoryItem } from '../../types/item';
import classes from './TableScrollArea.module.css';

interface ThProps {
  children: React.ReactNode;
  reversed: boolean;
  sorted: boolean;
  onSort: () => void;
}

function Th({ children, reversed, sorted, onSort }: ThProps) {
  const Icon = sorted ? (reversed ? IconChevronUp : IconChevronDown) : IconSelector;
  return (
    <Table.Th>
      <UnstyledButton
        onClick={onSort}
        className="w-full p-2 hover:bg-gray-50 rounded transition-colors"
      >
        <Group justify="space-between">
          <Text fw={500} fz="sm">
            {children}
          </Text>
          <Center>
            <Icon size={16} />
          </Center>
        </Group>
      </UnstyledButton>
    </Table.Th>
  );
}

function filterData(data: InventoryItem[], search: string) {
  const query = search.toLowerCase().trim();
  return data.filter((item) =>
    Object.values(item).some((value) => value?.toString().toLowerCase().includes(query))
  );
}

function sortData(
  data: InventoryItem[],
  payload: { sortBy: keyof InventoryItem | null; reversed: boolean; search: string }
) {
  const { sortBy } = payload;
  if (!sortBy) return filterData(data, payload.search);

  return filterData(
    [...data].sort((a, b) => {
      const aVal = a[sortBy] ?? '';
      const bVal = b[sortBy] ?? '';
      return payload.reversed
        ? bVal.toString().localeCompare(aVal.toString())
        : aVal.toString().localeCompare(bVal.toString());
    }),
    payload.search
  );
}

const getCategoryColor = (category: string) => {
  switch (category?.toLowerCase()) {
    case 'laptop':
      return 'blue';
    case 'desktop':
      return 'green';
    case 'monitor':
      return 'purple';
    case 'keyboard':
      return 'orange';
    case 'mouse':
      return 'red';
    case 'tablet':
      return 'cyan';
    case 'phone':
      return 'pink';
    case 'printer':
      return 'gray';
    case 'server':
      return 'dark';
    case 'router':
      return 'indigo';
    default:
      return 'gray';
  }
};

export function InventoryPage() {
  const { items, loading, error } = useInventory();
  const [search, setSearch] = useState('');
  const [scrolled, setScrolled] = useState(false);
  const [sortBy, setSortBy] = useState<keyof InventoryItem | null>(null);
  const [reverseSortDirection, setReverseSortDirection] = useState(false);
  const [selection, setSelection] = useState<string[]>([]);

  const sortedData = sortData(items, { sortBy, reversed: reverseSortDirection, search });

  const setSorting = (field: keyof InventoryItem) => {
    const reversed = field === sortBy ? !reverseSortDirection : false;
    setReverseSortDirection(reversed);
    setSortBy(field);
  };

  const toggleRow = (id: string) =>
    setSelection((current) =>
      current.includes(id) ? current.filter((item) => item !== id) : [...current, id]
    );

  const toggleAll = () =>
    setSelection((current) =>
      current.length === sortedData.length ? [] : sortedData.map((item) => item.id)
    );

  const rows = sortedData.map((item) => {
    const selected = selection.includes(item.id);
    return (
      <Table.Tr
        key={item.id}
        className={selected ? 'bg-blue-50 hover:bg-blue-100' : 'hover:bg-gray-50'}
      >
        <Table.Td>
          <Checkbox checked={selection.includes(item.id)} onChange={() => toggleRow(item.id)} />
        </Table.Td>
        <Table.Td>
          <Text size="sm" fw={500}>
            {item.item}
          </Text>
        </Table.Td>
        <Table.Td>
          <Badge color={getCategoryColor(item.category)} variant="light" size="sm">
            {item.category}
          </Badge>
        </Table.Td>
        <Table.Td>
          <Text size="sm" ff="monospace" c="dimmed">
            {item.serialNumber}
          </Text>
        </Table.Td>
        <Table.Td>
          <Group gap="sm">
            <Avatar size={32} radius="xl">{item.ownerInitials}</Avatar>
            <Text size="sm" fw={500}>
              {item.owner}
            </Text>
          </Group>
        </Table.Td>
        <Table.Td>
          <Text size="sm" c="blue">
            {item.location}
          </Text>
        </Table.Td>
        <Table.Td>
          <Group gap={0} justify="flex-end">
            <ActionIcon variant="subtle" color="gray">
              <IconPencil size={16} stroke={1.5} />
            </ActionIcon>
            <ActionIcon variant="subtle" color="red">
              <IconTrash size={16} stroke={1.5} />
            </ActionIcon>
            <Menu
              transitionProps={{ transition: 'pop' }}
              withArrow
              position="bottom-end"
              withinPortal
            >
              <Menu.Target>
                <ActionIcon variant="subtle" color="gray">
                  <IconDots size={16} stroke={1.5} />
                </ActionIcon>
              </Menu.Target>
              <Menu.Dropdown>
                <Menu.Item leftSection={<IconMessages size={16} stroke={1.5} />}>
                  Send message
                </Menu.Item>
                <Menu.Item leftSection={<IconNote size={16} stroke={1.5} />}>Add note</Menu.Item>
                <Menu.Item leftSection={<IconReportAnalytics size={16} stroke={1.5} />}>
                  Analytics
                </Menu.Item>
                <Menu.Item leftSection={<IconTrash size={16} stroke={1.5} />} color="red">
                  Terminate contract
                </Menu.Item>
              </Menu.Dropdown>
            </Menu>
          </Group>
        </Table.Td>
      </Table.Tr>
    );
  });

  return (
    <AppLayout>
      <div className="p-6 max-w-7xl mx-auto">
        <div className="mb-6">
          <Text size="xl" fw={700} mb="md">
            Global Inventory
          </Text>
          <TextInput
            placeholder="Search by item, category, serial number, owner, or location..."
            mb="md"
            leftSection={<IconSearch size={16} />}
            value={search}
            onChange={(e) => setSearch(e.currentTarget.value)}
            className="max-w-md"
          />
          {selection.length > 0 && (
            <Text size="sm" c="blue" mb="md">
              {selection.length} item{selection.length !== 1 ? 's' : ''} selected
            </Text>
          )}
        </div>

        {loading ? (
          <Center>
            <Loader size="lg" />
          </Center>
        ) : error ? (
          <Center>
            <Text c="red">{error}</Text>
          </Center>
        ) : (
          <ScrollArea h={600} onScrollPositionChange={({ y }) => setScrolled(y !== 0)}>
            <Table miw={1000} className="border border-gray-200 rounded-lg">
              <Table.Thead className={cx(classes.header, { [classes.scrolled]: scrolled })}>
                <Table.Tr>
                  <Table.Th w={40}>
                    <Checkbox
                      onChange={toggleAll}
                      checked={selection.length === sortedData.length && sortedData.length > 0}
                      indeterminate={selection.length > 0 && selection.length !== sortedData.length}
                    />
                  </Table.Th>
                  <Th
                    sorted={sortBy === 'item'}
                    reversed={reverseSortDirection}
                    onSort={() => setSorting('item')}
                  >
                    Item
                  </Th>
                  <Th
                    sorted={sortBy === 'category'}
                    reversed={reverseSortDirection}
                    onSort={() => setSorting('category')}
                  >
                    Category
                  </Th>
                  <Th
                    sorted={sortBy === 'serialNumber'}
                    reversed={reverseSortDirection}
                    onSort={() => setSorting('serialNumber')}
                  >
                    Serial Number
                  </Th>
                  <Th
                    sorted={sortBy === 'owner'}
                    reversed={reverseSortDirection}
                    onSort={() => setSorting('owner')}
                  >
                    Owner
                  </Th>
                  <Th
                    sorted={sortBy === 'location'}
                    reversed={reverseSortDirection}
                    onSort={() => setSorting('location')}
                  >
                    Location
                  </Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {rows.length > 0 ? (
                  rows
                ) : (
                  <Table.Tr>
                    <Table.Td colSpan={6}>
                      <Text fw={500} ta="center" py="xl" c="dimmed">
                        No items found
                      </Text>
                    </Table.Td>
                  </Table.Tr>
                )}
              </Table.Tbody>
            </Table>
          </ScrollArea>
        )}
      </div>
    </AppLayout>
  );
}
