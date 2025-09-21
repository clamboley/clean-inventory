import { useState } from 'react';
import { IconChevronDown, IconChevronUp, IconSearch, IconSelector } from '@tabler/icons-react';
import cx from 'clsx';
import {
  Avatar,
  Badge,
  Center,
  Checkbox,
  Group,
  ScrollArea,
  Table,
  Text,
  TextInput,
  UnstyledButton,
} from '@mantine/core';
import { AppLayout } from '../../components/layout/AppLayout';
import classes from './TableScrollArea.module.css';

interface InventoryItem {
  id: string;
  item: string;
  category: string;
  serialNumber: string;
  owner: string;
  ownerAvatar: string;
  location: string;
}

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
    Object.values(item).some((value) => value.toString().toLowerCase().includes(query))
  );
}

function sortData(
  data: InventoryItem[],
  payload: { sortBy: keyof InventoryItem | null; reversed: boolean; search: string }
) {
  const { sortBy } = payload;

  if (!sortBy) {
    return filterData(data, payload.search);
  }

  return filterData(
    [...data].sort((a, b) => {
      if (payload.reversed) {
        return b[sortBy].toString().localeCompare(a[sortBy].toString());
      }
      return a[sortBy].toString().localeCompare(b[sortBy].toString());
    }),
    payload.search
  );
}

const getCategoryColor = (category: string) => {
  switch (category.toLowerCase()) {
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

const inventoryData: InventoryItem[] = [
  {
    id: '1',
    item: 'MacBook Pro 16"',
    category: 'Laptop',
    serialNumber: 'MBP-2023-001',
    owner: 'Sarah Johnson',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-4.png',
    location: 'Room A-101',
  },
  {
    id: '2',
    item: 'Dell XPS Desktop',
    category: 'Desktop',
    serialNumber: 'DXD-2023-005',
    owner: 'Michael Brown',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-5.png',
    location: 'Room B-205',
  },
  {
    id: '3',
    item: 'Samsung 4K Monitor',
    category: 'Monitor',
    serialNumber: 'SM4K-2023-012',
    owner: 'Emma Wilson',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-6.png',
    location: 'Room A-103',
  },
  {
    id: '4',
    item: 'Logitech MX Keys',
    category: 'Keyboard',
    serialNumber: 'LMX-2023-034',
    owner: 'David Lee',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-8.png',
    location: 'Room B-201',
  },
  {
    id: '5',
    item: 'Razer DeathAdder V3',
    category: 'Mouse',
    serialNumber: 'RDA-2023-089',
    owner: 'Lisa Garcia',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-9.png',
    location: 'Room C-301',
  },
  {
    id: '6',
    item: 'iPad Pro 12.9"',
    category: 'Tablet',
    serialNumber: 'IPD-2023-023',
    owner: 'Robert Wilson',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-1.png',
    location: 'Room A-105',
  },
  {
    id: '7',
    item: 'iPhone 14 Pro',
    category: 'Phone',
    serialNumber: 'IP14-2023-067',
    owner: 'Jennifer Smith',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-7.png',
    location: 'Room B-203',
  },
  {
    id: '8',
    item: 'HP LaserJet Pro',
    category: 'Printer',
    serialNumber: 'HLP-2023-045',
    owner: 'Office Manager',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png',
    location: 'Print Room',
  },
  {
    id: '9',
    item: 'Dell PowerEdge R750',
    category: 'Server',
    serialNumber: 'DPE-2023-001',
    owner: 'IT Department',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-3.png',
    location: 'Server Room',
  },
  {
    id: '10',
    item: 'Cisco Catalyst 9300',
    category: 'Router',
    serialNumber: 'CC9-2023-007',
    owner: 'Network Admin',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-10.png',
    location: 'Network Closet',
  },
  {
    id: '11',
    item: 'ThinkPad X1 Carbon',
    category: 'Laptop',
    serialNumber: 'TX1-2023-078',
    owner: 'Alex Thompson',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-1.png',
    location: 'Room A-102',
  },
  {
    id: '12',
    item: 'LG UltraWide 34"',
    category: 'Monitor',
    serialNumber: 'LUW-2023-034',
    owner: 'Design Team',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-4.png',
    location: 'Design Studio',
  },
  {
    id: '13',
    item: 'Surface Studio 2+',
    category: 'Desktop',
    serialNumber: 'SS2-2023-019',
    owner: 'Creative Director',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-6.png',
    location: 'Room C-305',
  },
  {
    id: '14',
    item: 'Mechanical Keyboard',
    category: 'Keyboard',
    serialNumber: 'MK-2023-156',
    owner: 'Developer Team',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-8.png',
    location: 'Dev Room',
  },
  {
    id: '15',
    item: 'Epson EcoTank L3250',
    category: 'Printer',
    serialNumber: 'EET-2023-091',
    owner: 'Marketing Team',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-9.png',
    location: 'Room B-210',
  },
  {
    id: '16',
    item: 'Samsung Galaxy Tab S9',
    category: 'Tablet',
    serialNumber: 'SGT-2023-123',
    owner: 'Sales Manager',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-7.png',
    location: 'Room A-108',
  },
  {
    id: '17',
    item: 'MacBook Air M2',
    category: 'Laptop',
    serialNumber: 'MBA-2023-045',
    owner: 'Project Manager',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-5.png',
    location: 'Room B-207',
  },
  {
    id: '18',
    item: 'ASUS ProArt Display',
    category: 'Monitor',
    serialNumber: 'APD-2023-067',
    owner: 'Video Editor',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png',
    location: 'Media Room',
  },
  {
    id: '19',
    item: 'Google Pixel 7 Pro',
    category: 'Phone',
    serialNumber: 'GP7-2023-089',
    owner: 'QA Engineer',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-3.png',
    location: 'Room C-302',
  },
  {
    id: '20',
    item: 'Netgear Nighthawk AX12',
    category: 'Router',
    serialNumber: 'NNA-2023-012',
    owner: 'IT Support',
    ownerAvatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-10.png',
    location: 'Conference Room',
  },
];

export function InventoryPage() {
  const [search, setSearch] = useState('');
  const [scrolled, setScrolled] = useState(false);
  const [sortedData, setSortedData] = useState(inventoryData);
  const [sortBy, setSortBy] = useState<keyof InventoryItem | null>(null);
  const [reverseSortDirection, setReverseSortDirection] = useState(false);
  const [selection, setSelection] = useState<string[]>([]);

  const setSorting = (field: keyof InventoryItem) => {
    const reversed = field === sortBy ? !reverseSortDirection : false;
    setReverseSortDirection(reversed);
    setSortBy(field);
    setSortedData(sortData(inventoryData, { sortBy: field, reversed, search }));
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.currentTarget;
    setSearch(value);
    setSortedData(
      sortData(inventoryData, { sortBy, reversed: reverseSortDirection, search: value })
    );
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
            <Avatar size={32} src={item.ownerAvatar} radius="xl" />
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
      </Table.Tr>
    );
  });

  return (
    <AppLayout>
      <div className="p-6 max-w-7xl mx-auto">
        <div className="mb-6">
          <Text size="xl" fw={700} mb="md">
            IT Inventory
          </Text>
          <TextInput
            placeholder="Search by item, category, serial number, owner, or location..."
            mb="md"
            leftSection={<IconSearch size={16} />}
            value={search}
            onChange={handleSearchChange}
            className="max-w-md"
          />
          {selection.length > 0 && (
            <Text size="sm" c="blue" mb="md">
              {selection.length} item{selection.length !== 1 ? 's' : ''} selected
            </Text>
          )}
        </div>

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
      </div>
    </AppLayout>
  );
}
