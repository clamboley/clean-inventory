import { useState } from 'react';
import { IconChevronDown, IconChevronUp, IconSearch, IconSelector } from '@tabler/icons-react';
import cx from 'clsx';
import {
  Avatar,
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

interface RowData {
  id: string;
  name: string;
  email: string;
  country: string;
  job: string;
  company: string;
  avatar: string;
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

function filterData(data: RowData[], search: string) {
  const query = search.toLowerCase().trim();
  return data.filter((item) =>
    Object.values(item).some((value) => value.toString().toLowerCase().includes(query))
  );
}

function sortData(
  data: RowData[],
  payload: { sortBy: keyof RowData | null; reversed: boolean; search: string }
) {
  const { sortBy } = payload;

  if (!sortBy) {
    return filterData(data, payload.search);
  }

  return filterData(
    [...data].sort((a, b) => {
      if (payload.reversed) {
        return b[sortBy].localeCompare(a[sortBy]);
      }
      return a[sortBy].localeCompare(b[sortBy]);
    }),
    payload.search
  );
}

const data: RowData[] = [
  {
    id: '1',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-1.png',
    name: 'Robert Wolfkisser',
    email: 'rob_wolf@gmail.com',
    country: 'United States',
    job: 'Engineer',
    company: 'TechCorp Inc.',
  },
  {
    id: '2',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-7.png',
    name: 'Jill Jailbreaker',
    email: 'jj@breaker.com',
    country: 'Canada',
    job: 'Engineer',
    company: 'SecureTech Ltd.',
  },
  {
    id: '3',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png',
    name: 'Henry Silkeater',
    email: 'henry@silkeater.io',
    country: 'United Kingdom',
    job: 'Designer',
    company: 'Creative Solutions',
  },
  {
    id: '4',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-3.png',
    name: 'Bill Horsefighter',
    email: 'bhorsefighter@gmail.com',
    country: 'Australia',
    job: 'Designer',
    company: 'Design Studios',
  },
  {
    id: '5',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-10.png',
    name: 'Jeremy Footviewer',
    email: 'jeremy@foot.dev',
    country: 'Germany',
    job: 'Manager',
    company: 'ManagePro GmbH',
  },
  {
    id: '6',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-4.png',
    name: 'Sarah Johnson',
    email: 'sarah.j@techmail.com',
    country: 'France',
    job: 'Developer',
    company: 'CodeCraft SARL',
  },
  {
    id: '7',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-5.png',
    name: 'Michael Brown',
    email: 'mbrown@enterprise.org',
    country: 'Japan',
    job: 'Analyst',
    company: 'DataFlow Corp',
  },
  {
    id: '8',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-6.png',
    name: 'Emma Wilson',
    email: 'emma.wilson@startup.io',
    country: 'Netherlands',
    job: 'Product Manager',
    company: 'InnovateTech BV',
  },
  {
    id: '9',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-8.png',
    name: 'David Lee',
    email: 'dlee@consulting.com',
    country: 'South Korea',
    job: 'Consultant',
    company: 'Strategic Solutions',
  },
  {
    id: '10',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-9.png',
    name: 'Lisa Garcia',
    email: 'lisa.garcia@media.net',
    country: 'Spain',
    job: 'Marketing Director',
    company: 'MediaFlow SA',
  },
  {
    id: '11',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-1.png',
    name: 'Robert Wolfkisser',
    email: 'rob_wolf@gmail.com',
    country: 'United States',
    job: 'Engineer',
    company: 'TechCorp Inc.',
  },
  {
    id: '12',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-7.png',
    name: 'Jill Jailbreaker',
    email: 'jj@breaker.com',
    country: 'Canada',
    job: 'Engineer',
    company: 'SecureTech Ltd.',
  },
  {
    id: '13',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png',
    name: 'Henry Silkeater',
    email: 'henry@silkeater.io',
    country: 'United Kingdom',
    job: 'Designer',
    company: 'Creative Solutions',
  },
  {
    id: '14',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-3.png',
    name: 'Bill Horsefighter',
    email: 'bhorsefighter@gmail.com',
    country: 'Australia',
    job: 'Designer',
    company: 'Design Studios',
  },
  {
    id: '15',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-10.png',
    name: 'Jeremy Footviewer',
    email: 'jeremy@foot.dev',
    country: 'Germany',
    job: 'Manager',
    company: 'ManagePro GmbH',
  },
  {
    id: '16',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-4.png',
    name: 'Sarah Johnson',
    email: 'sarah.j@techmail.com',
    country: 'France',
    job: 'Developer',
    company: 'CodeCraft SARL',
  },
  {
    id: '17',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-5.png',
    name: 'Michael Brown',
    email: 'mbrown@enterprise.org',
    country: 'Japan',
    job: 'Analyst',
    company: 'DataFlow Corp',
  },
  {
    id: '18',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-6.png',
    name: 'Emma Wilson',
    email: 'emma.wilson@startup.io',
    country: 'Netherlands',
    job: 'Product Manager',
    company: 'InnovateTech BV',
  },
  {
    id: '19',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-8.png',
    name: 'David Lee',
    email: 'dlee@consulting.com',
    country: 'South Korea',
    job: 'Consultant',
    company: 'Strategic Solutions',
  },
  {
    id: '20',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-9.png',
    name: 'Lisa Garcia',
    email: 'lisa.garcia@media.net',
    country: 'Spain',
    job: 'Marketing Director',
    company: 'MediaFlow SA',
  },
];

export function InventoryPage() {
  const [search, setSearch] = useState('');
  const [scrolled, setScrolled] = useState(false);
  const [sortedData, setSortedData] = useState(data);
  const [sortBy, setSortBy] = useState<keyof RowData | null>(null);
  const [reverseSortDirection, setReverseSortDirection] = useState(false);
  const [selection, setSelection] = useState<string[]>([]);

  const setSorting = (field: keyof RowData) => {
    const reversed = field === sortBy ? !reverseSortDirection : false;
    setReverseSortDirection(reversed);
    setSortBy(field);
    setSortedData(sortData(data, { sortBy: field, reversed, search }));
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.currentTarget;
    setSearch(value);
    setSortedData(sortData(data, { sortBy, reversed: reverseSortDirection, search: value }));
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
          <Group gap="sm">
            <Avatar size={32} src={item.avatar} radius="xl" />
            <Text size="sm" fw={500}>
              {item.name}
            </Text>
          </Group>
        </Table.Td>
        <Table.Td>
          <Text size="sm">{item.email}</Text>
        </Table.Td>
        <Table.Td>
          <Text size="sm">{item.country}</Text>
        </Table.Td>
        <Table.Td>
          <Text size="sm" c="blue">
            {item.job}
          </Text>
        </Table.Td>
        <Table.Td>
          <Text size="sm" c="dimmed">
            {item.company}
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
            Team Members
          </Text>
          <TextInput
            placeholder="IconSearch by name, email, country, job, or company..."
            mb="md"
            leftSection={<IconSearch size={16} />}
            value={search}
            onChange={handleSearchChange}
            className="max-w-md"
          />
          {selection.length > 0 && (
            <Text size="sm" c="blue" mb="md">
              {selection.length} member{selection.length !== 1 ? 's' : ''} selected
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
                  sorted={sortBy === 'name'}
                  reversed={reverseSortDirection}
                  onSort={() => setSorting('name')}
                >
                  User
                </Th>
                <Th
                  sorted={sortBy === 'email'}
                  reversed={reverseSortDirection}
                  onSort={() => setSorting('email')}
                >
                  Email
                </Th>
                <Th
                  sorted={sortBy === 'country'}
                  reversed={reverseSortDirection}
                  onSort={() => setSorting('country')}
                >
                  Country
                </Th>
                <Th
                  sorted={sortBy === 'job'}
                  reversed={reverseSortDirection}
                  onSort={() => setSorting('job')}
                >
                  Job
                </Th>
                <Th
                  sorted={sortBy === 'company'}
                  reversed={reverseSortDirection}
                  onSort={() => setSorting('company')}
                >
                  Company
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
                      No results found
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
