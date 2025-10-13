// DownloadZone.tsx
import { IconDownload } from '@tabler/icons-react';
import { Button, Group, Text } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { downloadItems } from '../../services/items.service';

export function DownloadZone() {
  async function handleDownload(format: 'csv' | 'xlsx') {
    try {
      const blob = await downloadItems(format);
      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = `inventory.${format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);

      notifications.show({
        title: 'Download started',
        message: `Inventory ${format.toUpperCase()} file is being downloaded.`,
        color: 'green',
      });
    } catch (err) {
      notifications.show({
        title: 'Download error',
        message: String(err),
        color: 'red',
      });
    }
  }

  return (
    <Group
      justify="center"
      gap="xl"
      mih={220}
      style={{
        border: '1px solid var(--mantine-color-gray-8)',
        borderRadius: 'var(--mantine-radius-sm)',
        padding: 'var(--mantine-spacing-sm)',
      }}
    >
      <IconDownload size={52} color="var(--mantine-color-dimmed)" stroke={1.5} />
      <div>
        <Text size="xl" inline>
          Download current inventory
        </Text>
        <Text size="sm" c="dimmed" inline mt={7}>
          Export all items as CSV or Excel
        </Text>

        <Group mt="md" gap="md">
          <Button color="blue" variant="filled" onClick={() => handleDownload('csv')}>
            Download CSV
          </Button>
          <Button color="green" variant="filled" onClick={() => handleDownload('xlsx')}>
            Download XLSX
          </Button>
        </Group>
      </div>
    </Group>
  );
}
